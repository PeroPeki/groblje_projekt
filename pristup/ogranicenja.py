"""Ograničenje broja pogrešnih pokušaja (odluka 5).

Svaki neuspjeh se bilježi u NeuspjeliPokusaj. Prije provjere lozinke (ili
aktivacijskog koda, P-18) pita se je_zakljucano(): ako jest, tajna se uopće
ne provjerava. Brojevi su u postavci OGRANICENJA_POKUSAJA.
"""

import ipaddress
import logging
import math
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import NeuspjeliPokusaj

log = logging.getLogger(__name__)

NEPOZNATA_IP = "0.0.0.0"


def _normaliziraj_ip(tekst: str) -> str:
    """Valjana IP adresa u jedinstvenom obliku; ValueError ako tekst nije adresa."""
    adresa = ipaddress.ip_address(tekst.strip())
    if adresa.version == 6:
        if adresa.ipv4_mapped:
            return str(adresa.ipv4_mapped)
        # Jedan korisnik obično ima cijeli IPv6 /64 blok, pa se broji blok, a ne adresa.
        return str(ipaddress.ip_network(f"{adresa}/64", strict=False).network_address)
    return str(adresa)


def ip_posjetitelja(request) -> str:
    """IP adresa posjetitelja.

    Zaglavlje X-Forwarded-For čita se SAMO kad je IZA_PROXYJA=True (hosting):
    lokalno bi ga svatko mogao lažirati i tako zaobići ograničenje. Svaki
    posrednik svoju stranu dopisuje na KRAJ zaglavlja, pa se uzima adresa
    PROXY_BROJ_POSREDNIKA mjesta od kraja. Početak zaglavlja šalje sam
    posjetitelj i ne smije mu se vjerovati.
    """
    kandidati = []
    if settings.IZA_PROXYJA:
        dijelovi = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")
        if len(dijelovi) >= settings.PROXY_BROJ_POSREDNIKA:
            kandidati.append(dijelovi[-settings.PROXY_BROJ_POSREDNIKA])
    kandidati.append(request.META.get("REMOTE_ADDR", ""))
    for kandidat in kandidati:
        try:
            return _normaliziraj_ip(kandidat)
        except ValueError:
            continue
    log.warning("IP adresa posjetitelja nije poznata; provjeri IZA_PROXYJA i postavke posrednika.")
    return NEPOZNATA_IP


def _preostalo_minuta(pokusaji, granica, sada) -> int:
    """Koliko još minuta traje blokada za zadani skup pokušaja (0 = nema je).

    Blokada nastaje kad `najvise` zadnjih neuspjeha stane u isti prozor i traje
    cijeli prozor od zadnjeg od njih.
    """
    najvise, prozor_min = granica
    zadnji = list(pokusaji.order_by("-vrijeme").values_list("vrijeme", flat=True)[:najvise])
    prozor = timedelta(minutes=prozor_min)
    if len(zadnji) < najvise or zadnji[0] - zadnji[-1] > prozor:
        return 0
    preostalo = (zadnji[0] + prozor - sada).total_seconds()
    return max(0, math.ceil(preostalo / 60))


def je_zakljucano(vrsta: str, cilj, ip: str) -> int:
    """Vraća 0 ako pokušaj smije proći, inače koliko još minuta traje blokada.

    Granice: po IP adresi za isti cilj (npr. 5 u 15 minuta), po cilju s bilo
    koje adrese (npr. 30 u sat vremena) i, ako je zadana, po IP adresi za sve
    ciljeve zajedno ("po_ip_ukupno").
    """
    granice = settings.OGRANICENJA_POKUSAJA[vrsta]
    sada = timezone.now()
    pokusaji = NeuspjeliPokusaj.objects.filter(vrsta=vrsta, cilj=str(cilj))
    preostalo = [
        _preostalo_minuta(pokusaji, granice["po_cilju"], sada),
        _preostalo_minuta(pokusaji.filter(ip=ip), granice["po_ip"], sada),
    ]
    if "po_ip_ukupno" in granice:
        # Ista IP adresa bez obzira na cilj (npr. linkovi za prijavu na razne e-mailove).
        s_adrese = NeuspjeliPokusaj.objects.filter(vrsta=vrsta, ip=ip)
        preostalo.append(_preostalo_minuta(s_adrese, granice["po_ip_ukupno"], sada))
    return max(preostalo)


def zabiljezi_neuspjeh(vrsta: str, cilj, ip: str) -> None:
    NeuspjeliPokusaj.objects.create(vrsta=vrsta, cilj=str(cilj), ip=ip)


def najdulji_prozor() -> timedelta:
    """Najdulje razdoblje u kojem se neuspjesi još broje (za čišćenje starih zapisa)."""
    minute = [
        prozor for granice in settings.OGRANICENJA_POKUSAJA.values() for _, prozor in granice.values()
    ]
    return timedelta(minutes=max(minute))
