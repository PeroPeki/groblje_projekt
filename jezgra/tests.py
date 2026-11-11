"""Testovi zajedničkih dijelova: kodovi pločica, QR, noindex i sigurnosna zaglavlja."""

from unittest import mock

from django.contrib.auth.hashers import check_password
from django.test import TestCase, override_settings

from jezgra import kodovi
from jezgra.models import Partner, Plocica, SerijaPlocica
from jezgra.qr import link_za_kod, qr_za_kod


class KodoviTest(TestCase):
    def test_abeceda_nema_dvosmislenih_znakova(self):
        self.assertFalse(set(kodovi.ABECEDA) & set("0O1IL"))
        self.assertEqual(kodovi.ABECEDA, kodovi.ABECEDA.upper())

    def test_kod_plocice_ima_6_znakova_iz_abecede(self):
        for _ in range(1000):
            kod = kodovi.novi_kod(kodovi.DULJINA_KODA_PLOCICE)
            self.assertEqual(len(kod), 6)
            self.assertLessEqual(set(kod), set(kodovi.ABECEDA), kod)

    def test_aktivacijski_kod_ima_8_znakova_iz_abecede(self):
        for _ in range(1000):
            kod = kodovi.novi_aktivacijski_kod()
            self.assertEqual(len(kod), 8)
            self.assertLessEqual(set(kod), set(kodovi.ABECEDA), kod)

    def test_kodovi_se_ne_ponavljaju(self):
        uzorak = {kodovi.novi_kod(6) for _ in range(200)}
        self.assertGreater(len(uzorak), 195)

    def test_novi_kod_plocice_preskace_kod_koji_vec_postoji(self):
        partner = Partner.objects.create(naziv="Probni partner")
        serija = SerijaPlocica.objects.create(partner=partner, oznaka="TEST-KOD2", broj_komada=1)
        Plocica.objects.create(serija=serija, kod="K7M4QX", aktivacijski_kod_hash="!")
        with mock.patch.object(kodovi, "novi_kod", side_effect=["K7M4QX", "AB2CD3"]):
            self.assertEqual(kodovi.novi_kod_plocice(), "AB2CD3")

    def test_aktivacijski_kod_je_u_bazi_samo_kao_hash(self):
        partner = Partner.objects.create(naziv="Probni partner")
        serija = SerijaPlocica.objects.create(partner=partner, oznaka="TEST-KOD", broj_komada=1)
        plocica = Plocica(serija=serija, kod="K7M4QX")
        plocica.postavi_aktivacijski_kod("ABCD2345")
        plocica.save()
        plocica.refresh_from_db()
        self.assertNotIn("ABCD2345", plocica.aktivacijski_kod_hash)
        self.assertTrue(check_password("ABCD2345", plocica.aktivacijski_kod_hash))
        self.assertTrue(plocica.provjeri_aktivacijski_kod(" abcd2345 "))
        self.assertFalse(plocica.provjeri_aktivacijski_kod("ABCD2346"))


class QrTest(TestCase):
    @override_settings(QR_BAZNI_URL="HTTPS://VJECNASPOMEN.HR/G/")
    def test_qr_za_hr_domenu_je_verzija_3_s_korekcijom_h(self):
        self.assertEqual(link_za_kod("k7m4qx"), "HTTPS://VJECNASPOMEN.HR/G/K7M4QX")
        qr = qr_za_kod("K7M4QX")
        self.assertEqual(qr.version, 3)  # 29 × 29 modula (odluka 18)
        self.assertEqual(qr.error, "H")


class NoIndexTest(TestCase):
    def test_svaki_odgovor_ima_x_robots_tag(self):
        # početna, nepostojeća pločica, 404, robots.txt, admin (preusmjeravanje na prijavu)
        for adresa in ("/", "/g/ZZZZZ9/", "/nema-te-stranice/", "/robots.txt", "/admin/"):
            with self.subTest(adresa=adresa):
                odgovor = self.client.get(adresa)
                self.assertEqual(odgovor["X-Robots-Tag"], "noindex, nofollow")

    def test_zaglavlje_imaju_i_odgovori_koje_stvore_medjuslojevi(self):
        odgovor = self.client.get("/htmx-proba")  # CommonMiddleware dodaje kosu crtu (301)
        self.assertEqual(odgovor.status_code, 301)
        self.assertEqual(odgovor["X-Robots-Tag"], "noindex, nofollow")

    def test_stranice_imaju_meta_oznake_za_robote_i_referrer(self):
        for adresa in ("/", "/g/ZZZZZ9/"):
            with self.subTest(adresa=adresa):
                odgovor = self.client.get(adresa)
                self.assertContains(odgovor, '<meta name="robots" content="noindex, nofollow">')
                self.assertContains(odgovor, '<meta name="referrer" content="same-origin">')

    def test_robots_txt(self):
        odgovor = self.client.get("/robots.txt")
        self.assertEqual(odgovor.status_code, 200)
        self.assertTrue(odgovor["Content-Type"].startswith("text/plain"))
        sadrzaj = odgovor.content.decode()
        self.assertEqual(
            sadrzaj,
            "User-agent: *\n"
            "Disallow: /g/\n"
            "Disallow: /vlasnik/\n"
            "Disallow: /aktivacija/\n"
            "Disallow: /partner/\n",
        )

    def test_sigurnosna_zaglavlja(self):
        odgovor = self.client.get("/g/ZZZZZ9/")
        self.assertEqual(odgovor["X-Frame-Options"], "DENY")  # nema ugradnje u <iframe>
        self.assertEqual(odgovor["X-Content-Type-Options"], "nosniff")
        # Token obiteljskog linka u adresi ne odlazi drugim stranicama kroz Referer.
        self.assertEqual(odgovor["Referrer-Policy"], "same-origin")
