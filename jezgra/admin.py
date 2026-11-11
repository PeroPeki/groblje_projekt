from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from mediji.models import Medij
from pristup.models import ObiteljskiLink

from .forms import NovaSerijaForm
from .kodovi import novi_aktivacijski_kod, novi_kod_plocice
from .models import Grob, Partner, Plocica, Pokojnik, SerijaPlocica, Srodnik
from .qr import zip_s_qr_kodovima

admin.site.site_header = _("Vječna spomen – administracija")
admin.site.site_title = _("Vječna spomen")
admin.site.index_title = _("Administracija")


def zip_odgovor(sadrzaj: bytes, naziv: str) -> HttpResponse:
    odgovor = HttpResponse(sadrzaj, content_type="application/zip")
    odgovor["Content-Disposition"] = f'attachment; filename="{naziv}"'
    return odgovor


# --- Partner, serija, pločica ----------------------------------------------


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("naziv", "kontakt_ime", "kontakt_email", "postotak_provizije", "aktivan")
    list_filter = ("aktivan",)
    search_fields = ("naziv", "kontakt_ime", "kontakt_email")


class PlocicaInline(admin.TabularInline):
    model = Plocica
    fields = ("kod", "status", "aktivirana_u")
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SerijaPlocica)
class SerijaPlocicaAdmin(admin.ModelAdmin):
    list_display = ("oznaka", "partner", "broj_komada", "maloprodajna_cijena", "stvoreno")
    list_filter = ("partner",)
    search_fields = ("oznaka", "partner__naziv")
    inlines = [PlocicaInline]
    actions = ["preuzmi_qr_serije"]

    def get_readonly_fields(self, request, obj=None):
        # Nakon stvaranja broj komada i partner se ne mijenjaju: pločice već postoje.
        return ("partner", "broj_komada") if obj else ()

    def add_view(self, request, form_url="", extra_context=None):
        """Umjesto obične forme: stvori seriju s pločicama i odmah vrati ZIP."""
        if request.method == "POST":
            form = NovaSerijaForm(request.POST)
            if form.is_valid():
                serija, aktivacijski = self._stvori_seriju(form)
                self.log_addition(request, serija, [{"added": {}}])
                return zip_odgovor(
                    zip_s_qr_kodovima(serija.plocice.order_by("kod"), aktivacijski),
                    f"serija-{serija.oznaka}.zip",
                )
        else:
            form = NovaSerijaForm()

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": _("Nova serija pločica"),
            "form": form,
        }
        return render(request, "admin/jezgra/serijaplocica/nova_serija.html", context)

    @staticmethod
    @transaction.atomic
    def _stvori_seriju(form):
        serija = form.save()
        aktivacijski = {}
        for _i in range(serija.broj_komada):
            plocica = Plocica(serija=serija, kod=novi_kod_plocice())
            kod_za_papir = novi_aktivacijski_kod()
            plocica.postavi_aktivacijski_kod(kod_za_papir)
            plocica.save()
            aktivacijski[plocica.kod] = kod_za_papir
        return serija, aktivacijski

    @admin.action(description=_("Preuzmi QR slike (bez aktivacijskih kodova)"))
    def preuzmi_qr_serije(self, request, queryset):
        plocice = Plocica.objects.filter(serija__in=queryset).order_by("kod")
        return zip_odgovor(zip_s_qr_kodovima(plocice), "qr-kodovi.zip")


@admin.register(Plocica)
class PlocicaAdmin(admin.ModelAdmin):
    list_display = ("kod", "serija", "status", "aktivirana_u", "stvoreno")
    list_filter = ("status", "serija__partner", "serija")
    search_fields = ("kod", "serija__oznaka")
    readonly_fields = ("serija", "kod", "aktivacijski_kod_hash", "aktivirana_u", "stvoreno")
    actions = ["preuzmi_qr"]

    def has_add_permission(self, request):
        # Pločice nastaju samo kroz „Nova serija”, da svaka ima aktivacijski kod.
        return False

    @admin.action(description=_("Preuzmi QR slike (bez aktivacijskih kodova)"))
    def preuzmi_qr(self, request, queryset):
        return zip_odgovor(zip_s_qr_kodovima(queryset.order_by("kod")), "qr-kodovi.zip")


# --- Grob, pokojnik, srodnik -------------------------------------------------


class PokojnikInline(admin.TabularInline):
    model = Pokojnik
    fields = ("ime", "prezime", "datum_rodjenja", "datum_smrti", "redoslijed")
    extra = 0
    show_change_link = True


class ObiteljskiLinkInline(admin.TabularInline):
    model = ObiteljskiLink
    fields = ("aktivan", "stvoreno", "ponisteno_u")
    readonly_fields = ("stvoreno", "ponisteno_u")
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Grob)
class GrobAdmin(admin.ModelAdmin):
    list_display = ("naziv", "plocica", "partner", "kontakt_za_prijavu", "javni_prikaz", "stvoreno")
    list_filter = ("partner", "javni_prikaz")
    search_fields = (
        "naziv",
        "plocica__kod",
        "vlasnik_ime",
        "kontakt_za_prijavu__email",
        "pokojnici__ime",
        "pokojnici__prezime",
    )
    # lozinka_hash se namjerno ne prikazuje nigdje u adminu
    exclude = ("lozinka_hash",)
    readonly_fields = ("verzija_pristupa", "stvoreno", "promijenjeno")
    autocomplete_fields = ("plocica", "kontakt_za_prijavu")
    inlines = [PokojnikInline, ObiteljskiLinkInline]

    def has_add_permission(self, request):
        # Grob nastaje aktivacijom (P-18 do P-20), koja postavlja i lozinku.
        return False

    def has_delete_permission(self, request, obj=None):
        # OP-7: grob briše samo superuser, jer je pločica fizički na grobu i plaćena.
        return request.user.is_superuser


class SrodnikInline(admin.TabularInline):
    model = Srodnik
    fk_name = "pokojnik"  # Srodnik ima dvije veze na Pokojnika
    fields = ("vrsta_srodstva", "povezani_pokojnik", "ime_i_prezime", "pristanak_na_prikaz", "redoslijed")
    extra = 0


class MedijInline(admin.TabularInline):
    model = Medij
    fields = ("vrsta", "status", "opis", "skriven", "stvoreno")
    readonly_fields = ("vrsta", "status", "opis", "stvoreno")
    extra = 0
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Pokojnik)
class PokojnikAdmin(admin.ModelAdmin):
    list_display = ("__str__", "grob", "datum_rodjenja", "datum_smrti")
    search_fields = ("ime", "prezime", "grob__naziv", "grob__plocica__kod")
    list_select_related = ("grob__plocica",)
    raw_id_fields = ("grob", "profilna_slika")
    inlines = [SrodnikInline, MedijInline]


@admin.register(Srodnik)
class SrodnikAdmin(admin.ModelAdmin):
    list_display = ("__str__", "pokojnik", "pristanak_na_prikaz")
    list_filter = ("vrsta_srodstva", "pristanak_na_prikaz")
    search_fields = ("ime_i_prezime", "pokojnik__ime", "pokojnik__prezime")
    raw_id_fields = ("pokojnik", "povezani_pokojnik")
