"""Testovi čarobnjaka za aktivaciju pločice (P-18 do P-20)."""

import threading
import time
from datetime import date, timedelta
from unittest import mock

from django.core import mail
from django.db import connection
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from aktivacija.forms import normaliziraj_aktivacijski_kod
from aktivacija.servis import VecAktivirana, aktiviraj_plocicu
from jezgra.models import Grob, Partner, Plocica, Pokojnik, SerijaPlocica
from korisnici.models import Korisnik
from pristup.models import NeuspjeliPokusaj

AKT_KOD = "ABCD2345"
PODACI_GROBA = {
    "naziv": "Obitelj Probić",
    "oznaka_grobnog_mjesta": "Polje X, red 9, br. 99",
    "vlasnik_ime": "Stjepan Probić",
    "email": "unuka@example.com",
    "lozinka": "obitelj-probic",
    "lozinka2": "obitelj-probic",
}


def napravi_seriju(oznaka="TEST-AKT", naziv_partnera="Gradsko groblje Primjerovo"):
    partner = Partner.objects.create(naziv=naziv_partnera)
    return SerijaPlocica.objects.create(partner=partner, oznaka=oznaka, broj_komada=3)


def napravi_plocicu(serija, kod, aktivacijski_kod=AKT_KOD):
    plocica = Plocica(serija=serija, kod=kod)
    plocica.postavi_aktivacijski_kod(aktivacijski_kod)
    plocica.save()
    return plocica


class NormalizacijaTest(TestCase):
    def test_velika_slova_bez_razmaka_i_crtica(self):
        for unos in ("abcd2345", " ABCD 2345 ", "abcd-2345", "a b-c d 2 3 4 5", "ABCD–2345"):
            with self.subTest(unos=unos):
                self.assertEqual(normaliziraj_aktivacijski_kod(unos), "ABCD2345")


class Korak1Test(TestCase):
    """Unos aktivacijskog koda (P-18)."""

    @classmethod
    def setUpTestData(cls):
        serija = napravi_seriju()
        cls.plocica = napravi_plocicu(serija, "K7M4QX")
        cls.druga = napravi_plocicu(serija, "AB2CD3", aktivacijski_kod="WXYZ6789")
        cls.aktivirana = napravi_plocicu(serija, "AKT234", aktivacijski_kod="MNPQ2345")
        korisnik = Korisnik.objects.create(username="vlasnik", email="vlasnik@example.com")
        aktiviraj_plocicu(
            cls.aktivirana.pk,
            naziv="Već aktiviran",
            oznaka_grobnog_mjesta="A1",
            vlasnik_ime="Netko",
            email=korisnik.email,
            lozinka="lozinka-groba",
        )

    def upisi(self, aktivacijski_kod, kod="K7M4QX", ip="203.0.113.5"):
        return self.client.post(
            f"/aktivacija/{kod}/", {"aktivacijski_kod": aktivacijski_kod}, REMOTE_ADDR=ip
        )

    def test_ekran_neaktivirane_plocice_ima_formu_i_korak_1_od_4(self):
        odgovor = self.client.get("/g/K7M4QX/")
        self.assertContains(odgovor, 'name="aktivacijski_kod"')
        self.assertContains(odgovor, 'action="/aktivacija/K7M4QX/"')
        self.assertContains(odgovor, "Korak 1 od 4")
        self.assertContains(odgovor, 'autocomplete="off"')

    def test_tocan_kod_vodi_na_korak_2(self):
        self.assertRedirects(self.upisi(AKT_KOD), "/aktivacija/K7M4QX/grob/")
        self.assertContains(self.client.get("/aktivacija/K7M4QX/grob/"), "Korak 2 od 4")

    def test_kod_se_moze_upisati_malim_slovima_s_razmacima_i_crticama(self):
        self.assertRedirects(self.upisi(" abcd-23 45 "), "/aktivacija/K7M4QX/grob/")

    def test_pogresan_kod_kod_druge_plocice_i_aktivirana_plocica_daju_istu_poruku(self):
        pogresan = self.upisi("ZZZZ9999")
        tudji = self.upisi("WXYZ6789")  # točan kod, ali za drugu pločicu
        aktivirana = self.upisi("MNPQ2345", kod="AKT234")  # točan kod već aktivirane pločice
        nepostojeca = self.upisi(AKT_KOD, kod="ZZZZZ9")
        for odgovor in (pogresan, tudji, aktivirana, nepostojeca):
            self.assertEqual(odgovor.status_code, 200)
            self.assertTemplateUsed(odgovor, "aktivacija/unos_koda.html")
            self.assertContains(odgovor, "Aktivacijski kod nije točan.")
            self.assertNotContains(odgovor, "Primjerovo")
            self.assertNotContains(odgovor, "TEST-AKT")
        self.assertEqual(NeuspjeliPokusaj.objects.filter(vrsta="aktivacija").count(), 4)

    def test_upisani_kod_se_ne_vraca_u_html(self):
        self.assertNotContains(self.upisi("ZZZZ9999"), "ZZZZ9999")

    def test_sesti_pogresan_pokusaj_s_iste_adrese_je_blokiran(self):
        for _ in range(5):
            self.upisi("ZZZZ9999")
        odgovor = self.upisi(AKT_KOD)  # čak i točan kod
        self.assertEqual(odgovor.status_code, 429)
        self.assertTemplateUsed(odgovor, "greske/zakljucano.html")
        self.assertContains(odgovor, "60 min", status_code=429)
        self.assertNotIn("aktivacija_plocica", self.client.session)

    def test_blokada_po_adresi_prestaje_nakon_sat_vremena(self):
        for _ in range(5):
            self.upisi("ZZZZ9999")
        NeuspjeliPokusaj.objects.update(vrijeme=timezone.now() - timedelta(minutes=61))
        self.assertRedirects(self.upisi(AKT_KOD), "/aktivacija/K7M4QX/grob/")

    def test_deset_pogresnih_s_raznih_adresa_blokira_plocicu_na_dan(self):
        for i in range(10):
            self.upisi("ZZZZ9999", ip=f"198.51.100.{i}")
        odgovor = self.upisi(AKT_KOD, ip="192.0.2.77")
        self.assertEqual(odgovor.status_code, 429)
        self.assertContains(odgovor, "24 h", status_code=429)
        # Druga pločica nije blokirana.
        self.assertRedirects(
            self.upisi("WXYZ6789", kod="AB2CD3", ip="192.0.2.77"), "/aktivacija/AB2CD3/grob/"
        )

    def test_izravan_ulaz_na_korak_2_vraca_na_korak_1(self):
        self.assertRedirects(self.client.get("/aktivacija/K7M4QX/grob/"), "/g/K7M4QX/")
        self.assertRedirects(self.client.post("/aktivacija/K7M4QX/grob/", PODACI_GROBA), "/g/K7M4QX/")
        self.assertFalse(Grob.objects.filter(plocica=self.plocica).exists())

    def test_tocan_kod_jedne_plocice_ne_otvara_korak_2_druge(self):
        self.upisi(AKT_KOD)
        self.assertRedirects(self.client.get("/aktivacija/AB2CD3/grob/"), "/g/AB2CD3/")

    def test_stanje_carobnjaka_vrijedi_60_minuta(self):
        self.upisi(AKT_KOD)
        with mock.patch("aktivacija.views.time.time", return_value=time.time() + 61 * 60):
            self.assertRedirects(self.client.get("/aktivacija/K7M4QX/grob/"), "/g/K7M4QX/")

    def test_get_na_adresu_forme_vraca_na_grob(self):
        self.assertRedirects(self.client.get("/aktivacija/K7M4QX/"), "/g/K7M4QX/")


class Korak2Test(TestCase):
    """Podaci groba, lozinka i kontakt za prijavu (P-19)."""

    @classmethod
    def setUpTestData(cls):
        cls.serija = napravi_seriju()
        cls.plocica = napravi_plocicu(cls.serija, "K7M4QX")

    def setUp(self):
        self.client.post("/aktivacija/K7M4QX/", {"aktivacijski_kod": AKT_KOD})

    def aktiviraj(self, **izmjene):
        return self.client.post("/aktivacija/K7M4QX/grob/", {**PODACI_GROBA, **izmjene})

    def test_aktivacija_stvara_grob_s_partnerom_iz_serije(self):
        odgovor = self.aktiviraj()
        self.assertRedirects(odgovor, "/aktivacija/K7M4QX/pokojnik/")

        self.plocica.refresh_from_db()
        self.assertEqual(self.plocica.status, Plocica.Status.AKTIVIRANA)
        self.assertIsNotNone(self.plocica.aktivirana_u)

        grob = Grob.objects.get(plocica=self.plocica)
        self.assertEqual(grob.partner, self.serija.partner)
        self.assertEqual(grob.naziv, "Obitelj Probić")
        self.assertEqual(grob.oznaka_grobnog_mjesta, "Polje X, red 9, br. 99")
        self.assertEqual(grob.vlasnik_ime, "Stjepan Probić")
        self.assertEqual(grob.kontakt_za_prijavu.email, "unuka@example.com")
        self.assertFalse(grob.javni_prikaz)  # zadano je privatno (odluka 5)

    def test_lozinka_groba_je_u_bazi_samo_kao_hash(self):
        self.aktiviraj()
        grob = Grob.objects.get()
        self.assertNotIn("obitelj-probic", grob.lozinka_hash)
        self.assertTrue(grob.provjeri_lozinku("obitelj-probic"))

    def test_novi_korisnik_je_odmah_prijavljen_i_ima_pristup_grobu(self):
        self.aktiviraj()
        korisnik = Korisnik.objects.get(email="unuka@example.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), korisnik.pk)
        self.assertEqual(korisnik.username, "unuka@example.com")
        self.assertFalse(korisnik.has_usable_password())

    def test_e_mail_se_normalizira(self):
        self.aktiviraj(email="  Unuka@Example.COM ")
        self.assertTrue(Korisnik.objects.filter(email="unuka@example.com").exists())

    def test_postojecem_korisniku_grob_se_dodaje_ali_ga_se_ne_prijavljuje(self):
        # Inače bi svatko s aktivacijskim kodom upisom tuđe adrese ušao u tuđi račun.
        postojeci = Korisnik.objects.create(username="unuka", email="unuka@example.com")
        odgovor = self.aktiviraj()
        self.assertRedirects(odgovor, "/aktivacija/K7M4QX/pokojnik/")
        self.assertEqual(Grob.objects.get().kontakt_za_prijavu, postojeci)
        self.assertEqual(Korisnik.objects.count(), 1)
        self.assertNotIn("_auth_user_id", self.client.session)
        # Čarobnjak se ipak može dovršiti.
        self.assertEqual(self.client.get("/aktivacija/K7M4QX/pokojnik/").status_code, 200)

    def test_adresa_administratora_ili_iskljucenog_racuna_se_odbija(self):
        Korisnik.objects.create(username="admin", email="admin@example.com", is_staff=True, is_superuser=True)
        Korisnik.objects.create(username="stari", email="stari@example.com", is_active=False)
        for email in ("admin@example.com", "stari@example.com"):
            with self.subTest(email=email):
                odgovor = self.aktiviraj(email=email)
                self.assertContains(odgovor, "Ovu adresu nije moguće koristiti.")
                self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(Grob.objects.count(), 0)
        self.plocica.refresh_from_db()
        self.assertEqual(self.plocica.status, Plocica.Status.NEAKTIVIRANA)

    def test_dodavanje_groba_postojecem_racunu_odjavljuje_njegove_stare_prijave(self):
        # Netko je ranije otvorio račun na tuđu adresu i ostao prijavljen (30 dana).
        zrtva = Korisnik(username="unuka@example.com", email="unuka@example.com")
        zrtva.set_unusable_password()
        zrtva.save()
        napadac = self.client_class()
        napadac.force_login(zrtva)
        self.assertEqual(napadac.get("/vlasnik/").status_code, 200)

        self.aktiviraj()  # prava vlasnica aktivira svoju pločicu istom adresom
        self.assertEqual(napadac.get("/vlasnik/").status_code, 302)  # stara prijava više ne vrijedi

    def test_prijavljeni_vlasnik_ostaje_prijavljen_kad_sebi_doda_drugi_grob(self):
        vlasnica = Korisnik(username="unuka@example.com", email="unuka@example.com")
        vlasnica.set_unusable_password()
        vlasnica.save()
        self.client.force_login(vlasnica)
        self.client.post("/aktivacija/K7M4QX/", {"aktivacijski_kod": AKT_KOD})
        self.aktiviraj()
        self.assertEqual(self.client.get("/vlasnik/").status_code, 200)
        self.assertContains(self.client.get("/aktivacija/K7M4QX/gotovo/"), "Uredi sadržaj")

    def test_zauzeto_korisnicko_ime_ne_rusi_aktivaciju(self):
        Korisnik.objects.create(username="unuka@example.com", email="druga-adresa@example.com")
        odgovor = self.aktiviraj()
        self.assertContains(odgovor, "Ovu adresu nije moguće koristiti.")
        self.assertEqual(Grob.objects.count(), 0)

    def test_naziv_groba_je_jedan_red_teksta(self):
        self.aktiviraj(naziv="Obitelj\r\nProbić   Horvat")
        self.assertEqual(Grob.objects.get().naziv, "Obitelj Probić Horvat")
        self.assertEqual(len(mail.outbox), 1)

    def test_e_mail_dobrodoslice(self):
        self.aktiviraj()
        self.assertEqual(len(mail.outbox), 1)
        poruka = mail.outbox[0]
        self.assertEqual(poruka.to, ["unuka@example.com"])
        self.assertIn("Obitelj Probić", poruka.subject)
        self.assertIn("http://testserver/g/K7M4QX/", poruka.body)
        self.assertIn("http://testserver/vlasnik/prijava/", poruka.body)
        self.assertNotIn("obitelj-probic", poruka.body)  # lozinka groba ne ide e-mailom
        self.assertNotIn(AKT_KOD, poruka.body)

    def test_isti_aktivacijski_kod_vise_ne_radi(self):
        self.aktiviraj()
        self.client.logout()
        odgovor = self.client.post("/aktivacija/K7M4QX/", {"aktivacijski_kod": AKT_KOD})
        self.assertNotEqual(odgovor.status_code, 302)
        self.assertEqual(Grob.objects.count(), 1)

    def test_ponovno_slanje_koraka_2_ne_stvara_drugi_grob(self):
        self.aktiviraj()
        self.assertRedirects(self.aktiviraj(naziv="Drugi pokušaj"), "/g/K7M4QX/")
        self.assertEqual(Grob.objects.get().naziv, "Obitelj Probić")

    def test_neispravni_podaci_ne_aktiviraju_plocicu(self):
        slucajevi = [
            ({"lozinka": "12345", "lozinka2": "12345"}, "najmanje 6 znakova"),
            ({"lozinka2": "nesto-drugo"}, "Lozinke nisu jednake."),
            ({"email": "nije-adresa"}, None),
            ({"naziv": ""}, None),
            ({"oznaka_grobnog_mjesta": ""}, None),
            ({"vlasnik_ime": ""}, None),
        ]
        for izmjene, poruka in slucajevi:
            with self.subTest(izmjene=izmjene):
                odgovor = self.aktiviraj(**izmjene)
                self.assertEqual(odgovor.status_code, 200)
                if poruka:
                    self.assertContains(odgovor, poruka)
        self.assertEqual(Grob.objects.count(), 0)
        self.plocica.refresh_from_db()
        self.assertEqual(self.plocica.status, Plocica.Status.NEAKTIVIRANA)

    def test_forma_ima_tocan_tekst_iz_odluke_19_i_ne_vraca_lozinku(self):
        odgovor = self.aktiviraj(lozinka2="nesto-drugo")
        self.assertContains(odgovor, "E-mail osobe koja će voditi profil")
        self.assertNotContains(odgovor, "obitelj-probic")
        self.assertNotContains(odgovor, "nesto-drugo")

    def test_uredjaj_koji_je_aktivirao_ne_mora_upisivati_lozinku(self):
        Korisnik.objects.create(username="unuka", email="unuka@example.com")  # bez prijave
        self.aktiviraj()
        self.client.post("/aktivacija/K7M4QX/pokojnik/", {"ime": "Ana", "prezime": "Probić"})
        self.assertContains(self.client.get("/g/K7M4QX/", follow=True), "Ana Probić")


class Korak3i4Test(TestCase):
    """Prvi pokojnik, poziv na slike i završni ekran (P-20)."""

    @classmethod
    def setUpTestData(cls):
        cls.serija = napravi_seriju()
        napravi_plocicu(cls.serija, "K7M4QX")

    def setUp(self):
        self.client.post("/aktivacija/K7M4QX/", {"aktivacijski_kod": AKT_KOD})
        self.client.post("/aktivacija/K7M4QX/grob/", PODACI_GROBA)

    def test_cijeli_carobnjak_do_kraja(self):
        odgovor = self.client.get("/aktivacija/K7M4QX/pokojnik/")
        self.assertContains(odgovor, "Korak 3 od 4")
        self.assertContains(odgovor, 'type="date"', count=2)

        odgovor = self.client.post(
            "/aktivacija/K7M4QX/pokojnik/",
            {
                "ime": "Marija",
                "prezime": "Probić",
                "datum_rodjenja": "1934-03-12",
                "datum_smrti": "2019-11-05",
                "biografija": "Voljela je vrt.",
            },
        )
        self.assertRedirects(odgovor, "/aktivacija/K7M4QX/slike/")
        odgovor = self.client.get("/aktivacija/K7M4QX/slike/")
        self.assertContains(odgovor, "Korak 4 od 4")
        self.assertContains(odgovor, "/aktivacija/K7M4QX/gotovo/")

        odgovor = self.client.get("/aktivacija/K7M4QX/gotovo/")
        self.assertContains(odgovor, "unuka@example.com")
        self.assertContains(odgovor, 'href="/g/K7M4QX/"')

        # Pokojnik je vidljiv na stranici groba (jedan pokojnik: odmah profil).
        profil = self.client.get("/g/K7M4QX/", follow=True)
        self.assertContains(profil, "Marija Probić")
        self.assertContains(profil, "12. ožujka 1934. – 5. studenoga 2019.")

    def test_datumi_i_biografija_nisu_obavezni(self):
        odgovor = self.client.post("/aktivacija/K7M4QX/pokojnik/", {"ime": "Josip", "prezime": "Probić"})
        self.assertRedirects(odgovor, "/aktivacija/K7M4QX/slike/")

    def test_neispravni_datumi_se_odbijaju(self):
        sutra = (date.today() + timedelta(days=2)).isoformat()
        slucajevi = [
            ({"datum_rodjenja": "2000-01-01", "datum_smrti": "1990-01-01"}, "prije datuma rođenja"),
            ({"datum_smrti": sutra}, "u budućnosti"),
        ]
        for datumi, poruka in slucajevi:
            with self.subTest(datumi=datumi):
                odgovor = self.client.post(
                    "/aktivacija/K7M4QX/pokojnik/", {"ime": "Ana", "prezime": "Probić", **datumi}
                )
                self.assertContains(odgovor, poruka)
        self.assertEqual(Pokojnik.objects.count(), 0)

    def test_povratak_na_korak_3_ne_stvara_pokojnika_dvaput(self):
        podaci = {"ime": "Marija", "prezime": "Probić"}
        self.client.post("/aktivacija/K7M4QX/pokojnik/", podaci)
        self.assertRedirects(self.client.post("/aktivacija/K7M4QX/pokojnik/", podaci), "/aktivacija/K7M4QX/slike/")
        self.assertEqual(Pokojnik.objects.count(), 1)

    def test_tko_nije_aktivirao_grob_niti_mu_je_kontakt_dobiva_404(self):
        stranac = self.client_class()
        stranac.force_login(Korisnik.objects.create(username="netko", email="netko@example.com"))
        anoniman = self.client_class()
        for klijent in (stranac, anoniman):
            for korak in ("pokojnik", "slike", "gotovo"):
                with self.subTest(korak=korak):
                    self.assertEqual(klijent.get(f"/aktivacija/K7M4QX/{korak}/").status_code, 404)
            odgovor = klijent.post("/aktivacija/K7M4QX/pokojnik/", {"ime": "Uljez", "prezime": "Uljez"})
            self.assertEqual(odgovor.status_code, 404)
        self.assertEqual(Pokojnik.objects.count(), 0)

    def test_gumb_za_uredjivanje_vidi_samo_tko_je_prijavljen_kao_kontakt(self):
        self.assertContains(self.client.get("/aktivacija/K7M4QX/gotovo/"), "Uredi sadržaj")
        self.client.logout()  # oznaka čarobnjaka nestaje s odjavom, pa je vraćamo ručno
        sesija = self.client.session
        sesija["aktivacija_grob"] = {"grob_id": Grob.objects.get().pk, "vrijeme": time.time()}
        sesija.save()
        self.client.force_login(Korisnik.objects.create(username="netko", email="netko@example.com"))
        sesija = self.client.session
        sesija["aktivacija_grob"] = {"grob_id": Grob.objects.get().pk, "vrijeme": time.time()}
        sesija.save()
        self.assertNotContains(self.client.get("/aktivacija/K7M4QX/gotovo/"), "Uredi sadržaj")

    def test_kontakt_za_prijavu_moze_nastaviti_s_drugog_uredjaja(self):
        drugi_uredjaj = self.client_class()
        drugi_uredjaj.force_login(Korisnik.objects.get(email="unuka@example.com"))
        self.assertEqual(drugi_uredjaj.get("/aktivacija/K7M4QX/pokojnik/").status_code, 200)

    def test_koraci_za_nepostojeci_grob_vracaju_404(self):
        self.assertEqual(self.client.get("/aktivacija/ZZZZZ9/pokojnik/").status_code, 404)


@skipUnlessDBFeature("has_select_for_update")
class IstovremenaAktivacijaTest(TransactionTestCase):
    """Dva istovremena zahtjeva za istu pločicu stvaraju samo jedan grob (P-19)."""

    def test_dvije_niti_jedan_grob(self):
        plocica = napravi_plocicu(napravi_seriju(), "K7M4QX")
        start = threading.Barrier(2)
        ishodi = []

        def aktiviraj(broj):
            try:
                start.wait(timeout=10)
                aktiviraj_plocicu(
                    plocica.pk,
                    naziv=f"Grob {broj}",
                    oznaka_grobnog_mjesta="A1",
                    vlasnik_ime="Netko",
                    email=f"osoba{broj}@example.com",
                    lozinka="lozinka-groba",
                )
                ishodi.append("aktivirano")
            except VecAktivirana:
                ishodi.append("vec_aktivirana")
            finally:
                connection.close()  # svaka nit ima svoju vezu s bazom

        niti = [threading.Thread(target=aktiviraj, args=(broj,)) for broj in (1, 2)]
        for nit in niti:
            nit.start()
        for nit in niti:
            nit.join(timeout=30)

        self.assertEqual(sorted(ishodi), ["aktivirano", "vec_aktivirana"])
        self.assertEqual(Grob.objects.count(), 1)
        self.assertEqual(Korisnik.objects.count(), 1)  # gubitnikov korisnik je poništen s transakcijom
