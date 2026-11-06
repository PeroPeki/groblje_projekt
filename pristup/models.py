"""Pristup grobu: obiteljski link, neuspjeli pokušaji i zahtjevi za pristup."""

import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _


def novi_token():
    # 32 bajta slučajnosti (~43 znaka u URL-u)
    return secrets.token_urlsafe(32)


class ObiteljskiLink(models.Model):
    """Link kojim obitelj otvara profil bez upisivanja lozinke."""

    grob = models.ForeignKey(
        "jezgra.Grob",
        on_delete=models.CASCADE,
        related_name="obiteljski_linkovi",
        verbose_name=_("grob"),
    )
    token = models.CharField(_("token"), max_length=64, unique=True, default=novi_token)
    aktivan = models.BooleanField(_("aktivan"), default=True)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)
    ponisteno_u = models.DateTimeField(_("poništeno u"), null=True, blank=True)

    class Meta:
        verbose_name = _("obiteljski link")
        verbose_name_plural = _("obiteljski linkovi")
        ordering = ["-stvoreno"]

    def __str__(self):
        stanje = _("aktivan") if self.aktivan else _("poništen")
        return f"{self.grob.naziv} ({stanje})"


class NeuspjeliPokusaj(models.Model):
    """Pogrešna lozinka ili aktivacijski kod, za zaključavanje (P-13)."""

    class Vrsta(models.TextChoices):
        LOZINKA = "lozinka", _("lozinka groba")
        AKTIVACIJA = "aktivacija", _("aktivacijski kod")

    vrsta = models.CharField(_("vrsta"), max_length=20, choices=Vrsta.choices)
    cilj = models.CharField(_("cilj"), max_length=50, help_text=_("ID groba ili kod pločice"))
    ip = models.GenericIPAddressField(_("IP adresa"))
    vrijeme = models.DateTimeField(_("vrijeme"), auto_now_add=True)

    class Meta:
        verbose_name = _("neuspjeli pokušaj")
        verbose_name_plural = _("neuspjeli pokušaji")
        ordering = ["-vrijeme"]
        indexes = [
            models.Index(fields=["vrsta", "cilj", "vrijeme"], name="pokusaj_cilj_idx"),
            models.Index(fields=["vrsta", "ip", "vrijeme"], name="pokusaj_ip_idx"),
        ]

    def __str__(self):
        return f"{self.get_vrsta_display()} {self.cilj} s {self.ip}"


class ZahtjevZaPristup(models.Model):
    """Posjetitelj bez lozinke traži od vlasnika pristup (OP-1)."""

    class Status(models.TextChoices):
        NOVI = "novi", _("novi")
        ODOBREN = "odobren", _("odobren")
        ODBIJEN = "odbijen", _("odbijen")

    grob = models.ForeignKey(
        "jezgra.Grob",
        on_delete=models.CASCADE,
        related_name="zahtjevi_za_pristup",
        verbose_name=_("grob"),
    )
    ime = models.CharField(_("ime"), max_length=200)
    email = models.EmailField(_("e-mail"))
    poruka = models.TextField(_("poruka"), max_length=1000, blank=True)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.NOVI)
    stvoreno = models.DateTimeField(_("stvoreno"), auto_now_add=True)

    class Meta:
        verbose_name = _("zahtjev za pristup")
        verbose_name_plural = _("zahtjevi za pristup")
        ordering = ["-stvoreno"]

    def __str__(self):
        return f"{self.ime} → {self.grob.naziv}"
