from django import forms
from django.utils.translation import gettext_lazy as _

from jezgra.lozinke import MAX_DULJINA_LOZINKE_GROBA, provjeri_lozinku_groba
from jezgra.models import Grob


class PrijavaForm(forms.Form):
    email = forms.EmailField(
        label=_("E-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class NazivGrobaForm(forms.ModelForm):
    class Meta:
        model = Grob
        fields = ["naziv"]


class LozinkaGrobaForm(forms.Form):
    lozinka = forms.CharField(
        label=_("Nova lozinka groba"),
        max_length=MAX_DULJINA_LOZINKE_GROBA,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_("Najmanje 6 znakova."),
    )
    lozinka2 = forms.CharField(
        label=_("Ponovite novu lozinku"),
        max_length=MAX_DULJINA_LOZINKE_GROBA,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    odjavi_uredjaje = forms.BooleanField(
        label=_("Odjavi sve uređaje koji su upisali staru lozinku"),
        required=False,
        help_text=_("Tko je već otvarao stranicu, morat će upisati novu lozinku."),
    )

    def clean_lozinka(self):
        lozinka = self.cleaned_data["lozinka"]
        provjeri_lozinku_groba(lozinka)
        return lozinka

    def clean(self):
        podaci = super().clean()
        lozinka, lozinka2 = podaci.get("lozinka"), podaci.get("lozinka2")
        if lozinka and lozinka2 and lozinka != lozinka2:
            self.add_error("lozinka2", _("Lozinke nisu jednake."))
        return podaci
