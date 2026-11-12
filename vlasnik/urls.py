from django.urls import path, re_path

from pristup.urls import KOD

from . import views

app_name = "vlasnik"

urlpatterns = [
    path("", views.popis, name="popis"),
    path("prijava/", views.prijava, name="prijava"),
    path("prijava/poslano/", views.prijava_poslano, name="prijava_poslano"),
    path("potvrda/", views.potvrda, name="potvrda"),
    path("odjava/", views.odjava, name="odjava"),
    # Sve ispod /vlasnik/<KOD>/ prolazi kroz dekorator vlasnik_groba (tuđi grob = 404).
    # Svaki novi URL dodaj i na popis u testu dozvola (vlasnik/tests.py).
    re_path(rf"^{KOD}/postavke/$", views.postavke, name="postavke"),
    re_path(rf"^{KOD}/postavke/naziv/$", views.postavke_naziv, name="postavke_naziv"),
    re_path(rf"^{KOD}/postavke/lozinka/$", views.postavke_lozinka, name="postavke_lozinka"),
    re_path(rf"^{KOD}/postavke/odjavi-uredjaje/$", views.odjavi_uredjaje, name="odjavi_uredjaje"),
    re_path(rf"^{KOD}/postavke/javni-prikaz/$", views.javni_prikaz, name="javni_prikaz"),
]
