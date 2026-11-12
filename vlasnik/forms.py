from django import forms
from django.utils.translation import gettext_lazy as _

from jezgra.forms import NovaLozinkaGrobaForm
from jezgra.models import Grob
from jezgra.tekst import jedan_red


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

    def clean_naziv(self):
        return jedan_red(self.cleaned_data["naziv"])


class LozinkaGrobaForm(NovaLozinkaGrobaForm):
    odjavi_uredjaje = forms.BooleanField(
        label=_("Odjavi sve uređaje koji su upisali staru lozinku"),
        required=False,
        help_text=_("Tko je već otvarao stranicu, morat će upisati novu lozinku."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lozinka"].label = _("Nova lozinka groba")
        self.fields["lozinka"].help_text = _("Najmanje 6 znakova.")
        self.fields["lozinka2"].label = _("Ponovite novu lozinku")
