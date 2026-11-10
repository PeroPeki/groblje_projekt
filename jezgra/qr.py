"""QR kodovi za pločice (odluke 7 i 18).

Link je velikim slovima, da QR koristi alfanumerički način (manja verzija,
krupniji moduli), a korekcija pogrešaka je razine H (~30 % površine smije
biti oštećeno ili prljavo).
"""

import csv
import io
import zipfile

import segno
from django.conf import settings


def link_za_kod(kod: str) -> str:
    return f"{settings.QR_BAZNI_URL}{kod}".upper()


def qr_za_kod(kod: str) -> segno.QRCode:
    return segno.make_qr(link_za_kod(kod), error="h", boost_error=False)


def zip_s_qr_kodovima(plocice, aktivacijski_kodovi: dict[str, str] | None = None) -> bytes:
    """ZIP s KOD.svg i KOD.png za svaku pločicu te kodovi.csv.

    `aktivacijski_kodovi` ({kod: aktivacijski_kod}) postoji samo odmah nakon
    stvaranja serije. Kasnije se ne može vratiti iz hasha, pa CSV tada nema
    taj stupac.
    """
    spremnik = io.BytesIO()
    with zipfile.ZipFile(spremnik, "w", zipfile.ZIP_DEFLATED) as z:
        tablica = io.StringIO()
        pisac = csv.writer(tablica)
        if aktivacijski_kodovi is not None:
            pisac.writerow(["kod", "aktivacijski_kod", "link"])
        else:
            pisac.writerow(["kod", "link"])

        for plocica in plocice:
            qr = qr_za_kod(plocica.kod)
            for vrsta in ("svg", "png"):
                slika = io.BytesIO()
                qr.save(slika, kind=vrsta, scale=10, border=4)  # border 4 = obavezni bijeli rub
                z.writestr(f"{plocica.kod}.{vrsta}", slika.getvalue())

            if aktivacijski_kodovi is not None:
                pisac.writerow([plocica.kod, aktivacijski_kodovi[plocica.kod], link_za_kod(plocica.kod)])
            else:
                pisac.writerow([plocica.kod, link_za_kod(plocica.kod)])

        # BOM da Excel ispravno prikaže UTF-8
        z.writestr("kodovi.csv", "﻿" + tablica.getvalue())
    return spremnik.getvalue()
