"""Glavni URL-ovi projekta: koja adresa vodi na koji pogled."""

from django.contrib import admin
from django.urls import path

from jezgra import views as jezgra

urlpatterns = [
    path("", jezgra.pocetna, name="pocetna"),
    path("htmx-proba/", jezgra.htmx_proba, name="htmx_proba"),
    path("admin/", admin.site.urls),
]
