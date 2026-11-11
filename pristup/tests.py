"""Testovi javnog pristupa grobu: ruta /g/<kod>/, stranica groba i profil."""

import re
from datetime import date
from decimal import Decimal

from django.test import TestCase

from jezgra.models import Grob, Partner, Plocica, Pokojnik, SerijaPlocica
from korisnici.models import Korisnik


def napravi_plocicu(serija, kod):
    # Hash se ovdje ne provjerava, pa ne trošimo vrijeme na make_password.
    return Plocica.objects.create(serija=serija, kod=kod, aktivacijski_kod_hash="!")


def napravi_grob(serija, kod, naziv, korisnik):
    plocica = napravi_plocicu(serija, kod)
    plocica.status = Plocica.Status.AKTIVIRANA
    plocica.save()
    return Grob.objects.create(
        plocica=plocica,
        partner=serija.partner,
        naziv=naziv,
        oznaka_grobnog_mjesta="Polje X, red 9, br. 99",
        vlasnik_ime="Vlasnik Probni",
        kontakt_za_prijavu=korisnik,
        lozinka_hash="!",
    )


class RutaGrobaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        partner = Partner.objects.create(naziv="Partner Tajni Naziv")
        cls.serija = SerijaPlocica.objects.create(
            partner=partner, oznaka="TEST-TAJNA", broj_komada=4, maloprodajna_cijena=Decimal("119.00")
        )
        korisnik = Korisnik.objects.create(username="vlasnik", email="vlasnik@example.com")

        cls.grob_dva = napravi_grob(cls.serija, "K7M4QX", "Obitelj Probić", korisnik)
        cls.ana = Pokojnik.objects.create(
            grob=cls.grob_dva, ime="Ana", prezime="Probić", datum_smrti=date(2020, 11, 5)
        )
        cls.ivo = Pokojnik.objects.create(grob=cls.grob_dva, ime="Ivo", prezime="Probić")

        cls.grob_jedan = napravi_grob(cls.serija, "AB2CD3", "Obitelj Primjerić", korisnik)
        cls.mara = Pokojnik.objects.create(grob=cls.grob_jedan, ime="Mara", prezime="Primjerić")

        napravi_plocicu(cls.serija, "NEAKT2")

    # --- kanonska adresa -----------------------------------------------------

    def test_razliciti_zapisi_vode_na_kanonsku_adresu(self):
        for adresa in ("/g/k7m4qx/", "/G/K7M4QX", "/G/K7M4QX/", "/g/K7M4QX", "/G/k7m4Qx"):
            with self.subTest(adresa=adresa):
                odgovor = self.client.get(adresa)
                self.assertRedirects(odgovor, "/g/K7M4QX/", fetch_redirect_response=False)

    def test_kanonska_adresa_se_ne_preusmjerava(self):
        self.assertEqual(self.client.get("/g/K7M4QX/").status_code, 200)

    def test_link_iz_qr_koda_otvara_grob(self):
        # QR sadrži link velikim slovima i bez kose crte na kraju (odluka 18).
        odgovor = self.client.get("/G/K7M4QX", follow=True)
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, "javno/grob.html")

    def test_profil_se_takodjer_preusmjerava_na_kanonsku_adresu(self):
        odgovor = self.client.get(f"/G/k7m4qx/{self.ana.pk}")
        self.assertRedirects(odgovor, f"/g/K7M4QX/{self.ana.pk}/", fetch_redirect_response=False)

    # --- stranica groba ------------------------------------------------------

    def test_grob_s_dva_pokojnika_prikazuje_popis(self):
        odgovor = self.client.get("/g/K7M4QX/")
        self.assertTemplateUsed(odgovor, "javno/grob.html")
        self.assertContains(odgovor, "Ana Probić")
        self.assertContains(odgovor, "Ivo Probić")
        self.assertContains(odgovor, f"/g/K7M4QX/{self.ana.pk}/")

    def test_grob_s_jednim_pokojnikom_odmah_otvara_profil(self):
        odgovor = self.client.get("/g/AB2CD3/")
        self.assertRedirects(odgovor, f"/g/AB2CD3/{self.mara.pk}/")

    def test_oznaka_grobnog_mjesta_se_ne_prikazuje(self):
        for adresa in ("/g/K7M4QX/", f"/g/K7M4QX/{self.ana.pk}/"):
            with self.subTest(adresa=adresa):
                self.assertNotContains(self.client.get(adresa), "Polje X")

    # --- neaktivirana i nepostojeća pločica (odluka 8) -----------------------

    def test_nepostojeci_i_neaktivirani_kod_daju_isti_odgovor(self):
        neaktivirana = self.client.get("/g/NEAKT2/")
        nepostojeca = self.client.get("/g/ZZZZZ9/")

        for odgovor in (neaktivirana, nepostojeca):
            self.assertEqual(odgovor.status_code, 200)
            self.assertTemplateUsed(odgovor, "aktivacija/unos_koda.html")

        # Razlikovati se smiju samo upisani kod i CSRF token (svaki put je drugačiji).
        def ocisti(odgovor, kod):
            html = odgovor.content.decode().replace(kod, "KOD")
            return re.sub(r'"X-CSRFToken": "[^"]+"', "", html)

        self.assertEqual(ocisti(neaktivirana, "NEAKT2"), ocisti(nepostojeca, "ZZZZZ9"))
        self.assertEqual(dict(neaktivirana.headers), dict(nepostojeca.headers))

    def test_neaktivirana_plocica_ne_otkriva_partnera_ni_seriju(self):
        odgovor = self.client.get("/g/NEAKT2/")
        self.assertNotContains(odgovor, "Partner Tajni Naziv")
        self.assertNotContains(odgovor, "TEST-TAJNA")

    # --- profil --------------------------------------------------------------

    def test_profil_prikazuje_pokojnika(self):
        odgovor = self.client.get(f"/g/K7M4QX/{self.ana.pk}/")
        self.assertTemplateUsed(odgovor, "javno/profil.html")
        self.assertContains(odgovor, "Ana Probić")

    def test_pokojnik_iz_drugog_groba_vraca_404(self):
        odgovor = self.client.get(f"/g/K7M4QX/{self.mara.pk}/")
        self.assertEqual(odgovor.status_code, 404)

    def test_profil_za_nepostojeci_grob_i_nepostojeceg_pokojnika_vraca_404(self):
        self.assertEqual(self.client.get(f"/g/ZZZZZ9/{self.ana.pk}/").status_code, 404)
        self.assertEqual(self.client.get("/g/K7M4QX/999999/").status_code, 404)

    def test_datum_je_u_genitivu_a_nepoznati_datum_je_upitnik(self):
        odgovor = self.client.get(f"/g/K7M4QX/{self.ana.pk}/")
        self.assertContains(odgovor, "? – 5. studenoga 2020.")

    def test_link_na_grob_samo_kad_postoji_popis_pokojnika(self):
        self.assertContains(self.client.get(f"/g/K7M4QX/{self.ana.pk}/"), 'href="/g/K7M4QX/"')
        self.assertNotContains(self.client.get(f"/g/AB2CD3/{self.mara.pk}/"), 'href="/g/AB2CD3/"')

    def test_grob_s_neaktiviranom_plocicom_se_ne_prikazuje(self):
        Plocica.objects.filter(kod="K7M4QX").update(status=Plocica.Status.NEAKTIVIRANA)
        self.assertTemplateUsed(self.client.get("/g/K7M4QX/"), "aktivacija/unos_koda.html")
        self.assertEqual(self.client.get(f"/g/K7M4QX/{self.ana.pk}/").status_code, 404)

    def test_predugacak_ili_neobican_id_pokojnika_vraca_404(self):
        self.assertEqual(self.client.get("/g/K7M4QX/" + "9" * 5000 + "/").status_code, 404)
        self.assertEqual(self.client.get("/g/K7M4QX/٣/").status_code, 404)
