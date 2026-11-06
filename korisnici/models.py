from django.contrib.auth.models import AbstractUser
from django.db import models


class Korisnik(AbstractUser):
    """Korisnik aplikacije: vlasnik groba, administrator ili (kasnije) partner.

    Vlastiti model korisnika radi se na početku projekta jer ga je kasnije
    vrlo teško uvesti.
    """

    email = models.EmailField("e-mail", unique=True)
    partner = models.ForeignKey(
        "jezgra.Partner",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="korisnici",
        verbose_name="partner",
        help_text="Samo za korisnike koji gledaju pregled za partnera (P-38).",
    )

    class Meta:
        verbose_name = "korisnik"
        verbose_name_plural = "korisnici"

    def __str__(self):
        return self.email or self.username
