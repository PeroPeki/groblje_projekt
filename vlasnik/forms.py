from django import forms
from django.utils.translation import gettext_lazy as _


class PrijavaForm(forms.Form):
    email = forms.EmailField(
        label=_("E-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()
