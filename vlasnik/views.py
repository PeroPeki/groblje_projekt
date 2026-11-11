"""Vlasnički dio: prijava linkom na e-mail i popis grobova."""

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST
from sesame.utils import get_user

from .forms import PrijavaForm
from .prijava import zatrazi_link_za_prijavu

TOKEN = "sesame"  # naziv parametra u linku i skrivenog polja u formi (SESAME_TOKEN_NAME)


def prijava(request):
    """Forma s e-mailom. Odgovor je isti postoji li adresa u sustavu ili ne."""
    if request.user.is_authenticated:
        return redirect("vlasnik:popis")
    forma = PrijavaForm(request.POST or None)
    if request.method == "POST" and forma.is_valid():
        zatrazi_link_za_prijavu(request, forma.cleaned_data["email"])
        return redirect("vlasnik:prijava_poslano")
    return render(request, "vlasnik/prijava.html", {"forma": forma})


def prijava_poslano(request):
    return render(request, "vlasnik/prijava_poslano.html")


@sensitive_post_parameters(TOKEN)
@never_cache
def potvrda(request):
    """Stranica na koju vodi link iz e-maila.

    Samo otvaranje linka (GET) nikoga ne prijavljuje: programi za e-poštu
    znaju sami „otvoriti” link i tako bi potrošili jednokratni token. Prijava
    se događa tek klikom na gumb (POST).
    """
    if request.method == "POST":
        korisnik = get_user(request.POST.get(TOKEN, ""), update_last_login=False)
        if korisnik is None:
            return render(request, "vlasnik/potvrda.html", {"link_ne_vrijedi": True})
        login(request, korisnik)  # login() mijenja last_login, pa token više ne vrijedi
        return redirect("vlasnik:popis")

    token = request.GET.get(TOKEN)
    if not token:
        return redirect("vlasnik:prijava")
    return render(request, "vlasnik/potvrda.html", {"token": token, "link_ne_vrijedi": False})


@require_POST
def odjava(request):
    logout(request)
    return redirect("vlasnik:prijava")


@login_required
def popis(request):
    """Grobovi kojima je prijavljeni korisnik kontakt za prijavu."""
    grobovi = request.user.grobovi.select_related("plocica")
    return render(request, "vlasnik/popis.html", {"grobovi": grobovi})
