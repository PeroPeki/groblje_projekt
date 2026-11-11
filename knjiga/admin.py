from django.contrib import admin

from .models import PorukaSjecanja, PrijavaSadrzaja


@admin.register(PorukaSjecanja)
class PorukaSjecanjaAdmin(admin.ModelAdmin):
    list_display = ("ime_autora", "pokojnik", "status", "skrivena", "stvoreno")
    list_filter = ("status", "skrivena")
    search_fields = ("ime_autora", "tekst", "pokojnik__ime", "pokojnik__prezime")
    raw_id_fields = ("pokojnik",)
    readonly_fields = ("stvoreno", "odluceno_u")


@admin.register(PrijavaSadrzaja)
class PrijavaSadrzajaAdmin(admin.ModelAdmin):
    list_display = ("razlog", "pokojnik", "status", "stvoreno", "rok_odgovora")
    list_filter = ("status", "razlog")
    search_fields = ("opis", "email_prijavitelja", "pokojnik__ime", "pokojnik__prezime")
    raw_id_fields = ("pokojnik", "medij", "poruka")
    readonly_fields = ("stvoreno", "rijeseno_u", "rok_odgovora")

    @admin.display(description="rok odgovora")
    def rok_odgovora(self, obj):
        return obj.rok_odgovora
