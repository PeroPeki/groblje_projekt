"""Ograničenje broja pogrešnih pokušaja (odluka 5).

Svaki neuspjeh se bilježi u NeuspjeliPokusaj. Prije provjere lozinke (ili
aktivacijskog koda, P-18) pita se je_zakljucano(): ako jest, tajna se uopće
ne provjerava. Brojevi su u postavci OGRANICENJA_POKUSAJA.
"""

import ipaddress
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import NeuspjeliPokusaj

NEPOZNATA_IP = "0.0.0.0"


def ip_posjetitelja(request) -> str:
    """IP adresa posjetitelja.

    Zaglavlje X-Forwarded-For čita se SAMO kad je IZA_PROXYJA=True (hosting):
    lokalno bi ga svatko mogao lažirati i tako zaobići ograničenje.
    """
    kandidati = []
    if settings.IZA_PROXYJA:
        kandidati.append(request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0])
    kandidati.append(request.META.get("REMOTE_ADDR", ""))
    for kandidat in kandidati:
        try:
            return str(ipaddress.ip_address(kandidat.strip()))
        except ValueError:
            continue
    return NEPOZNATA_IP


def je_zakljucano(vrsta: str, cilj, ip: str) -> int:
    """Vraća 0 ako pokušaj smije proći, inače broj minuta koliko traje blokada.

    Dvije granice: po IP adresi za isti cilj (npr. 5 u 15 minuta) i po cilju
    s bilo koje adrese (npr. 30 u sat vremena).
    """
    max_ip, prozor_ip, max_cilj, prozor_cilj = settings.OGRANICENJA_POKUSAJA[vrsta]
    sada = timezone.now()
    pokusaji = NeuspjeliPokusaj.objects.filter(vrsta=vrsta, cilj=str(cilj))

    if pokusaji.filter(vrijeme__gt=sada - timedelta(minutes=prozor_cilj)).count() >= max_cilj:
        return prozor_cilj
    if (
        pokusaji.filter(ip=ip, vrijeme__gt=sada - timedelta(minutes=prozor_ip)).count()
        >= max_ip
    ):
        return prozor_ip
    return 0


def zabiljezi_neuspjeh(vrsta: str, cilj, ip: str) -> None:
    NeuspjeliPokusaj.objects.create(vrsta=vrsta, cilj=str(cilj), ip=ip)
