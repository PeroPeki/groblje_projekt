"""Slike i videi pokojnika. Ograničenja veličine su u settings.py (MEDIJI_*)."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Medij(models.Model):
    class Vrsta(models.TextChoices):
        SLIKA = "slika", _("slika")
        VIDEO = "video", _("video")

    class Status(models.TextChoices):
        CEKA_UPLOAD = "ceka_upload", _("čeka upload")
        U_OBRADI = "u_obradi", _("u obradi")
        GOTOV = "gotov", _("gotov")
        GRESKA = "greska", _("greška")

    pokojnik = models.ForeignKey(
        "jezgra.Pokojnik",
        on_delete=models.CASCADE,
        related_name="mediji",
        verbose_name=_("pokojnik"),
    )
    vrsta = models.CharField(_("vrsta"), max_length=10, choices=Vrsta.choices)
    status = models.CharField(
        _("status"), max_length=20, choices=Status.choices, default=Status.CEKA_UPLOAD
    )
    kljuc_izvornika = models.CharField(
        _("ključ izvornika"), max_length=300, blank=True, help_text=_("Putanja izvorne datoteke u spremniku.")
    )
    datoteka = models.FileField(_("obrađena datoteka"), upload_to="mediji/", blank=True)
    slicica = models.FileField(_("sličica"), upload_to="mediji/slicice/", blank=True)
    velicina_bajtova = models.PositiveBigIntegerField(_("veličina (bajtovi)"), default=0)
    trajanje_sekundi = models.PositiveIntegerField(_("trajanje (s)"), null=True, blank=True)
    sirina = models.PositiveIntegerField(_("širina"), null=True, blank=True)
    visina = models.PositiveIntegerField(_("visina"), null=True, blank=True)
    opis = models.CharField(
        _("opis"), max_length=500, blank=True, help_text=_("Koristi se i kao alternativni tekst.")
    )
    redoslijed = models.PositiveIntegerField(_("redoslijed"), default=0)
    skriven = models.BooleanField(_("skriven"), default=False, help_text=_("Za moderaciju."))
    poruka_greske = models.TextField(_("poruka greške"), blank=True)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)

    class Meta:
        verbose_name = _("medij")
        verbose_name_plural = _("mediji")
        ordering = ["redoslijed", "id"]

    def __str__(self):
        return f"{self.get_vrsta_display()} #{self.pk} ({self.pokojnik})"
