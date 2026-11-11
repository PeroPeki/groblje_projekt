"""Pamćenje uređaja: potpisani kolačić koji dokazuje pristup jednom grobu.

Vrijednost je "<grob_id>:<verzija_pristupa>:<link_id ili ->".
- verzija_pristupa: kad je vlasnik poveća, svi zapamćeni uređaji gube pristup (P-21);
- link_id: tko je ušao obiteljskim linkom, gubi pristup kad se taj link poništi (P-23).
Potpis (SECRET_KEY + SALT) sprječava da posjetitelj sam izmijeni vrijednost.
"""

from django.conf import settings

SALT = "pristup-grobu"
GODINA = 365 * 24 * 3600  # odluka 5: uređaj se pamti oko 12 mjeseci


def naziv(grob) -> str:
    return f"vs_g{grob.pk}"


def dodijeli_pristup(response, grob, link=None) -> None:
    vrijednost = f"{grob.pk}:{grob.verzija_pristupa}:{link.pk if link else '-'}"
    response.set_signed_cookie(
        naziv(grob),
        vrijednost,
        salt=SALT,
        max_age=GODINA,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
    )


def ima_kolacic_pristupa(request, grob) -> bool:
    vrijednost = request.get_signed_cookie(naziv(grob), default=None, salt=SALT, max_age=GODINA)
    if not vrijednost:
        return False
    try:
        grob_id, verzija, link_id = vrijednost.split(":")
        if int(grob_id) != grob.pk or int(verzija) != grob.verzija_pristupa:
            return False
        if link_id == "-":
            return True
        return grob.obiteljski_linkovi.filter(pk=int(link_id), aktivan=True).exists()
    except ValueError:
        return False


def ima_pristup(request, grob) -> bool:
    """Smije li ovaj posjetitelj vidjeti sadržaj groba bez upisa lozinke."""
    if grob.javni_prikaz:
        return True
    korisnik = request.user
    if korisnik.is_authenticated and (
        korisnik.is_superuser or grob.kontakt_za_prijavu_id == korisnik.pk
    ):
        return True
    return ima_kolacic_pristupa(request, grob)
