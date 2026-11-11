"""Prijava bez lozinke: jednokratni link poslan e-mailom (odluka 3, django-sesame)."""

import logging

from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext as _
from sesame.utils import get_query_string

from korisnici.models import Korisnik
from pristup.models import NeuspjeliPokusaj
from pristup.ogranicenja import ip_posjetitelja, je_zakljucano, zabiljezi_neuspjeh

log = logging.getLogger(__name__)


def _cilj(email: str) -> str:
    # U evidenciju ne spremamo e-mail adrese (ni onih koji nisu korisnici), nego otisak
    # s ključem (SECRET_KEY), koji se ne može pogoditi isprobavanjem popisa adresa.
    return salted_hmac("link-za-prijavu", email).hexdigest()[:50]


def prijavi(request, korisnik, backend=None) -> None:
    """login() uz trajanje prijave za vlasnički dio (30 dana)."""
    login(request, korisnik, backend=backend)
    request.session.set_expiry(settings.VLASNIK_PRIJAVA_SEKUNDI)


def link_za_prijavu(request, korisnik) -> str:
    return request.build_absolute_uri(reverse("vlasnik:potvrda")) + get_query_string(korisnik)


def zatrazi_link_za_prijavu(request, email: str) -> None:
    """Šalje link ako korisnik postoji. Pozivatelj ne saznaje je li poslan.

    Ograničenje (3 linka za isti e-mail u 15 minuta) broji i adrese koje ne
    postoje, da se ponašanje za postojeću i nepostojeću adresu ne razlikuje.
    """
    vrsta = NeuspjeliPokusaj.Vrsta.PRIJAVA
    ip = ip_posjetitelja(request)
    if je_zakljucano(vrsta, _cilj(email), ip):
        return
    zabiljezi_neuspjeh(vrsta, _cilj(email), ip)  # ovdje bilježi poslani link, ne neuspjeh

    # Administratori se prijavljuju lozinkom u /admin/. Link im se ne šalje, da
    # pristup poštanskom sandučiću ne bude dovoljan za ulaz u administraciju.
    korisnik = (
        Korisnik.objects.filter(email__iexact=email, is_active=True, is_staff=False, is_superuser=False)
        .order_by("pk")
        .first()
    )
    if korisnik is None:
        return
    poruka = render_to_string(
        "emailovi/prijava.txt",
        {"link": link_za_prijavu(request, korisnik), "minuta": settings.SESAME_MAX_AGE // 60},
    )
    try:
        send_mail(_("Vaš link za prijavu u Vječnu spomen"), poruka, None, [korisnik.email])
    except Exception:
        # Greška pri slanju ne smije promijeniti odgovor (otkrila bi da adresa postoji).
        log.exception("Slanje linka za prijavu nije uspjelo.")
