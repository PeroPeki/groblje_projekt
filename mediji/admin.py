from django.contrib import admin

from .models import Medij


@admin.register(Medij)
class MedijAdmin(admin.ModelAdmin):
    list_display = ("__str__", "vrsta", "status", "skriven", "velicina_bajtova", "stvoreno")
    list_filter = ("vrsta", "status", "skriven")
    search_fields = ("opis", "pokojnik__ime", "pokojnik__prezime", "pokojnik__grob__naziv")
    raw_id_fields = ("pokojnik",)
    readonly_fields = (
        "kljuc_izvornika",
        "velicina_bajtova",
        "trajanje_sekundi",
        "sirina",
        "visina",
        "poruka_greske",
        "stvoreno",
    )
