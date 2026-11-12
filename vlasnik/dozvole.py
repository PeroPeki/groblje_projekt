"""Tko smije u vlasnički dio jednog groba."""

from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, resolve_url
from django.views.decorators.cache import never_cache

from jezgra.models import Grob


def na_prijavu(request):
    """Neprijavljenog korisnika šalje na prijavu.

    HTMX bi obično preusmjeravanje slijedio sam i stranicu za prijavu ugurao u
    dio stranice koji je trebao zamijeniti. Zaglavlje HX-Redirect mu kaže da
    umjesto toga otvori prijavu kao cijelu stranicu.
    """
    if request.htmx:
        return HttpResponse(status=204, headers={"HX-Redirect": resolve_url("vlasnik:prijava")})
    return redirect_to_login(request.get_full_path(), resolve_url("vlasnik:prijava"))


def vlasnik_groba(view):
    """Pogled dobiva `grob` umjesto koda iz adrese.

    Prolazi samo kontakt za prijavu tog groba (ili superuser, za uslugu
    postavljanja sadržaja). Svi ostali dobivaju 404, a ne 403: tako se ne
    otkriva postoji li grob s tim kodom. Odgovori se ne spremaju u
    predmemoriju preglednika, da nakon odjave ne ostanu vidljivi tipkom „natrag”.
    """

    @never_cache
    @wraps(view)
    def omot(request, kod, *args, **kwargs):
        korisnik = request.user
        if not korisnik.is_authenticated:
            return na_prijavu(request)
        grob = get_object_or_404(Grob.objects.select_related("plocica", "partner"), plocica__kod=kod)
        if not (korisnik.is_superuser or grob.kontakt_za_prijavu_id == korisnik.pk):
            raise Http404
        return view(request, grob, *args, **kwargs)

    return omot
