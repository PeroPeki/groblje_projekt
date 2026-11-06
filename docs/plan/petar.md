# Plan rada: Petar

Arhitektura i razvoj aplikacije „Vječna spomen” (vjecnaspomen.hr): Django modeli, pogledi i URL-ovi, aktivacija, lozinke i sigurnost, mediji, pozadinski zadaci, administracija, izvještaji i objava.

## Kako koristiti ovaj plan

Radi korake redom kojim su numerirani. Ako te neki korak čeka na prijatelja, preskoči na sljedeći koji nema tu ovisnost, a privremeni „ružni” predložak poslužit će dok ne stigne pravi. Kad je korak gotov i svi uvjeti iz „Gotovo kada” su ispunjeni, u istom PR-u promijeni `- [ ] Gotovo` u `- [x] Gotovo`. Pomoć traži redom: link u „Novi pojmovi”, službena dokumentacija, issue s oznakom `pitanje`, pa poruka prijatelju.

Pojmovi iz rječnika u `docs/odluke.md` (grob, QR oznaka, pločica, pokojnik, profil, vlasnik, kontakt za prijavu, posjetitelj, partner, aktivacija, aktivacijski kod, knjiga sjećanja, srodnik) koriste se točno tako i u kodu, pa modeli imaju hrvatske nazive (`Grob`, `Pokojnik`, `Plocica` ...). Dijakritike se u kodu izostavljaju, a u tekstovima za korisnika pišu se normalno.

**Verzije alata** (provjereno u studenom 2026.; pri instalaciji ipak provjeri najnoviju stabilnu verziju): Django 6.1, Python 3.13 ili 3.14, PostgreSQL 18, Tailwind CSS 4.3 (preko paketa `django-tailwind-cli`, bez Node.js), HTMX 2.x (HTMX 4 je u trenutku pisanja još beta, pa ga ne koristimo). Za ostale pakete (`django-environ`, `django-htmx`, `django-sesame`, `django-q2`, `django-storages`, `boto3`, `segno`, `Pillow`, `pillow-heif`, `whitenoise`, `gunicorn`, `psycopg`) instaliraj najnoviju stabilnu verziju i zapiši je u `requirements.txt`.

## Pregled

| Faza | Cilj | Koraci | Procjena |
|---|---|---|---|
| 1. Priprema i kostur projekta | Alati, repozitorij, Django projekt, baza, Tailwind i HTMX: prijatelj može pokrenuti projekt. | 5 (P-01 – P-05) | 10–15 h |
| 2. Modeli podataka i administracija | Svi pojmovi iz rječnika postoje kao modeli, u adminu se stvaraju serije pločica s QR kodovima. | 5 (P-06 – P-10) | 13–18 h |
| 3. Prva radna verzija: QR → lozinka → profil | Skeniranje koda vodi na zaključani ekran, a točna lozinka na profil. Pristup je pokriven testovima. | 6 (P-11 – P-16) | 17–23 h |
| 4. Aktivacija i vlasnički dio | Obitelj aktivira pločicu čarobnjakom, prijavljuje se e-mailom i upravlja grobom. | 9 (P-17 – P-25) | 26–37 h |
| 5. Mediji | Upload slika i videa s mobitela izravno u R2, pozadinska obrada i prikaz kroz potpisane linkove. | 7 (P-26 – P-32) | 24–31 h |
| 6. Knjiga sjećanja i prijave | Poruke uz odobrenje vlasnika i gumb „Prijavi” na svakom sadržaju. | 2 (P-33 – P-34) | 7–9 h |
| 7. Administracija, izvoz i izvještaji | Udoban admin, izvoz groba, mjesečni izvještaj i pregled za partnera. | 4 (P-35 – P-38) | 13–17 h |
| 8. Demo, objava i CV | PWA, demo podaci, objava na Render, provjera mjerila uspjeha, README i studija slučaja. | 9 (P-39 – P-47) | 26–37 h |
| **Ukupno** | | **47** | **136–187 h** |

## Zajednički način rada

Ovaj odjeljak je isti u oba plana. Ako ga jedan od vas promijeni, promijenite ga u oba dokumenta u istom pull requestu.

### Gdje što stoji

| Što | Gdje |
|---|---|
| Kod, predlošci, statičke datoteke, dokumentacija | javni GitHub repozitorij (Petar je vlasnik, prijatelj je *collaborator* s pravom pisanja) |
| Dizajn | jedna Figma datoteka „Vječna spomen – MVP” sa stranicama: *Tokovi*, *Identitet*, *Komponente*, *Javni dio*, *Aktivacija*, *Vlasnik*, *Partner*, *Greške i prazna stanja*, *Pločica i letak* |
| Bugovi, nalazi testiranja, pitanja | GitHub Issues, s oznakama (*labels*) `bug`, `dizajn`, `nalaz-testiranja`, `pitanje`, `petar`, `prijatelj` |
| Napredak po planu | kvačica `- [x] Gotovo` u vlastitom planu (`docs/plan/petar.md` ili `docs/plan/prijatelj.md`) |
| Tajni podaci (lozinke, ključevi) | samo u lokalnoj datoteci `.env` i u postavkama hostinga. Drugome ih šaljete privatnom porukom, nikad kroz Git, Issues ni Figmu |

### Grane i pull requestovi

1. Grana `main` uvijek radi. Nitko ne šalje promjene (*push*) izravno u `main`, jer je uključena zaštita grane.
2. Za svaki korak napravi novu granu nazvanu po ID-u koraka, npr. `p-12-zakljucani-ekran` ili `d-17-predlozak-zakljucanog-ekrana`.
3. Kad je korak gotov, pošalji granu na GitHub i otvori *pull request* (PR) prema `main`. U opisu navedi ID koraka, što si napravio i kako drugi to može provjeriti. Ako se mijenja izgled, dodaj snimku zaslona s mobitela.
4. **Svaki PR pregledava drugi član tima.**
   - Petar pri pregledu prijateljevih PR-ova provjerava da predlošci nisu izgubili varijable, `{% csrf_token %}`, `name` atribute polja i `hx-*` atribute.
   - Prijatelj pri pregledu Petrovih PR-ova provjerava tekstove, izgled i radi li stvar kad je pokrene lokalno. Python kod ne mora razumjeti do kraja.
5. Spajanje radite gumbom **„Squash and merge”**: cijeli korak postaje jedan uredan commit u `main`. Nakon spajanja obrišite granu.
6. Prije početka novog koraka povuci najnoviji `main` (`git switch main && git pull`) i tek onda napravi novu granu.
7. Ako zapneš na nečemu dulje od sat vremena, otvori issue s oznakom `pitanje` ili se javi drugome. Zapinjanje nije sramota, ali gubitak tri večeri jest šteta.

Jednom tjedno (ili kad vam odgovara) imate kratak poziv od 15 do 30 minuta: što je gotovo, što koga blokira, što je sljedeće. To je navika, a ne rok.

### Struktura mapa

```
groblje_projekt/
├── config/              # postavke Django projekta (settings.py, urls.py)
├── korisnici/           # vlastiti model korisnika
├── jezgra/              # partner, serija, pločica, grob, pokojnik, srodnik
├── pristup/             # zaključani ekran, lozinka, obiteljski link, zahtjev za pristup
├── aktivacija/          # čarobnjak za aktivaciju
├── vlasnik/             # vlasnički dio (uređivanje, odobravanje)
├── mediji/              # slike, videi, pozadinska obrada
├── knjiga/              # knjiga sjećanja i prijave sadržaja
├── partneri/            # izvještaji i pregled za partnera
├── templates/
│   ├── base.html        # zajednički okvir svih stranica
│   ├── komponente/      # mali dijelovi koji se ponavljaju (_gumb.html, _poruka.html ...)
│   ├── javno/           # zaključani ekran, grob, profil, galerija, knjiga sjećanja
│   ├── aktivacija/      # koraci čarobnjaka
│   ├── vlasnik/         # vlasnički dio
│   ├── partner/         # pregled za partnera
│   ├── emailovi/        # tekstovi e-mail poruka
│   └── greske/          # 404.html, 500.html, zaključano
├── static/
│   ├── css/izlaz.css    # CSS koji generira Tailwind (nije u Gitu)
│   ├── js/              # mali vlastiti JavaScript (npr. upload)
│   ├── img/             # ikone, logotip
│   ├── fontovi/         # fontovi koje poslužujemo sami
│   └── vendor/          # htmx.min.js i slične preuzete datoteke
├── tailwind/ulaz.css    # izvorni Tailwind CSS (ovo se uređuje; izvan static/ da ga collectstatic ne dira)
├── demo/                # izmišljeni demo sadržaj i popis izvora fotografija
├── docs/                # odluke, planovi, dijagram modela, popis predložaka
├── .env.example         # popis potrebnih varijabli BEZ stvarnih vrijednosti
└── README.md
```

Predlošci su namjerno u jednoj mapi `templates/` na razini projekta, a ne razbacani po aplikacijama. Tako prijatelj sve što uređuje ima na jednom mjestu.

### Ugovor između pogleda i predloška

- Petar za svaki ekran prvo napravi „ružan” privremeni predložak koji radi. Na vrhu predloška stoji komentar s popisom varijabli koje pogled šalje, npr. `{# Varijable: grob (Grob), pokojnici (lista Pokojnik), greska (str ili None) #}`. Isti popis vodi se u `docs/predlosci.md`.
- Prijatelj zatim mijenja HTML strukturu i Tailwind klase. **Bez dogovora ne mijenja** imena varijabli, `name` atribute polja u formama, `{% csrf_token %}`, `hx-*` atribute ni nazive u `{% url '...' %}`.
- Ako predlošku treba još neki podatak (npr. broj poruka na čekanju), prijatelj otvori issue s oznakom `petar` i Petar ga doda u pogled.
- Svaki tekst koji korisnik vidi piše se kroz `{% translate "..." %}` ili `{% blocktranslate %}`, iako je aplikacija zasad samo na hrvatskom (odluka 18a).

### Tajni podaci i javni repozitorij

- Datoteka `.env` je u `.gitignore` i nikad ne ide u Git. U Git ide samo `.env.example`, s nazivima varijabli i praznim ili izmišljenim vrijednostima.
- Prije svakog commita pogledaj što šalješ (`git status`, `git diff --staged`).
- Ako ključ ipak završi na GitHubu, **odmah ga poništi i napravi novi** u servisu iz kojeg je došao (Cloudflare, Render, e-mail servis). Brisanje iz povijesti nije dovoljno, jer je repozitorij javan i netko ga je možda već kopirao.
- Demo sadržaj koristi samo izmišljene osobe i fotografije sa slobodnom licencom. Nikad stvarne pokojnike ni stvarne obitelji, pa ni svoje.

## Faza 1: Priprema i kostur projekta

Alati, repozitorij, Django projekt, baza, Tailwind i HTMX: prijatelj može pokrenuti projekt.

### P-01 Zajednički početak: alati i prvi sastanak
- [ ] Gotovo

Ovaj korak je isti u oba plana (P-01 i D-01). Radite ga zajedno.

**Cilj:** oba člana imaju instalirane alate, pristup GitHubu i Figmi te su zajedno pročitali `docs/odluke.md`.

**Zašto:** cijeli plan oslanja se na odluke iz `docs/odluke.md` i na zajednički način rada (odluke 17 i 20). Bez istog polazišta svaki sljedeći korak traje dulje.

**Preduvjeti:** nema.

**Novi pojmovi:**
- **Git** je program koji pamti svaku promjenu datoteka u projektu. Može se vratiti na bilo koju raniju verziju, a dvije osobe mogu raditi istovremeno bez prepisivanja tuđeg rada. [Pro Git knjiga](https://git-scm.com/book/en/v2)
- **GitHub** je web servis na kojem stoji zajednička kopija Git repozitorija, s pull requestovima i Issues. [GitHub Docs: Get started](https://docs.github.com/en/get-started)
- **Repozitorij** je mapa projekta zajedno s cijelom poviješću promjena.
- **Uređivač koda** je program za pisanje koda. Preporuka je **VS Code**. [VS Code](https://code.visualstudio.com/docs)
- **Figma** je alat za dizajn ekrana u pregledniku ili aplikaciji. [Figma Help Center](https://help.figma.com/)
- **Python** je programski jezik u kojem je napisan Django. **Node.js nije potreban**: Tailwind koristimo kao samostalni program (vidi P-05).

**Upute:**
1. Oboje instalirajte alate. Za sve navodi najnoviju stabilnu verziju koju nudi službena stranica.

   | Alat | macOS | Windows |
   |---|---|---|
   | Git | `xcode-select --install` ili `brew install git` | [Git for Windows](https://git-scm.com/download/win) ili `winget install Git.Git` |
   | GitHub Desktop (neobavezno, olakšava rad bez terminala) | [desktop.github.com](https://desktop.github.com/) | isto |
   | Python 3.13 ili 3.14 (provjeri da ga podržava Django 6.1) | [python.org](https://www.python.org/downloads/) ili `brew install python@3.13` | [python.org](https://www.python.org/downloads/) (pri instalaciji označi **„Add python.exe to PATH”**) ili `winget install Python.Python.3.13` |
   | VS Code | [code.visualstudio.com](https://code.visualstudio.com/) | isto |
   | Figma | [figma.com](https://www.figma.com/) (besplatni plan; studenti mogu zatražiti besplatni Education plan, provjeri uvjete) | isto |

2. U VS Codeu instalirajte proširenja: *Python* (Microsoft), *Django* (Baptiste Darthenay, za boje u predlošcima), *Tailwind CSS IntelliSense*.
3. Provjerite instalaciju u terminalu (macOS: Terminal; Windows: PowerShell):
   ```
   git --version
   python3 --version      # na Windowsu: python --version
   ```
4. Oboje napravite GitHub račun (ako ga nemate) i uključite dvostupanjsku prijavu (*two-factor authentication*) u postavkama računa. Javni repozitorij s pravom pisanja mora biti dobro zaštićen.
5. Postavite ime i e-mail za Git (jednom po računalu):
   ```
   git config --global user.name "Ime Prezime"
   git config --global user.email "adresa@primjer.hr"
   ```
6. Dogovorite poziv (uživo ili video) od otprilike 2 sata. Dnevni red:
   1. Zajedno pročitajte cijeli `docs/odluke.md`, naglas ili svatko za sebe pa razgovor. Posebno obratite pažnju na rječnik pojmova na kraju: te riječi koristite u kodu, dizajnu i razgovoru.
   2. Prođite oba plana (`docs/plan/petar.md` i `docs/plan/prijatelj.md`), posebno blokove „🔁 Predaja”.
   3. Pročitajte odjeljak „Zajednički način rada” i potvrdite da vam odgovara.
   4. Prođite „Otvorena pitanja” na kraju planova i zapišite odluke u `docs/odluke.md`.
   5. Dogovorite kad ćete napisati kratki pisani dogovor o udjelima 50/50 (odluka 17). Prijedlog je u otvorenim pitanjima.
7. Petar napravi Figma datoteku „Vječna spomen – MVP” ili je napravi prijatelj i pozove Petra s pravom uređivanja.

**Gotovo kada:**
- oba člana u terminalu vide verzije Gita i Pythona;
- oba GitHub računa imaju uključenu dvostupanjsku prijavu;
- oba člana imaju pristup Figma datoteci;
- odgovori na otvorena pitanja (ili odluka da se odgađaju) zapisani su u `docs/odluke.md`.

**Procjena:** 3–4 sata (instalacija 1–2 h, sastanak 2 h).

**Česte greške:**
- Na Windowsu `python` otvara Microsoft Store umjesto Pythona. Instaliraj Python s python.org uz kvačicu „Add to PATH” ili u postavkama isključi *App execution aliases* za Python.
- Na macOS-u postoji stari sistemski Python. Uvijek koristi `python3`, a kasnije Python iz virtualnog okruženja.

### P-02 GitHub repozitorij, `.gitignore` i README
- [ ] Gotovo

**Cilj:** postoji javni GitHub repozitorij s prvim commitom, zaštićenom granom `main`, `.gitignore` datotekom i README-om s napomenom „Sva prava pridržana”.

**Zašto:** repozitorij je javan zbog CV-a, ali tajni podaci nikad ne smiju u njega (odluka 20). Pravila postavljena u prvom commitu najlakše je poštovati.

**Preduvjeti:** P-01 gotov.

**Novi pojmovi:**
- **Commit** je spremljena točka u povijesti projekta, s porukom što je promijenjeno.
- **Grana (*branch*)** je odvojena linija rada. Na njoj mijenjaš kod bez diranja glavne grane `main`. [Pro Git: Branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- **Pull request (PR)** je zahtjev na GitHubu da se promjene s jedne grane spoje u drugu. Drugi član ih prije spajanja pregleda. [GitHub: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- **`.gitignore`** je popis datoteka koje Git ne prati (tajne, privremene datoteke, generirani CSS). [Git: gitignore](https://git-scm.com/docs/gitignore)
- **Zaštita grane (*branch protection*)** je GitHubovo pravilo koje zabranjuje izravno slanje u `main` i traži PR. [GitHub: Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

**Upute:**
1. U mapi projekta napravi `.gitignore`:
   ```
   .env
   .venv/
   __pycache__/
   *.pyc
   db.sqlite3
   media/
   staticfiles/
   static/css/izlaz.css
   .django_tailwind_cli/
   .DS_Store
   ```
2. Napravi `README.md` s naslovom, jednom rečenicom o projektu, odjeljkom „Pokretanje” (zasad prazan) i na dnu: `© 2026 Petar i [ime prijatelja]. Sva prava pridržana. Kod je javno vidljiv radi portfolija, ali se ne smije koristiti, kopirati ni mijenjati bez pisanog dopuštenja.` **Nemoj dodavati datoteku `LICENSE`.**
3. Prvi commit:
   ```
   git add .gitignore README.md docs/
   git commit -m "Početak projekta: odluke, planovi, README"
   ```
4. Na GitHubu napravi javni repozitorij `vjecnaspomen` (bez README-a i licence, jer ih već imaš), pa:
   ```
   git remote add origin git@github.com:<tvoj-korisnik>/vjecnaspomen.git
   git push -u origin main
   ```
5. *Settings → Collaborators*: pozovi prijatelja.
6. *Settings → Branches → Add rule* za `main`: uključi „Require a pull request before merging” i „Require approvals: 1”. Kao vlasnik možeš iznimno spojiti i bez odobrenja ako prijatelj dugo nije dostupan, ali neka to ostane iznimka.
7. *Settings → Code security*: uključi **Secret scanning** i **Push protection**. GitHub će tada odbiti push u kojem prepozna ključ.
8. *Issues → Labels*: dodaj oznake `bug`, `dizajn`, `nalaz-testiranja`, `pitanje`, `petar`, `prijatelj`.
9. *Settings → General → Pull Requests*: ostavi samo „Allow squash merging” i uključi „Automatically delete head branches”.

**Gotovo kada:**
- repozitorij je javan, a prijatelj je prihvatio poziv;
- pokušaj `git push` izravno u `main` (nakon prvog) GitHub odbija;
- Secret scanning i Push protection su uključeni;
- u repozitoriju nema datoteke `LICENSE`, a README sadrži „Sva prava pridržana”.

**Procjena:** 1–2 sata.

> 🔁 **Predaja:** Petar daje prijatelju pristup repozitoriju (pozivnica za *collaboratora*). Time može krenuti **D-02**.

### P-03 Django projekt i postavke iz `.env`
- [x] Gotovo

**Cilj:** u repozitoriju postoji Django projekt `config` s aplikacijom `korisnici` i vlastitim modelom korisnika, a sve tajne i postavke ovisne o okruženju čitaju se iz `.env`.

**Zašto:** kostur na koji se nadograđuje sve ostalo. Postavke iz `.env` omogućuju da isti kod radi lokalno i na hostingu bez tajni u Gitu (odluke 17 i 20).

**Preduvjeti:** P-02 gotov.

**Novi pojmovi:**
- **Virtualno okruženje (*venv*)** je izolirana mapa s Pythonom i paketima samo za ovaj projekt. [Python: venv](https://docs.python.org/3/library/venv.html)
- **Django projekt i aplikacija:** projekt (`config`) su postavke i glavni URL-ovi. Aplikacija je cjelina s vlastitim modelima i pogledima (npr. `jezgra`, `mediji`). Jedan projekt ima više aplikacija. [Django: Applications](https://docs.djangoproject.com/en/6.1/ref/applications/), [Tutorial 1](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
- **Postavke (*settings*)** su datoteka `config/settings.py` s konfiguracijom: baza, instalirane aplikacije, jezik, sigurnost. [Django: Settings](https://docs.djangoproject.com/en/6.1/topics/settings/)
- **`.env`** je tekstualna datoteka s parovima `NAZIV=vrijednost` koje program čita pri pokretanju. Tajne tako ostaju izvan koda. Paket `django-environ` ih učitava. [django-environ](https://django-environ.readthedocs.io/)
- **Upravljačka naredba (*management command*)** je naredba oblika `python manage.py <naziv>` (`runserver`, `migrate`, `createsuperuser` ...). Kasnije pišemo i vlastite. [Django: django-admin and manage.py](https://docs.djangoproject.com/en/6.1/ref/django-admin/)
- **Vlastiti model korisnika:** Django preporučuje da ga napraviš na početku projekta, jer ga je kasnije vrlo teško uvesti. [Django: Custom user model](https://docs.djangoproject.com/en/6.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)

**Upute:**
1. Virtualno okruženje i paketi:
   ```
   python3 -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install django django-environ "psycopg[binary]"
   django-admin startproject config .
   python manage.py startapp korisnici
   pip freeze > requirements.txt
   ```
2. U `korisnici/models.py` napravi `class Korisnik(AbstractUser)` s jedinstvenim poljem `email` i (za sada praznim) poljem `partner`, koje dodaješ u P-06. U postavkama postavi `AUTH_USER_MODEL = "korisnici.Korisnik"`. **Ne pokreći `migrate` prije ovoga.**
3. Napravi `.env.example` (ide u Git) i `.env` (ne ide u Git):
   ```
   DEBUG=True
   SECRET_KEY=promijeni-me
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://vjecnaspomen:PROMIJENI_ME@localhost:5432/vjecnaspomen
   ```
   U `.env` stavi pravi `SECRET_KEY`, koji dobiješ naredbom `python -c "import secrets; print(secrets.token_urlsafe(50))"`.
4. Početak `config/settings.py`:
   ```python
   import environ
   from pathlib import Path

   BASE_DIR = Path(__file__).resolve().parent.parent
   env = environ.Env(DEBUG=(bool, False))
   environ.Env.read_env(BASE_DIR / ".env")

   SECRET_KEY = env("SECRET_KEY")
   DEBUG = env("DEBUG")
   ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
   DATABASES = {"default": env.db("DATABASE_URL")}

   LANGUAGE_CODE = "hr"
   TIME_ZONE = "Europe/Zagreb"
   USE_I18N = True
   USE_TZ = True
   ```
5. U `TEMPLATES` postavi `"DIRS": [BASE_DIR / "templates"]`, a u `STATICFILES_DIRS` stavi `[BASE_DIR / "static"]`. Napravi mape iz odjeljka „Struktura mapa”.
6. U README pod „Pokretanje” zapiši korake 1 i 3 za macOS i Windows.

**Gotovo kada:**
- `python manage.py check` ne javlja greške;
- `git status` ne prikazuje `.env`, a `.env.example` je u Gitu bez stvarnih vrijednosti;
- u `settings.py` nema nijedne tajne vrijednosti (provjeri pretragom riječi `SECRET_KEY`, `password`, `key`);
- `AUTH_USER_MODEL` pokazuje na `korisnici.Korisnik`.

**Procjena:** 2–3 sata.

**Česte greške:**
- Pokretanje `migrate` prije postavljanja `AUTH_USER_MODEL`. Ako se to dogodi, obriši bazu i migracije pa kreni ispočetka (u ovoj fazi još je jednostavno).
- Zaboravljeno aktiviranje venv-a: `pip install` tada instalira pakete u sistemski Python.

### P-04 PostgreSQL lokalno i prva migracija
- [x] Gotovo

**Cilj:** lokalno radi PostgreSQL baza, migracije su primijenjene, postoji administratorski račun i radi Django admin na `http://localhost:8000/admin/`.

**Zašto:** u produkciji koristimo PostgreSQL (odluka 17), a razvoj na istoj bazi sprječava iznenađenja pri objavi.

**Preduvjeti:** P-03 gotov.

**Novi pojmovi:**
- **PostgreSQL** je relacijska baza podataka: tablice s redovima i vezama među njima. [PostgreSQL dokumentacija](https://www.postgresql.org/docs/)
- **Model** je Python klasa koja opisuje jednu tablicu u bazi. Svako polje klase je stupac. [Django: Models](https://docs.djangoproject.com/en/6.1/topics/db/models/)
- **Migracija** je datoteka koja opisuje promjenu sheme baze (nova tablica, novo polje). `makemigrations` je stvara iz modela, a `migrate` je primjenjuje na bazu. Migracije idu u Git. [Django: Migrations](https://docs.djangoproject.com/en/6.1/topics/migrations/)
- **Django admin** je gotovo administratorsko sučelje koje Django gradi iz modela. [Django: Admin site](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)

**Upute:**
1. Instaliraj PostgreSQL (provjeri najnoviju stabilnu verziju):
   ```
   brew install postgresql@18
   brew services start postgresql@18
   ```
   Alternativa bez terminala je [Postgres.app](https://postgresapp.com/).
2. Napravi korisnika i bazu:
   ```
   createuser vjecnaspomen --pwprompt
   createdb vjecnaspomen --owner vjecnaspomen
   ```
   Lozinku upiši samo u `.env` (`DATABASE_URL`).
3. Migracije i administrator:
   ```
   python manage.py makemigrations korisnici
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
4. Registriraj `Korisnik` u `korisnici/admin.py` s `UserAdmin`.
5. Za prijatelja: `DATABASE_URL=sqlite:///db.sqlite3` u njegovom `.env` također radi, pa ne mora instalirati PostgreSQL. To zapiši u README. Produkcija i testovi u CI-ju ipak koriste PostgreSQL.

**Gotovo kada:**
- prijava u admin radi s računom iz `createsuperuser`;
- `python manage.py showmigrations` prikazuje sve migracije s `[X]`;
- lozinka baze nalazi se samo u `.env`.

**Procjena:** 1–2 sata.

**Česte greške:**
- `psql: command not found`: Homebrew verzije PostgreSQL-a nisu u PATH-u. Pokreni ono što `brew info postgresql@18` predloži.
- Zaboravljen `makemigrations` nakon promjene modela: `migrate` tada kaže „No migrations to apply”, a tablica ne postoji.

### P-05 Tailwind, HTMX, osnovni predložak i prijevodi
- [x] Gotovo

**Cilj:** postoji `templates/base.html` koji učitava CSS koji Tailwind generira i HTMX. Svi tekstovi idu kroz `{% translate %}`, a jedna probna stranica na `/` prikazuje se lokalno.

**Zašto:** prijatelj od ovog trenutka može lokalno pokrenuti projekt i raditi predloške (odluke 17 i 18a).

**Preduvjeti:** P-04 gotov.

**Novi pojmovi:**
- **Predložak (*template*)** je HTML datoteka s Django oznakama: `{{ varijabla }}` ispisuje vrijednost, a `{% oznaka %}` izvodi logiku (petlje, uvjeti, nasljeđivanje). [Django: Templates](https://docs.djangoproject.com/en/6.1/topics/templates/), [jezik predložaka](https://docs.djangoproject.com/en/6.1/ref/templates/language/)
- **Nasljeđivanje predložaka:** `base.html` definira okvir s blokovima (`{% block sadrzaj %}`), a ostali predlošci s `{% extends "base.html" %}` popunjavaju te blokove.
- **Statičke datoteke** su CSS, JavaScript, fontovi i slike koji su isti za sve korisnike. Učitavaju se oznakom `{% static %}`. [Django: Static files](https://docs.djangoproject.com/en/6.1/howto/static-files/)
- **Tailwind CSS** je CSS okvir u kojem stil pišeš malim klasama izravno u HTML (`text-xl font-semibold p-4`). Alat pregleda predloške i generira CSS samo s klasama koje stvarno koristiš. Paket `django-tailwind-cli` sam preuzima samostalni Tailwind program, pa Node.js nije potreban. [Tailwind CSS](https://tailwindcss.com/docs), [django-tailwind-cli](https://django-tailwind-cli.readthedocs.io/)
- **HTMX** je mala JavaScript biblioteka. Atributima u HTML-u (`hx-post`, `hx-target`, `hx-swap`) omogućuje da gumb pošalje zahtjev i zamijeni samo dio stranice, bez pisanja JavaScripta. Poslužitelj vraća gotov HTML. [htmx.org/docs](https://htmx.org/docs/), [django-htmx](https://django-htmx.readthedocs.io/)
- **Sustav prijevoda:** `{% translate "Tekst" %}` u predlošcima i `gettext("Tekst")` u Pythonu označavaju tekst koji se kasnije može prevesti. Zasad je sve na hrvatskom, ali poslije neće trebati prepravljati predloške. [Django: Translation](https://docs.djangoproject.com/en/6.1/topics/i18n/translation/)

**Upute:**
1. `pip install django-tailwind-cli django-htmx`, dodaj `django_tailwind_cli` i `django_htmx` u `INSTALLED_APPS`, a `django_htmx.middleware.HtmxMiddleware` u `MIDDLEWARE`. Postavi `TAILWIND_CLI_SRC_CSS = "tailwind/ulaz.css"` i `TAILWIND_CLI_DIST_CSS = "css/izlaz.css"`. Točne nazive postavki i fiksiranje verzije Tailwinda (`TAILWIND_CLI_VERSION`) provjeri u dokumentaciji paketa.
2. `tailwind/ulaz.css` (izvan `static/`, jer bi ga `collectstatic` inače pokušao objaviti i pukao na `@import`):
   ```css
   @import "tailwindcss";
   @source "../templates";

   @theme {
     /* boje i fontovi iz Figme dodaje prijatelj u D-14 */
   }
   ```
3. Preuzmi `htmx.min.js` (najnovija 2.x verzija) u `static/vendor/`. Ne koristi CDN: datoteka je tako uvijek dostupna i ne ovisimo o tuđem poslužitelju.
4. `templates/base.html`: `<html lang="hr">`, `{% load static i18n tailwind_cli %}`, `{% tailwind_css %}`, `<script src="{% static 'vendor/htmx.min.js' %}" defer>`, blokovi `naslov` i `sadrzaj` te na `<body>` atribut `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'`, kako bi svi HTMX zahtjevi prošli CSRF zaštitu.
5. U `<head>` dodaj `<meta name="viewport" content="width=device-width, initial-scale=1">`. Bez nje mobitel prikazuje umanjenu verziju stranice za računalo.
6. Napravi aplikaciju `jezgra`, u njoj pogled `pocetna` koji prikazuje `templates/javno/pocetna.html` s jednim naslovom kroz `{% translate %}`. Poveži ga u `config/urls.py` na `/`.
7. Pokreni razvoj:
   ```
   python manage.py tailwind runserver
   ```
   (Ili u dva terminala: `python manage.py tailwind watch` i `python manage.py runserver`.)
8. U README dopuni „Pokretanje” za macOS i Windows, uključujući SQLite opciju za prijatelja i probu na mobitelu u istoj Wi-Fi mreži: `python manage.py tailwind runserver 0.0.0.0:8000` (provjeri točan oblik naredbe u dokumentaciji paketa), IP adresa računala u `ALLOWED_HOSTS` i otvaranje `http://<IP>:8000` na mobitelu.
9. Napravi `docs/predlosci.md` s tablicom: predložak, pogled, URL, varijable. Svaki sljedeći korak koji dodaje predložak dopunjava ovu tablicu.

**Gotovo kada:**
- stranica `/` prikazuje naslov stiliziran Tailwind klasom (npr. `text-4xl`), a promjena klase u predlošku vidljiva je nakon osvježavanja;
- u alatima preglednika (*Network*) vidi se da se `htmx.min.js` učitava s `localhost`, a ne s CDN-a;
- `static/css/izlaz.css` nije u Gitu;
- prijatelj može prema README-u pokrenuti projekt (provjerava se u D-03).

**Procjena:** 3–4 sata.

**Česte greške:**
- Tailwind ne generira klasu jer ne vidi mapu `templates/`. Provjeri `@source` ili pokreni `python manage.py tailwind troubleshoot`.
- Klase sastavljene u predlošku od dijelova (`text-{{ velicina }}`) Tailwind ne prepoznaje. Klasa uvijek mora biti napisana cijela.

> 🔁 **Predaja:** Petar predaje prijatelju projekt koji se može pokrenuti (README s uputama za macOS i Windows), strukturu mapa `templates/` i `static/`, `base.html` i `docs/predlosci.md`. Time može krenuti **D-03**, a kasnije i **D-16**.

## Faza 2: Modeli podataka i administracija

Svi pojmovi iz rječnika postoje kao modeli, u adminu se stvaraju serije pločica s QR kodovima.

### P-06 Modeli Partner, Serija pločica i Pločica
- [ ] Gotovo

**Cilj:** u bazi postoje partneri s postotkom provizije, serije pločica i pločice sa slučajnim 6-znakovnim kodom, hashiranim aktivacijskim kodom i statusom neaktivirana/aktivirana.

**Zašto:** svaka pločica nosi podatak o partneru kojem je dodijeljena, pa se provizija obračunava automatski (odluke 8 i 15). Format koda određen je u odluci 18.

**Preduvjeti:** P-05 gotov.

**Novi pojmovi:**
- **Strani ključ (`ForeignKey`)** je veza „više prema jednom”: mnogo pločica pripada jednoj seriji. [Django: Relationships](https://docs.djangoproject.com/en/6.1/topics/db/models/#relationships)
- **Izbori (`choices`)** ograničavaju polje na zadane vrijednosti, npr. status pločice. [Django: Enumeration types](https://docs.djangoproject.com/en/6.1/ref/models/fields/#field-choices-enum-types)
- **Hash** je jednosmjerni otisak vrijednosti. Iz hasha se izvorni kod ne može vratiti, ali se može provjeriti je li upisani kod točan. Django ima gotove funkcije `make_password` i `check_password`. [Django: Password management](https://docs.djangoproject.com/en/6.1/topics/auth/passwords/)
- **`secrets`** je Pythonov modul za kriptografski siguran slučajni odabir. Modul `random` nije siguran za kodove. [Python: secrets](https://docs.python.org/3/library/secrets.html)

**Upute:**
1. Napravi aplikaciju `jezgra` (ako već nije) i u njoj modele:
   - `Partner`: `naziv`, `kontakt_ime`, `kontakt_email`, `kontakt_telefon`, `postotak_provizije` (`DecimalField`, 5 znamenki, 2 decimale, zadano 25.00), `aktivan`, `napomena`, `stvoreno`.
   - `SerijaPlocica`: `partner` (FK, `PROTECT`), `oznaka` (npr. „DEMO-01”), `broj_komada`, `maloprodajna_cijena` (`DecimalField`, zadano 119.00; vidi otvoreno pitanje OP-3), `napomena`, `stvoreno`.
   - `Plocica`: `serija` (FK, `PROTECT`), `kod` (`CharField(6, unique=True)`), `aktivacijski_kod_hash`, `status` (`neaktivirana` / `aktivirana`), `aktivirana_u` (`DateTimeField`, može biti prazno), `stvoreno`.
2. U `Korisnik` dodaj `partner = ForeignKey("jezgra.Partner", null=True, blank=True, on_delete=SET_NULL)` za korisnike koji gledaju pregled za partnera (P-38).
3. U `jezgra/kodovi.py` napiši generiranje kodova:
   ```python
   import secrets

   # Bez dvosmislenih znakova 0, O, 1, I, L (odluka 18): 31 znak.
   ABECEDA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

   def novi_kod(duljina: int) -> str:
       return "".join(secrets.choice(ABECEDA) for _ in range(duljina))

   def novi_kod_plocice() -> str:
       from jezgra.models import Plocica
       while True:
           kod = novi_kod(6)
           if not Plocica.objects.filter(kod=kod).exists():
               return kod
   ```
4. Svaki model dobije `__str__`, `verbose_name` kroz `gettext_lazy` i `Meta.ordering`.
5. `python manage.py makemigrations jezgra korisnici && python manage.py migrate`.
6. U Django shellu (`python manage.py shell`) ručno napravi partnera, seriju i jednu pločicu da provjeriš da sve radi.

**Gotovo kada:**
- u bazi postoje tri tablice s poljima iz koraka 1;
- `novi_kod(6)` u 1000 poziva nikad ne vraća znakove `0`, `O`, `1`, `I`, `L` (provjeri kratkom petljom u shellu, a kasnije testom u P-16);
- aktivacijski kod nigdje se ne sprema u čitljivom obliku, nego samo kao hash (`make_password`);
- brisanje partnera koji ima seriju nije dopušteno (`PROTECT`).

**Procjena:** 2–3 sata.

**Česte greške:**
- `random.choice` umjesto `secrets.choice`: kodovi su tada predvidljivi.
- `on_delete=CASCADE` na partneru ili seriji: brisanje jednog partnera obrisalo bi sve pločice i grobove.

### P-07 Modeli Grob, Pokojnik i Srodnik
- [ ] Gotovo

**Cilj:** u bazi postoje grob s tekstualnom oznakom grobnog mjesta i odvojenim poljima za vlasnika i kontakt za prijavu, pokojnici u grobu i srodnici s vrstom srodstva.

**Zašto:** jedan QR po grobu i više pokojnika u grobu (odluka 4), vlasnik i kontakt za prijavu kao odvojeni podaci (odluka 19), oznaka grobnog mjesta (odluka 11) i odjeljak „Obitelj” (odluka 3a).

**Preduvjeti:** P-06 gotov.

**Novi pojmovi:**
- **`OneToOneField`** je veza „jedan prema jednom”: jedna pločica pripada najviše jednom grobu i obrnuto. [Django: One-to-one](https://docs.djangoproject.com/en/6.1/topics/db/examples/one_to_one/)
- **`related_name`** je naziv kojim se s druge strane veze dolazi do povezanih objekata, npr. `grob.pokojnici.all()`.
- **Ograničenje u bazi (`CheckConstraint`)** je pravilo koje baza sama provodi, pa ga ni greška u kodu ne može zaobići. [Django: Constraints](https://docs.djangoproject.com/en/6.1/ref/models/constraints/)

**Upute:**
1. `Grob` (u aplikaciji `jezgra`):
   - `plocica` (`OneToOneField(Plocica, PROTECT, related_name="grob")`);
   - `partner` (FK, `PROTECT`; pri aktivaciji se kopira iz serije pločice, jer i grob „pripada partneru”, odluka 15);
   - `naziv` (npr. „Obitelj Horvat”, prikazuje se na zaključanom ekranu);
   - `oznaka_grobnog_mjesta` (npr. „Polje C, red 4, br. 12”; **nikad se ne prikazuje posjetiteljima**);
   - `vlasnik_ime` (osoba iz evidencije uprave);
   - `kontakt_za_prijavu` (FK na `Korisnik`, `PROTECT`; to je osoba koja se prijavljuje e-mailom);
   - `lozinka_hash`, `verzija_pristupa` (`PositiveIntegerField`, zadano 1; objašnjeno u P-12);
   - `javni_prikaz` (`BooleanField`, zadano `False`, odluka 5);
   - `stvoreno`, `promijenjeno`.
2. `Pokojnik`: `grob` (FK, `CASCADE`, `related_name="pokojnici"`), `ime`, `prezime`, `datum_rodjenja` i `datum_smrti` (oba mogu biti prazna), `biografija` (`TextField`), `profilna_slika` (FK na `mediji.Medij`, može biti prazna; dodaješ u P-08), `redoslijed`, `stvoreno`.
3. `Srodnik`: `pokojnik` (FK, `related_name="srodnici"`), `vrsta_srodstva` (izbori: suprug, supruga, otac, majka, sin, kći, brat, sestra, djed, baka, unuk, unuka, ostalo), `povezani_pokojnik` (FK na `Pokojnik`, može biti prazno), `ime_i_prezime` (za živuće osobe), `pristanak_na_prikaz` (`BooleanField`), `redoslijed`.
4. Dodaj `CheckConstraint`: srodnik ima **ili** `povezani_pokojnik` **ili** `ime_i_prezime`, ali ne oboje i ne nijedno.
5. Za živuće srodnike nema polja za datum rođenja, kontakt ni sliku. To je namjerno (odluka 3a, GDPR).
6. Migracije, pa ručna provjera u shellu: grob s dva pokojnika, jedan srodnik povezan na drugog pokojnika i jedan živući srodnik.

**Gotovo kada:**
- `grob.pokojnici.all()` vraća oba pokojnika;
- spremanje srodnika bez imena i bez povezanog pokojnika baca `IntegrityError`;
- model `Srodnik` nema nijedno polje za kontakt, datum rođenja ni sliku živuće osobe;
- polje `lozinka_hash` ne sadrži čitljivu lozinku (provjera u P-12).

**Procjena:** 2–3 sata.

### P-08 Modeli za pristup, medije, knjigu sjećanja i prijave
- [ ] Gotovo

**Cilj:** postoje svi preostali modeli MVP-a: obiteljski link, neuspjeli pokušaj, zahtjev za pristup, medij, poruka u knjizi sjećanja i prijava sadržaja.

**Zašto:** potpun model podataka prije pisanja logike sprječava kasnije velike preinake (odluke 3, 5, 12, 18 i 19).

**Preduvjeti:** P-07 gotov.

**Novi pojmovi:**
- **`FileField`** je polje koje u bazi čuva samo putanju datoteke, a samu datoteku sprema *storage* (lokalna mapa ili Cloudflare R2, vidi P-26). [Django: File storage](https://docs.djangoproject.com/en/6.1/topics/files/)
- **Indeks (`Meta.indexes`)** ubrzava pretraživanje po stupcu, npr. pokušaje po IP adresi i vremenu. [Django: Indexes](https://docs.djangoproject.com/en/6.1/ref/models/indexes/)

**Upute:**
1. Aplikacija `pristup`:
   - `ObiteljskiLink`: `grob` (FK), `token` (`CharField(64, unique=True)`, puni se s `secrets.token_urlsafe(32)`), `aktivan`, `stvoreno`, `ponisteno_u`.
   - `NeuspjeliPokusaj`: `vrsta` (`lozinka` / `aktivacija`), `cilj` (ID groba ili kod pločice, kao tekst), `ip`, `vrijeme`, s indeksom na (`vrsta`, `cilj`, `vrijeme`) i (`vrsta`, `ip`, `vrijeme`).
   - `ZahtjevZaPristup`: `grob` (FK), `ime`, `email`, `poruka`, `status` (`novi` / `odobren` / `odbijen`), `stvoreno`.
2. Aplikacija `mediji`, model `Medij`: `pokojnik` (FK), `vrsta` (`slika` / `video`), `status` (`ceka_upload` / `u_obradi` / `gotov` / `greska`), `kljuc_izvornika` (putanja izvorne datoteke u spremniku), `datoteka` (`FileField`, obrađena datoteka), `slicica` (`FileField`, mala slika za popis ili kadar za video), `velicina_bajtova`, `trajanje_sekundi` (samo za video), `sirina`, `visina`, `opis` (koristi se i kao alternativni tekst), `redoslijed`, `skriven` (za moderaciju), `poruka_greske`, `stvoreno`.
3. Aplikacija `knjiga`:
   - `PorukaSjecanja`: `pokojnik` (FK), `ime_autora`, `tekst` (najviše 2000 znakova), `status` (`na_cekanju` / `odobrena` / `odbijena`), `skrivena` (za naše uklanjanje nakon prijave), `stvoreno`, `odluceno_u`.
   - `PrijavaSadrzaja`: `pokojnik` (FK), `medij` i `poruka` (FK, oba mogu biti prazna), `razlog` (izbori: „uvredljiv sadržaj”, „netočan podatak”, „na slici sam ja i tražim uklanjanje”, „drugo”), `opis`, `email_prijavitelja`, `status` (`nova` / `u_obradi` / `rijesena`), `napomena_admina`, `stvoreno`, `rijeseno_u`, te svojstvo `rok_odgovora` = `stvoreno + 7 dana` (odluka 19).
4. U `Pokojnik` dodaj `profilna_slika` (FK na `Medij`, `SET_NULL`).
5. Ograničenja iz odluka 12 i 18 stavi u postavke, da se mijenjaju na jednom mjestu:
   ```python
   MEDIJI_MAX_SLIKA_PO_GROBU = 300
   MEDIJI_MAX_VIDEO_SEKUNDI_PO_GROBU = 20 * 60
   MEDIJI_MAX_BAJTOVA_PO_GROBU = 2 * 1024**3
   MEDIJI_MAX_VIDEO_SEKUNDI = 5 * 60
   MEDIJI_MAX_VIDEO_BAJTOVA = 1024**3
   MEDIJI_MAX_SLIKA_BAJTOVA = 30 * 1024**2   # tehnička odluka: dovoljno za HEIC/JPEG s mobitela
   MEDIJI_MAX_STRANICA_SLIKE_PX = 2048
   ```
6. Migracije.

**Gotovo kada:**
- sve migracije prolaze na praznoj bazi (`python manage.py migrate` nakon brisanja i ponovne izrade baze);
- token obiteljskog linka ima najmanje 32 bajta slučajnosti (`token_urlsafe(32)`);
- ograničenja medija postoje samo u postavkama, a ne kao brojevi razbacani po kodu.

**Procjena:** 3–4 sata.

### P-09 Django admin za sve modele i dijagram modela
- [ ] Gotovo

**Cilj:** svi modeli vidljivi su i pretraživi u Django adminu, a u `docs/modeli.md` postoji dijagram modela i njihovih veza.

**Zašto:** administracija je dio mjerila uspjeha 5 (odluka 20). Dijagram je dio README-a i studije slučaja za CV.

**Preduvjeti:** P-08 gotov.

**Novi pojmovi:**
- **`ModelAdmin`** je klasa koja određuje kako admin prikazuje model: stupce (`list_display`), filtre (`list_filter`), pretragu (`search_fields`) i polja samo za čitanje (`readonly_fields`). [Django: ModelAdmin options](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/#modeladmin-options)
- **Inline** prikazuje povezane objekte unutar roditelja, npr. pokojnike na stranici groba. [Django: InlineModelAdmin](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/#inlinemodeladmin-objects)
- **Mermaid** je tekstualni zapis dijagrama koji GitHub sam iscrtava u Markdownu. [GitHub: Mermaid](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)

**Upute:**
1. Za svaki model napravi `ModelAdmin` s razumnim `list_display`, `list_filter` i `search_fields`.
   - `Plocica`: `aktivacijski_kod_hash` je samo za čitanje i ne prikazuje se u popisu.
   - `Grob`: `lozinka_hash` se ne prikazuje uopće (polje isključi iz forme).
   - `Grob` ima inline `Pokojnik`, a `Pokojnik` ima inline `Srodnik` i `Medij` (samo za čitanje).
2. Naslov admina promijeni u „Vječna spomen – administracija” (`admin.site.site_header`).
3. Napravi `docs/modeli.md` s Mermaid dijagramom, npr. početak:
   ```
   erDiagram
     Partner ||--o{ SerijaPlocica : ima
     SerijaPlocica ||--o{ Plocica : sadrzi
     Plocica ||--o| Grob : "aktivacijom postaje"
     Partner ||--o{ Grob : prodao
     Korisnik ||--o{ Grob : "kontakt za prijavu"
     Grob ||--o{ Pokojnik : "ukopani su"
     Pokojnik ||--o{ Srodnik : ima
     Pokojnik ||--o{ Medij : ima
     Pokojnik ||--o{ PorukaSjecanja : prima
     Grob ||--o{ ObiteljskiLink : ima
     Grob ||--o{ ZahtjevZaPristup : prima
   ```
   Ispod dijagrama u nekoliko rečenica objasni ključne odluke: jedan QR po grobu, vlasnik i kontakt za prijavu odvojeni, partner na pločici i grobu.

**Gotovo kada:**
- u adminu se mogu pregledati i pretraživati svi modeli;
- nigdje u adminu ne vidi se hash lozinke groba;
- dijagram se ispravno prikazuje na GitHubu.

**Procjena:** 2–3 sata.

### P-10 Stvaranje serije pločica, kodovi i QR slike
- [ ] Gotovo

**Cilj:** u adminu se jednom akcijom stvara serija od N pločica, a administrator preuzima CSV s kodovima i aktivacijskim kodovima te ZIP s QR slikama (SVG i PNG) u kojima je link velikim slovima i korekcija razine H.

**Zašto:** pločice se izrađuju u serijama sa slučajnim kodovima i aktivacijskim kodom na papiru (odluka 8), a QR koristi velika slova i korekciju H (odluke 7 i 18). Za demo ispisujemo kodove na papir (odluka 20).

**Preduvjeti:** P-09 gotov.

**Novi pojmovi:**
- **Admin akcija** je funkcija koja se izvodi nad odabranim objektima iz popisa u adminu. [Django: Admin actions](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/actions/)
- **Prilagođeni admin pogled** je vlastita stranica unutar admina (`get_urls`), npr. forma „Nova serija”. [Django: ModelAdmin.get_urls](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls)
- **Korekcija pogrešaka razine H:** QR kod se može pročitati i kad je do oko 30 % površine oštećeno ili prljavo.
- **Alfanumerički način QR koda** kodira samo velika slova, brojke i nekoliko znakova (`$%*+-./:` i razmak), ali zauzima manje mjesta. Zato je link pisan velikim slovima.
- **`segno`** je Python biblioteka za izradu QR kodova (SVG, PNG). [segno](https://segno.readthedocs.io/)

**Upute:**
1. `pip install segno`. U `.env` dodaj `QR_BAZNI_URL=HTTP://192.168.1.20:8000/G/` (lokalno: IP adresa tvog Maca u kućnoj mreži, da mobitel u istoj Wi-Fi mreži može otvoriti kod; vidi `ipconfig getifaddr en0`), a na hostingu adresu demo poddomene, npr. `HTTPS://VJECNASPOMEN.ONRENDER.COM/G/`. Kad se registrira domena, postaje `HTTPS://VJECNASPOMEN.HR/G/`.
2. Prilagođeni admin pogled „Nova serija”: forma s poljima partner, oznaka, broj komada i maloprodajna cijena. Pri spremanju u jednoj transakciji (`transaction.atomic`) za svaku pločicu:
   - `kod = novi_kod_plocice()`;
   - `aktivacijski = novi_kod(8)`;
   - spremi `make_password(aktivacijski)`.
3. Odmah nakon spremanja odgovor je preuzimanje ZIP datoteke koja sadrži:
   - `kodovi.csv` (stupci `kod`, `aktivacijski_kod`, `link`);
   - za svaki kod `KOD.svg` i `KOD.png`.

   **Aktivacijski kodovi u čitljivom obliku postoje samo u toj datoteci.** Upozori to na stranici forme.
4. QR:
   ```python
   import segno
   from django.conf import settings

   def qr_za_kod(kod: str) -> segno.QRCode:
       link = f"{settings.QR_BAZNI_URL}{kod}".upper()
       return segno.make_qr(link, error="h", boost_error=False)

   # qr.save(buffer, kind="svg", scale=10, border=4)   # border 4 = obavezni bijeli rub
   ```
5. Admin akcija „Preuzmi QR slike” za postojeće pločice (bez aktivacijskih kodova, jer se oni ne mogu vratiti iz hasha).
6. Zapiši u `docs/modeli.md` koju QR verziju dobivaš (`qr.version`) za demo adresu i za `HTTPS://VJECNASPOMEN.HR/G/XXXXXX`. Za `.hr` adresu očekuje se verzija 3 (29 × 29 modula, odluka 18). Za dulju demo adresu verzija može biti veća, što je za demo prihvatljivo.

**Gotovo kada:**
- u adminu mogu stvoriti seriju od 5 pločica i svaka ima jedinstven 6-znakovni kod bez znakova 0, O, 1, I, L;
- preuzeti CSV ima 5 redaka s 8-znakovnim aktivacijskim kodovima, a u bazi su samo njihovi hashevi;
- QR slike skenirane mobitelom otvaraju link velikim slovima;
- `segno` za adresu `HTTPS://VJECNASPOMEN.HR/G/K7M4QX` s korekcijom H daje verziju 3;
- stvaranje serije od 50 pločica završava bez greške (može trajati nekoliko sekundi zbog hashiranja).

**Procjena:** 4–5 sati.

**Česte greške:**
- `boost_error=True` (zadano u segnu) samo podiže razinu korekcije. Ovdje je svejedno, ali `error="h"` mora biti izričito naveden.
- Mala slova u linku: QR tada prelazi u bajtni način i treba mu veća verzija.

> 🔁 **Predaja:** Petar predaje prijatelju primjer QR SVG datoteke i 6-znakovnog koda (iz `docs/modeli.md` ili ZIP-a demo serije). Time prijatelj u **D-31** može dizajnirati demo pločicu i letak u točnoj veličini.

## Faza 3: Prva radna verzija: QR → lozinka → profil

Skeniranje koda vodi na zaključani ekran, a točna lozinka na profil. Pristup je pokriven testovima.

### P-11 Ruta `/g/<kod>` i stranica groba
- [ ] Gotovo

**Cilj:** otvaranje `/g/K7M4QX` (ili `/G/K7M4QX`, `/g/k7m4qx`) za aktiviran grob vodi na stranicu groba s popisom pokojnika, ili odmah na profil ako je pokojnik samo jedan. Neaktivirana i nepostojeća pločica daju isti ekran „Unesi aktivacijski kod”.

**Zašto:** jedan QR po grobu i preskakanje popisa kad je pokojnik jedan (odluka 4). Rute ne razlikuju velika i mala slova (odluka 18). Neaktivirana pločica ne smije ništa otkriti (odluka 8).

**Preduvjeti:** P-08 gotov (P-09 i P-10 nisu nužni).

**Novi pojmovi:**
- **URL uzorak (*URLconf*)** povezuje adresu s pogledom. `path()` koristi jednostavne uzorke, a `re_path()` regularne izraze. [Django: URL dispatcher](https://docs.djangoproject.com/en/6.1/topics/http/urls/)
- **Pogled (*view*)** je Python funkcija koja prima zahtjev (`request`) i vraća odgovor, najčešće prikazan predložak (`render`) ili preusmjeravanje (`redirect`). [Django: Writing views](https://docs.djangoproject.com/en/6.1/topics/http/views/)
- **`get_object_or_404`** dohvaća objekt ili vraća stranicu „404 Nije pronađeno”. [Django: Shortcuts](https://docs.djangoproject.com/en/6.1/topics/http/shortcuts/)

**Upute:**
1. U aplikaciji `pristup` napravi `urls.py`:
   ```python
   from django.urls import path, re_path
   from . import views

   app_name = "pristup"
   urlpatterns = [
       re_path(r"^[gG]/(?P<kod>[A-Za-z0-9]{6})/?$", views.grob, name="grob"),
       re_path(r"^[gG]/(?P<kod>[A-Za-z0-9]{6})/(?P<pokojnik_id>\d+)/$",
               views.profil, name="profil"),
   ]
   ```
2. U pogledu `grob` kod najprije pretvori u velika slova (`kod.upper()`). Ako adresa nije bila točno `/g/<VELIKA>/`, preusmjeri na kanonsku adresu, da svi linkovi izgledaju isto.
3. Logika pogleda `grob`:
   - pločica ne postoji **ili** je neaktivirana → prikaži `aktivacija/unos_koda.html` (isti predložak i isti HTTP status 200 u oba slučaja, da se izvana ne može pogoditi koji kodovi postoje);
   - grob postoji → (pristup se provjerava od P-12) ako ima jednog pokojnika, preusmjeri na `profil`, inače prikaži `javno/grob.html` s popisom.
4. Pogled `profil` provjerava da `pokojnik.grob == grob`. U suprotnom vraća 404, jer se pokojnik iz tuđeg groba ne smije otvoriti mijenjanjem broja u adresi.
5. Ružni predlošci `javno/grob.html`, `javno/profil.html` i `aktivacija/unos_koda.html` s komentarom varijabli na vrhu.

**Gotovo kada:**
- `/g/k7m4qx/`, `/G/K7M4QX` i `/g/K7M4QX/` vode na istu kanonsku adresu;
- grob s jednim pokojnikom odmah otvara profil, a s dva prikazuje popis;
- odgovor za nepostojeći kod i za neaktiviranu pločicu je identičan (isti predložak, isti status, nema imena partnera ni serije);
- `/g/K7M4QX/<id pokojnika iz drugog groba>/` vraća 404.

**Procjena:** 2–3 sata.

**Česte greške:**
- Django uzorci razlikuju velika i mala slova, pa `path("g/<str:kod>/")` ne hvata `/G/...` iz QR koda. Zato `re_path` s `[gG]`.

### P-12 Zaključani ekran, lozinka groba i pamćenje uređaja
- [ ] Gotovo

**Cilj:** posjetitelj bez pristupa vidi zaključani ekran s nazivom groba i nazivom partnera. Nakon točne lozinke preglednik dobije potpisani kolačić na 12 mjeseci i više se ne pita lozinka. Grob s uključenim javnim prikazom otvara se bez lozinke.

**Zašto:** zadano je sve privatno, jedna lozinka po grobu i pamćenje uređaja oko 12 mjeseci (odluka 5). Ime partnera prikazuje se na zaključanom ekranu (odluka 15).

**Preduvjeti:** P-11 gotov.

**Novi pojmovi:**
- **Forma (*Form*)** je Django klasa koja opisuje polja, provjerava unos i prikazuje greške. [Django: Forms](https://docs.djangoproject.com/en/6.1/topics/forms/)
- **Kolačić (*cookie*)** je mali podatak koji preglednik čuva i šalje uz svaki zahtjev istoj stranici.
- **Potpisani kolačić** sadrži i kriptografski potpis napravljen s `SECRET_KEY`. Korisnik ga može pročitati, ali ga ne može promijeniti bez otkrivanja. [Django: get_signed_cookie](https://docs.djangoproject.com/en/6.1/ref/request-response/#django.http.HttpRequest.get_signed_cookie), [Cryptographic signing](https://docs.djangoproject.com/en/6.1/topics/signing/)
- **CSRF** je napad u kojem tuđa stranica natjera preglednik da pošalje formu našoj stranici. `{% csrf_token %}` u svakoj POST formi to sprječava. [Django: CSRF](https://docs.djangoproject.com/en/6.1/ref/csrf/)

**Upute:**
1. Na `Grob` dodaj metode `postavi_lozinku(lozinka)` (sprema `make_password`) i `provjeri_lozinku(lozinka)` (`check_password`).
2. Validator lozinke: najmanje 6 znakova (odluka 5). Koristi ga u aktivaciji (P-19) i pri promjeni lozinke (P-21).
3. U `pristup/kolacici.py`:
   ```python
   SALT = "pristup-grobu"
   GODINA = 365 * 24 * 3600

   def naziv(grob):
       return f"vs_g{grob.pk}"

   def dodijeli_pristup(response, grob, link=None):
       vrijednost = f"{grob.pk}:{grob.verzija_pristupa}:{link.pk if link else '-'}"
       response.set_signed_cookie(naziv(grob), vrijednost, salt=SALT, max_age=GODINA,
                                  httponly=True, secure=not settings.DEBUG, samesite="Lax")

   def ima_pristup(request, grob):
       if grob.javni_prikaz:
           return True
       v = request.get_signed_cookie(naziv(grob), default=None, salt=SALT, max_age=GODINA)
       if not v:
           return False
       grob_id, verzija, link_id = v.split(":")
       if int(grob_id) != grob.pk or int(verzija) != grob.verzija_pristupa:
           return False
       return link_id == "-" or grob.obiteljskilink_set.filter(pk=link_id, aktivan=True).exists()
   ```
   `verzija_pristupa` omogućuje da vlasnik jednim klikom odjavi sve uređaje (P-21). `link_id` omogućuje da poništavanje obiteljskog linka odjavi uređaje koji su ušli preko njega (P-23).
4. Pogledi `grob` i `profil`: ako `ima_pristup` vrati `False`, prikaži `javno/zakljucano.html` s varijablama `grob.naziv`, `partner.naziv`, `forma` i linkom „Zatraži pristup” (P-24). Na zaključanom ekranu nema imena pokojnika, datuma ni slika.
5. POST forme lozinke: kod točne lozinke postavi kolačić i preusmjeri na istu adresu (uzorak *Post/Redirect/Get*). Kod pogrešne lozinke prikaži općenitu poruku „Lozinka nije točna” (zaključavanje dolazi u P-13).
6. Ako je korisnik prijavljen kao kontakt za prijavu tog groba (P-17) ili je *superuser*, ima pristup bez lozinke.

**Gotovo kada:**
- bez kolačića profil se ne vidi, a HTML zaključanog ekrana ne sadrži imena pokojnika;
- nakon točne lozinke, zatvaranja i ponovnog otvaranja preglednika profil se otvara bez lozinke;
- ručna izmjena vrijednosti kolačića u alatima preglednika poništava pristup;
- kolačić ima oznake `HttpOnly` i `SameSite=Lax`, a u produkciji i `Secure`;
- lozinka kraća od 6 znakova ne može se postaviti;
- grob s `javni_prikaz=True` otvara se bez lozinke.

**Procjena:** 4–5 sati.

**Česte greške:**
- Spremanje lozinke u čitljivom obliku „samo privremeno”. Uvijek `make_password`.
- Prikaz različitih poruka za „grob ne postoji” i „lozinka nije točna”: to otkriva informacije napadaču.

### P-13 Zaključavanje nakon više pogrešnih pokušaja
- [ ] Gotovo

**Cilj:** nakon 5 pogrešnih lozinki za isti grob s iste IP adrese u 15 minuta daljnji pokušaji su blokirani 15 minuta. Nakon 30 pogrešnih pokušaja za isti grob u sat vremena (s bilo koje adrese) blokira se grob na sat vremena.

**Zašto:** sigurnosni zahtjev iz odluke 5. Lozinka od 6 znakova bez ograničenja pokušaja mogla bi se pogoditi.

**Preduvjeti:** P-12 gotov.

**Novi pojmovi:**
- **IP adresa** je adresa uređaja na internetu. Iza posrednika (*proxyja*), kakav ima Render, prava adresa posjetitelja nalazi se u zaglavlju `X-Forwarded-For`.
- **Upit s filtrima i brojanjem:** `Model.objects.filter(...).count()` vraća broj redaka u bazi koji zadovoljavaju uvjet. [Django: Making queries](https://docs.djangoproject.com/en/6.1/topics/db/queries/)

**Upute:**
1. U `pristup/ogranicenja.py` napiši funkcije `ip_posjetitelja(request)`, `je_zakljucano(vrsta, cilj, ip)` i `zabiljezi_neuspjeh(vrsta, cilj, ip)`. Brojeve stavi u postavke (`PRISTUP_MAX_POKUSAJA_IP = 5`, `PRISTUP_PROZOR_MIN = 15`, `PRISTUP_MAX_POKUSAJA_GROB = 30`).
2. Ista funkcija kasnije štiti i unos aktivacijskog koda (P-18), s vrstom `aktivacija`.
3. Kad je zaključano, ne provjeravaj lozinku uopće, nego prikaži poruku „Previše pokušaja. Pokušajte ponovno za 15 minuta.” (predložak `greske/zakljucano.html`).
4. Neuspjele pokušaje starije od 24 sata briše upravljačka naredba `ocisti_pokusaje`. Kasnije je pokreće pozadinski raspored (P-27).
5. IP adresu čitaj iz `X-Forwarded-For` **samo** ako je u postavkama uključeno `IZA_PROXYJA=True` (na hostingu). Lokalno koristi `REMOTE_ADDR`, jer bi inače svatko mogao poslati lažno zaglavlje.

**Gotovo kada:**
- šesti pogrešan pokušaj unutar 15 minuta prikazuje poruku o zaključavanju čak i ako je lozinka točna;
- nakon 15 minuta (u testu se vrijeme pomiče) prijava opet radi;
- uspješna prijava ne briše evidenciju neuspjeha drugih IP adresa;
- poruka o zaključavanju ne otkriva postoji li grob.

**Procjena:** 3–4 sata.

**Česte greške:**
- Na hostingu sve izgleda kao ista IP adresa (adresa proxyja), pa se zaključaju svi posjetitelji. Provjeri `IZA_PROXYJA`.

### P-14 Privremeni predlošci javnog dijela i popis varijabli
- [ ] Gotovo

**Cilj:** zaključani ekran, stranica groba i profil (biografija i odjeljak „Obitelj”) prikazuju sve podatke u jednostavnim, neuređenim predlošcima, a svaka varijabla zapisana je u `docs/predlosci.md`.

**Zašto:** prijatelj dobiva radni predložak s točnim podacima i može ga urediti prema Figmi, a ne mora čekati (odluke 3a i 6).

**Preduvjeti:** P-12 gotov.

**Novi pojmovi:**
- **Kontekst predloška** je rječnik varijabli koje pogled šalje predlošku (`render(request, "x.html", {"grob": grob})`).
- **`{% include %}`** umeće manji predložak (komponentu) u veći. [Django: include](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/#include)
- **Filtri predložaka** mijenjaju prikaz vrijednosti, npr. `{{ pokojnik.datum_smrti|date:"j. F Y." }}` ili `{{ biografija|linebreaks }}`. [Django: Built-in filters](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/#built-in-filter-reference)

**Upute:**
1. Profil prikazuje: ime i prezime, datume, profilnu sliku (zasad prazan okvir), biografiju (s `|linebreaks`), odjeljak „Obitelj” i prazne odjeljke za galeriju, video i knjigu sjećanja.
2. Odjeljak „Obitelj”:
   - srodnik s `povezani_pokojnik` je link na njegov profil;
   - živući srodnik prikazuje se **samo** ako je `pristanak_na_prikaz=True`, i to samo ime i vrsta srodstva.

   Filtriranje napravi u pogledu, a ne u predlošku, da prijatelj ne može slučajno prikazati osobu bez pristanka.
3. Na vrh svakog predloška stavi komentar s varijablama i njihovim tipovima.
4. U `docs/predlosci.md` dopuni tablicu i opiši stanja koja dizajn mora pokriti: grob s jednim ili više pokojnika, pokojnik bez biografije, bez srodnika, srodnik u drugom grobu.
5. Napravi jednostavnu upravljačku naredbu `napravi_probni_grob`. Ona stvara jedan grob s dva izmišljena pokojnika i lozinkom „demo123”, a ispisuje kod i lozinku. Prava demo naredba dolazi u P-40. Ova služi prijatelju za razvoj.

**Gotovo kada:**
- svi podaci iz modela `Pokojnik` i `Srodnik` koje posjetitelj smije vidjeti prikazani su na profilu;
- živući srodnik bez pristanka ne pojavljuje se u HTML-u (provjeri „View source”);
- `docs/predlosci.md` sadrži varijable za `javno/zakljucano.html`, `javno/grob.html` i `javno/profil.html`;
- prijatelj naredbom `python manage.py napravi_probni_grob` dobije grob koji može otvoriti.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Petar predaje prijatelju predloške `templates/javno/zakljucano.html`, `templates/javno/grob.html`, `templates/javno/profil.html` i `templates/aktivacija/unos_koda.html`, popis varijabli u `docs/predlosci.md` i naredbu `napravi_probni_grob`. Time mogu krenuti **D-17** i **D-18**.

### P-15 Zaštita od indeksiranja i sigurnosna zaglavlja
- [ ] Gotovo

**Cilj:** svi odgovori aplikacije imaju zaglavlje `X-Robots-Tag: noindex, nofollow`, svaki predložak ima `<meta name="robots" content="noindex, nofollow">`, postoji `/robots.txt`, a uključena su osnovna sigurnosna zaglavlja.

**Zašto:** profili se ne indeksiraju na tražilicama (odluka 5), čak ni kad je uključen javni prikaz.

**Preduvjeti:** P-11 gotov.

**Novi pojmovi:**
- **Međusloj (*middleware*)** je kod koji se izvodi za svaki zahtjev i odgovor, npr. za dodavanje zaglavlja. [Django: Middleware](https://docs.djangoproject.com/en/6.1/topics/http/middleware/)
- **`robots.txt`** je datoteka kojom stranica tražilicama kaže koje dijelove ne smiju pregledavati. [Google: robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- **`noindex`** traži od tražilice da stranicu ne prikazuje u rezultatima, čak i ako je pronađe preko linka. [Google: noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing)

**Upute:**
1. Međusloj u `jezgra/middleware.py`:
   ```python
   class NoIndexMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           response = self.get_response(request)
           response["X-Robots-Tag"] = "noindex, nofollow"
           return response
   ```
2. `robots.txt` kao jednostavan pogled:
   ```
   User-agent: *
   Disallow: /g/
   Disallow: /vlasnik/
   Disallow: /aktivacija/
   Disallow: /partner/
   ```
   Početna stranica smije se indeksirati, ali `X-Robots-Tag` na njoj možeš ostaviti dok tim ne odluči drugačije.
3. U `base.html` dodaj meta oznaku za robote i `<meta name="referrer" content="same-origin">`, da se adresa s tokenom obiteljskog linka ne šalje drugim stranicama.
4. U postavkama provjeri da su uključeni `SecurityMiddleware`, `XFrameOptionsMiddleware` (`X_FRAME_OPTIONS = "DENY"`) i `SECURE_CONTENT_TYPE_NOSNIFF = True`.

**Gotovo kada:**
- `curl -I http://localhost:8000/g/K7M4QX/` prikazuje `X-Robots-Tag: noindex, nofollow`;
- `/robots.txt` vraća gornji sadržaj;
- stranica se ne može ugraditi u `<iframe>` na drugoj stranici;
- obiteljski link (od P-23) ne pojavljuje se u zaglavlju `Referer` kad posjetitelj klikne vanjski link.

**Procjena:** 1–2 sata.

### P-16 Automatski testovi pristupa i GitHub Actions
- [ ] Gotovo

**Cilj:** postoje automatski testovi za kodove, lozinku, pamćenje uređaja i zaključavanje, a GitHub ih pokreće na svakom pull requestu.

**Zašto:** pristup je najosjetljiviji dio proizvoda (odluka 5). Testovi sprječavaju da se zaštita slučajno pokvari pri kasnijim promjenama.

**Preduvjeti:** P-13 gotov.

**Novi pojmovi:**
- **Automatski test** je kod koji provjerava drugi kod. Django ga pokreće naredbom `python manage.py test` na privremenoj praznoj bazi. [Django: Testing](https://docs.djangoproject.com/en/6.1/topics/testing/overview/)
- **Testni klijent** glumi preglednik: šalje GET i POST zahtjeve i čita odgovore. [Django: Test client](https://docs.djangoproject.com/en/6.1/topics/testing/tools/#the-test-client)
- **GitHub Actions** je GitHubov servis koji na svaki push ili PR pokreće zadane naredbe na čistom poslužitelju (CI, *continuous integration*). [GitHub Actions](https://docs.github.com/en/actions)

**Upute:**
1. U `pristup/tests.py` napiši testove barem za:
   - kod pločice ne sadrži `0OI1L` i ima 6 znakova;
   - profil bez kolačića prikazuje zaključani ekran i ne sadrži ime pokojnika;
   - točna lozinka postavlja kolačić, a zatim profil sadrži ime pokojnika;
   - izmijenjen kolačić ne daje pristup;
   - pokojnik iz drugog groba vraća 404;
   - šesti pogrešan pokušaj je blokiran;
   - nepostojeći i neaktivirani kod daju isti odgovor.
2. Za brže testove u testnim postavkama koristi brzi hasher:
   ```python
   PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]  # SAMO u testovima
   ```
3. `.github/workflows/testovi.yml`:
   ```yaml
   name: testovi
   on: [pull_request, push]
   jobs:
     test:
       runs-on: ubuntu-latest
       services:
         postgres:
           image: postgres:18
           env: { POSTGRES_USER: test, POSTGRES_PASSWORD: test, POSTGRES_DB: test }
           ports: ["5432:5432"]
           options: --health-cmd pg_isready --health-interval 5s --health-retries 10
       env:
         SECRET_KEY: samo-za-ci
         DATABASE_URL: postgres://test:test@localhost:5432/test
         ALLOWED_HOSTS: localhost
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with: { python-version: "3.13" }
         - run: pip install -r requirements.txt
         - run: sudo apt-get install -y ffmpeg
         - run: python manage.py test
   ```
   Lozinka `test` ovdje nije tajna: baza postoji samo dok traje testiranje. Verzije akcija (`@v4`, `@v5`) provjeri na GitHubu.
4. U zaštiti grane `main` uključi „Require status checks to pass” i odaberi `test`.

**Gotovo kada:**
- `python manage.py test` lokalno prolazi;
- PR s namjerno pokvarenim testom GitHub označi crveno i ne dopušta spajanje;
- testovi pokrivaju svih 7 slučajeva iz koraka 1.

**Procjena:** 4–5 sati.

**Česte greške:**
- Test ovisi o redoslijedu ili o podacima iz lokalne baze. Svaki test sam stvara svoje podatke (`setUpTestData`).

## Faza 4: Aktivacija i vlasnički dio

Obitelj aktivira pločicu čarobnjakom, prijavljuje se e-mailom i upravlja grobom.

### P-17 Prijava vlasnika linkom na e-mail
- [ ] Gotovo

**Cilj:** kontakt za prijavu upiše e-mail na `/vlasnik/prijava/` i dobije jednokratni link koji vrijedi 15 minuta. Klikom na link prijavljen je u vlasnički dio.

**Zašto:** prijava bez lozinke, linkom poslanim e-mailom (odluka 3), uz paket `django-sesame` (odluka 17). Link stiže na kontakt za prijavu, a ne nužno vlasniku (odluka 19).

**Preduvjeti:** P-07 gotov.

**Novi pojmovi:**
- **Autentikacija** je provjera tko je korisnik, a **autorizacija** provjera smije li nešto napraviti. [Django: User authentication](https://docs.djangoproject.com/en/6.1/topics/auth/default/)
- **Sesija** je podatak na poslužitelju vezan uz preglednik preko kolačića. U sesiji Django pamti da je korisnik prijavljen. [Django: Sessions](https://docs.djangoproject.com/en/6.1/topics/http/sessions/)
- **`django-sesame`** stvara potpisane tokene za prijavu bez lozinke. [django-sesame](https://django-sesame.readthedocs.io/)
- **Slanje e-maila u Djangu:** lokalno `EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"` ispisuje poruku u terminal, a na hostingu se šalje preko SMTP poslužitelja. [Django: Sending email](https://docs.djangoproject.com/en/6.1/topics/email/)
- **`login_required`** je dekorator koji neprijavljenog korisnika preusmjerava na prijavu. [Django: login_required](https://docs.djangoproject.com/en/6.1/topics/auth/default/#the-login-required-decorator)

**Upute:**
1. `pip install django-sesame`. U `AUTHENTICATION_BACKENDS` dodaj `sesame.backends.ModelBackend` uz zadani backend. Postavke:
   ```python
   SESAME_MAX_AGE = 15 * 60
   SESAME_ONE_TIME = True
   LOGIN_URL = "vlasnik:prijava"
   EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
   DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Vječna spomen <noreply@localhost>")
   ```
2. Aplikacija `vlasnik`, pogled `prijava`: forma s e-mailom. Ako korisnik s tim e-mailom postoji, pošalji mu link iz predloška `emailovi/prijava.txt`. **U svakom slučaju** prikaži istu poruku: „Ako je adresa upisana u sustavu, poslali smo vam link za prijavu.”
3. Pogled `potvrda` prima token (`sesame.utils.get_user`), prijavljuje korisnika (`login`) i preusmjerava na `/vlasnik/`.
4. Ograniči slanje: najviše 3 linka za isti e-mail u 15 minuta (iskoristi `NeuspjeliPokusaj` ili sličnu evidenciju).
5. Odjava je POST forma s gumbom „Odjava” (ne GET link).
6. Rok trajanja prijave (sesije) postavi na 30 dana (`SESSION_COOKIE_AGE`), da se vlasnik ne mora stalno prijavljivati.

**Gotovo kada:**
- link iz terminala prijavljuje korisnika, a drugi klik na isti link više ne radi;
- link stariji od 15 minuta ne radi (test s pomakom vremena);
- odgovor za postojeći i nepostojeći e-mail je identičan;
- četvrti zahtjev za isti e-mail unutar 15 minuta ne šalje e-mail.

**Procjena:** 3–4 sata.

**Česte greške:**
- Programi za e-poštu ponekad „otvore” link radi provjere i tako potroše jednokratni token. Ako se to dogodi u testiranju, potvrdna stranica neka traži klik na gumb „Prijavi me” (POST) umjesto prijave već pri samom otvaranju linka.

### P-18 Čarobnjak za aktivaciju, korak 1: aktivacijski kod
- [ ] Gotovo

**Cilj:** na ekranu neaktivirane pločice posjetitelj upiše 8-znakovni aktivacijski kod. Ako je točan, ulazi u čarobnjak. Pokušaji su ograničeni.

**Zašto:** bez aktivacijskog koda pločica se ne može aktivirati (odluka 8).

**Preduvjeti:** P-11 i P-13 gotovi.

**Novi pojmovi:**
- **Čarobnjak (*wizard*)** je niz ekrana kroz koje korisnik prolazi korak po korak. Stanje između koraka čuvamo u sesiji.

**Upute:**
1. Forma na `aktivacija/unos_koda.html` šalje POST na `/aktivacija/<kod>/`.
2. Normaliziraj unos: velika slova, ukloni razmake i crtice (ljudi prepisuju „K7M4 QX2P”).
3. Prije provjere pozovi `je_zakljucano("aktivacija", kod_plocice, ip)`. Ograničenja: 5 neuspjeha po IP adresi na sat i 10 neuspjeha po pločici na dan.
4. Ako pločica ne postoji ili je već aktivirana, ponašaj se kao kod pogrešnog koda (ista poruka i isto bilježenje neuspjeha).
5. Kod točnog koda u sesiju spremi `{"aktivacija_plocica_id": ..., "aktivacija_vrijeme": ...}` i preusmjeri na korak 2. Stanje sesije vrijedi najviše 60 minuta.

**Gotovo kada:**
- točan kod (iz CSV-a iz P-10) vodi na korak 2;
- pogrešan kod, kod za drugu pločicu i kod za već aktiviranu pločicu daju istu poruku;
- šesti pogrešan pokušaj s iste IP adrese unutar sat vremena je blokiran;
- direktan odlazak na korak 2 bez prolaska koraka 1 vraća na korak 1.

**Procjena:** 2–3 sata.

### P-19 Čarobnjak, korak 2: podaci groba, lozinka i kontakt za prijavu
- [ ] Gotovo

**Cilj:** obitelj upiše naziv groba, oznaku grobnog mjesta, ime vlasnika, e-mail osobe koja će voditi profil i lozinku groba. Pločica se u jednoj transakciji aktivira i postaje QR oznaka novog groba.

**Zašto:** aktivacija je trenutak kad neaktivirana pločica postaje QR oznaka groba (rječnik, odluka 8). Oznaka grobnog mjesta (odluka 11), vlasnik i kontakt za prijavu (odluka 19) i lozinka (odluka 5) upisuju se upravo tada.

**Preduvjeti:** P-17 i P-18 gotovi.

**Novi pojmovi:**
- **Transakcija** je skupina promjena u bazi koje se izvrše sve ili nijedna. [Django: Database transactions](https://docs.djangoproject.com/en/6.1/topics/db/transactions/)
- **`select_for_update`** zaključava redak u bazi do kraja transakcije, pa dvije osobe ne mogu istovremeno aktivirati istu pločicu. [Django: select_for_update](https://docs.djangoproject.com/en/6.1/ref/models/querysets/#select-for-update)

**Upute:**
1. Forma s poljima i objašnjenjima za korisnika:
   - naziv groba („npr. Obitelj Horvat”, prikazuje se posjetiteljima);
   - oznaka grobnog mjesta („prepišite s računa uprave groblja, npr. Polje C, red 4, br. 12”, ne prikazuje se posjetiteljima);
   - ime i prezime vlasnika („osoba na koju glasi grobno mjesto”);
   - „E-mail osobe koja će voditi profil” (točan tekst iz odluke 19);
   - lozinka groba i ponovljena lozinka (najmanje 6 znakova).
2. Spremanje:
   ```python
   with transaction.atomic():
       plocica = Plocica.objects.select_for_update().get(pk=plocica_id)
       if plocica.status != Plocica.Status.NEAKTIVIRANA:
           raise VecAktivirana
       korisnik, _ = Korisnik.objects.get_or_create(
           email=email, defaults={"username": email})
       grob = Grob(plocica=plocica, partner=plocica.serija.partner,
                   kontakt_za_prijavu=korisnik, **podaci)
       grob.postavi_lozinku(lozinka)
       grob.save()
       plocica.status = Plocica.Status.AKTIVIRANA
       plocica.aktivirana_u = timezone.now()
       plocica.save()
   ```
3. Nakon spremanja prijavi korisnika (`login`), obriši podatke čarobnjaka iz sesije, pošalji e-mail dobrodošlice s linkom za prijavu (`emailovi/aktivacija.txt`) i preusmjeri na korak 3. Odluka o tome je li potrebna prethodna potvrda e-maila je u OP-5.
4. Ako korisnik s tim e-mailom već postoji (ista osoba vodi dva groba), grob se dodaje njemu.

**Gotovo kada:**
- nakon koraka 2 pločica je u adminu `aktivirana`, ima datum aktivacije, a grob ima partnera iz serije;
- ponovni ulazak s istim aktivacijskim kodom više ne radi;
- dva istovremena zahtjeva za istu pločicu (test s dvije niti ili ručno s dva preglednika) stvaraju samo jedan grob;
- lozinka groba u bazi postoji samo kao hash;
- e-mail dobrodošlice vidljiv je u terminalu.

**Procjena:** 4–5 sati.

### P-20 Čarobnjak, korak 3: prvi pokojnik i poziv na dodavanje slika
- [ ] Gotovo

**Cilj:** nakon aktivacije vlasnik upiše prvog pokojnika (ime, prezime, datumi, kratka biografija) i dođe na ekran „Dodajte slike” s gumbom za upload (P-28) i gumbom „Preskoči, dodat ću kasnije”.

**Zašto:** redoslijed čarobnjaka iz odluke 8: aktivacijski kod → lozinka groba → prvi pokojnik → slike.

**Preduvjeti:** P-19 gotov.

**Novi pojmovi:**
- **`ModelForm`** je forma napravljena izravno iz modela, s istim poljima i provjerama. [Django: ModelForm](https://docs.djangoproject.com/en/6.1/topics/forms/modelforms/)

**Upute:**
1. `PokojnikForm(ModelForm)` s poljima `ime`, `prezime`, `datum_rodjenja`, `datum_smrti`, `biografija`. Za datume koristi `<input type="date">`, koji mobitel prikazuje kao kalendar.
2. Pogled je zaštićen: korisnik mora biti prijavljen i biti kontakt za prijavu tog groba.
3. Na vrhu svakog koraka prikaži „Korak X od 4”. U kontekst pošalji `korak` i `ukupno_koraka`, da ga prijatelj može dizajnirati.
4. Ružni predlošci `aktivacija/korak_kod.html`, `aktivacija/korak_grob.html`, `aktivacija/korak_pokojnik.html`, `aktivacija/korak_slike.html` i `aktivacija/gotovo.html`, s varijablama zapisanima u `docs/predlosci.md`.

**Gotovo kada:**
- cijeli čarobnjak od skeniranja neaktivirane pločice do ekrana „Gotovo” prolazi na mobitelu;
- na kraju je pokojnik vidljiv na stranici groba (`/g/<kod>/`);
- korisnik koji nije kontakt za prijavu tog groba ne može otvoriti korak 3 (404).

**Procjena:** 2–3 sata.

> 🔁 **Predaja:** Petar predaje prijatelju predloške `templates/aktivacija/*.html` s popisom varijabli u `docs/predlosci.md` (uključujući `korak`, `ukupno_koraka` i greške forme) i CSV s demo aktivacijskim kodovima za lokalno testiranje. Time može krenuti **D-25**.

### P-21 Vlasnički dio: popis grobova i postavke groba
- [ ] Gotovo

**Cilj:** prijavljeni kontakt za prijavu na `/vlasnik/` vidi svoje grobove. Za svaki grob može promijeniti naziv i lozinku, uključiti ili isključiti javni prikaz i odjaviti sve uređaje.

**Zašto:** vlasnik postavlja i mijenja lozinku i odlučuje o javnom prikazu (odluka 5).

**Preduvjeti:** P-19 gotov.

**Novi pojmovi:**
- **Vlastiti dekorator** je funkcija koja omata pogled i prije njega izvodi provjeru, npr. „je li ovo tvoj grob”. [Python: decorators](https://docs.python.org/3/glossary.html#term-decorator)
- **Poruke (*messages*)** su kratke obavijesti nakon radnje („Lozinka je promijenjena.”). [Django: Messages framework](https://docs.djangoproject.com/en/6.1/ref/contrib/messages/)

**Upute:**
1. Dekorator koji vraća grob ili 404:
   ```python
   def vlasnik_groba(view):
       @login_required
       @wraps(view)
       def omot(request, kod, *args, **kwargs):
           grob = get_object_or_404(Grob, plocica__kod=kod.upper())
           if not (request.user.is_superuser or grob.kontakt_za_prijavu_id == request.user.id):
               raise Http404
           return view(request, grob, *args, **kwargs)
       return omot
   ```
   Vraćamo 404, a ne 403, da se ne otkriva postoji li grob.
2. Stranice: `/vlasnik/` (popis grobova s brojem poruka i zahtjeva na čekanju) i `/vlasnik/<kod>/postavke/`.
3. Promjena lozinke traži novu lozinku dvaput i ima kvačicu „Odjavi sve uređaje koji su upisali staru lozinku”. Ako je kvačica označena, `verzija_pristupa += 1`.
4. Uključivanje javnog prikaza traži potvrdu („Sadržaj će vidjeti svatko tko ima link ili skenira kod. Tražilice ga i dalje neće prikazivati.”).
5. `oznaka_grobnog_mjesta` i `vlasnik_ime` vlasnik vidi, ali ih ne mijenja sam. Promjena ide preko nas, uz potvrdu (odluka 19).
6. Na `/vlasnik/` dodaj HTMX primjer: prekidač javnog prikaza šalje `hx-post` i vraća samo novi dio stranice.

**Gotovo kada:**
- korisnik A ne može otvoriti postavke groba korisnika B (404) ni POST-om promijeniti njegovu lozinku;
- nakon promjene lozinke s označenom kvačicom uređaj koji je imao pristup ponovno vidi zaključani ekran;
- bez kvačice uređaji ostaju prijavljeni;
- nova lozinka kraća od 6 znakova se odbija.

**Procjena:** 3–4 sata.

### P-22 Vlasnički dio: pokojnici i srodnici
- [ ] Gotovo

**Cilj:** vlasnik dodaje, uređuje i briše pokojnike u svom grobu, određuje redoslijed i upravlja srodnicima (povezani pokojnik ili živuća osoba s pristankom).

**Zašto:** više pokojnika u jednom grobu (odluka 4) i odjeljak „Obitelj” (odluka 3a).

**Preduvjeti:** P-21 gotov.

**Novi pojmovi:**
- **Djelomični predložak (*partial*)** je mali predložak koji HTMX dohvaća i umeće u stranicu, npr. jedan redak srodnika. Isti predložak koristi se pri punom prikazu stranice i pri HTMX odgovoru. [django-htmx: tips](https://django-htmx.readthedocs.io/en/latest/tips.html)

**Upute:**
1. Stranice `/vlasnik/<kod>/pokojnik/novi/`, `/vlasnik/<kod>/pokojnik/<id>/` (uređivanje) i brisanje uz potvrdu („Upišite ime pokojnika za potvrdu brisanja”).
2. Brisanje pokojnika briše i njegove medije iz spremnika (od P-31). Do tada samo zapis u bazi.
3. Srodnici se dodaju HTMX formom na stranici pokojnika:
   - padajući izbornik vrste srodstva;
   - izbor „Pokojnik u ovom grobu” ili „Živuća osoba”;
   - za živuću osobu samo ime i obavezna kvačica „Osoba je pristala da se njezino ime prikaže na profilu” (vidi OP-6).
4. Povezivanje na pokojnika u **drugom** grobu vlasnik radi upisom koda tog groba. Ponude se samo grobovi kojima je on kontakt za prijavu. Za ostale grobove to zasad radimo mi u adminu.
5. Redoslijed pokojnika i srodnika: gumbi „Gore” i „Dolje” (HTMX). Povlačenje mišem nije potrebno.
6. Dodavanje pokojnika u postojeći grob je u MVP-u slobodno, a izvještaj ga broji (P-37, OP-2).

**Gotovo kada:**
- vlasnik može dodati drugog pokojnika i grob tada prikazuje popis umjesto izravnog profila;
- živući srodnik ne može se spremiti bez kvačice pristanka;
- korisnik ne može uređivati pokojnika ni srodnika tuđeg groba ni promjenom ID-a u adresi ni POST zahtjevom;
- HTMX dodavanje srodnika radi bez ponovnog učitavanja cijele stranice.

**Procjena:** 4–6 sati.

### P-23 Obiteljski link i njegovo poništavanje
- [ ] Gotovo

**Cilj:** vlasnik u postavkama groba vidi obiteljski link (`/g/<kod>/o/<token>/`) koji može kopirati ili podijeliti. Tko ga otvori, dobiva pristup bez lozinke. Gumb „Poništi link i napravi novi” odmah oduzima pristup svima koji su ušli preko starog linka.

**Zašto:** obiteljski link za rođake na daljinu, koji vlasnik može poništiti (odluka 5, uočeno u odluci 2).

**Preduvjeti:** P-12 i P-21 gotovi.

**Novi pojmovi:**
- **Web Share API** otvara izbornik dijeljenja na mobitelu (WhatsApp, Viber, SMS) iz preglednika. Ako ga preglednik ne podržava, dovoljan je gumb „Kopiraj”. [MDN: navigator.share](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share)

**Upute:**
1. Grob ima najviše jedan aktivan `ObiteljskiLink`. Prvi se stvara pri prvom otvaranju postavki.
2. Pogled `/g/<kod>/o/<token>/`:
   - ako je token aktivan i pripada tom grobu, `dodijeli_pristup(response, grob, link=link)` i preusmjeri na `/g/<kod>/` (token tako nestaje iz adresne trake);
   - inače prikaži zaključani ekran s porukom „Ovaj link više ne vrijedi. Upišite lozinku ili zatražite pristup.”
3. Usporedbu tokena radi pretragom po jedinstvenom polju u bazi (`filter(token=...)`), a ne petljom po svim linkovima.
4. Poništavanje: stari `aktivan=False`, `ponisteno_u=now()` i odmah novi link. `ima_pristup` (P-12) već provjerava da je link aktivan.
5. Na stranici objasni: „Svatko tko ima ovaj link vidi profile bez lozinke. Šaljite ga samo obitelji.”

**Gotovo kada:**
- otvaranje obiteljskog linka u novom pregledniku daje pristup bez lozinke;
- nakon poništavanja isti preglednik ponovno vidi zaključani ekran, a stari link ne radi;
- novi link radi;
- token ima najmanje 43 znaka (`token_urlsafe(32)`) i ne ostaje u adresnoj traci nakon ulaska.

**Procjena:** 2–3 sata.

### P-24 Zahtjev za pristup
- [ ] Gotovo

**Cilj:** posjetitelj na zaključanom ekranu klikne „Zatraži pristup”, upiše ime, e-mail i poruku, a vlasnik dobiva e-mail i u vlasničkom dijelu vidi zahtjev s gumbima „Pošalji obiteljski link” i „Odbij”.

**Zašto:** gumb „Zatraži pristup” šalje zahtjev vlasniku (odluka 5). Što se događa nakon toga nije zapisano, pa je prijedlog u OP-1.

**Preduvjeti:** P-23 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Forma na `/g/<kod>/zahtjev/` (HTMX: forma se zamijeni porukom „Zahtjev je poslan. Vlasnik će vam se javiti.”).
2. Ograničenje: najviše 3 zahtjeva s iste IP adrese za isti grob na dan i najviše 20 zahtjeva po grobu na dan. Polje „mamac” (*honeypot*) skriveno CSS-om odbija jednostavne botove.
3. E-mail kontaktu za prijavu (`emailovi/zahtjev_za_pristup.txt`) sadrži ime i poruku posjetitelja te link na vlasnički dio. E-mail posjetitelja u njemu se ne navodi, nego se vidi tek u vlasničkom dijelu.
4. `/vlasnik/<kod>/zahtjevi/`: popis zahtjeva. „Pošalji obiteljski link” šalje posjetitelju e-mail s trenutačnim obiteljskim linkom i označava zahtjev `odobren`. „Odbij” samo mijenja status, a posjetitelj ne dobiva obavijest.

**Gotovo kada:**
- zahtjev s mobitela stiže kao e-mail kontaktu za prijavu (u terminalu);
- odobrenje šalje posjetitelju obiteljski link koji radi;
- četvrti zahtjev s iste IP adrese istog dana se odbija;
- zahtjeve groba vidi samo njegov kontakt za prijavu.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Petar predaje prijatelju predloške vlasničkog dijela iz koraka P-21 do P-24: `templates/vlasnik/prijava.html`, `templates/vlasnik/popis.html`, `templates/vlasnik/postavke.html` (uključujući obiteljski link), `templates/vlasnik/zahtjevi.html`, `templates/javno/zahtjev.html`, te iz P-22 `templates/vlasnik/pokojnik.html` i `templates/vlasnik/_srodnik_redak.html`, sve s varijablama u `docs/predlosci.md`. Time mogu krenuti **D-26** i (dio za pokojnike i srodnike) **D-27**.

### P-25 Testovi aktivacije i dozvola
- [ ] Gotovo

**Cilj:** automatski testovi pokrivaju cijeli čarobnjak, prijavu linkom, obiteljski link i to da nitko ne može dirati tuđi grob.

**Zašto:** aktivacija i dozvole su kritični dijelovi (mjerilo uspjeha 2, odluke 5, 8 i 19).

**Preduvjeti:** P-24 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Testovi barem za:
   - aktivacija od koda do prvog pokojnika;
   - pogrešan aktivacijski kod i zaključavanje;
   - nemogućnost ponovne aktivacije;
   - grob dobiva partnera iz serije;
   - prijava linkom (jednokratnost, istek);
   - isti odgovor za nepostojeći e-mail;
   - promjena lozinke s odjavom uređaja i bez nje;
   - obiteljski link prije i poslije poništavanja;
   - zahtjev za pristup i odobrenje.
2. Napiši jedan test koji prolazi kroz **sve** URL-ove vlasničkog dijela kao drugi prijavljeni korisnik i očekuje 404 na svakome. Popis URL-ova drži u testu, a kad dodaš novi URL, dodaj ga i tamo.
3. E-mailove u testovima provjeravaj kroz `django.core.mail.outbox`. [Django: Email services in tests](https://docs.djangoproject.com/en/6.1/topics/testing/tools/#email-services)

**Gotovo kada:**
- svi testovi prolaze lokalno i u GitHub Actions;
- test dozvola pokriva svaki URL pod `/vlasnik/<kod>/`;
- nijedan test ne šalje stvarni e-mail.

**Procjena:** 3–5 sati.

## Faza 5: Mediji

Upload slika i videa s mobitela izravno u R2, pozadinska obrada i prikaz kroz potpisane linkove.

### P-26 Cloudflare R2 i privremeni potpisani linkovi
- [ ] Gotovo

**Cilj:** datoteke se spremaju u privatni Cloudflare R2 spremnik (*bucket*), a aplikacija ih prikazuje isključivo kroz privremene potpisane linkove koji vrijede sat vremena.

**Zašto:** mediji su dostupni samo preko privremenih potpisanih linkova, nikad preko javnog URL-a (odluka 5). Pohrana je Cloudflare R2 preko `django-storages` (odluka 17), a podaci su na EU poslužiteljima (odluka 19).

**Preduvjeti:** P-08 gotov.

**Novi pojmovi:**
- **Pohrana objekata (*object storage*)**: datoteke („objekti”) spremaju se pod ključem (npr. `grobovi/12/slike/abc.webp`) u spremnik, a ne na disk poslužitelja. **Cloudflare R2** je takva usluga, kompatibilna s Amazonovim S3 sučeljem i bez naplate prijenosa podataka. [Cloudflare R2](https://developers.cloudflare.com/r2/)
- **Potpisani link (*presigned URL*)** je adresa datoteke s ugrađenim potpisom i rokom trajanja. Nakon isteka više ne radi, pa ga nema smisla dijeliti. [R2: Presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/)
- **`django-storages`** je paket koji Djangu omogućuje spremanje datoteka u S3/R2. **`boto3`** je Amazonova Python biblioteka za S3 sučelje. [django-storages: S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
- **Storage u Djangu** je sloj koji odlučuje gdje `FileField` sprema datoteke. Lokalno može biti mapa na disku, a na hostingu R2, bez promjene ostatka koda. [Django: STORAGES](https://docs.djangoproject.com/en/6.1/ref/settings/#std-setting-STORAGES)

**Upute:**
1. Na Cloudflareu napravi račun i dva spremnika: `vjecnaspomen-dev` i `vjecnaspomen-prod`. Kao lokaciju odaberi EU (*jurisdiction* EU, ako se nudi). **Ne uključuj javni pristup (*Public access*) ni prilagođenu domenu (*custom domain*).**
2. Napravi API token s pravima „Object Read & Write” samo za ta dva spremnika. Vrijednosti stavi u `.env`:
   ```
   R2_ACCESS_KEY_ID=
   R2_SECRET_ACCESS_KEY=
   R2_BUCKET=vjecnaspomen-dev
   R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
   ```
3. `pip install django-storages boto3`. U postavkama:
   ```python
   if env("R2_BUCKET", default=""):
       STORAGES["default"] = {
           "BACKEND": "storages.backends.s3.S3Storage",
           "OPTIONS": {
               "bucket_name": env("R2_BUCKET"),
               "endpoint_url": env("R2_ENDPOINT"),
               "access_key": env("R2_ACCESS_KEY_ID"),
               "secret_key": env("R2_SECRET_ACCESS_KEY"),
               "region_name": "auto",
               "signature_version": "s3v4",
               "querystring_auth": True,      # potpisani linkovi
               "querystring_expire": 3600,    # 1 sat
               "file_overwrite": False,
               "default_acl": None,
           },
       }
   ```
   Bez `R2_BUCKET` koristi se lokalna mapa `media/` (u testovima i kod prijatelja ako nema pristup R2).
4. Ključevi datoteka nikad ne sadrže ime pokojnika: `grobovi/<grob_id>/<uuid>.webp`.
5. Pristupne podatke za `vjecnaspomen-dev` pošalji prijatelju privatnom porukom, ako ih želi za lokalni rad (D-03).
6. U `docs/arhitektura.md` (ili README) zapiši zašto su mediji privatni i kako rade potpisani linkovi.

**Gotovo kada:**
- datoteka spremljena kroz Django shell (`default_storage.save(...)`) pojavi se u R2 spremniku;
- `default_storage.url(...)` vraća link s parametrima `X-Amz-Signature` i `X-Amz-Expires`;
- isti link bez parametara potpisa vraća grešku pristupa;
- link stariji od sat vremena više ne radi;
- ključevi R2 nalaze se samo u `.env`.

**Procjena:** 3–4 sata.

**Česte greške:**
- Uključen *custom domain* ili `custom_domain` u postavkama: `django-storages` tada vraća nepotpisane javne linkove.
- Zaboravljen `region_name="auto"` i `signature_version="s3v4"`: R2 odbija potpis.

### P-27 Pozadinski zadaci s `django-q2`
- [ ] Gotovo

**Cilj:** postoji radni proces (*worker*) koji izvodi pozadinske zadatke iz baze. Probni zadatak pokrenut iz pogleda izvrši se izvan zahtjeva, a čišćenje starih pokušaja pokreće se po rasporedu.

**Zašto:** obrada videa u pozadinskom zadatku (odluka 17). Pretvorba videa traje minutama i ne smije blokirati stranicu.

**Preduvjeti:** P-26 gotov.

**Novi pojmovi:**
- **Pozadinski zadatak** je posao koji se ne izvodi dok korisnik čeka odgovor stranice. Pogled ga stavi u red čekanja, a zaseban proces (*worker*) ga preuzme i izvrši.
- **`django-q2`** je biblioteka za pozadinske zadatke koja kao red čekanja može koristiti samu PostgreSQL bazu, pa ne treba Redis ni dodatni servis. Odabrana je umjesto Hueyja upravo zato. [django-q2](https://django-q2.readthedocs.io/)
- **Raspored (*schedule*)** je zadatak koji se ponavlja, npr. jednom dnevno.

**Upute:**
1. `pip install django-q2`, dodaj `django_q` u `INSTALLED_APPS` i postavke:
   ```python
   Q_CLUSTER = {
       "name": "vjecnaspomen",
       "orm": "default",       # red čekanja u PostgreSQL-u
       "workers": 1,           # ffmpeg je zahtjevan, jedan po jedan
       "timeout": 1800,        # 30 min za najdulji video
       "retry": 2000,          # mora biti veće od timeout
       "max_attempts": 2,
   }
   ```
2. `python manage.py migrate`, a u drugom terminalu `python manage.py qcluster`.
3. Probni zadatak: `async_task("mediji.zadaci.proba", grob_id)` koji upiše zapis u log.
4. Raspored za `ocisti_pokusaje` (P-13) jednom dnevno (u adminu pod *Scheduled tasks* ili migracijom podataka).
5. U README zapiši da lokalni razvoj s medijima traži tri terminala: `tailwind watch`, `runserver` i `qcluster`.

**Gotovo kada:**
- probni zadatak izvrši se dok stranica odmah vraća odgovor;
- uspješni i neuspjeli zadaci vidljivi su u adminu;
- `retry` je veći od `timeout` (inače se dugi zadatak pokrene dvaput).

**Procjena:** 2–3 sata.

### P-28 Upload s mobitela izravno u R2
- [ ] Gotovo

**Cilj:** vlasnik na mobitelu odabere jednu ili više slika ili videa iz galerije ili kamere. Preglednik ih šalje izravno u R2 uz napredak u postocima, a nakon slanja medij dobiva status „u obradi” i ulazi u red za obradu. Ograničenja po datoteci i po grobu provjeravaju se prije slanja.

**Zašto:** upload slike i videa s mobitela uz automatsku obradu je mjerilo uspjeha 3. Ograničenja su iz odluka 12 i 18. Video do 1 GB ne šalje se kroz naš poslužitelj, jer bi ga zagušio.

**Preduvjeti:** P-26, P-27 i P-22 gotovi.

**Novi pojmovi:**
- **Izravni upload (*direct upload*):** poslužitelj ne prima datoteku, nego pregledniku izda potpisani link za slanje (PUT) u R2. Preglednik šalje datoteku izravno, a zatim javi poslužitelju da je gotovo.
- **CORS** je pravilo spremnika koje dopušta pregledniku s naše adrese slanje datoteka u R2. [R2: CORS](https://developers.cloudflare.com/r2/buckets/cors/)
- **`<input type="file" accept="image/*,video/*" multiple>`** na mobitelu nudi galeriju i kameru. [MDN: input file](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file)

**Upute:**
1. CORS na oba spremnika: dopuštene adrese `http://localhost:8000` i adresa demoa, metoda `PUT`, zaglavlja `Content-Type`.
2. Pogled `POST /vlasnik/<kod>/mediji/priprema/` prima JSON s nazivom, MIME vrstom i veličinom. Zatim:
   - provjeri vrstu (`image/jpeg`, `image/png`, `image/heic`, `image/heif`, `image/webp`, `video/mp4`, `video/quicktime`, `video/webm` ...);
   - provjeri veličinu po datoteci i preostali prostor groba (broj slika, bajtovi);
   - napravi `Medij(status="ceka_upload", kljuc_izvornika="ulaz/<grob_id>/<uuid>")`;
   - vrati potpisani PUT link:
   ```python
   klijent = boto3.client("s3", endpoint_url=..., region_name="auto", ...)
   url = klijent.generate_presigned_url(
       "put_object",
       Params={"Bucket": bucket, "Key": medij.kljuc_izvornika,
               "ContentType": mime, "ContentLength": velicina},
       ExpiresIn=900,
   )
   ```
   `ContentLength` je dio potpisa, pa preglednik ne može poslati veću datoteku od prijavljene.
3. `static/js/upload.js` (oko 60 linija, bez biblioteka): za svaku datoteku pozovi `priprema`, pošalji `XMLHttpRequest` PUT s praćenjem napretka (`upload.onprogress`), zatim pozovi `POST /vlasnik/<kod>/mediji/<id>/poslano/`.
4. Pogled `poslano` napravi `head_object` u R2 i provjeri da veličina odgovara. Postavi status `u_obradi` i pokreni `async_task("mediji.zadaci.obradi", medij.id)`.
5. Duljina videa ne zna se prije obrade, pa je provjerava zadatak (P-30).
6. Ružni predložak `vlasnik/mediji.html` s popisom medija i statusima. Dok ima medija u obradi, popis se osvježava HTMX-om svakih 5 sekundi (`hx-trigger="every 5s"`).
7. Medije sa statusom `ceka_upload` starije od 24 sata briše dnevni raspored.

**Gotovo kada:**
- slika i video odabrani na iPhoneu i Androidu stižu u R2 pod `ulaz/`, uz vidljiv napredak;
- datoteka veća od 1 GB (video) ili 30 MB (slika) odbija se prije slanja, s porukom na hrvatskom;
- 301. slika u grobu se odbija;
- zahtjev `priprema` za tuđi grob vraća 404;
- prijavljena veličina koja ne odgovara stvarnoj (test kroz `curl`) ne prolazi.

**Procjena:** 5–6 sati.

**Česte greške:**
- Nedostaje CORS pravilo: u konzoli preglednika piše „blocked by CORS policy”.
- iPhone za HEIC fotografiju ponekad šalje prazan MIME tip. Tada vrstu odredi iz nastavka datoteke.

### P-29 Obrada slika: HEIC u WebP, smanjivanje i uklanjanje lokacije
- [ ] Gotovo

**Cilj:** pozadinski zadatak svaku sliku pretvara u WebP s duljom stranicom najviše 2048 px i malu sličicu od 600 px, uklanja EXIF podatke (uključujući GPS lokaciju) i briše izvornik.

**Zašto:** slike se pretvaraju iz HEIC u JPEG ili WebP i smanjuju na oko 2048 px (odluka 18). Uklanjanje lokacije štiti privatnost obitelji (odluka 19).

**Preduvjeti:** P-28 gotov.

**Novi pojmovi:**
- **HEIC** je zadani format fotografija na iPhoneu. Većina preglednika ga ne prikazuje. [pillow-heif](https://pillow-heif.readthedocs.io/)
- **WebP** je format slike manji od JPEG-a uz istu kvalitetu, podržan u svim današnjim preglednicima. Odabran je umjesto JPEG-a zbog manje potrošnje prostora.
- **EXIF** su skriveni podaci u fotografiji: model mobitela, vrijeme i često GPS lokacija.
- **Pillow** je Python biblioteka za obradu slika. [Pillow](https://pillow.readthedocs.io/)

**Upute:**
1. `pip install Pillow pillow-heif`.
2. Jezgra obrade:
   ```python
   from PIL import Image, ImageOps
   from pillow_heif import register_heif_opener

   register_heif_opener()
   MAX = settings.MEDIJI_MAX_STRANICA_SLIKE_PX

   def obradi_sliku(izvor) -> tuple[bytes, bytes, int, int]:
       with Image.open(izvor) as slika:
           slika = ImageOps.exif_transpose(slika)   # ispravna orijentacija
           slika = slika.convert("RGB")
           slika.thumbnail((MAX, MAX))
           sirina, visina = slika.size
           velika = io.BytesIO()
           slika.save(velika, "WEBP", quality=82)   # bez exif=, pa se EXIF ne prenosi
           slika.thumbnail((600, 600))
           mala = io.BytesIO()
           slika.save(mala, "WEBP", quality=75)
           return velika.getvalue(), mala.getvalue(), sirina, visina
   ```
3. Zadatak `obradi`: preuzmi izvornik iz R2 u privremenu datoteku, obradi ga, spremi `datoteka` i `slicica`, postavi status `gotov` i obriši izvornik iz `ulaz/`. Kod greške postavi `greska` i `poruka_greske`, a izvornik ostavi za ponovni pokušaj.
4. Postavi `Image.MAX_IMAGE_PIXELS` na razumnu vrijednost (npr. 80 milijuna) da preveliki ili zlonamjerni dokument ne potroši svu memoriju.
5. Prvu gotovu sliku pokojnika automatski postavi kao profilnu sliku, ako je nema.

**Gotovo kada:**
- HEIC fotografija s iPhonea prikazuje se kao WebP s duljom stranicom ≤ 2048 px;
- fotografija snimljena „naopako” prikazuje se uspravno;
- obrađena slika nema EXIF ni GPS podatke (provjeri s `exiftool` ili Pillowom `img.getexif()`);
- izvornik je obrisan iz `ulaz/` nakon uspješne obrade;
- oštećena datoteka daje status `greska`, a ne ruši worker.

**Procjena:** 3–4 sata.

### P-30 Obrada videa: ffmpeg u 720p
- [ ] Gotovo

**Cilj:** pozadinski zadatak provjerava duljinu videa (najviše 5 minuta po isječku i 20 minuta po grobu), pretvara video u MP4 (H.264/AAC) s duljom stranicom najviše 1280 px (720p), izrađuje sliku kadra i briše izvornik.

**Zašto:** video do 5 minuta i 1 GB po isječku, pretvorba u 720p (odluka 18), ograničenje od 20 minuta po grobu i automatska kompresija (odluka 12), ffmpeg u pozadinskom zadatku (odluka 17).

**Preduvjeti:** P-29 gotov.

**Novi pojmovi:**
- **ffmpeg** je besplatan program naredbenog retka za pretvorbu videa i zvuka. **ffprobe** iz istog paketa čita podatke o videu (duljina, rezolucija). [ffmpeg dokumentacija](https://ffmpeg.org/documentation.html)
- **H.264 i AAC** su formati videa i zvuka koje reproducira svaki mobitel i preglednik.
- **`subprocess`** je Pythonov modul za pokretanje vanjskih programa. Argumenti se daju kao lista, nikad kao jedan niz sastavljen od korisničkog unosa. [Python: subprocess](https://docs.python.org/3/library/subprocess.html)

**Upute:**
1. `brew install ffmpeg` lokalno. Na hostingu ffmpeg dolazi kroz Dockerfile (P-41).
2. Duljina:
   ```python
   rezultat = subprocess.run(
       ["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", ulaz],
       capture_output=True, text=True, check=True, timeout=60)
   trajanje = float(rezultat.stdout.strip())
   ```
   Ako je dulje od 5 minuta ili bi grob prešao 20 minuta, status `greska` s porukom za korisnika („Video je dulji od 5 minuta. Skratite ga i pošaljite ponovno.”) i brisanje izvornika.
3. Pretvorba:
   ```python
   subprocess.run([
       "ffmpeg", "-y", "-i", ulaz,
       "-vf", "scale=1280:1280:force_original_aspect_ratio=decrease:force_divisible_by=2",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", izlaz,
   ], check=True, timeout=1500)
   ```
   Uspravni video s mobitela tako postaje 720 × 1280, a vodoravni 1280 × 720. Manji video se ne povećava.
4. Slika kadra: `ffmpeg -ss 1 -i izlaz.mp4 -frames:v 1 kadar.jpg`, pa kroz `obradi_sliku` u WebP.
5. Spremi `datoteka`, `slicica`, `trajanje_sekundi` i `velicina_bajtova`, a zatim obriši izvornik i privremene datoteke (`tempfile.TemporaryDirectory`).
6. Ukupnu potrošnju groba (bajtovi i sekunde) računaj zbrojem preko `Medij` (`aggregate(Sum(...))`).

**Gotovo kada:**
- video od 1–2 minute snimljen iPhoneom (HEVC, `.mov`) i Androidom (`.mp4`) reproducira se u Safariju i Chromeu na mobitelu;
- video dulji od 5 minuta odbija se s porukom na hrvatskom;
- obrađeni video ima dulju stranicu ≤ 1280 px (`ffprobe` potvrđuje);
- privremene datoteke ne ostaju na disku nakon zadatka;
- naziv datoteke od korisnika nikad se ne prosljeđuje ffmpegu (koristi se naš UUID ključ).

**Procjena:** 4–5 sati.

**Česte greške:**
- HDR video s iPhonea nakon pretvorbe izgleda isprano. Za MVP je to prihvatljivo. Ako smeta, kasnije dodaj tonsko mapiranje.
- Bez `-movflags +faststart` video na mobitelu kreće tek kad se cijeli preuzme.

### P-31 Galerija i video na profilu, uređivanje i brisanje medija
- [ ] Gotovo

**Cilj:** profil prikazuje galeriju slika (sličice, a dodirom veliki prikaz) i videe s reprodukcijom. Vlasnik mijenja opis i redoslijed, bira profilnu sliku i briše medije, pri čemu se brišu i datoteke u R2. Vidi i koliko je prostora iskoristio.

**Zašto:** galerija slika i video su dio profila u MVP-u (odluka 6). Mediji se prikazuju samo kroz potpisane linkove (odluka 5). Ograničenja po grobu (odluka 12) vlasnik mora razumjeti.

**Preduvjeti:** P-30 i P-14 gotovi.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. U pogled `profil` dodaj `slike` i `videi` (samo `status="gotov"` i `skriven=False`). Linkove generira `medij.datoteka.url`, koji je potpisan.
2. Video: `<video controls playsinline preload="none" poster="{{ video.slicica.url }}">`. Bez `playsinline` iPhone odmah otvara video preko cijelog zaslona.
3. Veliki prikaz slike: zasebna stranica `/g/<kod>/<pokojnik_id>/slika/<id>/` s gumbima „Prethodna” i „Sljedeća” (radi i bez JavaScripta). Prijatelj je može kasnije pretvoriti u prikaz preko stranice.
4. `vlasnik/mediji.html`: opis (HTMX spremanje), „Gore” i „Dolje”, „Postavi kao profilnu”, „Obriši” uz potvrdu, te traka iskorištenosti („124 od 300 slika, 6 od 20 minuta videa”).
5. Brisanje medija i pokojnika briše datoteke iz R2. Signal `post_delete` ili eksplicitni poziv `medij.datoteka.delete(save=False)`.
6. Dopuni `docs/predlosci.md`: varijable galerije, videa, velikog prikaza i vlasničkog popisa medija, te stanja: nema medija, u obradi, greška.

**Gotovo kada:**
- galerija i video rade na iPhoneu (Safari) i Androidu (Chrome);
- HTML profila ne sadrži nijedan link na R2 bez potpisa;
- nakon brisanja medija datoteka ne postoji u R2;
- posjetitelj ne vidi medije `u_obradi`, `greska` ni `skriven`;
- slika tuđeg groba ne može se otvoriti promjenom ID-a u adresi (404).

**Procjena:** 4–5 sati.

> 🔁 **Predaja:** Petar predaje prijatelju predloške `templates/javno/_galerija.html`, `templates/javno/_video.html`, `templates/javno/slika.html`, `templates/vlasnik/mediji.html`, skriptu `static/js/upload.js` (prijatelj je ne mijenja, nego samo stilizira elemente koje ona koristi, navedene u `docs/predlosci.md`) i popis stanja medija. Time mogu krenuti **D-19** i **D-27**.

### P-32 Testovi medija
- [ ] Gotovo

**Cilj:** automatski testovi provjeravaju ograničenja uploada, obradu slike (format, veličina, uklonjen EXIF), obradu kratkog videa i dozvole nad medijima.

**Zašto:** mediji su najskuplji i najosjetljiviji dio sustava (odluke 5, 12 i 18, mjerilo uspjeha 3).

**Preduvjeti:** P-31 gotov.

**Novi pojmovi:**
- **Mock** je lažni objekt koji u testu zamjenjuje pravi servis (npr. R2), da test ne ovisi o internetu. [Python: unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

**Upute:**
1. U testovima koristi lokalni storage (bez `R2_BUCKET`) i `mock.patch` za `generate_presigned_url` i `head_object`.
2. Testne datoteke u `mediji/tests/datoteke/`: mala JPEG slika s GPS EXIF-om, mala HEIC slika i video od 2 sekunde (izradi ga ffmpegom: `ffmpeg -f lavfi -i testsrc=duration=2:size=640x480 -f lavfi -i sine=duration=2 test.mp4`).
3. Testovi:
   - slika postaje WebP ≤ 2048 px bez EXIF-a;
   - HEIC radi;
   - video postaje MP4 s dulju stranicom ≤ 1280;
   - prevelika datoteka se odbija;
   - 301. slika se odbija;
   - tuđi grob vraća 404;
   - skriveni medij se ne prikazuje.
4. Zadatke u testovima pokreći izravno (sinkrono), bez `qcluster`. `django-q2` za to ima postavku `"sync": True`.

**Gotovo kada:**
- svi testovi prolaze lokalno i u GitHub Actions (ffmpeg je instaliran u radnom tijeku iz P-16);
- nijedan test ne šalje zahtjev na stvarni R2.

**Procjena:** 3–4 sata.

## Faza 6: Knjiga sjećanja i prijave

Poruke uz odobrenje vlasnika i gumb „Prijavi” na svakom sadržaju.

### P-33 Knjiga sjećanja s odobravanjem
- [ ] Gotovo

**Cilj:** posjetitelj s pristupom grobu ostavlja poruku na profilu pokojnika. Poruka je vidljiva tek kad je vlasnik odobri u vlasničkom dijelu, a vlasnik o novoj poruci dobiva e-mail.

**Zašto:** knjiga sjećanja s odobravanjem je mjerilo uspjeha 4 (odluke 3, 6 i 19).

**Preduvjeti:** P-21 i P-14 gotovi.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Forma na profilu: „Vaše ime” (obavezno, do 100 znakova) i „Poruka” (obavezno, do 2000 znakova). Šalje se HTMX-om i nakon slanja zamjenjuje porukom „Hvala. Poruka će biti vidljiva kad je obitelj odobri.”
2. Poruku može ostaviti samo tko ima pristup grobu (`ima_pristup`). Ograničenje: 5 poruka po IP adresi na sat, uz polje „mamac”.
3. Tekst se uvijek ispisuje kroz zadano Django escapiranje (`{{ poruka.tekst|linebreaksbr }}`), **nikad** s `|safe`.
4. E-mail kontaktu za prijavu (`emailovi/nova_poruka.txt`): ime autora i početak poruke te link na `/vlasnik/<kod>/knjiga/`. Ako u sat vremena stigne više poruka, šalje se najviše jedan e-mail (zapamti vrijeme zadnjeg slanja na grobu).
5. `/vlasnik/<kod>/knjiga/`: poruke na čekanju s gumbima „Odobri” i „Odbij” (HTMX zamjenjuje redak), a ispod odobrene poruke s gumbom „Ukloni”.
6. Profil prikazuje samo `status="odobrena"` i `skrivena=False`, od najnovije.
7. Dopuni `docs/predlosci.md`: `javno/_knjiga.html`, `vlasnik/knjiga.html`, `vlasnik/_poruka_redak.html`.

**Gotovo kada:**
- nova poruka ne vidi se na profilu dok je vlasnik ne odobri, a nakon odobrenja vidi se;
- poruka s tekstom `<script>alert(1)</script>` prikazuje se kao običan tekst;
- posjetitelj bez pristupa grobu ne može poslati poruku ni izravnim POST zahtjevom;
- tuđi korisnik ne može odobriti poruku (404);
- testovi pokrivaju sve četiri točke.

**Procjena:** 4–5 sati.

### P-34 Gumb „Prijavi” i obrada prijava
- [ ] Gotovo

**Cilj:** uz svaki profil, sliku, video i poruku u knjizi sjećanja postoji gumb „Prijavi”. Prijava stiže nama e-mailom i u admin, s rokom odgovora od 7 dana, a administrator jednim klikom skriva prijavljeni sadržaj.

**Zašto:** gumb „Prijavi” na svakom sadržaju, odgovor u 7 dana i reakcija na prijave umjesto prethodnog pregleda (odluka 19). Zahtjev živuće osobe za uklanjanje vlastite slike ima prednost (odluka 19, GDPR).

**Preduvjeti:** P-31 i P-33 gotovi.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Forma `/g/<kod>/<pokojnik_id>/prijavi/?medij=<id>` (ili `?poruka=<id>`): razlog (izbori iz P-08), opis i e-mail za odgovor (neobavezan, ali preporučen). Isto ograničenje kao kod poruka i polje „mamac”.
2. Prijavu može poslati samo tko ima pristup grobu, jer drugi sadržaj ni ne vidi.
3. E-mail na adresu iz postavke `PRIJAVE_EMAIL` (u `.env`) s linkom na prijavu u adminu.
4. Admin `PrijavaSadrzaja`:
   - stupci status, razlog i rok;
   - filtar „Prekoračen rok”;
   - prijave s razlogom „na slici sam ja” označene su i poredane prve;
   - akcije „Sakrij prijavljeni sadržaj” (postavlja `skriven`/`skrivena=True`) i „Označi riješeno”.
5. Vlasnik ne vidi tko je prijavio sadržaj.

**Gotovo kada:**
- prijava slike s mobitela stiže u admin i kao e-mail (u terminalu);
- akcija u adminu skriva sliku s profila, a vlasnik je ne može ponovno prikazati;
- filtar „Prekoračen rok” prikazuje prijave starije od 7 dana koje nisu riješene;
- prijava ne otkriva vlasniku e-mail prijavitelja.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Petar predaje prijatelju predloške `templates/javno/_knjiga.html`, `templates/javno/prijava.html`, `templates/vlasnik/knjiga.html` i `templates/vlasnik/_poruka_redak.html` s varijablama u `docs/predlosci.md`. Time može krenuti **D-20**, a vlasnički dio knjige ulazi u **D-27**.

## Faza 7: Administracija, izvoz i izvještaji

Udoban admin, izvoz groba, mjesečni izvještaj i pregled za partnera.

### P-35 Administracija: pregledi, pretraga i usluga postavljanja sadržaja
- [ ] Gotovo

**Cilj:** admin je udoban za svakodnevni rad: brza pretraga groba po kodu, nazivu, vlasniku i e-mailu, pregled potrošnje prostora po grobu, ručna promjena kontakta za prijavu i ulaz u vlasnički dio bilo kojeg groba za uslugu „pošaljite nam slike, mi postavimo”.

**Zašto:** administracija je mjerilo uspjeha 5. Usluga postavljanja sadržaja uključena je u cijenu (odluke 3 i 13), a promjena kontakta ide preko nas (odluka 19).

**Preduvjeti:** P-31 gotov.

**Novi pojmovi:**
- **`list_select_related` i `annotate`** smanjuju broj upita prema bazi kad popis prikazuje podatke iz povezanih tablica (izbjegavaš problem „N+1 upita”). [Django: Database access optimization](https://docs.djangoproject.com/en/6.1/topics/db/optimization/)
- **Povijest promjena u adminu** (`LogEntry`) Django bilježi sam za svaku izmjenu kroz admin. [Django: LogEntry](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/#logentry-objects)

**Upute:**
1. `GrobAdmin`:
   - `search_fields = ["plocica__kod", "naziv", "vlasnik_ime", "kontakt_za_prijavu__email", "oznaka_grobnog_mjesta"]`;
   - stupci partner, broj pokojnika, broj slika, minute videa, datum aktivacije;
   - link „Otvori vlasnički dio” (radi jer *superuser* prolazi dekorator iz P-21).
2. Promjena `kontakt_za_prijavu` u adminu traži popunjeno polje „Razlog promjene i tko je potvrdio” (npr. „potvrda uprave, e-mail od …”), koje se sprema u napomenu groba.
3. `PlocicaAdmin`: filtri po partneru, seriji i statusu.
4. `MedijAdmin`: filtar po statusu i akcija „Ponovno obradi” za medije u statusu `greska`.
5. Svaki ulaz administratora u vlasnički dio tuđeg groba bilježi se u log (tko, kada, koji grob).

**Gotovo kada:**
- pretraga po 6-znakovnom kodu ili e-mailu nalazi grob;
- popis grobova se ne usporava s brojem grobova (najviše nekoliko upita po stranici, provjeri s `django-debug-toolbar` ili `assertNumQueries` u testu);
- administrator može kroz vlasnički dio dodati sliku u tuđi grob, a to je zabilježeno;
- promjena kontakta za prijavu bez obrazloženja se ne može spremiti.

**Procjena:** 3–4 sata.

### P-36 Izvoz sadržaja groba u ZIP
- [ ] Gotovo

**Cilj:** upravljačka naredba `python manage.py izvezi_grob <kod>` i admin akcija stvaraju ZIP sa svim podacima i obrađenim medijima groba te jednostavnom `index.html` stranicom koja se otvara bez interneta.

**Zašto:** obećanje izvoza svih sadržaja (ZIP) pri gašenju servisa ulazi u uvjete korištenja (odluka 12). Isti izvoz služi i za GDPR zahtjeve.

**Preduvjeti:** P-31 i P-33 gotovi.

**Novi pojmovi:**
- **Vlastita upravljačka naredba** je klasa `BaseCommand` u `<aplikacija>/management/commands/<naziv>.py`. [Django: Custom management commands](https://docs.djangoproject.com/en/6.1/howto/custom-management-commands/)
- **`zipfile`** je Pythonov modul za izradu ZIP datoteka. [Python: zipfile](https://docs.python.org/3/library/zipfile.html)

**Upute:**
1. Sadržaj ZIP-a:
   - `podaci.json` (grob bez hasha lozinke, pokojnici, srodnici, odobrene poruke);
   - `mediji/` (obrađene slike i videi);
   - `index.html` s biografijama, slikama i porukama.
2. Za velike grobove izvoz se radi kao pozadinski zadatak. Gotov ZIP sprema se u R2 pod `izvozi/`, a administrator dobiva potpisani link koji vrijedi 24 sata.
3. Dnevni raspored briše izvoze starije od 7 dana.

**Gotovo kada:**
- izvoz demo groba otvara se na računalu bez interneta i prikazuje sve pokojnike, slike i poruke;
- ZIP ne sadrži hash lozinke, oznaku grobnog mjesta ni e-mailove posjetitelja;
- link na izvoz je potpisan i vremenski ograničen.

**Procjena:** 3–4 sata.

### P-37 Mjesečni izvještaj o aktivacijama po partneru
- [ ] Gotovo

**Cilj:** u adminu postoji stranica „Mjesečni izvještaj” na kojoj se bira mjesec i partner. Prikazuje broj aktiviranih pločica, broj dodanih pokojnika u postojeće grobove i obračun po postotku partnera, uz preuzimanje CSV-a.

**Zašto:** sustav generira mjesečni izvještaj o aktiviranim pločicama za usklađivanje s prodajom uprave (odluka 10), a provizija se obračunava automatski iz partnera pločice (odluke 8 i 15). Mjerilo uspjeha 5.

**Preduvjeti:** P-35 gotov.

**Novi pojmovi:**
- **Agregacija** je računanje zbroja, broja ili prosjeka u bazi (`Count`, `Sum`), umjesto petlje u Pythonu. [Django: Aggregation](https://docs.djangoproject.com/en/6.1/topics/db/aggregation/)
- **`Decimal`** je točan zapis decimalnih brojeva. Za novac se nikad ne koristi `float`. [Python: decimal](https://docs.python.org/3/library/decimal.html)
- **CSV** je tablica u tekstualnom obliku koja se otvara u Excelu ili LibreOfficeu. [Python: csv](https://docs.python.org/3/library/csv.html)

**Upute:**
1. Logika u `partneri/izvjestaji.py`, kao funkcija koju koriste i admin (P-37) i pregled za partnera (P-38):
   ```python
   def mjesecni_izvjestaj(partner, godina, mjesec):
       aktivirane = Plocica.objects.filter(
           serija__partner=partner,
           status=Plocica.Status.AKTIVIRANA,
           aktivirana_u__year=godina, aktivirana_u__month=mjesec,
       ).select_related("serija", "grob")
       ukupno = sum((p.serija.maloprodajna_cijena for p in aktivirane), Decimal("0"))
       udio_partnera = (ukupno * partner.postotak_provizije / 100).quantize(Decimal("0.01"))
       return {
           "aktivirane": aktivirane,
           "broj": len(aktivirane),
           "ukupno": ukupno,
           "udio_partnera": udio_partnera,
           "nama": ukupno - udio_partnera,
           "dodatni_pokojnici": dodatni_pokojnici(partner, godina, mjesec),
       }
   ```
2. `dodatni_pokojnici` broji pokojnike stvorene u tom mjesecu u grobovima tog partnera koji nisu prvi pokojnik u grobu (vidi OP-2 i OP-3).
3. CSV ima stupce: kod pločice, serija, datum aktivacije, naziv groba, oznaka grobnog mjesta, maloprodajna cijena. Uprava prema oznaci grobnog mjesta uspoređuje izvještaj sa svojim računima (odluka 11).
4. Granice mjeseca računaj u vremenskoj zoni `Europe/Zagreb` (aktivacija u 23:30 zadnjeg dana mjeseca pripada tom mjesecu).
5. Stranica izvještaja dostupna je samo osoblju (`is_staff`).

**Gotovo kada:**
- za demo partnera s 3 aktivacije u mjesecu izvještaj prikazuje broj 3, ukupni iznos i udio partnera prema njegovom postotku, točno na cent;
- aktivacija 31. u 23:30 po zagrebačkom vremenu ulazi u taj mjesec (test);
- CSV se otvara u Excelu s ispravnim dijakritikama (UTF-8 s BOM-om, `utf-8-sig`);
- korisnik bez `is_staff` ne može otvoriti izvještaj.

**Procjena:** 4–5 sati.

### P-38 Pregled za partnera
- [ ] Gotovo

**Cilj:** korisnik povezan s partnerom prijavljuje se linkom na e-mail i na `/partner/` vidi broj pločica na zalihi, aktiviranih pločica, aktivacije po mjesecima i mjesečni izvještaj s CSV-om, i to samo za svog partnera.

**Zašto:** pregled za partnera s brojem prodanih i aktiviranih pločica i mjesečnim izvještajem je dio MVP-a (odluka 15).

**Preduvjeti:** P-37 i P-17 gotovi.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Prijava kroz isti `vlasnik:prijava` (link na e-mail). Nakon prijave korisnik s `partner` ide na `/partner/`, a ostali na `/vlasnik/`.
2. Pregled: tri broja (na zalihi, aktivirane, ukupno) i tablica zadnjih 12 mjeseci (broj aktivacija). Klikom na mjesec otvara se izvještaj iz P-37.
3. Partner **ne vidi** sadržaj profila, lozinke, imena pokojnika ni e-mailove kontakata. Vidi samo kod pločice, datum, naziv groba i oznaku grobnog mjesta, kao u CSV-u.
4. Korisnika partnera stvaraš u adminu: novi `Korisnik` s e-mailom i odabranim partnerom.
5. Ružni predlošci `partner/pregled.html` i `partner/izvjestaj.html` s varijablama u `docs/predlosci.md`.
6. Napravi i ružne predloške grešaka `greske/404.html` i `greske/500.html` te ih poveži kroz `handler404` i `handler500` u `config/urls.py` ([Django: Customizing error views](https://docs.djangoproject.com/en/6.1/topics/http/views/#customizing-error-views)). Predložak 500 ne smije koristiti varijable iz baze, jer se prikazuje i kad baza ne radi.

**Gotovo kada:**
- korisnik partnera A ne vidi podatke partnera B ni promjenom parametara u adresi (test);
- vlasnik groba koji nije partner dobiva 404 na `/partner/`;
- brojevi u pregledu slažu se s izvještajem iz admina.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Petar predaje prijatelju predloške `templates/partner/*.html`, `templates/emailovi/*.txt` (prijava, aktivacija, zahtjev za pristup, nova poruka, obiteljski link) i `templates/greske/*.html` s varijablama u `docs/predlosci.md`. Time može krenuti **D-28**.

## Faza 8: Demo, objava i CV

PWA, demo podaci, objava na Render, provjera mjerila uspjeha, README i studija slučaja.

### P-39 Dodavanje na početni zaslon (PWA) za vlasnike
- [ ] Gotovo

**Cilj:** vlasnik na iPhoneu (Safari → Dijeli → Dodaj na početni zaslon) i Androidu (Chrome → Instaliraj aplikaciju) dodaje vlasnički dio na početni zaslon, s vlastitom ikonom i nazivom „Vječna spomen”.

**Zašto:** mogućnost dodavanja na početni zaslon (PWA) za vlasnike (odluka 16).

**Preduvjeti:** P-21 gotov, D-30 gotov (ikone).

**Novi pojmovi:**
- **PWA (*Progressive Web App*)** je web stranica koju mobitel može „instalirati” kao aplikaciju, s ikonom na početnom zaslonu i bez adresne trake. Osnova je datoteka **manifest**. [MDN: Web app manifest](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest)
- **Service worker** je skripta koja omogućuje rad bez interneta i obavijesti. U MVP-u nam to ne treba. Provjeri trenutačne zahtjeve Chromea za instalaciju; ako i dalje traži service worker, dodaj prazan. [web.dev: Install criteria](https://web.dev/articles/install-criteria)

**Upute:**
1. `static/manifest.webmanifest`: `name`, `short_name`, `start_url: "/vlasnik/"`, `scope: "/"`, `display: "standalone"`, `background_color`, `theme_color` (iz D-05) i ikone 192 i 512 px (i *maskable*).
2. U `base.html`: `<link rel="manifest">`, `<meta name="theme-color">`, `<link rel="apple-touch-icon" href="...180.png">`.
3. Na `/vlasnik/` jednom prikaži kratku uputu „Dodajte na početni zaslon” s koracima za iPhone i Android (tekst i izgled iz D-24).

**Gotovo kada:**
- na iPhoneu i Androidu ikona na početnom zaslonu otvara `/vlasnik/` bez adresne trake;
- Lighthouse (Chrome DevTools → Lighthouse) ne javlja greške manifesta.

**Procjena:** 1–2 sata.

> 🔁 **Predaja:** prijatelj predaje Petru ikone u `static/img/ikone/` (180, 192, 512 px i *maskable* 512 px) i boje teme (D-30). Time ovaj korak može krenuti.

### P-40 Demo podaci kroz upravljačku naredbu
- [ ] Gotovo

**Cilj:** naredba `python manage.py napuni_demo` na praznoj bazi stvara izmišljenog partnera, seriju demo pločica (neke aktivirane, neke ne), demo grob s više pokojnika, srodnicima, slikama, videom i odobrenim porukama te ispisuje kodove, lozinke i aktivacijske kodove za demonstraciju.

**Zašto:** MVP mora imati izmišljeni demo grob s pokojnicima, slikama i videom te nekoliko demo QR kodova (odluka 20). Demo sadržaj koristi samo izmišljene osobe i slobodne fotografije.

**Preduvjeti:** P-32, P-33 i P-37 gotovi, D-07 gotov (demo sadržaj).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Prijatelj u `demo/` predaje `demo/sadrzaj.json` (pokojnici, biografije, srodnici, poruke), slike i kratki video te `demo/IZVORI.md` s licencom i linkom za svaku datoteku.
2. Naredba:
   - odbija rad ako `DEBUG=False` i nije zadana zastavica `--da-sigurno`, da se slučajno ne pokrene na produkciji s pravim podacima;
   - briše samo ono što je sama stvorila (partner s oznakom „DEMO”);
   - mediji prolaze **istu** obradu kao upload (P-29 i P-30), pozvanu sinkrono.
3. Sadržaj demoa:
   - partner „Gradsko groblje Primjerovo (demo)” s 25 %;
   - serija `DEMO-01` od 10 pločica;
   - grob „Obitelj Kovačić” s 3 pokojnika (jedan s videom), srodnicima (povezani pokojnik i živuća osoba s pristankom) i 5 odobrenih te 2 poruke na čekanju;
   - drugi grob s jednim pokojnikom (provjera izravnog otvaranja profila);
   - 3 aktivacije u prošlom mjesecu (da izvještaj nije prazan);
   - 5 neaktiviranih pločica za demonstraciju čarobnjaka;
   - korisnik partnera i vlasnik demo groba, s e-mailovima na `@example.com`.
4. Na kraju ispiši tablicu: kod, link, lozinka groba ili aktivacijski kod. Te podatke spremi i u `demo/demo_pristup.csv`, koji je u `.gitignore`.
5. Demo lozinke **nisu tajne** (namijenjene su demonstraciji), ali ih ne stavljaj u README. Prikazuju se na stranici za demo ili u studiji slučaja, prema dogovoru.

**Gotovo kada:**
- na praznoj bazi `napuni_demo` završava bez greške i ispisuje kodove;
- ponovno pokretanje ne stvara duplikate;
- svaka datoteka u `demo/` ima zapis u `demo/IZVORI.md`;
- u demo podacima nema stvarnih osoba;
- naredba odbija rad na produkciji bez `--da-sigurno`.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** prijatelj predaje Petru `demo/sadrzaj.json`, `demo/slike/`, `demo/video/` i `demo/IZVORI.md` (D-07). Time ovaj korak može krenuti.

### P-41 Produkcijske postavke i Dockerfile
- [ ] Gotovo

**Cilj:** aplikacija se gradi u Docker sliku s ffmpegom, Tailwind CSS-om i statičkim datotekama, a `python manage.py check --deploy` ne javlja upozorenja.

**Zašto:** objava na Render ili Railway (odluka 17). ffmpeg mora postojati na poslužitelju (odluka 17), a javno dostupan demo je mjerilo uspjeha 6.

**Preduvjeti:** P-40 gotov.

**Novi pojmovi:**
- **Docker** pakira aplikaciju sa svim programima koje treba (Python, ffmpeg) u **sliku** koja se jednako pokreće na svakom računalu i hostingu. **Dockerfile** je recept za tu sliku. [Docker: Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- **gunicorn** je poslužitelj koji na hostingu pokreće Django umjesto `runserver`, koji je samo za razvoj. [gunicorn](https://docs.gunicorn.org/)
- **WhiteNoise** poslužuje statičke datoteke (CSS, JS) izravno iz Djanga, bez zasebnog poslužitelja. [WhiteNoise](https://whitenoise.readthedocs.io/)
- **`collectstatic`** skuplja sve statičke datoteke u jednu mapu za produkciju. [Django: Deployment of static files](https://docs.djangoproject.com/en/6.1/howto/static-files/deployment/)
- **Kontrolni popis za objavu** je Djangov popis sigurnosnih postavki za produkciju. [Django: Deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)

**Upute:**
1. `pip install gunicorn whitenoise`. WhiteNoise dodaj odmah ispod `SecurityMiddleware`, a za statičke datoteke postavi `CompressedManifestStaticFilesStorage`.
2. Produkcijske postavke, sve iz `.env` s bezopasnim zadanim vrijednostima:
   - `DEBUG=False`;
   - `ALLOWED_HOSTS` i `CSRF_TRUSTED_ORIGINS`;
   - `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`;
   - `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`;
   - `SECURE_HSTS_SECONDS` (počni s 3600, a kad sve radi, povećaj);
   - `IZA_PROXYJA=True`.
3. `Dockerfile` (ideja):
   ```dockerfile
   FROM python:3.13-slim
   RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
       && rm -rf /var/lib/apt/lists/*
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   RUN SECRET_KEY=build DATABASE_URL=sqlite:///tmp.db ALLOWED_HOSTS=* \
       python manage.py tailwind build && \
       SECRET_KEY=build DATABASE_URL=sqlite:///tmp.db ALLOWED_HOSTS=* \
       python manage.py collectstatic --noinput
   CMD ["./pokreni.sh"]
   ```
   `SECRET_KEY=build` postoji samo dok se slika gradi i nije tajna. Pravi ključ dolazi iz postavki hostinga.
4. `pokreni.sh`: `python manage.py migrate --noinput`, zatim `python manage.py qcluster &` i na kraju `exec gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 60`. Za demo worker radi u istom servisu kao web, što štedi trošak drugog servisa. To zapiši u README kao svjesni kompromis.
5. Napravi `.dockerignore` (`.env`, `.venv`, `media`, `.git`, `demo/demo_pristup.csv`).
6. Lokalna provjera: `docker build -t vjecnaspomen .` i `docker run --env-file .env -p 8000:8000 -e PORT=8000 vjecnaspomen`.

**Gotovo kada:**
- `DEBUG=False python manage.py check --deploy` ne javlja upozorenja (osim onih koje svjesno prihvaćaš i zapišeš u README);
- Docker slika se gradi i lokalno pokreće s PostgreSQL-om i R2 dev spremnikom;
- slika ne sadrži `.env` (provjeri: `docker run --rm vjecnaspomen ls -a /app`);
- s `DEBUG=False` nepostojeća stranica prikazuje `greske/404.html`, a ne Djangov tehnički ispis.

**Procjena:** 4–5 sati.

**Česte greške:**
- `tailwind build` pokušava preuzeti Tailwind program tijekom gradnje slike. Fiksiraj `TAILWIND_CLI_VERSION` da gradnja bude ponovljiva.

### P-42 Objava na Render
- [ ] Gotovo

**Cilj:** demo radi javno na adresi poput `https://vjecnaspomen.onrender.com`, s PostgreSQL bazom, R2 produkcijskim spremnikom, slanjem e-mailova i demo podacima.

**Zašto:** javno dostupan demo (odluka 20, mjerilo uspjeha 6) na Renderu (odluka 17), uz EU poslužitelje (odluka 19).

**Preduvjeti:** P-41 gotov.

**Novi pojmovi:**
- **Render** je hosting koji iz GitHub repozitorija sam gradi i pokreće aplikaciju pri svakom spajanju u `main`. Odabran je umjesto Railwaya jer ima regiju u Frankfurtu i jednostavnu bazu u istoj regiji (Railway bi radio jednako dobro s istim Dockerfileom). [Render Docs](https://render.com/docs), [Deploy Django](https://render.com/docs/deploy-django)
- **SMTP** je protokol za slanje e-maila. Za demo koristimo besplatni plan e-mail servisa s poslužiteljima u EU (prijedlog: Brevo; vidi OP-8). [Django: SMTP backend](https://docs.djangoproject.com/en/6.1/topics/email/#smtp-backend)

**Upute:**
1. Na Renderu: *New → PostgreSQL*, regija Frankfurt. Provjeri cijene i rok trajanja besplatne baze. Za trajni demo vjerojatno treba najmanji plaćeni plan.
2. *New → Web Service* iz GitHub repozitorija, okruženje Docker, regija Frankfurt. Besplatni plan spava i ima premalo memorije za ffmpeg, pa odaberi najmanji plaćeni (provjeri cijenu; očekivano unutar 15–25 € mjesečno iz odluke 17).
3. U *Environment* upiši sve varijable iz `.env.example` s produkcijskim vrijednostima: novi `SECRET_KEY`, `DATABASE_URL` (*Internal URL* baze), R2 ključevi za `vjecnaspomen-prod`, SMTP podaci, `QR_BAZNI_URL`, `PRIJAVE_EMAIL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
4. CORS na `vjecnaspomen-prod` dopušta samo produkcijsku adresu.
5. E-mail servis: provjeri adresu pošiljatelja i postavi SPF/DKIM ako servis to traži. Bez vlastite domene e-mailovi mogu završiti u neželjenoj pošti, što je za demo prihvatljivo (vidi P-47).
6. Nakon prve objave: Render *Shell* → `python manage.py createsuperuser` i `python manage.py napuni_demo --da-sigurno`.
7. Uključi *Auto-Deploy* samo za `main`.

**Gotovo kada:**
- `https://<adresa>/g/<demo-kod>/` otvara zaključani ekran na mobitelu, preko HTTPS-a;
- prijava linkom stiže na stvarni e-mail;
- upload slike i videa s mobitela radi i obrađuje se;
- `curl -I http://<adresa>/` preusmjerava na HTTPS, a odgovor ima `Strict-Transport-Security` i `X-Robots-Tag`;
- nijedna tajna nije u repozitoriju ni u logovima objave.

**Procjena:** 4–6 sati.

> 🔁 **Predaja:** Petar predaje prijatelju javnu adresu demoa, demo kodove i lozinke te nekoliko neaktiviranih pločica s aktivacijskim kodovima (privatnom porukom). Time mogu krenuti **D-33** i **D-34**, a kasnije **D-37** i **D-38**.

### P-43 Integracija pravih predložaka i popravci nalaza testiranja
- [ ] Gotovo

**Cilj:** svi PR-ovi prijatelja s pravim predlošcima su pregledani i spojeni, a svi nalazi testiranja ozbiljnosti 1 i 2 iz GitHub Issues su popravljeni.

**Zašto:** mjerilo uspjeha 1 traži da tok radi na iPhoneu i Androidu, a velik dio korisnika su starije osobe (odluka 17, podjela posla).

**Preduvjeti:** D-25, D-26, D-27 i D-28 gotovi, D-33 i D-35 gotovi (nalazi u Issues).

> 🔁 **Predaja:** Prijatelj predaje Petru PR-ove s pravim predlošcima (**D-25** do **D-28**), nalaze prve runde testiranja kao issue i tablicu `docs/testiranje/runda-1.md` (**D-33**) te sažetak `docs/testiranje/nalazi.md` s issueima označenima `petar` (**D-35**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Za svaki PR prijatelja: pokreni ga lokalno, prođi tokove i provjeri da su ostale sve varijable, `{% csrf_token %}`, `name` atributi i `hx-*` atributi. Pokreni testove.
2. Prođi Issues s oznakom `nalaz-testiranja`. Ono što je backend (npr. poruka greške, dulji rok linka, novi podatak u kontekstu) popravi ti, a ono što je izgled vrati prijatelju s oznakom `prijatelj`.
3. Svaki popravak u zasebnom malom PR-u koji u opisu navodi broj issuea (`Popravlja #23`), pa se issue sam zatvori.
4. Ponovno pokreni `python manage.py makemessages -l hr` (treba GNU gettext: `brew install gettext`) i provjeri da nijedan tekst nije ostao izvan `{% translate %}`.

**Gotovo kada:**
- u `main` nema više ružnih privremenih predložaka (svi su zamijenjeni prijateljevim);
- nema otvorenih issuea `nalaz-testiranja` ozbiljnosti 1 ili 2;
- `makemessages` ne pronalazi tekstove u predlošcima koji nisu označeni za prijevod (provjera pretragom predložaka za hrvatske riječi izvan `translate` oznaka);
- svi testovi prolaze.

**Procjena:** 4–6 sati (ovisi o broju nalaza; ako ih je više, razbij na više PR-ova i ponovi korak).

> 🔁 **Predaja:** Petar javlja prijatelju da su popravci spojeni i objavljeni na demou. Time može krenuti **D-37**.

### P-44 Demo QR kodovi na papiru i provjera svih mjerila uspjeha
- [ ] Gotovo

**Cilj:** postoji ispisan list s demo QR pločicama i demo letkom. Petar i prijatelj zajedno su na stvarnim mobitelima prošli svih šest mjerila uspjeha MVP-a, a rezultat je zapisan u `docs/provjera-mvp.md`.

**Zašto:** nekoliko demo QR kodova ispisanih na papiru i provjera mjerila uspjeha (odluka 20).

**Preduvjeti:** P-43 gotov, D-31 gotov (dizajn pločice i letka), D-37 gotov (druga runda testiranja).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Iz demo serije preuzmi QR SVG datoteke. Prijatelj ih umeće u dizajn pločice (5 × 5 cm) i letka iz D-31. Ispiši list na običnom papiru u stvarnoj veličini (ispis bez skaliranja, „100 %”).
2. Provjera po mjerilima (svako na iPhoneu i Androidu):
   1. skeniranje demo koda kamerom → lozinka → profil;
   2. skeniranje neaktivirane demo pločice → aktivacijski kod s letka → cijeli čarobnjak → novi grob;
   3. upload slike i videa s mobitela, pa provjera obrade;
   4. poruka u knjizi sjećanja → odobrenje → prikaz;
   5. admin: novi partner, nova serija, mjesečni izvještaj (i pregled za partnera);
   6. javni demo radi, a repozitorij je uredan (README, nema tajni, testovi prolaze).
3. U `docs/provjera-mvp.md` zapiši za svako mjerilo: uređaj, preglednik, rezultat (✅/❌) i napomenu. Za svaki ❌ otvori issue i nakon popravka ponovi provjeru.

**Gotovo kada:**
- sva mjerila u `docs/provjera-mvp.md` imaju ✅ na barem jednom iPhoneu i jednom Android mobitelu;
- QR na ispisanoj pločici od 5 cm skenira se s 30–50 cm udaljenosti;
- nakon ponovnog skeniranja nakon 24 sata profil se otvara bez lozinke (pamćenje uređaja).

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** zajednički korak s prijateljem: on donosi ispisane demo pločice i letak (D-31) i rezultate druge runde testiranja (D-37). Petar donosi demo kodove i pristup adminu.

### P-45 README i opis arhitekture
- [ ] Gotovo

**Cilj:** README na GitHubu u nekoliko minuta objašnjava što je proizvod, kako radi, kako je građen i kako se pokreće, sa snimkama zaslona, dijagramom i linkom na demo.

**Zašto:** README s opisom arhitekture i uredan repozitorij za CV (odluka 20, mjerilo uspjeha 6).

**Preduvjeti:** P-42 gotov, D-38 gotov (snimke zaslona i video).

> 🔁 **Predaja:** Prijatelj predaje Petru snimke zaslona u `docs/slike/` i link na video demo (**D-38**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Struktura README-a:
   - naslov i jedna rečenica;
   - snimka zaslona ili GIF;
   - link na demo i na kratki video;
   - „Što radi” (tokovi posjetitelja, vlasnika i administratora u 3–4 točke);
   - „Arhitektura” (dijagram komponenti u Mermaidu: preglednik → Render (Django + gunicorn + django-q2) → PostgreSQL; preglednik ⇄ R2 preko potpisanih linkova; worker → ffmpeg → R2; e-mail servis);
   - dijagram modela (link na `docs/modeli.md`);
   - „Sigurnost” (lozinke kao hash, zaključavanje, potpisani kolačići, potpisani linkovi za medije, noindex, dozvole i testovi);
   - „Ključne odluke” (link na `docs/odluke.md`);
   - „Pokretanje lokalno”;
   - „Testovi”;
   - „Tim” (oba člana i uloge);
   - „Sva prava pridržana”.
2. Dodaj badge GitHub Actions testova.
3. Provjeri da README ne sadrži lozinke, demo lozinke ni privatne adrese.

**Gotovo kada:**
- osoba koja ne zna projekt (pitaj nekoga) iz README-a za 5 minuta može reći što aplikacija radi i kako je građena;
- novi klon repozitorija pokreće se lokalno samo prema README-u (provjeri u čistoj mapi);
- README završava napomenom „Sva prava pridržana”, a u repozitoriju nema datoteke `LICENSE`.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Petar javlja prijatelju da je README gotov (arhitektura, snimke). Time prijatelj može dovršiti **D-39**.

### P-46 Javna studija slučaja za CV
- [ ] Gotovo

**Cilj:** postoji javna studija slučaja (stranica u repozitoriju `docs/studija-slucaja.md` ili na osobnoj stranici) koja opisuje problem, rješenje, tehničke izazove i Petrov doprinos.

**Zašto:** primarni cilj MVP-a je portfolio i CV (odluka 20).

**Preduvjeti:** P-45 gotov. Prijateljev dio (D-39) piše se usporedno, a spaja se prije završetka ovog koraka.

> 🔁 **Predaja:** Prijatelj predaje Petru svoj dio studije slučaja, o dizajnu i testiranju (**D-39**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Odjeljci:
   - problem i korisnici;
   - poslovni model ukratko (bez detalja pregovora i bez imena stvarnih osoba);
   - arhitektura;
   - tri tehnička izazova s rješenjem (npr. izravni upload velikih videa u R2 i obrada ffmpegom; privatnost: lozinka, pamćenje uređaja, potpisani linkovi; aktivacija bez online plaćanja i obračun po partneru);
   - što bi napravio drugačije;
   - sljedeći koraci (iz „Nije u MVP-u”).
2. Dizajnerski dio (proces, testiranje sa starijim osobama) piše prijatelj u D-39. Dogovorite jedan zajednički dokument s dva potpisana dijela.
3. Ne navodi stvarno groblje kao partnera, jer do veljače 2027. nema komunikacije s upravom (odluka 20). Piši „lokalno groblje kao prvi partner”.

**Gotovo kada:**
- studija slučaja je javno dostupna i linkana iz README-a;
- ne sadrži stvarne osobe, stvarne pokojnike ni povjerljive brojke;
- prijatelj je pregledao i odobrio tekst (PR).

**Procjena:** 3–4 sata.

### P-47 (Neobavezno) Registracija domene vjecnaspomen.hr
- [ ] Gotovo

**Cilj:** domene vjecnaspomen.hr (i vjecnaspomen.com) registrirane su na više godina, a demo radi na `https://vjecnaspomen.hr`.

**Zašto:** neobavezna rana registracija kako bi se zadržao naziv (odluka 20). Domena se plaća više godina unaprijed (odluke 12 i 18). Ovaj korak možeš napraviti u bilo kojem trenutku.

**Preduvjeti:** nema (za spajanje na hosting: P-42 gotov).

**Novi pojmovi:**
- **DNS** je sustav koji ime domene pretvara u adresu poslužitelja. Zapis **CNAME** usmjerava domenu na Renderovu adresu. [Render: Custom domains](https://render.com/docs/custom-domains)
- **CARNET / .hr registar:** .hr domene registriraju se preko ovlaštenih registrara, a uvjete za fizičke osobe provjeri na [domene.hr](https://www.domene.hr/).

**Upute:**
1. Provjeri dostupnost i cijenu kod registrara, te koliko se godina unaprijed može platiti (odluka 12).
2. Registriraj obje domene. Ako ne želiš dodatni trošak, dovoljna je .hr.
3. Na Renderu dodaj *Custom domain* i u DNS-u zapis prema uputama. Promijeni `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `QR_BAZNI_URL` i CORS na R2.
4. Postavi e-mail servis da šalje s `noreply@vjecnaspomen.hr` (SPF, DKIM).
5. **Pozor:** demo QR kodovi ispisani ranije vode na staru adresu. Ostavi staru Render adresu aktivnom ili ponovno ispiši demo kodove.

**Gotovo kada:**
- `https://vjecnaspomen.hr/g/<demo-kod>/` radi preko HTTPS-a;
- novi QR za `HTTPS://VJECNASPOMEN.HR/G/XXXXXX` je verzija 3 (provjera iz P-10).

**Procjena:** 1–2 sata (bez čekanja na DNS).

## Kasnije, ako krenemo u pilot

Ništa od ovoga ne radi se prije veljače 2027. ni prije zajedničke odluke o pilotu (odluka 20). Popis služi da se ne zaboravi.

**Razgovori i dogovori (odluke 2, 10, 14 i 19):**
- Pročitati gradski pravilnik o grobljima (što se smije postaviti na grob).
- Sastanak s direktorom uprave groblja: ponuda besplatnog pilota na 6 mjeseci, model veleprodaje, tko odobrava novu stavku u cjeniku, koji klesari rade na groblju.
- Savjetovanje s knjigovođom ili Obrtničkom komorom o obliku pravnog subjekta za studente (paušalni obrt ili j.d.o.o.) i otvaranje subjekta prije prve prodaje.
- Nacrti uvjeta korištenja (uključujući obvezu obavijesti 6 mjeseci prije gašenja i izvoz u ZIP), politike privatnosti i sporazuma o suradnji s upravom. Pregled pravnika (pravna klinika PFRI, STEP RI ili poznanik).
- Prijava na STEP RI, natjecanja poslovnih ideja i provjera programa za rane faze (HAMAG-BICRO).

**Pločice i izvođači (odluke 7, 8 i 9):**
- Pronaći lasersku radionicu (direktor groblja, Google Maps / eMajstor, RITEH) i dogovoriti fiksnu cijenu po komadu.
- Naručiti 3 do 5 testnih uzoraka i 2 do 3 mjeseca testirati izdržljivost (sol, mraz, ribanje).
- **Prije narudžbe pločica registrirati domenu** (P-47 tada više nije neobavezan) i stvoriti prvu pravu seriju od 50 pločica s `QR_BAZNI_URL=HTTPS://VJECNASPOMEN.HR/G/`.
- Dodati izvoz QR-a kao vektorske datoteke u točnoj veličini u milimetrima, s kratkim uputama za klesara.

**Tehnička priprema za stvarne korisnike:**
- Plan hostinga za pilot (odluka 17: oko 15–25 € mjesečno), dnevne sigurnosne kopije baze i provjera vraćanja iz kopije.
- Odvojiti pozadinski worker u zaseban servis ako obrada videa usporava stranicu.
- Pravila životnog ciklusa u R2 (brisanje napuštenih uploada u `ulaz/`) i praćenje troška pohrane prema fondu za čuvanje (odluka 12).
- Praćenje grešaka (npr. Sentry, besplatni plan) i obavijest nama kad prijava sadržaja prijeđe rok od 7 dana.
- Odluke o OP-2 i OP-3 (naplata dodatnog pokojnika, pilot cijena) prenijeti u kod.
- Odlučiti hoće li se repozitorij prebaciti u privatni (odluka 20).
- Praćenje mjerila pilota: 30 prodaja u 6 mjeseci, ≥ 80 % aktivacija (izvještaj iz P-37 već daje osnovu).

## Nije u MVP-u (namjerno)

Ove funkcije su u `docs/odluke.md` označene kao „faza 2”, „kasnije” ili „izvan opsega”. Ne planiraju se i ne rade prije odluke tima:

- **Urednik**, član obitelji kojeg vlasnik pozove (odluka 3).
- **Interaktivni vizualni prikaz obiteljskog stabla** kroz više generacija (odluka 3a).
- **Audio, vremenska crta života, virtualna svijeća, podsjetnici na godišnjice** (odluka 6).
- **Navigacija do groba** i karta groblja (odluke 6 i 11).
- **NFC** na pločici (odluka 7).
- **Online plaćanje**, uključujući dodatnu pohranu kao jednokratnu nadoplatu (odluke 10 i 12).
- **Prijava SMS-om** (odluka 19).
- **Nativna aplikacija** i obavijesti na mobitel (odluka 16).
- **Integracija s programom uprave groblja** (odluka 11).
- **Klesari kao prodajni kanal** i izravna web narudžba za postojeće grobove (odluke 1 i 9).
- **White-label licenca** (odluka 15).
- **Njemački i engleski prijevod** (odluka 18a). Tekstovi su ipak od početka u `{% translate %}`.
- **Specijalizirani video servisi** (Mux, Cloudflare Stream), odbačeni zbog mjesečne naplate (odluka 17).

## Otvorena pitanja

Ova pitanja `docs/odluke.md` ne pokriva, a za izvedbu su potrebna. Uz svako je prijedlog koji plan zasad slijedi. Odgovore zapišite u `docs/odluke.md` (najbolje na sastanku u P-01/D-01) i, ako se razlikuju od prijedloga, prilagodite korake.

| # | Pitanje | Prijedlog i obrazloženje | Koraci |
|---|---|---|---|
| OP-1 | Što se događa nakon „Zatraži pristup”? | Vlasnik dobiva e-mail i u vlasničkom dijelu vidi ime i poruku posjetitelja. Gumb „Pošalji obiteljski link” sustav šalje posjetitelju e-mailom, a „Odbij” samo zatvara zahtjev, bez obavijesti. Vlasnik tako ne mora nikome otkrivati lozinku. | P-24, D-08, D-22, D-26 |
| OP-2 | Kako se u MVP-u bilježi „dodatni pokojnik u postojeći grob” (49 €)? | Vlasnik u MVP-u dodaje pokojnike slobodno, a mjesečni izvještaj ih broji kao zasebnu stavku po partneru. Prije pilota treba odlučiti traži li se za to novi aktivacijski kod s računa uprave. | P-22, P-37 |
| OP-3 | Koja se cijena koristi u izvještaju (119 € ili pilot 49 €)? | Cijena se zapisuje na seriju pločica (`maloprodajna_cijena`). Pilot serija dobiva 49 €, a redovna 119 €. Iznos za partnera računa se iz postotka partnera. | P-06, P-37 |
| OP-4 | Pisani dogovor o udjelima 50/50: kada? | Prije javne objave demoa (P-42), jer tada kod i dizajn postaju javno vidljivi pod oba imena. | P-01, D-01 |
| OP-5 | Treba li potvrditi e-mail kontakta za prijavu prije završetka aktivacije? | Ne: osoba se u čarobnjaku odmah prijavljuje i dobiva e-mail dobrodošlice. Ako je adresa pogrešno upisana, ispravljamo je u adminu uz potvrdu (odluka 19). Starijim korisnicima tako ne treba prebacivanje između preglednika i e-pošte usred čarobnjaka. | P-19, D-21 |
| OP-6 | Kako se bilježi pristanak živuće osobe na prikaz imena (odluka 3a)? | Vlasnik označava kvačicu „Osoba je pristala da se njezino ime prikaže”. Bez kvačice srodnik se posjetiteljima ne prikazuje. Zahtjev za uklanjanje ide kroz gumb „Prijavi”. | P-22, P-34, D-23 |
| OP-7 | Može li vlasnik sam obrisati cijeli grob? | Ne. Vlasnik briše pokojnike i medije, a grob (pločicu) samo administrator, jer je pločica fizički na grobu i plaćena. | P-22, P-35 |
| OP-8 | Koji e-mail servis za slanje linkova u demou? | Besplatni plan servisa s poslužiteljima u EU (npr. Brevo), preko SMTP-a. Trošak je nula, a može se zamijeniti bez promjene koda. | P-42 |
| OP-9 | Smije li se u studiji slučaja i README-u spomenuti Crikvenica? | Ne do odluke o pilotu. Piše se „lokalno groblje”, jer do veljače 2027. nema komunikacije s upravom. | P-46, D-39 |

## Odluka → koraci

Svaka MVP odluka iz `docs/odluke.md` pokrivena je barem jednim korakom. Koraci prijatelja navedeni su radi potpunosti.

| Odluka | Što iz nje ulazi u MVP | Koraci (Petar) | Koraci (prijatelj) |
|---|---|---|---|
| 1. Tko plaća i tko prodaje | partner s postotkom, obračun iz pločice | P-06, P-37 | – (pregovori: „Kasnije”) |
| 2. Pilot lokacija | rad na daljinu (obiteljski link, javni demo) | P-23, P-42 | D-04 |
| 3. Uloge i uređivanje | vlasnik, posjetitelj, prijava linkom, odobravanje, usluga postavljanja | P-17, P-21, P-22, P-33, P-35 | D-04, D-22, D-23, D-26, D-27 |
| 3a. Obiteljsko stablo | odjeljak „Obitelj”, srodnici, živuće osobe samo ime uz pristanak | P-07, P-14, P-22 | D-09, D-18, D-23, D-27 |
| 4. QR kod po grobu | jedan QR po grobu, popis pokojnika, izravni profil kad je pokojnik jedan, novi pokojnik bez nove pločice | P-07, P-11, P-22 | D-08, D-17 |
| 5. Privatnost i pristup | zaključani ekran, lozinka ≥ 6, pamćenje uređaja, obiteljski link, zahtjev za pristup, zaključavanje, potpisani linkovi, noindex, javni prikaz | P-12, P-13, P-15, P-16, P-21, P-23, P-24, P-26 | D-08, D-17, D-22, D-26 |
| 6. Opseg profila | biografija, galerija, video, obitelj, knjiga sjećanja | P-14, P-31, P-33 | D-09, D-10, D-11, D-18, D-19, D-20 |
| 7. Fizička oznaka | QR s korekcijom H, kratki kod ispod koda, trajni link | P-10 | D-31 |
| 8. Izrada i aktivacija kodova | serije, aktivacijski kod, čarobnjak, neaktivirana pločica ne otkriva ništa, partner na pločici | P-06, P-10, P-11, P-18, P-19, P-20 | D-21, D-25 |
| 9. Odnos s izvođačima | – (samo demo QR datoteke) | P-10 | D-31 (ostalo „Kasnije”) |
| 10. Naplata | bez plaćanja u aplikaciji, mjesečni izvještaj | P-37 | D-24, D-28 |
| 11. Lokacija groba | tekstualna oznaka, nevidljiva posjetiteljima, u izvještaju | P-07, P-19, P-37 | D-21 |
| 12. Jednokratna cijena i čuvanje | ograničenja po grobu, kompresija videa, izvoz u ZIP | P-08, P-28, P-30, P-31, P-36 | D-23, D-27 |
| 13. Cijena | cijena na seriji za izvještaj (OP-3) | P-06, P-37 | – |
| 14. Financiranje | samo trošak hostinga i neobavezne domene | P-42, P-47 | – |
| 15. Strategija rasta | više partnera od prvog dana, ime partnera na zaključanom ekranu, pregled za partnera | P-06, P-12, P-38 | D-08, D-24, D-28 |
| 16. Web aplikacija | mobile-first, tri dijela, PWA za vlasnike | P-05, P-11, P-21, P-35, P-39 | D-05 do D-28, D-30 |
| 17. Tim i tehnologije | Django, HTMX, Tailwind, PostgreSQL, admin, django-sesame, R2, ffmpeg, django-q2, Render | P-03 do P-05, P-17, P-26, P-27, P-30, P-41, P-42 | D-03, D-13 do D-15, D-32 do D-36 |
| 18. Naziv, domena i format koda | 6 znakova bez 0/O/1/I/L, velika slova u QR-u, rute bez razlike velikih i malih slova, aktivacijski kod od 8 znakova, ograničenja datoteka | P-06, P-10, P-11, P-18, P-28, P-29, P-30, P-47 | D-31 |
| 18a. Jezik | samo hrvatski, tekstovi kroz `{% translate %}` | P-05, P-43 | D-13, D-16 do D-28 |
| 19. Vlasništvo i moderacija | vlasnik i kontakt za prijavu odvojeni, knjiga uz odobrenje, „Prijavi” s rokom 7 dana, GDPR prednost | P-07, P-19, P-33, P-34, P-35 | D-11, D-20, D-21 |
| 20. Tempo i cilj | javni repo bez licence, demo podaci, javni demo, ispisani QR, README | P-02, P-40, P-42, P-44, P-45, P-46 | D-07, D-31, D-37, D-38, D-39 |

### Mjerila uspjeha MVP-a (odluka 20) → koraci

| Mjerilo | Koraci |
|---|---|
| 1. skeniranje demo koda → lozinka → profil na iPhoneu i Androidu | P-10, P-11, P-12, P-14, P-42, P-44 (+ D-17, D-18, D-31, D-33, D-37) |
| 2. aktivacija nove pločice od početka do kraja | P-18, P-19, P-20, P-25 (+ D-21, D-25) |
| 3. upload slike i videa s mobitela uz automatsku obradu | P-26 do P-32 (+ D-27) |
| 4. knjiga sjećanja s odobravanjem | P-33 (+ D-20, D-27) |
| 5. administracija: partneri, serije pločica, mjesečni izvještaj | P-09, P-10, P-35, P-37, P-38 (+ D-28) |
| 6. javno dostupan demo i uredan repozitorij za CV | P-02, P-16, P-40 do P-42, P-45, P-46 (+ D-38, D-39) |
