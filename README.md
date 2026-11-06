# Vječna spomen

Digitalna spomen-stranica uz QR pločicu na grobu: posjetitelj skenira kod i otvara profil pokojnika sa slikama, videom i knjigom sjećanja.

Tehnologije: Django 6.1, PostgreSQL 18, Tailwind CSS 4 (bez Node.js), HTMX 2.

## Pokretanje

Potrebni su **Git** i **Python 3.13 ili 3.14**. Node.js nije potreban.

### 1. Preuzimanje i virtualno okruženje

macOS:
```
git clone https://github.com/PeroPeki/groblje_projekt.git
cd groblje_projekt
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```
git clone https://github.com/PeroPeki/groblje_projekt.git
cd groblje_projekt
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ako PowerShell javi da ne smije pokretati skripte, jednom pokreni
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` pa ponovno aktiviraj.

Svaki put kad otvoriš novi terminal, prvo aktiviraj okruženje (`source .venv/bin/activate` ili `.venv\Scripts\activate`). Ispred prompta tada piše `(.venv)`.

### 2. Datoteka `.env`

Kopiraj primjer (macOS: `cp .env.example .env`, Windows: `copy .env.example .env`) i u `.env` upiši:

- `SECRET_KEY`: dugi slučajni niz, dobiješ ga naredbom `python -c "import secrets; print(secrets.token_urlsafe(50))"`;
- `DATABASE_URL`: vidi sljedeći korak.

`.env` se **nikad** ne šalje u Git.

### 3. Baza podataka

**Najjednostavnije (rad na predlošcima i dizajnu):** SQLite, ne treba ništa instalirati. U `.env`:
```
DATABASE_URL=sqlite:///db.sqlite3
```

**PostgreSQL (kao u produkciji):** na macOS-u
```
brew install postgresql@18
brew services start postgresql@18
createuser vjecnaspomen --pwprompt
createdb vjecnaspomen --owner vjecnaspomen
```
i u `.env`: `DATABASE_URL=postgres://vjecnaspomen:<lozinka>@localhost:5432/vjecnaspomen`.

Zatim:
```
python manage.py migrate
python manage.py createsuperuser
```

### 4. Pokretanje

```
python manage.py tailwind runserver
```

Prvi put se preuzima Tailwind program (~80 MB), pa treba pričekati. Nakon toga otvori:

- http://localhost:8000/: probna stranica (velik naslov znači da Tailwind radi, a gumb „Isprobaj HTMX” provjerava HTMX)
- http://localhost:8000/admin/: administracija (prijava računom iz `createsuperuser`)

Tailwind prati predloške i sam ponovno generira CSS kad promijeniš klasu: samo osvježi stranicu.

### 5. Proba na mobitelu (ista Wi-Fi mreža)

1. Saznaj IP adresu računala: macOS `ipconfig getifaddr en0`, Windows `ipconfig` (redak *IPv4 Address*).
2. Dodaj je u `.env`: `ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.23` (s tvojom adresom).
3. Pokreni `python manage.py tailwind runserver 0.0.0.0:8000`.
4. Na mobitelu otvori `http://192.168.1.23:8000`.

Na Windowsu vatrozid može pitati za dopuštenje: dopusti pristup za privatne mreže.

### Česti problemi

- **`ModuleNotFoundError: No module named 'django'`**: okruženje nije aktivirano.
- **Klasa se ne primjenjuje:** Tailwind ne prepoznaje klase sastavljene od dijelova (`text-{{ velicina }}`), klasa mora biti napisana cijela. Pomoć: `python manage.py tailwind troubleshoot`.
- **`DisallowedHost`**: adresa s koje otvaraš stranicu nije u `ALLOWED_HOSTS` u `.env`.

## Struktura

| Mapa | Što je unutra |
|---|---|
| `config/` | postavke projekta (`settings.py`) i glavni URL-ovi (`urls.py`) |
| `korisnici/` | vlastiti model korisnika `Korisnik` |
| `jezgra/` | zajednički pogledi (zasad probna početna stranica) |
| `templates/` | svi HTML predlošci (`base.html` je okvir za sve stranice) |
| `static/` | CSS, JavaScript, slike i fontovi koji se poslužuju pregledniku |
| `tailwind/ulaz.css` | izvorni Tailwind CSS i tema (boje, fontovi) |
| `docs/` | odluke, planovi rada, popis predložaka (`predlosci.md`) |

---

© 2026 Petar Car i Karlo Vlašić. Sva prava pridržana. Kod je javno vidljiv radi portfolija, ali se ne smije koristiti, kopirati ni mijenjati bez pisanog dopuštenja.
