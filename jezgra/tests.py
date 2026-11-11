"""Testovi zajedničkih dijelova: zaštita od indeksiranja i sigurnosna zaglavlja (P-15)."""

from django.test import TestCase


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
