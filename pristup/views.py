"""Javni pogledi: što posjetitelj vidi kad skenira QR kod na grobu.

Lozinka groba i zaključani ekran dolaze u P-12. Do tada ovi pogledi NE
provjeravaju pristup, pa se ne smiju objaviti na javnom poslužitelju.
"""

from django.shortcuts import get_object_or_404, redirect, render

from jezgra.models import Grob, Plocica

# Grob posjetitelju postoji samo ako je njegova pločica aktivirana.
AKTIVIRANI_GROBOVI = Grob.objects.filter(plocica__status=Plocica.Status.AKTIVIRANA)


def na_kanonsku_adresu(request, kod, pokojnik_id=None):
    """Preusmjerava /G/k7m4qx i slične zapise na /g/K7M4QX/ (odluka 18)."""
    if pokojnik_id is None:
        return redirect("pristup:grob", kod=kod.upper())
    return redirect("pristup:profil", kod=kod.upper(), pokojnik_id=pokojnik_id)


def grob(request, kod):
    """Stranica groba: popis pokojnika, ili odmah profil ako je pokojnik jedan."""
    grob = AKTIVIRANI_GROBOVI.filter(plocica__kod=kod).first()
    if grob is None:
        # Pločica ne postoji ILI još nije aktivirana: namjerno isti odgovor,
        # da se izvana ne može pogoditi koji kodovi postoje (odluka 8).
        return render(request, "aktivacija/unos_koda.html", {"kod": kod})

    pokojnici = list(grob.pokojnici.all())
    if len(pokojnici) == 1:
        return redirect("pristup:profil", kod=kod, pokojnik_id=pokojnici[0].pk)
    return render(request, "javno/grob.html", {"grob": grob, "kod": kod, "pokojnici": pokojnici})


def profil(request, kod, pokojnik_id):
    """Profil jednog pokojnika. Pokojnik se traži samo unutar groba iz adrese."""
    grob = get_object_or_404(AKTIVIRANI_GROBOVI, plocica__kod=kod)
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
