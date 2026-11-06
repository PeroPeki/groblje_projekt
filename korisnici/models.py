from django.contrib.auth.models import AbstractUser
from django.db import models


class Korisnik(AbstractUser):
    """Korisnik aplikacije: vlasnik groba, administrator ili (kasnije) partner.

    Vlastiti model korisnika radi se na početku projekta jer ga je kasnije
    vrlo teško uvesti. Polje `partner` dodaje se u koraku P-06.
    """

    email = models.EmailField("e-mail", unique=True)

    class Meta:
        verbose_name = "korisnik"
        verbose_name_plural = "korisnici"

    def __str__(self):
        return self.email or self.username
