from django.shortcuts import render


def pocetna(request):
    """Probna početna stranica: provjera da Tailwind i HTMX rade."""
    return render(request, "javno/pocetna.html")


def htmx_proba(request):
    """Vraća mali komad HTML-a koji HTMX umeće u stranicu bez osvježavanja."""
    return render(request, "javno/_htmx_proba.html")
