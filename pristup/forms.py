from django import forms
from django.utils.translation import gettext_lazy as _

from jezgra.lozinke import MAX_DULJINA_LOZINKE_GROBA


class LozinkaForm(forms.Form):
    lozinka = forms.CharField(
        label=_("Lozinka"),
        max_length=MAX_DULJINA_LOZINKE_GROBA,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
