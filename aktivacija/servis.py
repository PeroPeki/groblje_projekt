"""Aktivacija: trenutak kad neaktivirana pločica postaje QR oznaka groba (odluka 8)."""

from django.db import IntegrityError, transaction
from django.utils import timezone

from jezgra.models import Grob, Plocica
from korisnici.models import Korisnik


class VecAktivirana(Exception):
    """Pločicu je u međuvremenu netko drugi aktivirao."""


class NedopustenaAdresa(Exception):
    """E-mail pripada računu koji ne može biti kontakt za prijavu (administrator, isključen račun)."""


def _kontakt_za_prijavu(email, prijavljeni_korisnik):
    """Vraća (korisnik, je_li_novi) za upisanu e-mail adresu."""
    korisnik = Korisnik.objects.filter(email__iexact=email).order_by("pk").first()
    if korisnik is None:
        try:
            with transaction.atomic():  # savepoint: neuspjeli INSERT ne ruši cijelu aktivaciju
                korisnik = Korisnik(email=email, username=email)
                korisnik.set_unusable_password()  # prijava je samo linkom na e-mail
                korisnik.save()
            return korisnik, True
        except IntegrityError:
            # Netko je isti račun stvorio u istom trenutku, ili je korisničko ime zauzeto.
            korisnik = Korisnik.objects.filter(email__iexact=email).order_by("pk").first()
            if korisnik is None:
                raise NedopustenaAdresa from None

    # Administratori i isključeni računi ne mogu se prijaviti linkom, pa grob ne bi imao tko uređivati.
    if not korisnik.is_active or korisnik.is_staff or korisnik.is_superuser:
        raise NedopustenaAdresa

    if korisnik != prijavljeni_korisnik and not korisnik.has_usable_password():
        # Grob se dodaje postojećem računu, a upisao ga je netko tko nije prijavljen kao
        # taj račun. Nova (neupotrebljiva) lozinka odjavljuje sve postojeće prijave tog
        # računa: ako ga je ranije netko otvorio na tuđu adresu, sada gubi pristup.
        # Pravi vlasnik adrese prijavljuje se ponovno linkom iz e-maila.
        korisnik.set_unusable_password()
        korisnik.save(update_fields=["password"])
    return korisnik, False


def aktiviraj_plocicu(
    plocica_id, *, naziv, oznaka_grobnog_mjesta, vlasnik_ime, email, lozinka, prijavljeni_korisnik=None
):
    """Stvara grob i označava pločicu aktiviranom, sve ili ništa.

    select_for_update zaključava redak pločice do kraja transakcije, pa dva
    istovremena zahtjeva ne mogu stvoriti dva groba za istu pločicu.
    Vraća (grob, je_li_korisnik_novi).
    """
    grob = Grob(naziv=naziv, oznaka_grobnog_mjesta=oznaka_grobnog_mjesta, vlasnik_ime=vlasnik_ime)
    grob.postavi_lozinku(lozinka)  # hash je spor, pa se računa prije zaključavanja retka

    try:
        with transaction.atomic():
            plocica = Plocica.objects.select_for_update().get(pk=plocica_id)
            if plocica.status != Plocica.Status.NEAKTIVIRANA:
                raise VecAktivirana

            korisnik, novi_korisnik = _kontakt_za_prijavu(email, prijavljeni_korisnik)
            grob.plocica = plocica
            grob.partner = plocica.serija.partner  # odluka 15: partner se kopira iz serije
            grob.kontakt_za_prijavu = korisnik
            grob.save()

            plocica.status = Plocica.Status.AKTIVIRANA
            plocica.aktivirana_u = timezone.now()
            plocica.save(update_fields=["status", "aktivirana_u"])
    except IntegrityError:
        # Baza bez zaključavanja redaka (SQLite): drugi zahtjev je bio brži, a
        # jedinstvena veza grob–pločica je spriječila drugi grob.
        raise VecAktivirana from None
    return grob, novi_korisnik
