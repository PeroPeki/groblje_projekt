"""Pravila za lozinku groba (odluka 5). Koriste ih aktivacija i vlasnički dio."""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

MIN_DULJINA_LOZINKE_GROBA = 6
MAX_DULJINA_LOZINKE_GROBA = 128


def normaliziraj_lozinku_groba(lozinka: str) -> str:
    """Razmaci na početku i kraju se ne računaju (mobitel ih često sam doda)."""
    return (lozinka or "").strip()


def provjeri_lozinku_groba(lozinka: str) -> None:
    """Baca ValidationError ako lozinka groba nije dopuštene duljine."""
    duljina = len(normaliziraj_lozinku_groba(lozinka))
    if duljina < MIN_DULJINA_LOZINKE_GROBA:
        raise ValidationError(
            _("Lozinka mora imati najmanje %(min)s znakova.") % {"min": MIN_DULJINA_LOZINKE_GROBA},
            code="prekratka_lozinka",
        )
    if duljina > MAX_DULJINA_LOZINKE_GROBA:
        raise ValidationError(
            _("Lozinka smije imati najviše %(max)s znakova.") % {"max": MAX_DULJINA_LOZINKE_GROBA},
            code="preduga_lozinka",
        )
