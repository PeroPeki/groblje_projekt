"""Probni grobovi za razvoj predložaka (P-14). Pravi demo dolazi u P-40."""

from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from jezgra.models import Grob, Partner, Plocica, Pokojnik, SerijaPlocica, Srodnik
from jezgra.qr import link_za_kod
from korisnici.models import Korisnik

OZNAKA_SERIJE = "PROBA-01"
KOD_OBITELJSKOG = "PRB234"  # dva pokojnika: stranica groba prikazuje popis
KOD_JEDNOG = "PRB345"  # jedan pokojnik: odmah se otvara profil
LOZINKA = "demo123"
EMAIL = "proba@example.com"

BIOGRAFIJA = (
    "Marija je rođena u malom mjestu uz more. Cijeli radni vijek provela je kao "
    "učiteljica u osnovnoj školi.\n\n"
    "Voljela je vrt, knjige i nedjeljne ručkove s obitelji. Ovo je izmišljena "
    "osoba i služi samo za isprobavanje stranice."
)


class Command(BaseCommand):
    help = (
        "Stvara dva izmišljena probna groba (lozinka demo123) za razvoj predložaka. "
        "Ponovno pokretanje ne stvara duplikate."
    )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Probni grob ima javno poznatu lozinku, pa se stvara samo uz DEBUG=True.")

        if Plocica.objects.filter(kod__in=[KOD_OBITELJSKOG, KOD_JEDNOG]).exists():
            self.stdout.write("Probni grobovi već postoje, ništa nije promijenjeno.")
        else:
            self.stvori()
            self.stdout.write(self.style.SUCCESS("Probni grobovi su stvoreni."))

        self.stdout.write(f"\nLozinka oba groba: {LOZINKA}")
        self.stdout.write(f"Grob s dva pokojnika:  /g/{KOD_OBITELJSKOG}/")
        self.stdout.write(f"Grob s jednim pokojnikom: /g/{KOD_JEDNOG}/")
        self.stdout.write(f"Link kao u QR kodu: {link_za_kod(KOD_OBITELJSKOG)}")
        self.stdout.write(f"Kontakt za prijavu (od P-17): {EMAIL}")

    @transaction.atomic
    def stvori(self):
        partner, _ = Partner.objects.get_or_create(naziv="Probni partner (razvoj)")
        serija, _ = SerijaPlocica.objects.get_or_create(
            oznaka=OZNAKA_SERIJE, defaults={"partner": partner, "broj_komada": 2}
        )
        korisnik, _ = Korisnik.objects.get_or_create(email=EMAIL, defaults={"username": EMAIL})

        obiteljski = self.stvori_grob(serija, korisnik, KOD_OBITELJSKOG, "Obitelj Probić")
        marija = Pokojnik.objects.create(
            grob=obiteljski,
            ime="Marija",
            prezime="Probić",
            datum_rodjenja=date(1934, 3, 12),
            datum_smrti=date(2019, 11, 5),
            biografija=BIOGRAFIJA,
            redoslijed=1,
        )
        # Namjerno bez biografije i bez datuma rođenja: stanja koja dizajn mora pokriti.
        josip = Pokojnik.objects.create(
            grob=obiteljski, ime="Josip", prezime="Probić", datum_smrti=date(2008, 6, 21), redoslijed=2
        )

        jedan = self.stvori_grob(serija, korisnik, KOD_JEDNOG, "Obitelj Primjerić")
        ivan = Pokojnik.objects.create(
            grob=jedan,
            ime="Ivan",
            prezime="Primjerić",
            datum_rodjenja=date(1930, 1, 2),
            datum_smrti=date(2015, 8, 30),
            biografija="Ivan je bio ribar. Ovo je izmišljena osoba.",
        )

        V = Srodnik.VrstaSrodstva
        Srodnik.objects.bulk_create(
            [
                Srodnik(pokojnik=marija, vrsta_srodstva=V.SUPRUG, povezani_pokojnik=josip, redoslijed=1),
                # srodnik u drugom grobu
                Srodnik(pokojnik=marija, vrsta_srodstva=V.BRAT, povezani_pokojnik=ivan, redoslijed=2),
                # živuća osoba s pristankom: prikazuje se samo ime
                Srodnik(
                    pokojnik=marija,
                    vrsta_srodstva=V.UNUKA,
                    ime_i_prezime="Ana Probić",
                    pristanak_na_prikaz=True,
                    redoslijed=3,
                ),
                # živuća osoba BEZ pristanka: ne smije se pojaviti na profilu
                Srodnik(
                    pokojnik=marija,
                    vrsta_srodstva=V.SIN,
                    ime_i_prezime="Marko Probić",
                    pristanak_na_prikaz=False,
                    redoslijed=4,
                ),
                Srodnik(pokojnik=josip, vrsta_srodstva=V.SUPRUGA, povezani_pokojnik=marija),
                Srodnik(pokojnik=ivan, vrsta_srodstva=V.SESTRA, povezani_pokojnik=marija),
            ]
        )

    def stvori_grob(self, serija, korisnik, kod, naziv):
        plocica = Plocica.objects.create(
            serija=serija,
            kod=kod,
            aktivacijski_kod_hash="!",  # već aktivirana, aktivacijski kod ne postoji
            status=Plocica.Status.AKTIVIRANA,
            aktivirana_u=timezone.now(),
        )
        grob = Grob(
            plocica=plocica,
            partner=serija.partner,
            naziv=naziv,
            oznaka_grobnog_mjesta="Polje P, red 1, br. 1",
            vlasnik_ime="Probni Vlasnik",
            kontakt_za_prijavu=korisnik,
        )
        grob.postavi_lozinku(LOZINKA)
        grob.save()
        return grob
