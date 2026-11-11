"""Glavni modeli: partner, serija pločica, pločica, grob, pokojnik i srodnik.

Nazivi prate rječnik pojmova iz docs/odluke.md.
"""

from decimal import Decimal

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .lozinke import provjeri_lozinku_groba


# ---------------------------------------------------------------------------
# P-06: partner, serija pločica, pločica
# ---------------------------------------------------------------------------


class Partner(models.Model):
    """Pogrebno poduzeće ili uprava groblja koja prodaje pločice (odluke 8 i 15)."""

    naziv = models.CharField(_("naziv"), max_length=200)
    kontakt_ime = models.CharField(_("kontakt osoba"), max_length=200, blank=True)
    kontakt_email = models.EmailField(_("kontakt e-mail"), blank=True)
    kontakt_telefon = models.CharField(_("kontakt telefon"), max_length=50, blank=True)
    postotak_provizije = models.DecimalField(
        _("postotak provizije"), max_digits=5, decimal_places=2, default=Decimal("25.00")
    )
    aktivan = models.BooleanField(_("aktivan"), default=True)
    napomena = models.TextField(_("napomena"), blank=True)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)

    class Meta:
        verbose_name = _("partner")
        verbose_name_plural = _("partneri")
        ordering = ["naziv"]

    def __str__(self):
        return self.naziv


class SerijaPlocica(models.Model):
    """Skupina pločica izrađenih odjednom za jednog partnera."""

    partner = models.ForeignKey(
        Partner, on_delete=models.PROTECT, related_name="serije", verbose_name=_("partner")
    )
    oznaka = models.CharField(_("oznaka"), max_length=50, unique=True, help_text=_("npr. DEMO-01"))
    broj_komada = models.PositiveIntegerField(_("broj komada"))
    maloprodajna_cijena = models.DecimalField(
        _("maloprodajna cijena (€)"), max_digits=7, decimal_places=2, default=Decimal("119.00")
    )
    napomena = models.TextField(_("napomena"), blank=True)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)

    class Meta:
        verbose_name = _("serija pločica")
        verbose_name_plural = _("serije pločica")
        ordering = ["-stvoreno"]

    def __str__(self):
        return f"{self.oznaka} ({self.partner})"


class Plocica(models.Model):
    """Fizička pločica s QR oznakom koja se postavlja na grob."""

    class Status(models.TextChoices):
        NEAKTIVIRANA = "neaktivirana", _("neaktivirana")
        AKTIVIRANA = "aktivirana", _("aktivirana")

    serija = models.ForeignKey(
        SerijaPlocica, on_delete=models.PROTECT, related_name="plocice", verbose_name=_("serija")
    )
    kod = models.CharField(_("kod"), max_length=6, unique=True)
    aktivacijski_kod_hash = models.CharField(_("hash aktivacijskog koda"), max_length=128)
    status = models.CharField(
        _("status"), max_length=20, choices=Status.choices, default=Status.NEAKTIVIRANA
    )
    aktivirana_u = models.DateTimeField(_("aktivirana u"), null=True, blank=True)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)

    class Meta:
        verbose_name = _("pločica")
        verbose_name_plural = _("pločice")
        ordering = ["-stvoreno"]

    def __str__(self):
        return self.kod

    def postavi_aktivacijski_kod(self, aktivacijski_kod: str) -> None:
        """Sprema samo hash: čitljiv aktivacijski kod nikad ne ide u bazu."""
        self.aktivacijski_kod_hash = make_password(aktivacijski_kod.upper())

    def provjeri_aktivacijski_kod(self, aktivacijski_kod: str) -> bool:
        return check_password(aktivacijski_kod.strip().upper(), self.aktivacijski_kod_hash)


# ---------------------------------------------------------------------------
# P-07: grob, pokojnik, srodnik
# ---------------------------------------------------------------------------


class Grob(models.Model):
    """Grob s jednom pločicom i jednim ili više pokojnika (odluka 4)."""

    plocica = models.OneToOneField(
        Plocica, on_delete=models.PROTECT, related_name="grob", verbose_name=_("pločica")
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.PROTECT,
        related_name="grobovi",
        verbose_name=_("partner"),
        help_text=_("Pri aktivaciji se kopira iz serije pločice (odluka 15)."),
    )
    naziv = models.CharField(
        _("naziv"), max_length=200, help_text=_("npr. Obitelj Horvat; vidi se na zaključanom ekranu")
    )
    oznaka_grobnog_mjesta = models.CharField(
        _("oznaka grobnog mjesta"),
        max_length=200,
        blank=True,
        help_text=_("npr. Polje C, red 4, br. 12. Nikad se ne prikazuje posjetiteljima."),
    )
    vlasnik_ime = models.CharField(
        _("vlasnik"), max_length=200, help_text=_("Osoba iz evidencije uprave groblja.")
    )
    kontakt_za_prijavu = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="grobovi",
        verbose_name=_("kontakt za prijavu"),
    )
    lozinka_hash = models.CharField(_("hash lozinke groba"), max_length=128)
    verzija_pristupa = models.PositiveIntegerField(
        _("verzija pristupa"),
        default=1,
        help_text=_("Povećava se pri promjeni lozinke, pa zapamćeni uređaji gube pristup (P-12)."),
    )
    javni_prikaz = models.BooleanField(_("javni prikaz"), default=False)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)
    promijenjeno = models.DateTimeField(_("promijenjeno"), auto_now=True)

    class Meta:
        verbose_name = _("grob")
        verbose_name_plural = _("grobovi")
        ordering = ["naziv"]

    def __str__(self):
        return f"{self.naziv} ({self.plocica.kod})"

    def postavi_lozinku(self, lozinka: str) -> None:
        """Sprema samo hash. Prekratka lozinka baca ValidationError (odluka 5)."""
        provjeri_lozinku_groba(lozinka)
        self.lozinka_hash = make_password(lozinka)

    def provjeri_lozinku(self, lozinka: str) -> bool:
        return check_password(lozinka, self.lozinka_hash)


class Pokojnik(models.Model):
    grob = models.ForeignKey(
        Grob, on_delete=models.CASCADE, related_name="pokojnici", verbose_name=_("grob")
    )
    ime = models.CharField(_("ime"), max_length=100)
    prezime = models.CharField(_("prezime"), max_length=100)
    datum_rodjenja = models.DateField(_("datum rođenja"), null=True, blank=True)
    datum_smrti = models.DateField(_("datum smrti"), null=True, blank=True)
    biografija = models.TextField(_("biografija"), blank=True)
    profilna_slika = models.ForeignKey(
        "mediji.Medij",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("profilna slika"),
    )
    redoslijed = models.PositiveIntegerField(_("redoslijed"), default=0)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)

    class Meta:
        verbose_name = _("pokojnik")
        verbose_name_plural = _("pokojnici")
        ordering = ["redoslijed", "id"]

    def __str__(self):
        return f"{self.ime} {self.prezime}"


class Srodnik(models.Model):
    """Član obitelji prikazan na profilu pokojnika (odluka 3a).

    Srodnik je ili drugi pokojnik (povezani_pokojnik) ili živuća osoba
    (samo ime_i_prezime). Za živuće osobe namjerno nema datuma rođenja,
    kontakta ni slike (GDPR).
    """

    class VrstaSrodstva(models.TextChoices):
        SUPRUG = "suprug", _("suprug")
        SUPRUGA = "supruga", _("supruga")
        OTAC = "otac", _("otac")
        MAJKA = "majka", _("majka")
        SIN = "sin", _("sin")
        KCI = "kci", _("kći")
        BRAT = "brat", _("brat")
        SESTRA = "sestra", _("sestra")
        DJED = "djed", _("djed")
        BAKA = "baka", _("baka")
        UNUK = "unuk", _("unuk")
        UNUKA = "unuka", _("unuka")
        OSTALO = "ostalo", _("ostalo")

    pokojnik = models.ForeignKey(
        Pokojnik, on_delete=models.CASCADE, related_name="srodnici", verbose_name=_("pokojnik")
    )
    vrsta_srodstva = models.CharField(
        _("vrsta srodstva"), max_length=20, choices=VrstaSrodstva.choices
    )
    povezani_pokojnik = models.ForeignKey(
        Pokojnik,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="kao_srodnik",
        verbose_name=_("povezani pokojnik"),
    )
    ime_i_prezime = models.CharField(
        _("ime i prezime"), max_length=200, blank=True, help_text=_("Samo za živuće osobe.")
    )
    pristanak_na_prikaz = models.BooleanField(
        _("osoba je pristala da se njezino ime prikaže"), default=False
    )
    redoslijed = models.PositiveIntegerField(_("redoslijed"), default=0)

    class Meta:
        verbose_name = _("srodnik")
        verbose_name_plural = _("srodnici")
        ordering = ["redoslijed", "id"]
        constraints = [
            # Točno jedno od dvoje: ili povezani pokojnik ili ime živuće osobe.
            models.CheckConstraint(
                condition=(
                    Q(povezani_pokojnik__isnull=False, ime_i_prezime="")
                    | (Q(povezani_pokojnik__isnull=True) & ~Q(ime_i_prezime=""))
                ),
                name="srodnik_pokojnik_ili_ime",
            ),
        ]

    def __str__(self):
        osoba = self.povezani_pokojnik or self.ime_i_prezime
        return f"{self.get_vrsta_srodstva_display()}: {osoba}"
