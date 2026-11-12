from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from jezgra.forms import NovaLozinkaGrobaForm
from jezgra.models import Pokojnik
from jezgra.tekst import jedan_red


def normaliziraj_aktivacijski_kod(unos: str) -> str:
    """Velika slova, bez razmaka i crtica: ljudi prepisuju „k7m4 qx2p” ili „K7M4-QX2P”."""
    return "".join(znak for znak in unos.upper() if znak.isalnum())


class AktivacijskiKodForm(forms.Form):
    aktivacijski_kod = forms.CharField(label=_("Aktivacijski kod"), max_length=40)

    def clean_aktivacijski_kod(self):
        return normaliziraj_aktivacijski_kod(self.cleaned_data["aktivacijski_kod"])


class GrobForm(NovaLozinkaGrobaForm):
    # Polja lozinka i lozinka2 dolaze iz NovaLozinkaGrobaForm.
    field_order = ["naziv", "oznaka_grobnog_mjesta", "vlasnik_ime", "email", "lozinka", "lozinka2"]

    naziv = forms.CharField(
        label=_("Naziv groba"),
        max_length=200,
        help_text=_("Npr. Obitelj Horvat. Ovaj naziv vide posjetitelji."),
    )
    oznaka_grobnog_mjesta = forms.CharField(
        label=_("Oznaka grobnog mjesta"),
        max_length=200,
        help_text=_(
            "Prepišite s računa uprave groblja, npr. Polje C, red 4, br. 12. "
            "Posjetitelji je ne vide."
        ),
    )
    vlasnik_ime = forms.CharField(
        label=_("Ime i prezime vlasnika"),
        max_length=200,
        help_text=_("Osoba na koju glasi grobno mjesto."),
    )
    email = forms.EmailField(
        label=_("E-mail osobe koja će voditi profil"),  # točan tekst iz odluke 19
        max_length=150,  # e-mail je ujedno korisničko ime (najviše 150 znakova)
        help_text=_("Na ovu adresu šaljemo link za prijavu. Lozinka za prijavu ne postoji."),
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_naziv(self):
        return jedan_red(self.cleaned_data["naziv"])


class PokojnikForm(forms.ModelForm):
    class Meta:
        model = Pokojnik
        fields = ["ime", "prezime", "datum_rodjenja", "datum_smrti", "biografija"]
        widgets = {
            # format="%Y-%m-%d": preglednik u <input type="date"> očekuje baš taj zapis
            "datum_rodjenja": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "datum_smrti": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "biografija": forms.Textarea(attrs={"rows": 8}),
        }

    def clean(self):
        podaci = super().clean()
        rodjenje, smrt = podaci.get("datum_rodjenja"), podaci.get("datum_smrti")
        danas = timezone.localdate()
        for polje, datum in (("datum_rodjenja", rodjenje), ("datum_smrti", smrt)):
            if datum and datum > danas:
                self.add_error(polje, _("Datum ne može biti u budućnosti."))
        if rodjenje and smrt and smrt < rodjenje:
            self.add_error("datum_smrti", _("Datum smrti ne može biti prije datuma rođenja."))
        return podaci
