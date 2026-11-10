from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Korisnik


@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "partner", "is_staff")
    list_filter = UserAdmin.list_filter + ("partner",)
    fieldsets = UserAdmin.fieldsets + (("Partner", {"fields": ("partner",)}),)
