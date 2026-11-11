"""Testovi javnog pristupa grobu: ruta /g/<kod>/, lozinka, pamćenje uređaja."""

import io
import re
from datetime import date
from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import models
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.utils import timezone

from jezgra.models import Grob, Partner, Plocica, Pokojnik, SerijaPlocica
from korisnici.models import Korisnik
from pristup import kolacici
from pristup.models import NeuspjeliPokusaj, ObiteljskiLink


def napravi_plocicu(serija, kod):
    # Hash se ovdje ne provjerava, pa ne trošimo vrijeme na make_password.
    return Plocica.objects.create(serija=serija, kod=kod, aktivacijski_kod_hash="!")


def napravi_grob(serija, kod, naziv, korisnik, lozinka=None, javni_prikaz=False):
    plocica = napravi_plocicu(serija, kod)
    plocica.status = Plocica.Status.AKTIVIRANA
    plocica.save()
    grob = Grob(
        plocica=plocica,
        partner=serija.partner,
        naziv=naziv,
        oznaka_grobnog_mjesta="Polje X, red 9, br. 99",
        vlasnik_ime="Vlasnik Probni",
        kontakt_za_prijavu=korisnik,
        lozinka_hash="!",
        javni_prikaz=javni_prikaz,
    )
    if lozinka:
        grob.postavi_lozinku(lozinka)
    grob.save()
    return grob


class RutaGrobaTest(TestCase):
    """Adrese i prikaz. Grobovi su ovdje javni, da lozinka ne smeta (pristup: PristupTest)."""

    @classmethod
    def setUpTestData(cls):
        partner = Partner.objects.create(naziv="Partner Tajni Naziv")
        cls.serija = SerijaPlocica.objects.create(
            partner=partner, oznaka="TEST-TAJNA", broj_komada=4, maloprodajna_cijena=Decimal("119.00")
        )
        korisnik = Korisnik.objects.create(username="vlasnik", email="vlasnik@example.com")

        cls.grob_dva = napravi_grob(
            cls.serija, "K7M4QX", "Obitelj Probić", korisnik, javni_prikaz=True
        )
        cls.ana = Pokojnik.objects.create(
            grob=cls.grob_dva, ime="Ana", prezime="Probić", datum_smrti=date(2020, 11, 5)
        )
        cls.ivo = Pokojnik.objects.create(grob=cls.grob_dva, ime="Ivo", prezime="Probić")

        cls.grob_jedan = napravi_grob(
            cls.serija, "AB2CD3", "Obitelj Primjerić", korisnik, javni_prikaz=True
        )
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


class PristupTest(TestCase):
    """Zaključani ekran, lozinka groba i pamćenje uređaja (odluka 5, P-12)."""

    LOZINKA = "tajna-lozinka"

    @classmethod
    def setUpTestData(cls):
        partner = Partner.objects.create(naziv="Gradsko groblje Primjerovo")
        serija = SerijaPlocica.objects.create(partner=partner, oznaka="TEST-P12", broj_komada=2)
        cls.vlasnik = Korisnik.objects.create(username="vlasnik", email="vlasnik@example.com")
        cls.grob = napravi_grob(serija, "K7M4QX", "Obitelj Probić", cls.vlasnik, lozinka=cls.LOZINKA)
        cls.ana = Pokojnik.objects.create(
            grob=cls.grob, ime="Ana", prezime="Probić", biografija="Voljela je more."
        )
        cls.ivo = Pokojnik.objects.create(grob=cls.grob, ime="Ivo", prezime="Probić")
        cls.adresa_groba = "/g/K7M4QX/"
        cls.adresa_profila = f"/g/K7M4QX/{cls.ana.pk}/"

    def upisi_lozinku(self, lozinka, adresa=None):
        return self.client.post(adresa or self.adresa_profila, {"lozinka": lozinka})

    # --- bez pristupa --------------------------------------------------------

    def test_bez_kolacica_vidi_se_zakljucani_ekran_bez_podataka_o_pokojnicima(self):
        for adresa in (self.adresa_groba, self.adresa_profila):
            with self.subTest(adresa=adresa):
                odgovor = self.client.get(adresa)
                self.assertEqual(odgovor.status_code, 200)
                self.assertTemplateUsed(odgovor, "javno/zakljucano.html")
                self.assertContains(odgovor, "Obitelj Probić")
                self.assertContains(odgovor, "Gradsko groblje Primjerovo")
                for tajno in ("Ana", "Ivo", "Voljela je more", "Polje X", "Vlasnik Probni"):
                    self.assertNotContains(odgovor, tajno)

    def test_zakljucani_ekran_ne_otkriva_koji_pokojnici_postoje(self):
        postojeci = self.client.get(self.adresa_profila)
        nepostojeci = self.client.get("/g/K7M4QX/999999/")
        self.assertEqual(postojeci.status_code, nepostojeci.status_code)
        self.assertTemplateUsed(nepostojeci, "javno/zakljucano.html")

    def test_pogresna_lozinka_ne_daje_pristup(self):
        odgovor = self.upisi_lozinku("kriva-lozinka")
        self.assertEqual(odgovor.status_code, 200)
        self.assertContains(odgovor, "Lozinka nije točna.")
        self.assertNotIn(kolacici.naziv(self.grob), odgovor.cookies)
        self.assertTemplateUsed(self.client.get(self.adresa_profila), "javno/zakljucano.html")

    def test_prazna_lozinka_ne_daje_pristup(self):
        odgovor = self.upisi_lozinku("")
        self.assertTemplateUsed(odgovor, "javno/zakljucano.html")
        self.assertNotIn(kolacici.naziv(self.grob), odgovor.cookies)

    # --- točna lozinka i pamćenje uređaja ------------------------------------

    def test_tocna_lozinka_postavlja_kolacic_i_otvara_profil(self):
        odgovor = self.upisi_lozinku(self.LOZINKA)
        self.assertRedirects(odgovor, self.adresa_profila)  # Post/Redirect/Get
        self.assertContains(self.client.get(self.adresa_profila), "Ana Probić")
        # Isti kolačić vrijedi za cijeli grob.
        self.assertContains(self.client.get(self.adresa_groba), "Ivo Probić")

    def test_kolacic_je_httponly_samesite_lax_secure_i_traje_godinu_dana(self):
        kolacic = self.upisi_lozinku(self.LOZINKA).cookies[kolacici.naziv(self.grob)]
        self.assertTrue(kolacic["httponly"])
        self.assertEqual(kolacic["samesite"], "Lax")
        self.assertTrue(kolacic["secure"])  # testovi rade s DEBUG=False, kao produkcija
        self.assertEqual(kolacic["max-age"], 365 * 24 * 3600)

    @override_settings(DEBUG=True)
    def test_lokalno_bez_https_a_kolacic_nije_secure(self):
        kolacic = self.upisi_lozinku(self.LOZINKA).cookies[kolacici.naziv(self.grob)]
        self.assertFalse(kolacic["secure"])

    def test_kolacic_ne_sadrzi_lozinku(self):
        kolacic = self.upisi_lozinku(self.LOZINKA).cookies[kolacici.naziv(self.grob)]
        self.assertNotIn(self.LOZINKA, kolacic.value)

    def test_izmijenjen_kolacic_ne_daje_pristup(self):
        self.upisi_lozinku(self.LOZINKA)
        naziv = kolacici.naziv(self.grob)
        izvorni = self.client.cookies[naziv].value
        for lazni in (
            izvorni[:-2] + ("xx" if not izvorni.endswith("xx") else "yy"),  # pokvaren potpis
            f"{self.grob.pk}:{self.grob.verzija_pristupa}:-",  # bez potpisa
            izvorni.replace(f"{self.grob.pk}:1:", f"{self.grob.pk}:2:", 1),  # druga verzija
            "",
        ):
            with self.subTest(lazni=lazni):
                self.client.cookies[naziv] = lazni
                odgovor = self.client.get(self.adresa_profila)
                self.assertTemplateUsed(odgovor, "javno/zakljucano.html")

    def test_povecana_verzija_pristupa_odjavljuje_uredjaj(self):
        self.upisi_lozinku(self.LOZINKA)
        Grob.objects.filter(pk=self.grob.pk).update(verzija_pristupa=2)
        self.assertTemplateUsed(self.client.get(self.adresa_profila), "javno/zakljucano.html")

    def test_kolacic_jednog_groba_ne_otvara_drugi_grob(self):
        drugi = napravi_grob(
            self.grob.plocica.serija, "AB2CD3", "Obitelj Primjerić", self.vlasnik, lozinka="druga-lozinka"
        )
        Pokojnik.objects.create(grob=drugi, ime="Mara", prezime="Primjerić")
        self.upisi_lozinku(self.LOZINKA)
        # Čak i ako posjetitelj svoj valjani kolačić podmetne pod imenom drugog groba.
        self.client.cookies[kolacici.naziv(drugi)] = self.client.cookies[kolacici.naziv(self.grob)].value
        self.assertTemplateUsed(self.client.get("/g/AB2CD3/"), "javno/zakljucano.html")

    def test_pristup_preko_obiteljskog_linka_prestaje_kad_se_link_ponisti(self):
        link = ObiteljskiLink.objects.create(grob=self.grob)
        odgovor = HttpResponse()
        kolacici.dodijeli_pristup(odgovor, self.grob, link=link)
        naziv = kolacici.naziv(self.grob)
        self.client.cookies[naziv] = odgovor.cookies[naziv].value
        self.assertContains(self.client.get(self.adresa_profila), "Ana Probić")

        ObiteljskiLink.objects.filter(pk=link.pk).update(aktivan=False)
        self.assertTemplateUsed(self.client.get(self.adresa_profila), "javno/zakljucano.html")

    # --- pristup bez lozinke -------------------------------------------------

    def test_javni_prikaz_otvara_grob_bez_lozinke(self):
        Grob.objects.filter(pk=self.grob.pk).update(javni_prikaz=True)
        self.assertContains(self.client.get(self.adresa_profila), "Ana Probić")

    def test_kontakt_za_prijavu_i_superuser_ne_trebaju_lozinku(self):
        admin = Korisnik.objects.create(username="admin", email="admin@example.com", is_superuser=True)
        for korisnik in (self.vlasnik, admin):
            with self.subTest(korisnik=korisnik):
                self.client.force_login(korisnik)
                self.assertContains(self.client.get(self.adresa_profila), "Ana Probić")

    def test_drugi_prijavljeni_korisnik_treba_lozinku(self):
        self.client.force_login(Korisnik.objects.create(username="netko", email="netko@example.com"))
        self.assertTemplateUsed(self.client.get(self.adresa_profila), "javno/zakljucano.html")

    # --- lozinka groba -------------------------------------------------------

    def test_lozinka_kraca_od_6_znakova_ne_moze_se_postaviti(self):
        for losa in ("12345", "      ", "  12345  ", "x" * 129):
            with self.subTest(losa=losa), self.assertRaises(ValidationError):
                self.grob.postavi_lozinku(losa)
        self.grob.postavi_lozinku("123456")

    def test_razmaci_oko_lozinke_ne_smetaju(self):
        self.grob.postavi_lozinku("more i sol ")
        self.grob.save()
        self.assertRedirects(self.upisi_lozinku(" more i sol"), self.adresa_profila)

    def test_kolacic_se_salje_samo_na_adrese_tog_groba(self):
        kolacic = self.upisi_lozinku(self.LOZINKA).cookies[kolacici.naziv(self.grob)]
        self.assertEqual(kolacic["path"], "/g/K7M4QX/")

    def test_lozinka_je_u_bazi_samo_kao_hash(self):
        self.grob.refresh_from_db()
        self.assertNotIn(self.LOZINKA, self.grob.lozinka_hash)
        self.assertTrue(self.grob.provjeri_lozinku(self.LOZINKA))


class ZakljucavanjeTest(TestCase):
    """Blokada nakon više pogrešnih lozinki (odluka 5, P-13)."""

    LOZINKA = "tajna-lozinka"

    @classmethod
    def setUpTestData(cls):
        partner = Partner.objects.create(naziv="Gradsko groblje Primjerovo")
        serija = SerijaPlocica.objects.create(partner=partner, oznaka="TEST-P13", broj_komada=2)
        vlasnik = Korisnik.objects.create(username="vlasnik", email="vlasnik@example.com")
        cls.grob = napravi_grob(serija, "K7M4QX", "Obitelj Probić", vlasnik, lozinka=cls.LOZINKA)
        Pokojnik.objects.create(grob=cls.grob, ime="Ana", prezime="Probić")
        Pokojnik.objects.create(grob=cls.grob, ime="Ivo", prezime="Probić")
        cls.drugi_grob = napravi_grob(serija, "AB2CD3", "Obitelj Primjerić", vlasnik, lozinka=cls.LOZINKA)

    def upisi(self, lozinka, ip="203.0.113.5", adresa="/g/K7M4QX/", **zaglavlja):
        return self.client.post(adresa, {"lozinka": lozinka}, REMOTE_ADDR=ip, **zaglavlja)

    def pogrijesi(self, puta, **kwargs):
        for _ in range(puta):
            odgovor = self.upisi("kriva-lozinka", **kwargs)
        return odgovor

    def pomakni_pokusaje_u_proslost(self, minuta):
        NeuspjeliPokusaj.objects.update(vrijeme=timezone.now() - timedelta(minutes=minuta))

    def assertZakljucano(self, odgovor):
        self.assertEqual(odgovor.status_code, 429)
        self.assertTemplateUsed(odgovor, "greske/zakljucano.html")

    def test_peti_pogresan_pokusaj_jos_prikazuje_obicnu_poruku(self):
        odgovor = self.pogrijesi(5)
        self.assertContains(odgovor, "Lozinka nije točna.")

    def test_sesti_pokusaj_je_blokiran_cak_i_s_tocnom_lozinkom(self):
        self.pogrijesi(5)
        odgovor = self.upisi(self.LOZINKA)
        self.assertZakljucano(odgovor)
        self.assertContains(odgovor, "15 minuta", status_code=429)
        self.assertNotIn(kolacici.naziv(self.grob), odgovor.cookies)

    def test_poruka_o_blokadi_ne_otkriva_nista_o_grobu(self):
        self.pogrijesi(5)
        odgovor = self.upisi("kriva-lozinka")
        for tajno in ("Probić", "Primjerovo", "Ana"):
            self.assertNotContains(odgovor, tajno, status_code=429)

    def test_blokirani_pokusaji_se_ne_biljeze_pa_blokada_ne_traje_vjecno(self):
        self.pogrijesi(9)
        self.assertEqual(NeuspjeliPokusaj.objects.count(), 5)

    def test_nakon_15_minuta_prijava_opet_radi(self):
        self.pogrijesi(5)
        self.pomakni_pokusaje_u_proslost(minuta=16)
        self.assertRedirects(self.upisi(self.LOZINKA), "/g/K7M4QX/", fetch_redirect_response=False)

    def test_blokada_vrijedi_samo_za_tu_ip_adresu_i_taj_grob(self):
        self.pogrijesi(5)
        druga_adresa = self.upisi(self.LOZINKA, ip="198.51.100.7")
        self.assertRedirects(druga_adresa, "/g/K7M4QX/", fetch_redirect_response=False)
        drugi_grob = self.upisi(self.LOZINKA, adresa="/g/AB2CD3/")
        self.assertRedirects(drugi_grob, "/g/AB2CD3/", fetch_redirect_response=False)

    def test_uspjesna_prijava_ne_brise_neuspjehe_drugih_adresa(self):
        self.pogrijesi(5)
        self.upisi(self.LOZINKA, ip="198.51.100.7")
        self.client.cookies.clear()  # prva adresa je drugi uređaj, bez kolačića pristupa
        self.assertEqual(NeuspjeliPokusaj.objects.count(), 5)
        self.assertZakljucano(self.upisi(self.LOZINKA))

    def test_30_pokusaja_s_raznih_adresa_blokira_grob_na_sat_vremena(self):
        for i in range(30):
            self.upisi("kriva-lozinka", ip=f"198.51.100.{i}")
        odgovor = self.upisi(self.LOZINKA, ip="192.0.2.99")
        self.assertZakljucano(odgovor)
        self.assertContains(odgovor, "60 minuta", status_code=429)

        self.pomakni_pokusaje_u_proslost(minuta=61)
        odgovor = self.upisi(self.LOZINKA, ip="192.0.2.99")
        self.assertRedirects(odgovor, "/g/K7M4QX/", fetch_redirect_response=False)

    def test_prazna_lozinka_se_ne_broji_kao_pokusaj(self):
        for _ in range(6):
            self.upisi("")
        self.assertEqual(NeuspjeliPokusaj.objects.count(), 0)

    # --- IP adresa -----------------------------------------------------------

    def test_lokalno_se_x_forwarded_for_ne_gleda(self):
        # Napadač mijenja zaglavlje pri svakom pokušaju, ali ga lokalno ne gledamo.
        for i in range(5):
            self.upisi("kriva-lozinka", HTTP_X_FORWARDED_FOR=f"198.51.100.{i}")
        self.assertZakljucano(self.upisi(self.LOZINKA, HTTP_X_FORWARDED_FOR="198.51.100.200"))

    @override_settings(IZA_PROXYJA=True)
    def test_iza_proxyja_se_broji_adresa_koju_je_dopisao_proxy(self):
        # Svi zahtjevi dolaze s adrese proxyja (REMOTE_ADDR), a posjetitelji su različiti.
        self.pogrijesi(5, ip="10.0.0.1", HTTP_X_FORWARDED_FOR="203.0.113.5")
        isti = self.upisi(self.LOZINKA, ip="10.0.0.1", HTTP_X_FORWARDED_FOR="203.0.113.5")
        self.assertZakljucano(isti)
        drugi = self.upisi(self.LOZINKA, ip="10.0.0.1", HTTP_X_FORWARDED_FOR="198.51.100.7")
        self.assertRedirects(drugi, "/g/K7M4QX/", fetch_redirect_response=False)

    @override_settings(IZA_PROXYJA=True)
    def test_lazni_pocetak_zaglavlja_ne_zaobilazi_ogranicenje(self):
        # Napadač sam šalje X-Forwarded-For; proxy njegovu pravu adresu dopisuje na kraj.
        for i in range(5):
            self.upisi("kriva-lozinka", ip="10.0.0.1", HTTP_X_FORWARDED_FOR=f"1.2.3.{i}, 203.0.113.5")
        odgovor = self.upisi(self.LOZINKA, ip="10.0.0.1", HTTP_X_FORWARDED_FOR="1.2.3.99, 203.0.113.5")
        self.assertZakljucano(odgovor)

    @override_settings(IZA_PROXYJA=True, PROXY_BROJ_POSREDNIKA=2)
    def test_dva_posrednika_uzimaju_predzadnju_adresu(self):
        self.upisi("kriva-lozinka", ip="10.0.0.1", HTTP_X_FORWARDED_FOR="1.2.3.4, 203.0.113.5, 10.0.0.9")
        self.assertEqual(NeuspjeliPokusaj.objects.get().ip, "203.0.113.5")

    @override_settings(IZA_PROXYJA=True)
    def test_neispravno_zaglavlje_ne_rusi_stranicu(self):
        odgovor = self.upisi("kriva-lozinka", HTTP_X_FORWARDED_FOR="<script>, nije-adresa")
        self.assertEqual(odgovor.status_code, 200)
        self.assertEqual(NeuspjeliPokusaj.objects.get().ip, "203.0.113.5")

    def test_ipv6_se_broji_po_bloku_a_ipv4_u_ipv6_zapisu_kao_ipv4(self):
        self.upisi("kriva-lozinka", ip="2001:db8:1:2:aaaa:bbbb:cccc:dddd")
        self.upisi("kriva-lozinka", ip="::ffff:203.0.113.5")
        self.assertEqual(
            sorted(NeuspjeliPokusaj.objects.values_list("ip", flat=True)),
            ["2001:db8:1:2::", "203.0.113.5"],
        )

    def test_blokada_traje_15_minuta_od_zadnjeg_pogresnog_pokusaja(self):
        # Četiri stara neuspjeha i peti maloprije: blokada tek počinje.
        self.pogrijesi(4)
        self.pomakni_pokusaje_u_proslost(minuta=14)
        self.pogrijesi(1)
        self.assertContains(self.upisi(self.LOZINKA), "15 minuta", status_code=429)

        # Deset minuta kasnije i dalje je blokirano, a poruka kaže koliko je ostalo.
        NeuspjeliPokusaj.objects.update(vrijeme=models.F("vrijeme") - timedelta(minutes=10))
        self.assertContains(self.upisi(self.LOZINKA), "5 minuta", status_code=429)

    # --- čišćenje ------------------------------------------------------------

    def test_ocisti_pokusaje_brise_samo_starije_od_24_sata(self):
        self.pogrijesi(2)
        stari = NeuspjeliPokusaj.objects.first()
        NeuspjeliPokusaj.objects.filter(pk=stari.pk).update(
            vrijeme=timezone.now() - timedelta(hours=25)
        )
        izlaz = io.StringIO()
        call_command("ocisti_pokusaje", stdout=izlaz)
        self.assertIn("Obrisano neuspjelih pokušaja: 1", izlaz.getvalue())
        self.assertEqual(NeuspjeliPokusaj.objects.count(), 1)
