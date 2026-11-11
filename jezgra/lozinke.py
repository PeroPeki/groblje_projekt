"""Pravila za lozinku groba (odluka 5). Koriste ih aktivacija i vlasnički dio."""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

MIN_DULJINA_LOZINKE_GROBA = 6


def provjeri_lozinku_groba(lozinka: str) -> None:
    """Baca ValidationError ako lozinka groba nije dovoljno duga."""
    if len(lozinka) < MIN_DULJINA_LOZINKE_GROBA:
        raise ValidationError(
            _("Lozinka mora imati najmanje %(min)s znakova.") % {"min": MIN_DULJINA_LOZINKE_GROBA},
            code="prekratka_lozinka",
        )
