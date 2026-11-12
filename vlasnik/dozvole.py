"""Tko smije u vlasnički dio jednog groba."""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404

from jezgra.models import Grob


def vlasnik_groba(view):
    """Pogled dobiva `grob` umjesto koda iz adrese.

    Prolazi samo kontakt za prijavu tog groba (ili superuser, za uslugu
    postavljanja sadržaja). Svi ostali dobivaju 404, a ne 403: tako se ne
    otkriva postoji li grob s tim kodom.
    """

    @login_required
    @wraps(view)
    def omot(request, kod, *args, **kwargs):
        grob = get_object_or_404(Grob.objects.select_related("plocica", "partner"), plocica__kod=kod)
        korisnik = request.user
        if not (korisnik.is_superuser or grob.kontakt_za_prijavu_id == korisnik.pk):
            raise Http404
        return view(request, grob, *args, **kwargs)

    return omot
