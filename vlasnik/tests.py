"""Testovi vlasničkog dijela: prijava linkom na e-mail (P-17)."""

import re
import time
from unittest import mock

from django.core import mail
from django.test import TestCase

from korisnici.models import Korisnik
from pristup.models import NeuspjeliPokusaj


def link_iz_poruke(poruka) -> str:
    """Putanja i token iz linka u e-mailu, npr. /vlasnik/potvrda/?sesame=..."""
    return re.search(r"http://testserver(/vlasnik/potvrda/\?sesame=\S+)", poruka.body).group(1)


class PrijavaLinkomTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.korisnik = Korisnik.objects.create(username="ana", email="ana@example.com")

    def zatrazi(self, email="ana@example.com"):
        return self.client.post("/vlasnik/prijava/", {"email": email})

    def potvrdi(self, link):
        token = link.split("sesame=")[1]
        return self.client.post("/vlasnik/potvrda/", {"sesame": token})

    def prijavljen(self) -> bool:
        return "_auth_user_id" in self.client.session

    # --- slanje linka --------------------------------------------------------

    def test_postojeci_e_mail_dobiva_poruku_s_linkom(self):
        odgovor = self.zatrazi()
        self.assertRedirects(odgovor, "/vlasnik/prijava/poslano/")
        self.assertEqual(len(mail.outbox), 1)
        poruka = mail.outbox[0]
        self.assertEqual(poruka.to, ["ana@example.com"])
        self.assertIn("/vlasnik/potvrda/?sesame=", poruka.body)
        self.assertIn("15 minuta", poruka.body)
        self.assertNotIn("&amp;", poruka.body)  # obični tekst, bez HTML escapiranja

    def test_velika_slova_i_razmaci_u_adresi_ne_smetaju(self):
        self.zatrazi("  Ana@Example.COM ")
        self.assertEqual(len(mail.outbox), 1)

    def test_odgovor_je_isti_za_postojeci_i_nepostojeci_e_mail(self):
        postojeci = self.zatrazi("ana@example.com")
        nepostojeci = self.zatrazi("nitko@example.com")
        self.assertEqual(postojeci.status_code, nepostojeci.status_code)
        self.assertEqual(postojeci["Location"], nepostojeci["Location"])
        self.assertEqual(len(mail.outbox), 1)  # samo postojeća adresa je dobila poruku
        stranica = self.client.get("/vlasnik/prijava/poslano/")
        self.assertContains(stranica, "Ako je adresa upisana u sustavu")
        self.assertNotContains(stranica, "example.com")

    def test_neaktivan_korisnik_ne_dobiva_link(self):
        Korisnik.objects.filter(pk=self.korisnik.pk).update(is_active=False)
        self.assertRedirects(self.zatrazi(), "/vlasnik/prijava/poslano/")
        self.assertEqual(mail.outbox, [])

    def test_cetvrti_zahtjev_u_15_minuta_ne_salje_e_mail(self):
        for _ in range(4):
            odgovor = self.zatrazi()
        self.assertEqual(len(mail.outbox), 3)
        self.assertRedirects(odgovor, "/vlasnik/prijava/poslano/")  # odgovor je i dalje isti

    def test_ogranicenje_vrijedi_po_adresi_a_ne_za_sve(self):
        Korisnik.objects.create(username="iva", email="iva@example.com")
        for _ in range(3):
            self.zatrazi()
        self.zatrazi("iva@example.com")
        self.assertEqual(mail.outbox[-1].to, ["iva@example.com"])

    def test_s_jedne_ip_adrese_najvise_10_zahtjeva_na_razne_adrese(self):
        for i in range(10):
            Korisnik.objects.create(username=f"k{i}", email=f"k{i}@example.com")
            self.zatrazi(f"k{i}@example.com")
        self.assertEqual(len(mail.outbox), 10)
        self.zatrazi("ana@example.com")
        self.assertEqual(len(mail.outbox), 10)

    def test_administrator_ne_dobiva_link_i_ne_moze_se_prijaviti_linkom(self):
        admin = Korisnik.objects.create(
            username="admin", email="admin@example.com", is_staff=True, is_superuser=True
        )
        self.zatrazi("admin@example.com")
        self.assertEqual(mail.outbox, [])

        from sesame.utils import get_token

        odgovor = self.client.post("/vlasnik/potvrda/", {"sesame": get_token(admin)})
        self.assertContains(odgovor, "Ovaj link više ne vrijedi")
        self.assertFalse(self.prijavljen())

    def test_u_evidenciji_nema_e_mail_adrese(self):
        self.zatrazi()
        self.assertNotIn("ana", NeuspjeliPokusaj.objects.get().cilj)

    def test_greska_pri_slanju_ne_mijenja_odgovor(self):
        with mock.patch("vlasnik.prijava.send_mail", side_effect=OSError("SMTP ne radi")):
            with self.assertLogs("vlasnik.prijava", level="ERROR"):
                odgovor = self.zatrazi()
        self.assertRedirects(odgovor, "/vlasnik/prijava/poslano/")

    # --- potvrda linka -------------------------------------------------------

    def test_otvaranje_linka_ne_prijavljuje_nego_trazi_klik_na_gumb(self):
        self.zatrazi()
        odgovor = self.client.get(link_iz_poruke(mail.outbox[0]))
        self.assertContains(odgovor, "Prijavi me")
        self.assertFalse(self.prijavljen())

    def test_klik_na_gumb_prijavljuje_i_vodi_na_popis_grobova(self):
        self.zatrazi()
        link = link_iz_poruke(mail.outbox[0])
        self.client.get(link)  # program za e-poštu ili korisnik otvore link
        odgovor = self.potvrdi(link)
        self.assertRedirects(odgovor, "/vlasnik/")
        self.assertTrue(self.prijavljen())
        self.assertContains(self.client.get("/vlasnik/"), "ana@example.com")

    def test_isti_link_ne_radi_drugi_put(self):
        self.zatrazi()
        link = link_iz_poruke(mail.outbox[0])
        self.potvrdi(link)
        self.client.post("/vlasnik/odjava/")

        odgovor = self.potvrdi(link)
        self.assertContains(odgovor, "Ovaj link više ne vrijedi")
        self.assertFalse(self.prijavljen())

    def test_link_stariji_od_15_minuta_ne_radi(self):
        self.zatrazi()
        link = link_iz_poruke(mail.outbox[0])
        za_16_minuta = time.time() + 16 * 60
        with mock.patch("sesame.tokens_v2.time.time", return_value=za_16_minuta):
            odgovor = self.potvrdi(link)
        self.assertContains(odgovor, "Ovaj link više ne vrijedi")
        self.assertFalse(self.prijavljen())

    def test_link_nakon_14_minuta_jos_radi(self):
        self.zatrazi()
        link = link_iz_poruke(mail.outbox[0])
        with mock.patch("sesame.tokens_v2.time.time", return_value=time.time() + 14 * 60):
            self.assertRedirects(self.potvrdi(link), "/vlasnik/")

    def test_izmisljen_ili_prazan_token_ne_prijavljuje(self):
        for token in ("", "izmisljeno", "AAAAAAAAAAAAAAAAAAAAAAAA"):
            with self.subTest(token=token):
                odgovor = self.client.post("/vlasnik/potvrda/", {"sesame": token})
                self.assertContains(odgovor, "Ovaj link više ne vrijedi")
                self.assertFalse(self.prijavljen())

    def test_potvrda_bez_tokena_vraca_na_prijavu(self):
        self.assertRedirects(self.client.get("/vlasnik/potvrda/"), "/vlasnik/prijava/")

    # --- popis i odjava ------------------------------------------------------

    def test_popis_grobova_trazi_prijavu(self):
        odgovor = self.client.get("/vlasnik/")
        self.assertRedirects(odgovor, "/vlasnik/prijava/?next=/vlasnik/")

    def test_odjava_radi_samo_post_zahtjevom(self):
        self.client.force_login(self.korisnik)
        self.assertEqual(self.client.get("/vlasnik/odjava/").status_code, 405)
        self.assertTrue(self.prijavljen())
        self.assertRedirects(self.client.post("/vlasnik/odjava/"), "/vlasnik/prijava/")
        self.assertFalse(self.prijavljen())

    def test_prijavljeni_korisnik_s_prijave_ide_na_popis(self):
        self.client.force_login(self.korisnik)
        self.assertRedirects(self.client.get("/vlasnik/prijava/"), "/vlasnik/")

    def test_prijava_traje_30_dana(self):
        self.zatrazi()
        self.potvrdi(link_iz_poruke(mail.outbox[0]))
        self.assertEqual(self.client.session.get_expiry_age(), 30 * 24 * 3600)
