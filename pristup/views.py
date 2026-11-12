"""Javni pogledi: što posjetitelj vidi kad skenira QR kod na grobu."""

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from aktivacija.views import ekran_unosa_koda
from jezgra.models import Grob, Plocica

from .forms import LozinkaForm
from .kolacici import dodijeli_pristup, ima_pristup
from .models import NeuspjeliPokusaj
from .ogranicenja import ip_posjetitelja, je_zakljucano, odgovor_blokade, zabiljezi_neuspjeh

# Grob posjetitelju postoji samo ako je njegova pločica aktivirana.
AKTIVIRANI_GROBOVI = Grob.objects.filter(
    plocica__status=Plocica.Status.AKTIVIRANA
).select_related("partner", "plocica")


def na_kanonsku_adresu(request, kod, pokojnik_id=None):
    """Preusmjerava /G/k7m4qx i slične zapise na /g/K7M4QX/ (odluka 18)."""
    if pokojnik_id is None:
        return redirect("pristup:grob", kod=kod.upper())
    return redirect("pristup:profil", kod=kod.upper(), pokojnik_id=pokojnik_id)


def zakljucani_ekran(request, grob, kod):
    """Zaključani ekran s formom za lozinku groba (odluka 5).

    Predlošku se namjerno šalju samo naziv groba i naziv partnera, a ne cijeli
    grob: tako se u predlošku ne mogu slučajno prikazati pokojnici.
    """
    forma = LozinkaForm(request.POST or None)
    if request.method == "POST" and forma.is_valid():
        ip = ip_posjetitelja(request)
        minuta = je_zakljucano(NeuspjeliPokusaj.Vrsta.LOZINKA, grob.pk, ip)
        if minuta:
            # Dok traje blokada, lozinka se uopće ne provjerava (ni točna ne prolazi).
            return odgovor_blokade(request, minuta)
        if grob.provjeri_lozinku(forma.cleaned_data["lozinka"]):
            # Post/Redirect/Get: nakon točne lozinke vraćamo se na istu adresu.
            odgovor = redirect(request.get_full_path())
            dodijeli_pristup(odgovor, grob)
            return odgovor
        zabiljezi_neuspjeh(NeuspjeliPokusaj.Vrsta.LOZINKA, grob.pk, ip)
        forma.add_error("lozinka", _("Lozinka nije točna."))

    kontekst = {
        "naziv_groba": grob.naziv,
        "naziv_partnera": grob.partner.naziv,
        "kod": kod,
        "forma": forma,
        "url_zahtjeva": None,  # „Zatraži pristup” dolazi u P-24
    }
    return render(request, "javno/zakljucano.html", kontekst)


# sensitive_post_parameters: lozinka se ne ispisuje u izvještajima o greškama.
@sensitive_post_parameters("lozinka")
@never_cache
def grob(request, kod):
    """Stranica groba: popis pokojnika, ili odmah profil ako je pokojnik jedan."""
    grob = AKTIVIRANI_GROBOVI.filter(plocica__kod=kod).first()
    if grob is None:
        # Pločica ne postoji ILI još nije aktivirana: namjerno isti odgovor,
        # da se izvana ne može pogoditi koji kodovi postoje (odluka 8).
        return ekran_unosa_koda(request, kod)
    if not ima_pristup(request, grob):
        return zakljucani_ekran(request, grob, kod)

    pokojnici = list(grob.pokojnici.all())
    if len(pokojnici) == 1:
        return redirect("pristup:profil", kod=kod, pokojnik_id=pokojnici[0].pk)
    return render(request, "javno/grob.html", {"grob": grob, "kod": kod, "pokojnici": pokojnici})


def srodnici_za_prikaz(pokojnik) -> list[dict]:
    """Srodnici koje posjetitelj smije vidjeti (odluka 3a, GDPR).

    Filtrira se ovdje, a ne u predlošku: živuća osoba bez pristanka uopće ne
    dolazi do predloška, a za onu s pristankom šalju se samo ime i srodstvo.
    """
    srodnici = []
    for srodnik in pokojnik.srodnici.select_related("povezani_pokojnik__grob__plocica"):
        povezani = srodnik.povezani_pokojnik
        if povezani is not None:
            if povezani.grob.plocica.status != Plocica.Status.AKTIVIRANA:
                continue  # grob koji za posjetitelje ne postoji: ni ime ni link
            ime = str(povezani)
            url = reverse(
                "pristup:profil",
                kwargs={"kod": povezani.grob.plocica.kod, "pokojnik_id": povezani.pk},
            )
        elif srodnik.pristanak_na_prikaz:
            ime, url = srodnik.ime_i_prezime, None
        else:
            continue
        srodnici.append({"srodstvo": srodnik.get_vrsta_srodstva_display(), "ime": ime, "url": url})
    return srodnici


@sensitive_post_parameters("lozinka")
@never_cache
def profil(request, kod, pokojnik_id):
    """Profil jednog pokojnika. Pokojnik se traži samo unutar groba iz adrese."""
    grob = get_object_or_404(AKTIVIRANI_GROBOVI, plocica__kod=kod)
    # Pristup se provjerava PRIJE traženja pokojnika, da zaključani ekran ne
    # otkriva koji ID-evi pokojnika postoje.
    if not ima_pristup(request, grob):
        return zakljucani_ekran(request, grob, kod)

    pokojnik = get_object_or_404(grob.pokojnici, pk=pokojnik_id)
    kontekst = {
        "grob": grob,
        "kod": kod,
        "pokojnik": pokojnik,
        "srodnici": srodnici_za_prikaz(pokojnik),
        # Kad je pokojnik jedini, stranica groba samo vraća na ovaj profil,
        # pa link „natrag na grob” nema smisla.
        "ima_popis_pokojnika": grob.pokojnici.count() > 1,
    }
    return render(request, "javno/profil.html", kontekst)
