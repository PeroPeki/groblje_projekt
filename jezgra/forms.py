from django import forms
from django.utils.translation import gettext_lazy as _

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
