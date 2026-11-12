"""Sitne pomoćne funkcije za tekst koji upisuju korisnici."""


def jedan_red(tekst: str) -> str:
    """Tekst u jednom retku, bez viška razmaka (npr. naziv groba, koji ide i u naslov e-maila)."""
    return " ".join(tekst.split())
