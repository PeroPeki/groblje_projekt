"""Čarobnjak za aktivaciju pločice (odluka 8).

Koraci: 1. aktivacijski kod → 2. podaci groba i lozinka → 3. prvi pokojnik →
4. slike → gotovo. Stanje između koraka čuva se u sesiji i vrijedi 60 minuta.
"""

import logging
import time
from functools import wraps

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import lazy
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from jezgra.models import Grob, Plocica
from pristup.kolacici import dodijeli_pristup
from pristup.models import NeuspjeliPokusaj
from pristup.ogranicenja import (
    ip_posjetitelja,
    je_zakljucano,
    odgovor_blokade,
    zabiljezi_neuspjeh,
)

from vlasnik.prijava import prijavi

from .forms import AktivacijskiKodForm, GrobForm, PokojnikForm
from .servis import VecAktivirana, aktiviraj_plocicu

log = logging.getLogger(__name__)

UKUPNO_KORAKA = 4
TRAJANJE_SEKUNDI = 60 * 60
SESIJA_PLOCICA = "aktivacija_plocica"  # nakon točnog aktivacijskog koda (korak 1)
SESIJA_GROB = "aktivacija_grob"  # nakon stvaranja groba (korak 2)

POGRESAN_KOD = lazy(lambda: _("Aktivacijski kod nije točan. Provjerite kod na papiru uz pločicu."), str)()

# Za nepostojeću pločicu ipak računamo jedan hash, da odgovor traje jednako dugo
# kao za postojeću (inače bi se po brzini odgovora vidjelo koji kodovi postoje).
_lazni_hash = None


def _potrosi_vrijeme_kao_prava_provjera(aktivacijski_kod):
    global _lazni_hash
    if _lazni_hash is None:
        _lazni_hash = make_password("nepostojeca-plocica")
    check_password(aktivacijski_kod, _lazni_hash)


def _svjeze(zapis) -> bool:
    return bool(zapis) and time.time() - zapis.get("vrijeme", 0) < TRAJANJE_SEKUNDI


def ekran_unosa_koda(request, kod, forma=None):
    """Korak 1. Isti ekran za nepostojeću, neaktiviranu i već aktiviranu pločicu."""
    kontekst = {
        "kod": kod,
        "forma": forma or AktivacijskiKodForm(),
        "korak": 1,
        "ukupno_koraka": UKUPNO_KORAKA,
    }
    return render(request, "aktivacija/unos_koda.html", kontekst)


@sensitive_post_parameters("aktivacijski_kod")
@never_cache
def unos_koda(request, kod):
    if request.method != "POST":
        return redirect("pristup:grob", kod=kod)
    forma = AktivacijskiKodForm(request.POST)
    if not forma.is_valid():
        return ekran_unosa_koda(request, kod, forma)

    vrsta = NeuspjeliPokusaj.Vrsta.AKTIVACIJA
    ip = ip_posjetitelja(request)
    minuta = je_zakljucano(vrsta, kod, ip)
    if minuta:
        return odgovor_blokade(request, minuta)

    aktivacijski_kod = forma.cleaned_data["aktivacijski_kod"]
    plocica = Plocica.objects.filter(kod=kod, status=Plocica.Status.NEAKTIVIRANA).first()
    if plocica is None:
        _potrosi_vrijeme_kao_prava_provjera(aktivacijski_kod)
        tocan = False
    else:
        tocan = plocica.provjeri_aktivacijski_kod(aktivacijski_kod)

    if not tocan:
        # Nepostojeća pločica, već aktivirana pločica i pogrešan kod: ista poruka
        # i isto bilježenje, da se ne otkrije koji je od ta tri slučaja.
        zabiljezi_neuspjeh(vrsta, kod, ip)
        forma.add_error("aktivacijski_kod", POGRESAN_KOD)
        return ekran_unosa_koda(request, kod, forma)

    request.session[SESIJA_PLOCICA] = {"plocica_id": plocica.pk, "kod": kod, "vrijeme": time.time()}
    return redirect("aktivacija:grob", kod=kod)


@sensitive_post_parameters("lozinka", "lozinka2")
@never_cache
def korak_grob(request, kod):
    """Korak 2: podaci groba, kontakt za prijavu i lozinka groba."""
    stanje = request.session.get(SESIJA_PLOCICA)
    if not _svjeze(stanje) or stanje.get("kod") != kod:
        # Bez točnog aktivacijskog koda (ili nakon 60 minuta) natrag na korak 1.
        request.session.pop(SESIJA_PLOCICA, None)
        return redirect("pristup:grob", kod=kod)

    forma = GrobForm(request.POST or None)
    if request.method == "POST" and forma.is_valid():
        podaci = forma.cleaned_data
        try:
            grob, novi_korisnik = aktiviraj_plocicu(
                stanje["plocica_id"],
                naziv=podaci["naziv"],
                oznaka_grobnog_mjesta=podaci["oznaka_grobnog_mjesta"],
                vlasnik_ime=podaci["vlasnik_ime"],
                email=podaci["email"],
                lozinka=podaci["lozinka"],
            )
        except VecAktivirana:
            request.session.pop(SESIJA_PLOCICA, None)
            return redirect("pristup:grob", kod=kod)

        korisnik = grob.kontakt_za_prijavu
        if novi_korisnik:
            # Novi račun postoji samo zbog ovog groba, pa osobu odmah prijavljujemo (OP-5).
            # U POSTOJEĆI račun ne prijavljujemo: inače bi svatko s aktivacijskim kodom
            # upisom tuđe adrese ušao u tuđi račun. Ta osoba dobiva e-mail, a čarobnjak
            # se nastavlja preko oznake u sesiji.
            prijavi(request, korisnik, backend="django.contrib.auth.backends.ModelBackend")
        request.session.pop(SESIJA_PLOCICA, None)
        request.session[SESIJA_GROB] = {"grob_id": grob.pk, "vrijeme": time.time()}
        posalji_dobrodoslicu(request, grob)

        odgovor = redirect("aktivacija:pokojnik", kod=kod)
        dodijeli_pristup(odgovor, grob)  # uređaj koji je postavio lozinku ne mora je upisivati
        return odgovor

    kontekst = {"kod": kod, "forma": forma, "korak": 2, "ukupno_koraka": UKUPNO_KORAKA}
    return render(request, "aktivacija/korak_grob.html", kontekst)


def posalji_dobrodoslicu(request, grob):
    kontekst = {
        "naziv_groba": grob.naziv,
        "link_groba": request.build_absolute_uri(
            reverse("pristup:grob", kwargs={"kod": grob.plocica.kod})
        ),
        "link_prijave": request.build_absolute_uri(reverse("vlasnik:prijava")),
    }
    try:
        send_mail(
            _("Pločica je aktivirana: %(naziv)s") % {"naziv": grob.naziv},
            render_to_string("emailovi/aktivacija.txt", kontekst),
            None,
            [grob.kontakt_za_prijavu.email],
        )
    except Exception:
        log.exception("Slanje e-maila dobrodošlice nije uspjelo.")


def nastavak_aktivacije(view):
    """Koraci nakon stvaranja groba: smije ih otvoriti samo tko je grob upravo
    aktivirao (oznaka u sesiji) ili njegov kontakt za prijavu. Ostali dobivaju 404."""

    @never_cache
    @wraps(view)
    def omot(request, kod, *args, **kwargs):
        grob = get_object_or_404(Grob.objects.select_related("plocica"), plocica__kod=kod)
        stanje = request.session.get(SESIJA_GROB)
        iz_carobnjaka = _svjeze(stanje) and stanje.get("grob_id") == grob.pk
        korisnik = request.user
        kontakt = korisnik.is_authenticated and (
            korisnik.is_superuser or grob.kontakt_za_prijavu_id == korisnik.pk
        )
        if not (iz_carobnjaka or kontakt):
            raise Http404
        return view(request, grob, *args, **kwargs)

    return omot


@nastavak_aktivacije
def korak_pokojnik(request, grob):
    """Korak 3: prvi pokojnik."""
    kod = grob.plocica.kod
    if grob.pokojnici.exists():
        # Povratak na ovaj korak (tipka „natrag”) ne smije stvoriti istog pokojnika dvaput.
        return redirect("aktivacija:slike", kod=kod)

    forma = PokojnikForm(request.POST or None)
    if request.method == "POST" and forma.is_valid():
        pokojnik = forma.save(commit=False)
        pokojnik.grob = grob
        pokojnik.save()
        return redirect("aktivacija:slike", kod=kod)

    kontekst = {
        "kod": kod,
        "grob": grob,
        "forma": forma,
        "korak": 3,
        "ukupno_koraka": UKUPNO_KORAKA,
    }
    return render(request, "aktivacija/korak_pokojnik.html", kontekst)


@nastavak_aktivacije
def korak_slike(request, grob):
    """Korak 4: poziv na dodavanje slika. Sam upload dolazi u P-28."""
    kontekst = {
        "kod": grob.plocica.kod,
        "grob": grob,
        "pokojnik": grob.pokojnici.first(),
        "korak": 4,
        "ukupno_koraka": UKUPNO_KORAKA,
    }
    return render(request, "aktivacija/korak_slike.html", kontekst)


@nastavak_aktivacije
def gotovo(request, grob):
    kontekst = {
        "kod": grob.plocica.kod,
        "grob": grob,
        "email": grob.kontakt_za_prijavu.email,
        "prijavljen": request.user.is_authenticated,
    }
    return render(request, "aktivacija/gotovo.html", kontekst)
