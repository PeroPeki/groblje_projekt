from django.urls import path

from . import views

app_name = "vlasnik"

urlpatterns = [
    path("", views.popis, name="popis"),
    path("prijava/", views.prijava, name="prijava"),
    path("prijava/poslano/", views.prijava_poslano, name="prijava_poslano"),
    path("potvrda/", views.potvrda, name="potvrda"),
    path("odjava/", views.odjava, name="odjava"),
]
