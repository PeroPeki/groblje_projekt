"""Vlasnički dio: prijava linkom na e-mail i popis grobova."""

from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Count, F, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST
from sesame.utils import get_user

from jezgra.models import Grob
from knjiga.models import PorukaSjecanja
from pristup.models import ZahtjevZaPristup

from .dozvole import na_prijavu, vlasnik_groba
from .forms import LozinkaGrobaForm, NazivGrobaForm, PrijavaForm
from .prijava import prijavi, zatrazi_link_za_prijavu

TOKEN = "sesame"  # naziv parametra u linku i skrivenog polja u formi (SESAME_TOKEN_NAME)


def prijava(request):
    """Forma s e-mailom. Odgovor je isti postoji li adresa u sustavu ili ne."""
    if request.user.is_authenticated:
        return redirect("vlasnik:popis")
    forma = PrijavaForm(request.POST or None)
    if request.method == "POST" and forma.is_valid():
        zatrazi_link_za_prijavu(request, forma.cleaned_data["email"])
        return redirect("vlasnik:prijava_poslano")
    return render(request, "vlasnik/prijava.html", {"forma": forma})


def prijava_poslano(request):
    return render(request, "vlasnik/prijava_poslano.html")


@sensitive_post_parameters(TOKEN)
@never_cache
def potvrda(request):
    """Stranica na koju vodi link iz e-maila.

    Samo otvaranje linka (GET) nikoga ne prijavljuje: programi za e-poštu
    znaju sami „otvoriti” link i tako bi potrošili jednokratni token. Prijava
    se događa tek klikom na gumb (POST).
    """
    if request.method == "POST":
        korisnik = get_user(request.POST.get(TOKEN, ""), update_last_login=False)
        if korisnik is None or korisnik.is_staff or korisnik.is_superuser:
            return render(request, "vlasnik/potvrda.html", {"link_ne_vrijedi": True})
        prijavi(request, korisnik)  # login() mijenja last_login, pa token više ne vrijedi
        return redirect("vlasnik:popis")

    token = request.GET.get(TOKEN)
    if not token:
        return redirect("vlasnik:prijava")
    return render(request, "vlasnik/potvrda.html", {"token": token, "link_ne_vrijedi": False})


@require_POST
def odjava(request):
    logout(request)
    return redirect("vlasnik:prijava")


def _broj(upit):
    """Podupit koji vraća broj redaka (za stupac u popisu, bez množenja redaka JOIN-om)."""
    return Subquery(upit.order_by().values("grob").annotate(broj=Count("pk")).values("broj"))


@never_cache
def popis(request):
    """Grobovi kojima je prijavljeni korisnik kontakt za prijavu."""
    if not request.user.is_authenticated:
        return na_prijavu(request)
    poruke = PorukaSjecanja.objects.filter(
        pokojnik__grob=OuterRef("pk"), status=PorukaSjecanja.Status.NA_CEKANJU, skrivena=False
    ).annotate(grob=F("pokojnik__grob"))
    zahtjevi = ZahtjevZaPristup.objects.filter(grob=OuterRef("pk"), status=ZahtjevZaPristup.Status.NOVI)
    grobovi = (
        request.user.grobovi.select_related("plocica")
        .annotate(
            poruka_na_cekanju=Coalesce(_broj(poruke), 0),
            zahtjeva_na_cekanju=Coalesce(_broj(zahtjevi), 0),
        )
        .order_by("naziv")
    )
    return render(request, "vlasnik/popis.html", {"grobovi": grobovi})


# --- Postavke groba (P-21) --------------------------------------------------


def _stranica_postavki(request, grob, forma_naziv=None, forma_lozinka=None, status=200):
    kontekst = {
        "grob": grob,
        "kod": grob.plocica.kod,
        "forma_naziv": forma_naziv or NazivGrobaForm(instance=grob),
        "forma_lozinka": forma_lozinka or LozinkaGrobaForm(),
    }
    return render(request, "vlasnik/postavke.html", kontekst, status=status)


def _natrag_na_postavke(grob):
    return redirect("vlasnik:postavke", kod=grob.plocica.kod)


@vlasnik_groba
def postavke(request, grob):
    return _stranica_postavki(request, grob)


@vlasnik_groba
@require_POST
def postavke_naziv(request, grob):
    forma = NazivGrobaForm(request.POST, instance=grob)
    if not forma.is_valid():
        grob.refresh_from_db()  # da se u naslovu stranice ne prikaže nespremljeni naziv
        return _stranica_postavki(request, grob, forma_naziv=forma, status=400)
    # Sprema se samo naziv: spremanje cijelog retka moglo bi vratiti staru lozinku
    # ili javni prikaz ako ih je u međuvremenu promijenio drugi zahtjev.
    forma.save(commit=False).save(update_fields=["naziv", "promijenjeno"])
    messages.success(request, _("Naziv groba je promijenjen."))
    return _natrag_na_postavke(grob)


@sensitive_post_parameters("lozinka", "lozinka2")
@vlasnik_groba
@require_POST
def postavke_lozinka(request, grob):
    forma = LozinkaGrobaForm(request.POST)
    if not forma.is_valid():
        return _stranica_postavki(request, grob, forma_lozinka=forma, status=400)
    grob.postavi_lozinku(forma.cleaned_data["lozinka"])
    grob.save(update_fields=["lozinka_hash", "promijenjeno"])
    if forma.cleaned_data["odjavi_uredjaje"]:
        _povecaj_verziju_pristupa(grob)
        messages.success(request, _("Lozinka je promijenjena, a svi uređaji su odjavljeni."))
    else:
        messages.success(request, _("Lozinka je promijenjena."))
    return _natrag_na_postavke(grob)


def _povecaj_verziju_pristupa(grob):
    """Kolačić pristupa sadrži verziju: kad se ona poveća, stari kolačići više ne vrijede.

    F() povećava vrijednost u samoj bazi, pa se dvije istovremene odjave ne ponište.
    """
    Grob.objects.filter(pk=grob.pk).update(
        verzija_pristupa=F("verzija_pristupa") + 1, promijenjeno=timezone.now()
    )


@vlasnik_groba
@require_POST
def odjavi_uredjaje(request, grob):
    _povecaj_verziju_pristupa(grob)
    messages.success(request, _("Svi uređaji su odjavljeni. Za ulaz treba ponovno upisati lozinku."))
    return _natrag_na_postavke(grob)


@vlasnik_groba
@require_POST
def javni_prikaz(request, grob):
    """Prekidač javnog prikaza. Uključivanje traži izričitu potvrdu (odluka 5)."""
    zeljeno = request.POST.get("javni_prikaz")
    if zeljeno not in ("da", "ne"):
        return HttpResponseBadRequest()
    ukljuci = zeljeno == "da"
    greska = None
    if ukljuci and request.POST.get("potvrda") != "da":
        greska = _("Za uključivanje označite da razumijete što javni prikaz znači.")
    else:
        grob.javni_prikaz = ukljuci
        grob.save(update_fields=["javni_prikaz", "promijenjeno"])

    if request.htmx:
        # HTMX mijenja samo ovaj dio stranice.
        kontekst = {"grob": grob, "kod": grob.plocica.kod, "greska_javnog_prikaza": greska}
        return render(request, "vlasnik/_javni_prikaz.html", kontekst)
    if greska:
        messages.error(request, greska)
    return _natrag_na_postavke(grob)
