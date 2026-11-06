"""Generiranje slučajnih kodova za pločice (odluka 18).

Koristi se modul `secrets`, a ne `random`: kodovi moraju biti nepredvidljivi.
"""

import secrets

# Bez dvosmislenih znakova 0, O, 1, I, L (odluka 18): 31 znak.
ABECEDA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

DULJINA_KODA_PLOCICE = 6
DULJINA_AKTIVACIJSKOG_KODA = 8


def novi_kod(duljina: int) -> str:
    """Slučajan kod zadane duljine iz ABECEDE."""
    return "".join(secrets.choice(ABECEDA) for _ in range(duljina))


def novi_kod_plocice() -> str:
    """6-znakovni kod pločice koji još ne postoji u bazi."""
    from jezgra.models import Plocica

    while True:
        kod = novi_kod(DULJINA_KODA_PLOCICE)
        if not Plocica.objects.filter(kod=kod).exists():
            return kod


def novi_aktivacijski_kod() -> str:
    """8-znakovni aktivacijski kod. U bazu se sprema samo njegov hash."""
    return novi_kod(DULJINA_AKTIVACIJSKOG_KODA)
