"""Javni pogledi: što posjetitelj vidi kad skenira QR kod na grobu."""

from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from jezgra.models import Grob, Plocica

from .forms import LozinkaForm
from .kolacici import dodijeli_pristup, ima_pristup

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
        if grob.provjeri_lozinku(forma.cleaned_data["lozinka"]):
            # Post/Redirect/Get: nakon točne lozinke vraćamo se na istu adresu.
            odgovor = redirect(request.get_full_path())
            dodijeli_pristup(odgovor, grob)
            return odgovor
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
        return render(request, "aktivacija/unos_koda.html", {"kod": kod})
    if not ima_pristup(request, grob):
        return zakljucani_ekran(request, grob, kod)

    pokojnici = list(grob.pokojnici.all())
    if len(pokojnici) == 1:
        return redirect("pristup:profil", kod=kod, pokojnik_id=pokojnici[0].pk)
    return render(request, "javno/grob.html", {"grob": grob, "kod": kod, "pokojnici": pokojnici})


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
        # Kad je pokojnik jedini, stranica groba samo vraća na ovaj profil,
        # pa link „natrag na grob” nema smisla.
        "ima_popis_pokojnika": grob.pokojnici.count() > 1,
    }
    return render(request, "javno/profil.html", kontekst)
