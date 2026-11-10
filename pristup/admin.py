from django.contrib import admin

from .models import NeuspjeliPokusaj, ObiteljskiLink, ZahtjevZaPristup


@admin.register(ObiteljskiLink)
class ObiteljskiLinkAdmin(admin.ModelAdmin):
    list_display = ("grob", "aktivan", "stvoreno", "ponisteno_u")
    list_filter = ("aktivan",)
    search_fields = ("grob__naziv", "grob__plocica__kod")
    # token je tajan kao lozinka: ne prikazujemo ga
    exclude = ("token",)
    readonly_fields = ("grob", "stvoreno", "ponisteno_u")


@admin.register(NeuspjeliPokusaj)
class NeuspjeliPokusajAdmin(admin.ModelAdmin):
    list_display = ("vrsta", "cilj", "ip", "vrijeme")
    list_filter = ("vrsta",)
    search_fields = ("cilj", "ip")
    readonly_fields = ("vrsta", "cilj", "ip", "vrijeme")

    def has_add_permission(self, request):
        return False


@admin.register(ZahtjevZaPristup)
class ZahtjevZaPristupAdmin(admin.ModelAdmin):
    list_display = ("ime", "email", "grob", "status", "stvoreno")
    list_filter = ("status",)
    search_fields = ("ime", "email", "grob__naziv")
    raw_id_fields = ("grob",)
