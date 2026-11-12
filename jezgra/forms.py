from django import forms
from django.utils.translation import gettext_lazy as _

from .lozinke import MAX_DULJINA_LOZINKE_GROBA, provjeri_lozinku_groba
from .models import SerijaPlocica

MAX_KOMADA_U_SERIJI = 500


class NovaSerijaForm(forms.ModelForm):
    class Meta:
        model = SerijaPlocica
        fields = ["partner", "oznaka", "broj_komada", "maloprodajna_cijena", "napomena"]

    def clean_broj_komada(self):
        broj = self.cleaned_data["broj_komada"]
        if not 1 <= broj <= MAX_KOMADA_U_SERIJI:
            raise forms.ValidationError(
                _("Broj komada mora biti između 1 i %(max)s.") % {"max": MAX_KOMADA_U_SERIJI}
            )
        return broj


class NovaLozinkaGrobaForm(forms.Form):
    """Polja i pravila za postavljanje lozinke groba (aktivacija i vlasnički dio)."""

    lozinka = forms.CharField(
        label=_("Lozinka groba"),
        max_length=MAX_DULJINA_LOZINKE_GROBA,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_("Najmanje 6 znakova. Ovu lozinku dajete obitelji i prijateljima."),
    )
    lozinka2 = forms.CharField(
        label=_("Ponovite lozinku groba"),
        max_length=MAX_DULJINA_LOZINKE_GROBA,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
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
