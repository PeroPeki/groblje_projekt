# Predlošci

Ugovor između pogleda (Python) i predloška (HTML). Karlo smije mijenjati izgled
predloška, ali **ne smije izgubiti** varijable, `{% csrf_token %}`, `name`
atribute polja ni `hx-*` atribute navedene ovdje. Ako predlošku treba novi
podatak, otvori issue s oznakom `petar`.

Svaki korak koji dodaje predložak dopunjuje ovu tablicu.

| Predložak | Pogled | URL | Varijable | Napomene |
|---|---|---|---|---|
| `base.html` | – | – | `csrf_token` (automatski) | Blokovi `naslov` i `sadrzaj`. Na `<body>` mora ostati `hx-headers` s CSRF tokenom, a u `<head>` oznake `<meta name="robots" content="noindex, nofollow">` i `<meta name="referrer" content="same-origin">` (P-15). |
| `javno/pocetna.html` | `jezgra.views.pocetna` | `/` | – | Probna stranica. Gumb ima `hx-post`, `hx-target="#htmx-odgovor"`, `hx-swap`. |
| `javno/_htmx_proba.html` | `jezgra.views.htmx_proba` | `/htmx-proba/` (POST) | – | Komad HTML-a koji HTMX umeće u `#htmx-odgovor`. |
| `aktivacija/unos_koda.html` | `pristup.views.grob` (GET) i `aktivacija.views.unos_koda` (POST) | `/g/<KOD>/` i `/aktivacija/<KOD>/` | `kod` (str), `forma` (polje `aktivacijski_kod`), `korak` (1), `ukupno_koraka` (4) | Korak 1 čarobnjaka. Prikazuje se za **nepostojeću, neaktiviranu i već aktiviranu** pločicu, uvijek jednako, i ne smije prikazati ništa drugo o pločici. Forma: `method="post"`, `action="{% url 'aktivacija:unos_koda' kod=kod %}"`, `{% csrf_token %}`, `name="aktivacijski_kod"`, `autocomplete="off"`. Stanja: prazno; pogrešan kod (`forma.aktivacijski_kod.errors`). Nakon previše pokušaja prikazuje se `greske/zakljucano.html`. |
| `aktivacija/korak_grob.html` | `aktivacija.views.korak_grob` | `/aktivacija/<KOD>/grob/` | `kod`, `forma` (GrobForm), `korak` (2), `ukupno_koraka` | Polja (`name`): `naziv`, `oznaka_grobnog_mjesta`, `vlasnik_ime`, `email`, `lozinka`, `lozinka2`. Svako polje ima `label`, `help_text` i `errors`. Oznaka polja `email` mora ostati točno „E-mail osobe koja će voditi profil” (odluka 19). Forma: POST na istu adresu, `{% csrf_token %}`. Lozinke se nakon greške ne vraćaju u polja. |
| `aktivacija/korak_pokojnik.html` | `aktivacija.views.korak_pokojnik` | `/aktivacija/<KOD>/pokojnik/` | `kod`, `grob`, `forma` (PokojnikForm), `korak` (3), `ukupno_koraka` | Polja: `ime`, `prezime`, `datum_rodjenja`, `datum_smrti` (oba `type="date"`, neobavezna), `biografija` (neobavezna). Greške: datum u budućnosti, smrt prije rođenja. |
| `aktivacija/korak_slike.html` | `aktivacija.views.korak_slike` | `/aktivacija/<KOD>/slike/` | `kod`, `grob`, `pokojnik` (ili `None`), `korak` (4), `ukupno_koraka` | Zasad samo link „Preskoči, dodat ću kasnije” na `{% url 'aktivacija:gotovo' kod=kod %}`. Gumb za dodavanje slika dolazi u P-28. |
| `aktivacija/gotovo.html` | `aktivacija.views.gotovo` | `/aktivacija/<KOD>/gotovo/` | `kod`, `grob`, `email` (str), `prijavljen` (bool) | Završni ekran. Link „Uredi sadržaj” prikazuje se samo kad je `prijavljen` (osoba s već postojećim računom nije prijavljena, nego dobiva e-mail). |
| `aktivacija/_forma_polja.html` | uključuju ga `korak_grob.html` i `korak_pokojnik.html` | – | `forma` | Privremeni ispis svih polja forme (oznaka, polje, pomoćni tekst, greške). Smije se zamijeniti komponentom `_polje.html`, uz iste `name` atribute. |
| `emailovi/aktivacija.txt` | `aktivacija.views.posalji_dobrodoslicu` | e-mail | `naziv_groba`, `link_groba`, `link_prijave` | Obični tekst. Ne sadrži lozinku groba ni aktivacijski kod. |
| `javno/zakljucano.html` | `pristup.views.zakljucani_ekran` (poziva se iz `grob` i `profil`) | `/g/<KOD>/` i `/g/<KOD>/<pokojnik_id>/`, dok posjetitelj nema pristup | `naziv_groba` (str), `naziv_partnera` (str), `kod` (str), `forma` (polje `lozinka`), `url_zahtjeva` (str ili `None`) | Forma: `method="post"` na istu adresu, `{% csrf_token %}`, `name="lozinka"`. **Smije prikazati samo naziv groba i naziv partnera**: bez imena pokojnika, datuma i slika (zato pogled ne šalje objekt `grob`). Stanja: prvi dolazak; pogrešna lozinka (`forma.lozinka.errors`); s linkom „Zatraži pristup” ili bez njega (`url_zahtjeva` je `None` do P-24). Nakon previše pogrešnih pokušaja umjesto ovog predloška prikazuje se `greske/zakljucano.html`. |
| `greske/zakljucano.html` | `pristup.views.zakljucani_ekran` | POST lozinke nakon previše pogrešnih pokušaja (status 429) | `cekanje` (str, npr. „15 min”, „60 min” ili „24 h”) | Poruka „Previše pokušaja. Pokušajte ponovno za {{ cekanje }}.” **Ne smije prikazati ništa o grobu ni pločici.** Koriste ga lozinka groba i unos aktivacijskog koda. |
| `javno/grob.html` | `pristup.views.grob` | `/g/<KOD>/` | `grob` (Grob), `kod` (str), `pokojnici` (lista Pokojnik) | Popis pokojnika s linkovima `{% url 'pristup:profil' kod=kod pokojnik_id=pokojnik.pk %}`. Prikazuje se tek kad posjetitelj ima pristup. Stanja: 2 ili više pokojnika; nijedan pokojnik (poruka). Grob s točno jednim pokojnikom ne dolazi ovamo, nego pogled odmah otvara profil. `grob.oznaka_grobnog_mjesta` se **nikad** ne prikazuje. |
| `javno/profil.html` | `pristup.views.profil` | `/g/<KOD>/<pokojnik_id>/` | `grob` (Grob), `kod` (str), `pokojnik` (Pokojnik), `ima_popis_pokojnika` (bool), `srodnici` (lista rječnika s ključevima `srodstvo` (str), `ime` (str), `url` (str ili `None`)) | Ime, datumi, biografija (`|linebreaks`, bez `|safe`), odjeljak „Obitelj” i zasad prazni odjeljci za slike, video i knjigu sjećanja (P-31, P-33). Datum se piše `|date:"j. E Y."` (mjesec u genitivu: „5. studenoga 2020.”). Link natrag na grob samo kad je `ima_popis_pokojnika`. **`srodnici` su već filtrirani u pogledu**: živuća osoba bez pristanka ne dolazi do predloška, a za onu s pristankom postoje samo ime i srodstvo. Ne dodaji druge izvore podataka o obitelji. Stanja su popisana ispod tablice. |
| `vlasnik/prijava.html` | `vlasnik.views.prijava` | `/vlasnik/prijava/` | `forma` (polje `email`) | Forma: `method="post"`, `{% csrf_token %}`, `name="email"`. Stanja: prazna forma; neispravna adresa (`forma.email.errors`). |
| `vlasnik/prijava_poslano.html` | `vlasnik.views.prijava_poslano` | `/vlasnik/prijava/poslano/` | – | Poruka „Ako je adresa upisana u sustavu, poslali smo Vam link za prijavu.” **Ista je za postojeću i nepostojeću adresu i ne smije prikazati upisanu adresu.** |
| `vlasnik/potvrda.html` | `vlasnik.views.potvrda` | `/vlasnik/potvrda/?sesame=<token>` (link iz e-maila) | `link_ne_vrijedi` (bool), `token` (str) | Dva stanja: gumb „Prijavi me” (forma `method="post"`, `{% csrf_token %}`, skriveno polje `name="sesame"` s vrijednošću `token`); „Ovaj link više ne vrijedi” s linkom na novu prijavu. Prijava se događa tek klikom na gumb, jer programi za e-poštu znaju sami otvoriti link. |
| `vlasnik/popis.html` | `vlasnik.views.popis` | `/vlasnik/` (samo prijavljeni) | `grobovi` (lista Grob), `user` | Popis grobova prijavljenog korisnika. Odjava je **POST forma** na `{% url 'vlasnik:odjava' %}` s `{% csrf_token %}`, nikad link. Stanja: bez grobova; jedan ili više. Proširuje se u P-21. |
| `emailovi/prijava.txt` | `vlasnik.prijava.zatrazi_link_za_prijavu` | e-mail | `link` (str), `minuta` (int) | Obični tekst (bez HTML-a), unutar `{% autoescape off %}`, da se link ne pokvari. |

Konvencija: predlošci čije ime počinje s `_` su **dijelovi** (*partials*) koji se
umeću u druge predloške ili ih vraća HTMX, a nisu cijele stranice.

Adrese groba: kanonski oblik je `/g/<KOD>/` (malo `g`, kod velikim slovima, kosa
crta na kraju). Svi ostali zapisi (`/G/K7M4QX` iz QR koda, mala slova) sami se
preusmjeravaju na kanonski oblik, pa u predlošcima uvijek koristi `{% url %}`.

## Stanja javnog dijela koja dizajn mora pokriti (P-14)

Sva se mogu izazvati lokalno naredbom `python manage.py napravi_probni_grob`
(lozinka oba groba je `demo123`; naredba radi samo uz `DEBUG=True` i može se
pokretati više puta).

| Stanje | Gdje se vidi |
|---|---|
| Zaključani ekran, prvi dolazak | `/g/PRB234/` u privatnom prozoru preglednika |
| Pogrešna lozinka | upiši krivu lozinku |
| Previše pokušaja (`greske/zakljucano.html`) | šest puta upiši krivu lozinku; blokada traje 15 minuta, a prekida je `python manage.py shell -c "from pristup.models import NeuspjeliPokusaj as N; N.objects.all().delete()"` |
| Grob s više pokojnika (popis) | `/g/PRB234/` nakon lozinke |
| Grob s jednim pokojnikom (odmah profil, bez linka natrag) | `/g/PRB345/` |
| Profil s biografijom, oba datuma i srodnicima | Marija Probić |
| Profil bez biografije, bez datuma rođenja, s jednim srodnikom | Josip Probić |
| Srodnik s vlastitim profilom u istom grobu (link) | Marija → suprug Josip |
| Srodnik s profilom u drugom grobu (link vodi na drugi grob) | Marija → brat Ivan Primjerić |
| Živuća osoba s pristankom (samo ime, bez linka) | Marija → unuka Ana Probić |
| Živuća osoba bez pristanka (ne smije se vidjeti ni u izvornom HTML-u) | Marko Probić postoji u bazi, ali ne i na stranici |
| Neaktivirana ili nepostojeća pločica | `/g/ZZZZZ9/` |
| Grob bez ijednog pokojnika | obriši pokojnike probnog groba u adminu, a zatim ih vrati s `python manage.py napravi_probni_grob --ponovno` |

Sve osobe u probnom grobu su izmišljene.

## Čarobnjak za aktivaciju (P-18 do P-20)

Svi koraci dobivaju `korak` i `ukupno_koraka` za prikaz „Korak X od 4”.

Kako lokalno doći do neaktivirane pločice i aktivacijskog koda: u adminu
(`/admin/`) dodaj partnera, zatim *Serije pločica → Dodaj*. Odmah se preuzima
ZIP s datotekom `kodovi.csv` (stupci `kod`, `aktivacijski_kod`, `link`). Otvori
`/g/<kod>/` i upiši aktivacijski kod. Ti kodovi vrijede samo u tvojoj lokalnoj
bazi; ZIP ne ide u Git.

| Stanje | Kako ga izazvati |
|---|---|
| Korak 1, pogrešan kod | upiši bilo kojih 8 znakova |
| Previše pokušaja (blokada 60 min) | šest pogrešnih kodova zaredom |
| Korak 2, greške | lozinka kraća od 6 znakova; različite lozinke; neispravan e-mail; prazno polje |
| Korak 3, greške | datum smrti prije datuma rođenja; datum u budućnosti |
| Korak 4 | zasad samo „Preskoči” |
| Gotovo, prijavljen | aktivacija s novom e-mail adresom |
| Gotovo, bez prijave | aktivacija s adresom koja već ima račun (npr. `proba@example.com` nakon `napravi_probni_grob`) |
