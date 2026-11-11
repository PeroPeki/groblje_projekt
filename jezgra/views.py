from django.http import HttpResponse
from django.shortcuts import render


def pocetna(request):
    """Probna početna stranica: provjera da Tailwind i HTMX rade."""
    return render(request, "javno/pocetna.html")


def htmx_proba(request):
    """Vraća mali komad HTML-a koji HTMX umeće u stranicu bez osvježavanja."""
    return render(request, "javno/_htmx_proba.html")


ROBOTS_TXT = """User-agent: *
Disallow: /g/
Disallow: /vlasnik/
Disallow: /aktivacija/
Disallow: /partner/
Disallow: /admin/
"""


def robots_txt(request):
    """Tražilicama kaže koje dijelove ne smiju pregledavati (odluka 5)."""
    return HttpResponse(ROBOTS_TXT, content_type="text/plain; charset=utf-8")
