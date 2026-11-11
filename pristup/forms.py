from django import forms
from django.utils.translation import gettext_lazy as _


class LozinkaForm(forms.Form):
    lozinka = forms.CharField(
        label=_("Lozinka"),
        max_length=128,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
