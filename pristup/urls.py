"""Javne adrese groba: /g/<kod>/ i /g/<kod>/<pokojnik_id>/."""

from django.urls import re_path

from jezgra.kodovi import DULJINA_KODA_PLOCICE

from . import views

app_name = "pristup"

KOD = rf"(?P<kod>[A-Z0-9]{{{DULJINA_KODA_PLOCICE}}})"
KOD_BILO_KAKO = rf"(?P<kod>[A-Za-z0-9]{{{DULJINA_KODA_PLOCICE}}})"
# [0-9], a ne \d: \d hvata i znamenke drugih pisama, a duljina je ograničena.
POKOJNIK = r"(?P<pokojnik_id>[0-9]{1,9})"

urlpatterns = [
    # Kanonske adrese: malo "g", kod VELIKIM slovima, kosa crta na kraju.
    re_path(rf"^g/{KOD}/$", views.grob, name="grob"),
    re_path(rf"^g/{KOD}/{POKOJNIK}/$", views.profil, name="profil"),
    # Svi ostali zapisi (/G/... iz QR koda, mala slova, bez kose crte) preusmjeravaju
    # se na kanonsku adresu. Django uzorci razlikuju velika i mala slova, zato [gG].
    re_path(rf"^[gG]/{KOD_BILO_KAKO}/?$", views.na_kanonsku_adresu),
    re_path(rf"^[gG]/{KOD_BILO_KAKO}/{POKOJNIK}/?$", views.na_kanonsku_adresu),
]
