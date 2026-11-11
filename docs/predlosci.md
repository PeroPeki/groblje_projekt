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

Konvencija: predlošci čije ime počinje s `_` su **dijelovi** (*partials*) koji se
umeću u druge predloške ili ih vraća HTMX, a nisu cijele stranice.
