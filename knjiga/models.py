"""Knjiga sjećanja i prijave sadržaja (odluke 3 i 19)."""

from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

ROK_ODGOVORA_NA_PRIJAVU = timedelta(days=7)  # odluka 19


class PorukaSjecanja(models.Model):
    """Poruka posjetitelja; vidi se tek kad je vlasnik odobri."""

    class Status(models.TextChoices):
        NA_CEKANJU = "na_cekanju", _("na čekanju")
        ODOBRENA = "odobrena", _("odobrena")
        ODBIJENA = "odbijena", _("odbijena")

    pokojnik = models.ForeignKey(
        "jezgra.Pokojnik",
        on_delete=models.CASCADE,
        related_name="poruke",
        verbose_name=_("pokojnik"),
    )
    ime_autora = models.CharField(_("ime autora"), max_length=200)
    tekst = models.TextField(_("tekst"), max_length=2000)
    status = models.CharField(
        _("status"), max_length=20, choices=Status.choices, default=Status.NA_CEKANJU
    )
    skrivena = models.BooleanField(
        _("skrivena"), default=False, help_text=_("Naše uklanjanje nakon prijave.")
    )
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)
    odluceno_u = models.DateTimeField(_("odlučeno u"), null=True, blank=True)

    class Meta:
        verbose_name = _("poruka sjećanja")
        verbose_name_plural = _("poruke sjećanja")
        ordering = ["-stvoreno"]

    def __str__(self):
        return f"{self.ime_autora}: {self.tekst[:40]}"


class PrijavaSadrzaja(models.Model):
    """Prijava neprimjerenog ili netočnog sadržaja (gumb „Prijavi”)."""

    class Razlog(models.TextChoices):
        UVREDLJIV = "uvredljiv", _("uvredljiv sadržaj")
        NETOCAN = "netocan", _("netočan podatak")
        NA_SLICI_SAM = "na_slici_sam", _("na slici sam ja i tražim uklanjanje")
        DRUGO = "drugo", _("drugo")

    class Status(models.TextChoices):
        NOVA = "nova", _("nova")
        U_OBRADI = "u_obradi", _("u obradi")
        RIJESENA = "rijesena", _("riješena")

    pokojnik = models.ForeignKey(
        "jezgra.Pokojnik",
        on_delete=models.CASCADE,
        related_name="prijave",
        verbose_name=_("pokojnik"),
    )
    medij = models.ForeignKey(
        "mediji.Medij",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prijave",
        verbose_name=_("medij"),
    )
    poruka = models.ForeignKey(
        PorukaSjecanja,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prijave",
        verbose_name=_("poruka"),
    )
    razlog = models.CharField(_("razlog"), max_length=20, choices=Razlog.choices)
    opis = models.TextField(_("opis"), max_length=2000, blank=True)
    email_prijavitelja = models.EmailField(_("e-mail prijavitelja"), blank=True)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.NOVA)
    napomena_admina = models.TextField(_("napomena administratora"), blank=True)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)
    rijeseno_u = models.DateTimeField(_("riješeno u"), null=True, blank=True)

    class Meta:
        verbose_name = _("prijava sadržaja")
        verbose_name_plural = _("prijave sadržaja")
        ordering = ["-stvoreno"]

    def __str__(self):
        return f"{self.get_razlog_display()} ({self.pokojnik})"

    @property
    def rok_odgovora(self):
        """Do kada moramo odgovoriti na prijavu (odluka 19)."""
        if self.stvoreno is None:
            return None
        return self.stvoreno + ROK_ODGOVORA_NA_PRIJAVU
