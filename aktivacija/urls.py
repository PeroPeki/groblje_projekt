from django.urls import re_path

from pristup.urls import KOD

from . import views

app_name = "aktivacija"

urlpatterns = [
    re_path(rf"^{KOD}/$", views.unos_koda, name="unos_koda"),
    re_path(rf"^{KOD}/grob/$", views.korak_grob, name="grob"),
    re_path(rf"^{KOD}/pokojnik/$", views.korak_pokojnik, name="pokojnik"),
    re_path(rf"^{KOD}/slike/$", views.korak_slike, name="slike"),
    re_path(rf"^{KOD}/gotovo/$", views.gotovo, name="gotovo"),
]
