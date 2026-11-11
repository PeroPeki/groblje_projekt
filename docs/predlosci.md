# Predlošci

Ugovor između pogleda (Python) i predloška (HTML). Karlo smije mijenjati izgled
predloška, ali **ne smije izgubiti** varijable, `{% csrf_token %}`, `name`
atribute polja ni `hx-*` atribute navedene ovdje. Ako predlošku treba novi
podatak, otvori issue s oznakom `petar`.

Svaki korak koji dodaje predložak dopunjuje ovu tablicu.

| Predložak | Pogled | URL | Varijable | Napomene |
|---|---|---|---|---|
| `base.html` | – | – | `csrf_token` (automatski) | Blokovi `naslov` i `sadrzaj`. Na `<body>` mora ostati `hx-headers` s CSRF tokenom. |
| `javno/pocetna.html` | `jezgra.views.pocetna` | `/` | – | Probna stranica. Gumb ima `hx-post`, `hx-target="#htmx-odgovor"`, `hx-swap`. |
| `javno/_htmx_proba.html` | `jezgra.views.htmx_proba` | `/htmx-proba/` (POST) | – | Komad HTML-a koji HTMX umeće u `#htmx-odgovor`. |
| `aktivacija/unos_koda.html` | `pristup.views.grob` | `/g/<KOD>/` | `kod` (str, 6 znakova) | Prikazuje se za **nepostojeću i za neaktiviranu** pločicu, uvijek jednako. Ne smije prikazati ništa drugo o pločici (partner, serija). Forma za aktivacijski kod dolazi u P-18. |
| `javno/zakljucano.html` | `pristup.views.zakljucani_ekran` (poziva se iz `grob` i `profil`) | `/g/<KOD>/` i `/g/<KOD>/<pokojnik_id>/`, dok posjetitelj nema pristup | `naziv_groba` (str), `naziv_partnera` (str), `kod` (str), `forma` (polje `lozinka`), `url_zahtjeva` (str ili `None`) | Forma: `method="post"` na istu adresu, `{% csrf_token %}`, `name="lozinka"`. **Smije prikazati samo naziv groba i naziv partnera**: bez imena pokojnika, datuma i slika (zato pogled ne šalje objekt `grob`). Stanja: prvi dolazak; pogrešna lozinka (`forma.lozinka.errors`); s linkom „Zatraži pristup” ili bez njega (`url_zahtjeva` je `None` do P-24). Nakon previše pogrešnih pokušaja umjesto ovog predloška prikazuje se `greske/zakljucano.html`. |
| `greske/zakljucano.html` | `pristup.views.zakljucani_ekran` | POST lozinke nakon previše pogrešnih pokušaja (status 429) | `minuta` (int: 15 ili 60) | Poruka „Previše pokušaja. Pokušajte ponovno za N minuta.” **Ne smije prikazati ništa o grobu ni pločici.** Isti predložak kasnije koristi i unos aktivacijskog koda (P-18). |
| `javno/grob.html` | `pristup.views.grob` | `/g/<KOD>/` | `grob` (Grob), `kod` (str), `pokojnici` (lista Pokojnik) | Popis pokojnika s linkovima `{% url 'pristup:profil' kod=kod pokojnik_id=pokojnik.pk %}`. Prikazuje se tek kad posjetitelj ima pristup. Stanja: 2 ili više pokojnika; nijedan pokojnik (poruka). Grob s točno jednim pokojnikom ne dolazi ovamo, nego pogled odmah otvara profil. `grob.oznaka_grobnog_mjesta` se **nikad** ne prikazuje. |
| `javno/profil.html` | `pristup.views.profil` | `/g/<KOD>/<pokojnik_id>/` | `grob` (Grob), `kod` (str), `pokojnik` (Pokojnik), `ima_popis_pokojnika` (bool), `srodnici` (lista rječnika s ključevima `srodstvo` (str), `ime` (str), `url` (str ili `None`)) | Ime, datumi, biografija (`|linebreaks`, bez `|safe`), odjeljak „Obitelj” i zasad prazni odjeljci za slike, video i knjigu sjećanja (P-31, P-33). Datum se piše `|date:"j. E Y."` (mjesec u genitivu: „5. studenoga 2020.”). Link natrag na grob samo kad je `ima_popis_pokojnika`. **`srodnici` su već filtrirani u pogledu**: živuća osoba bez pristanka ne dolazi do predloška, a za onu s pristankom postoje samo ime i srodstvo. Ne dodaji druge izvore podataka o obitelji. Stanja su popisana ispod tablice. |

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
| Grob bez ijednog pokojnika | obriši pokojnike probnog groba u adminu |

Sve osobe u probnom grobu su izmišljene.
