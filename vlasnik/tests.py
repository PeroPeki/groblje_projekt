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


# --- Vlasnički dio groba (od P-21) ------------------------------------------

from jezgra.models import Grob, Partner, Plocica, Pokojnik, SerijaPlocica  # noqa: E402
from knjiga.models import PorukaSjecanja  # noqa: E402
from pristup.models import ZahtjevZaPristup  # noqa: E402


def napravi_grob(kod, korisnik, naziv="Obitelj Probić", lozinka="stara-lozinka"):
    partner, _ = Partner.objects.get_or_create(naziv="Gradsko groblje Primjerovo")
    serija, _ = SerijaPlocica.objects.get_or_create(
        oznaka="TEST-VL", defaults={"partner": partner, "broj_komada": 5}
    )
    plocica = Plocica.objects.create(
        serija=serija, kod=kod, aktivacijski_kod_hash="!", status=Plocica.Status.AKTIVIRANA
    )
    grob = Grob(
        plocica=plocica,
        partner=partner,
        naziv=naziv,
        oznaka_grobnog_mjesta="Polje X, red 9, br. 99",
        vlasnik_ime="Stjepan Probić",
        kontakt_za_prijavu=korisnik,
    )
    grob.postavi_lozinku(lozinka)
    grob.save()
    return grob


class VlasnickiDioBaza(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = Korisnik.objects.create(username="ana", email="ana@example.com")
        cls.boris = Korisnik.objects.create(username="boris", email="boris@example.com")
        cls.grob = napravi_grob("K7M4QX", cls.ana)
        cls.pokojnik = Pokojnik.objects.create(grob=cls.grob, ime="Marija", prezime="Probić")
        cls.borisov_grob = napravi_grob("AB2CD3", cls.boris, naziv="Obitelj Primjerić")

    def setUp(self):
        self.client.force_login(self.ana)


class DozvoleTest(VlasnickiDioBaza):
    """Nitko ne smije u vlasnički dio tuđeg groba (P-21, P-25).

    Kad dodaš novi URL pod /vlasnik/<KOD>/, dodaj ga i ovdje.
    """

    def vlasnicki_urlovi(self, kod):
        return [
            ("get", f"/vlasnik/{kod}/postavke/", {}),
            ("post", f"/vlasnik/{kod}/postavke/naziv/", {"naziv": "Uljez"}),
            (
                "post",
                f"/vlasnik/{kod}/postavke/lozinka/",
                {"lozinka": "uljez-lozinka", "lozinka2": "uljez-lozinka", "odjavi_uredjaje": "on"},
            ),
            ("post", f"/vlasnik/{kod}/postavke/odjavi-uredjaje/", {}),
            ("post", f"/vlasnik/{kod}/postavke/javni-prikaz/", {"javni_prikaz": "da", "potvrda": "da"}),
        ]

    def test_popis_pokriva_sve_vlasnicke_urlove(self):
        from vlasnik.urls import urlpatterns

        pod_kodom = [u for u in urlpatterns if "kod" in u.pattern.regex.groupindex]
        self.assertEqual(len(pod_kodom), len(self.vlasnicki_urlovi("K7M4QX")))

    def test_drugi_korisnik_na_svakom_urlu_dobiva_404_i_nista_ne_mijenja(self):
        prije = Grob.objects.filter(pk=self.borisov_grob.pk).values().get()
        for metoda, adresa, podaci in self.vlasnicki_urlovi("AB2CD3"):
            with self.subTest(adresa=adresa):
                odgovor = getattr(self.client, metoda)(adresa, podaci)
                self.assertEqual(odgovor.status_code, 404)
        self.assertEqual(Grob.objects.filter(pk=self.borisov_grob.pk).values().get(), prije)

    def test_nepostojeci_grob_izgleda_isto_kao_tudji(self):
        for metoda, adresa, podaci in self.vlasnicki_urlovi("ZZZZZ9"):
            with self.subTest(adresa=adresa):
                self.assertEqual(getattr(self.client, metoda)(adresa, podaci).status_code, 404)

    def test_neprijavljeni_posjetitelj_ide_na_prijavu(self):
        self.client.logout()
        for metoda, adresa, podaci in self.vlasnicki_urlovi("K7M4QX"):
            with self.subTest(adresa=adresa):
                odgovor = getattr(self.client, metoda)(adresa, podaci)
                self.assertEqual(odgovor.status_code, 302)
                self.assertTrue(odgovor["Location"].startswith("/vlasnik/prijava/"))
        self.grob.refresh_from_db()
        self.assertEqual(self.grob.naziv, "Obitelj Probić")

    def test_superuser_smije_u_svaki_grob(self):
        self.client.force_login(
            Korisnik.objects.create(username="admin", email="admin@example.com", is_superuser=True)
        )
        self.assertEqual(self.client.get("/vlasnik/AB2CD3/postavke/").status_code, 200)

    def test_radnje_koje_mijenjaju_podatke_ne_rade_get_zahtjevom(self):
        for metoda, adresa, _ in self.vlasnicki_urlovi("K7M4QX"):
            if metoda == "post":
                with self.subTest(adresa=adresa):
                    self.assertEqual(self.client.get(adresa).status_code, 405)


class PopisGrobovaTest(VlasnickiDioBaza):
    def test_vide_se_samo_vlastiti_grobovi(self):
        odgovor = self.client.get("/vlasnik/")
        self.assertContains(odgovor, "Obitelj Probić")
        self.assertNotContains(odgovor, "Obitelj Primjerić")
        self.assertContains(odgovor, "/vlasnik/K7M4QX/postavke/")

    def test_broj_poruka_i_zahtjeva_na_cekanju(self):
        druga = Pokojnik.objects.create(grob=self.grob, ime="Josip", prezime="Probić")
        for pokojnik in (self.pokojnik, self.pokojnik, druga):
            PorukaSjecanja.objects.create(pokojnik=pokojnik, ime_autora="Susjeda", tekst="Počivala u miru.")
        PorukaSjecanja.objects.create(
            pokojnik=druga, ime_autora="Već odobrena", tekst="x", status=PorukaSjecanja.Status.ODOBRENA
        )
        for i in range(2):
            ZahtjevZaPristup.objects.create(grob=self.grob, ime=f"Rođak {i}", email=f"r{i}@example.com")
        ZahtjevZaPristup.objects.create(
            grob=self.grob, ime="Odbijen", email="o@example.com", status=ZahtjevZaPristup.Status.ODBIJEN
        )

        grob = self.client.get("/vlasnik/").context["grobovi"][0]
        self.assertEqual(grob.poruka_na_cekanju, 3)
        self.assertEqual(grob.zahtjeva_na_cekanju, 2)

    def test_popis_ima_stalan_broj_upita(self):
        for i in range(5):
            napravi_grob(f"GRB{i}22", self.ana, naziv=f"Grob {i}")
        with self.assertNumQueries(3):  # sesija, korisnik, grobovi s brojevima
            self.client.get("/vlasnik/")


class PostavkeGrobaTest(VlasnickiDioBaza):
    def posjetitelj_s_lozinkom(self, lozinka="stara-lozinka"):
        """Drugi uređaj koji je upisao lozinku groba i dobio kolačić pristupa."""
        uredjaj = self.client_class()
        uredjaj.post("/g/K7M4QX/", {"lozinka": lozinka})
        return uredjaj

    def vidi_profil(self, uredjaj) -> bool:
        return "Marija Probić" in uredjaj.get("/g/K7M4QX/", follow=True).content.decode()

    def promijeni_lozinku(self, **podaci):
        zadano = {"lozinka": "nova-lozinka", "lozinka2": "nova-lozinka"}
        return self.client.post("/vlasnik/K7M4QX/postavke/lozinka/", {**zadano, **podaci})

    def test_stranica_postavki(self):
        odgovor = self.client.get("/vlasnik/K7M4QX/postavke/")
        self.assertContains(odgovor, "Obitelj Probić")
        # Vlasnik vidi podatke iz evidencije, ali za njih nema polja za izmjenu.
        self.assertContains(odgovor, "Stjepan Probić")
        self.assertContains(odgovor, "Polje X, red 9, br. 99")
        self.assertNotContains(odgovor, 'name="vlasnik_ime"')
        self.assertNotContains(odgovor, 'name="oznaka_grobnog_mjesta"')
        self.assertNotContains(odgovor, self.grob.lozinka_hash)

    def test_promjena_naziva(self):
        odgovor = self.client.post("/vlasnik/K7M4QX/postavke/naziv/", {"naziv": "Obitelj Probić-Horvat"})
        self.assertRedirects(odgovor, "/vlasnik/K7M4QX/postavke/")
        self.grob.refresh_from_db()
        self.assertEqual(self.grob.naziv, "Obitelj Probić-Horvat")

    def test_vlasnik_ne_moze_post_om_promijeniti_podatke_iz_evidencije(self):
        self.client.post(
            "/vlasnik/K7M4QX/postavke/naziv/",
            {"naziv": "Novi naziv", "vlasnik_ime": "Uljez", "oznaka_grobnog_mjesta": "Drugo", "javni_prikaz": "on"},
        )
        self.grob.refresh_from_db()
        self.assertEqual(self.grob.vlasnik_ime, "Stjepan Probić")
        self.assertEqual(self.grob.oznaka_grobnog_mjesta, "Polje X, red 9, br. 99")
        self.assertFalse(self.grob.javni_prikaz)

    def test_prazan_naziv_se_odbija(self):
        odgovor = self.client.post("/vlasnik/K7M4QX/postavke/naziv/", {"naziv": ""})
        self.assertEqual(odgovor.status_code, 400)
        self.grob.refresh_from_db()
        self.assertEqual(self.grob.naziv, "Obitelj Probić")

    def test_promjena_lozinke_s_kvacicom_odjavljuje_uredjaje(self):
        uredjaj = self.posjetitelj_s_lozinkom()
        self.assertTrue(self.vidi_profil(uredjaj))

        self.assertRedirects(self.promijeni_lozinku(odjavi_uredjaje="on"), "/vlasnik/K7M4QX/postavke/")
        self.assertFalse(self.vidi_profil(uredjaj))
        # Stara lozinka više ne radi, nova radi.
        self.assertFalse(self.vidi_profil(self.posjetitelj_s_lozinkom("stara-lozinka")))
        self.assertTrue(self.vidi_profil(self.posjetitelj_s_lozinkom("nova-lozinka")))

    def test_promjena_lozinke_bez_kvacice_ostavlja_uredjaje_prijavljene(self):
        uredjaj = self.posjetitelj_s_lozinkom()
        self.promijeni_lozinku()
        self.assertTrue(self.vidi_profil(uredjaj))
        self.assertFalse(self.vidi_profil(self.posjetitelj_s_lozinkom("stara-lozinka")))

    def test_neispravna_nova_lozinka_se_odbija(self):
        for podaci, poruka in (
            ({"lozinka": "12345", "lozinka2": "12345"}, "najmanje 6 znakova"),
            ({"lozinka2": "drukcija-lozinka"}, "Lozinke nisu jednake."),
        ):
            with self.subTest(podaci=podaci):
                odgovor = self.promijeni_lozinku(**podaci, odjavi_uredjaje="on")
                self.assertContains(odgovor, poruka, status_code=400)
        self.grob.refresh_from_db()
        self.assertTrue(self.grob.provjeri_lozinku("stara-lozinka"))
        self.assertEqual(self.grob.verzija_pristupa, 1)

    def test_gumb_odjavi_sve_uredjaje(self):
        uredjaj = self.posjetitelj_s_lozinkom()
        self.client.post("/vlasnik/K7M4QX/postavke/odjavi-uredjaje/")
        self.assertFalse(self.vidi_profil(uredjaj))
        # Lozinka je ostala ista, pa se uređaj može ponovno prijaviti.
        self.assertTrue(self.vidi_profil(self.posjetitelj_s_lozinkom()))

    # --- javni prikaz --------------------------------------------------------

    def javni_prikaz(self, htmx=False, **podaci):
        zaglavlja = {"HTTP_HX_REQUEST": "true"} if htmx else {}
        return self.client.post("/vlasnik/K7M4QX/postavke/javni-prikaz/", podaci, **zaglavlja)

    def test_ukljucivanje_javnog_prikaza_trazi_potvrdu(self):
        self.javni_prikaz(javni_prikaz="da")
        self.grob.refresh_from_db()
        self.assertFalse(self.grob.javni_prikaz)

        self.javni_prikaz(javni_prikaz="da", potvrda="da")
        self.grob.refresh_from_db()
        self.assertTrue(self.grob.javni_prikaz)
        self.assertTrue(self.vidi_profil(self.client_class()))  # bez lozinke

    def test_iskljucivanje_javnog_prikaza_ne_trazi_potvrdu(self):
        Grob.objects.filter(pk=self.grob.pk).update(javni_prikaz=True)
        self.javni_prikaz(javni_prikaz="ne")
        self.grob.refresh_from_db()
        self.assertFalse(self.grob.javni_prikaz)
        self.assertFalse(self.vidi_profil(self.client_class()))

    def test_htmx_zahtjev_vraca_samo_dio_stranice(self):
        odgovor = self.javni_prikaz(htmx=True, javni_prikaz="da", potvrda="da")
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, "vlasnik/_javni_prikaz.html")
        self.assertTemplateNotUsed(odgovor, "base.html")
        self.assertContains(odgovor, 'id="javni-prikaz"')
        self.assertContains(odgovor, "Isključi javni prikaz")

    def test_htmx_bez_potvrde_vraca_gresku_u_istom_dijelu(self):
        odgovor = self.javni_prikaz(htmx=True, javni_prikaz="da")
        self.assertContains(odgovor, "označite da razumijete")
        self.assertContains(odgovor, "Uključi javni prikaz")

    def test_obican_zahtjev_bez_htmx_a_preusmjerava(self):
        self.assertRedirects(self.javni_prikaz(javni_prikaz="da", potvrda="da"), "/vlasnik/K7M4QX/postavke/")
