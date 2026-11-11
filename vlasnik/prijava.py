"""Prijava bez lozinke: jednokratni link poslan e-mailom (odluka 3, django-sesame)."""

import hashlib
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from sesame.utils import get_query_string

from korisnici.models import Korisnik
from pristup.models import NeuspjeliPokusaj
from pristup.ogranicenja import ip_posjetitelja, je_zakljucano, zabiljezi_neuspjeh

log = logging.getLogger(__name__)


def _cilj(email: str) -> str:
    # U evidenciju ne spremamo e-mail adrese (ni onih koji nisu korisnici), nego otisak.
    return hashlib.sha256(email.encode()).hexdigest()[:50]


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

    korisnik = Korisnik.objects.filter(email__iexact=email, is_active=True).first()
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
