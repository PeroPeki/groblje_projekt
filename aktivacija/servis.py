"""Aktivacija: trenutak kad neaktivirana pločica postaje QR oznaka groba (odluka 8)."""

from django.db import transaction
from django.utils import timezone

from jezgra.models import Grob, Plocica
from korisnici.models import Korisnik


class VecAktivirana(Exception):
    """Pločicu je u međuvremenu netko drugi aktivirao."""


def aktiviraj_plocicu(plocica_id, *, naziv, oznaka_grobnog_mjesta, vlasnik_ime, email, lozinka):
    """Stvara grob i označava pločicu aktiviranom, sve ili ništa.

    select_for_update zaključava redak pločice do kraja transakcije, pa dva
    istovremena zahtjeva ne mogu stvoriti dva groba za istu pločicu.
    Vraća (grob, je_li_korisnik_novi).
    """
    with transaction.atomic():
        plocica = (
            Plocica.objects.select_for_update().select_related("serija__partner").get(pk=plocica_id)
        )
        if plocica.status != Plocica.Status.NEAKTIVIRANA:
            raise VecAktivirana

        # Ista osoba može voditi više grobova: postojećem korisniku grob se samo dodaje.
        korisnik = Korisnik.objects.filter(email__iexact=email).first()
        novi_korisnik = korisnik is None
        if novi_korisnik:
            korisnik = Korisnik(email=email, username=email)
            korisnik.set_unusable_password()  # prijava je samo linkom na e-mail
            korisnik.save()

        grob = Grob(
            plocica=plocica,
            partner=plocica.serija.partner,  # odluka 15: partner se kopira iz serije
            naziv=naziv,
            oznaka_grobnog_mjesta=oznaka_grobnog_mjesta,
            vlasnik_ime=vlasnik_ime,
            kontakt_za_prijavu=korisnik,
        )
        grob.postavi_lozinku(lozinka)
        grob.save()

        plocica.status = Plocica.Status.AKTIVIRANA
        plocica.aktivirana_u = timezone.now()
        plocica.save(update_fields=["status", "aktivirana_u"])
    return grob, novi_korisnik
