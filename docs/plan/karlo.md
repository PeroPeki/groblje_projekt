# Plan rada: Karlo (dizajn, predlošci i testiranje)

Dizajn svih ekrana u Figmi, pretvaranje dizajna u HTML i Tailwind CSS predloške (Django templates) te testiranje na stvarnim mobitelima i sa starijim osobama za aplikaciju „Vječna spomen” (vjecnaspomen.hr).

## Kako koristiti ovaj plan

Radi korake redom kojim su numerirani. Ako korak čeka na Petra (vidi „Preduvjeti” i blokove „🔁 Predaja”), prijeđi na sljedeći dizajnerski korak bez te ovisnosti, jer Figma ne čeka kod. Kad je korak gotov i svi uvjeti iz „Gotovo kada” su ispunjeni, u svom PR-u promijeni `- [ ] Gotovo` u `- [x] Gotovo`. Pomoć traži redom: link u „Novi pojmovi”, službena dokumentacija, issue s oznakom `pitanje`, pa poruka Petru.

Pojmove iz rječnika u `docs/odluke.md` (grob, QR oznaka, pločica, pokojnik, profil, vlasnik, kontakt za prijavu, posjetitelj, partner, aktivacija, aktivacijski kod, knjiga sjećanja, srodnik) koristi točno tako u Figmi, na ekranima i u nazivima komponenti. Velik dio korisnika su starije osobe, pa je svaka odluka o dizajnu i pitanje čitljivosti: veliki fontovi, jak kontrast, velike tipke, jednostavan jezik.

**Verzije alata** (provjereno u studenom 2026.; pri instalaciji ipak provjeri najnoviju stabilnu verziju): Python 3.13 ili 3.14, Django 6.1, Tailwind CSS 4.3 (pokreće se kroz Django, Node.js nije potreban), HTMX 2.x.

## Pregled

| Faza | Cilj | Koraci | Procjena |
|---|---|---|---|
| 1. Početak | Alati, Git i GitHub te projekt pokrenut na tvom računalu. | 3 (D-01 – D-03) | 7–10 h |
| 2. Temelji dizajna | Korisnički tokovi, vizualni identitet, komponente u Figmi i izmišljeni demo sadržaj. | 4 (D-04 – D-07) | 14–21 h |
| 3. Dizajn javnog dijela | Zaključani ekran, grob, profil, galerija, video i knjiga sjećanja u Figmi, isprobani sa starijim osobama. | 5 (D-08 – D-12) | 12–17 h |
| 4. Predlošci javnog dijela | Osnove Django predložaka, Tailwinda i HTMX-a, zatim pravi predlošci javnog dijela. | 8 (D-13 – D-20) | 23–31 h |
| 5. Aktivacija i vlasnički dio | Dizajn i predlošci čarobnjaka, vlasničkog dijela, grešaka, e-mailova i pregleda za partnera. | 8 (D-21 – D-28) | 25–37 h |
| 6. Pristupačnost i materijali | Provjera pristupačnosti, ikone za početni zaslon, demo QR pločica i letak. | 3 (D-29 – D-31) | 7–11 h |
| 7. Testiranje | Plan testiranja, testiranje na mobitelima i sa starijim osobama, popravci nalaza. | 6 (D-32 – D-37) | 19–27 h |
| 8. Prezentacija za CV | Snimke zaslona, video demo i dizajnerski dio studije slučaja. | 2 (D-38 – D-39) | 6–8 h |
| **Ukupno** | | **39** | **113–162 h** |

## Zajednički način rada

Ovaj odjeljak je isti u oba plana. Ako ga jedan od vas promijeni, promijenite ga u oba dokumenta u istom pull requestu.

### Gdje što stoji

| Što | Gdje |
|---|---|
| Kod, predlošci, statičke datoteke, dokumentacija | javni GitHub repozitorij (Petar je vlasnik, Karlo je *collaborator* s pravom pisanja) |
| Dizajn | jedna Figma datoteka „Vječna spomen – MVP” sa stranicama: *Tokovi*, *Identitet*, *Komponente*, *Javni dio*, *Aktivacija*, *Vlasnik*, *Partner*, *Greške i prazna stanja*, *Pločica i letak* |
| Bugovi, nalazi testiranja, pitanja | GitHub Issues, s oznakama (*labels*) `bug`, `dizajn`, `nalaz-testiranja`, `pitanje`, `petar`, `prijatelj` |
| Napredak po planu | kvačica `- [x] Gotovo` u vlastitom planu (`docs/plan/petar.md` ili `docs/plan/prijatelj.md`) |
| Tajni podaci (lozinke, ključevi) | samo u lokalnoj datoteci `.env` i u postavkama hostinga. Drugome ih šaljete privatnom porukom, nikad kroz Git, Issues ni Figmu |

### Grane i pull requestovi

1. Grana `main` uvijek radi. Nitko ne šalje promjene (*push*) izravno u `main`, jer je uključena zaštita grane.
2. Za svaki korak napravi novu granu nazvanu po ID-u koraka, npr. `p-12-zakljucani-ekran` ili `d-17-predlozak-zakljucanog-ekrana`.
3. Kad je korak gotov, pošalji granu na GitHub i otvori *pull request* (PR) prema `main`. U opisu navedi ID koraka, što si napravio i kako drugi to može provjeriti. Ako se mijenja izgled, dodaj snimku zaslona s mobitela.
4. **Svaki PR pregledava drugi član tima.**
   - Petar pri pregledu Karlovih PR-ova provjerava da predlošci nisu izgubili varijable, `{% csrf_token %}`, `name` atribute polja i `hx-*` atribute.
   - Karlo pri pregledu Petrovih PR-ova provjerava tekstove, izgled i radi li stvar kad je pokrene lokalno. Python kod ne mora razumjeti do kraja.
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
│   ├── css/ulaz.css     # izvorni Tailwind CSS (ovo se uređuje)
│   ├── js/              # mali vlastiti JavaScript (npr. upload)
│   ├── img/             # ikone, logotip
│   ├── fontovi/         # fontovi koje poslužujemo sami
│   └── vendor/          # htmx.min.js i slične preuzete datoteke
├── demo/                # izmišljeni demo sadržaj i popis izvora fotografija
├── docs/                # odluke, planovi, dijagram modela, popis predložaka
├── .env.example         # popis potrebnih varijabli BEZ stvarnih vrijednosti
└── README.md
```

Predlošci su namjerno u jednoj mapi `templates/` na razini projekta, a ne razbacani po aplikacijama. Tako Karlo sve što uređuje ima na jednom mjestu.

### Ugovor između pogleda i predloška

- Petar za svaki ekran prvo napravi „ružan” privremeni predložak koji radi. Na vrhu predloška stoji komentar s popisom varijabli koje pogled šalje, npr. `{# Varijable: grob (Grob), pokojnici (lista Pokojnik), greska (str ili None) #}`. Isti popis vodi se u `docs/predlosci.md`.
- Karlo zatim mijenja HTML strukturu i Tailwind klase. **Bez dogovora ne mijenja** imena varijabli, `name` atribute polja u formama, `{% csrf_token %}`, `hx-*` atribute ni nazive u `{% url '...' %}`.
- Ako predlošku treba još neki podatak (npr. broj poruka na čekanju), Karlo otvori issue s oznakom `petar` i Petar ga doda u pogled.
- Svaki tekst koji korisnik vidi piše se kroz `{% translate "..." %}` ili `{% blocktranslate %}`, iako je aplikacija zasad samo na hrvatskom (odluka 18a).

### Tajni podaci i javni repozitorij

- Datoteka `.env` je u `.gitignore` i nikad ne ide u Git. U Git ide samo `.env.example`, s nazivima varijabli i praznim ili izmišljenim vrijednostima.
- Prije svakog commita pogledaj što šalješ (`git status`, `git diff --staged`).
- Ako ključ ipak završi na GitHubu, **odmah ga poništi i napravi novi** u servisu iz kojeg je došao (Cloudflare, Render, e-mail servis). Brisanje iz povijesti nije dovoljno, jer je repozitorij javan i netko ga je možda već kopirao.
- Demo sadržaj koristi samo izmišljene osobe i fotografije sa slobodnom licencom. Nikad stvarne pokojnike ni stvarne obitelji, pa ni svoje.

## Faza 1: Početak

Alati, Git i GitHub te projekt pokrenut na tvom računalu.

### D-01 Zajednički početak: alati i prvi sastanak
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
7. Petar napravi Figma datoteku „Vječna spomen – MVP” ili je napravi Karlo i pozove Petra s pravom uređivanja.

**Gotovo kada:**
- oba člana u terminalu vide verzije Gita i Pythona;
- oba GitHub računa imaju uključenu dvostupanjsku prijavu;
- oba člana imaju pristup Figma datoteci;
- odgovori na otvorena pitanja (ili odluka da se odgađaju) zapisani su u `docs/odluke.md`.

**Procjena:** 3–4 sata (instalacija 1–2 h, sastanak 2 h).

**Česte greške:**
- Na Windowsu `python` otvara Microsoft Store umjesto Pythona. Instaliraj Python s python.org uz kvačicu „Add to PATH” ili u postavkama isključi *App execution aliases* za Python.
- Na macOS-u postoji stari sistemski Python. Uvijek koristi `python3`, a kasnije Python iz virtualnog okruženja.

### D-02 Git i GitHub za tvoj dio posla
- [ ] Gotovo

**Cilj:** imaš kopiju repozitorija na računalu i znaš napraviti granu, commit, push i pull request, te pregledati tuđi PR.

**Zašto:** cijeli tim radi kroz grane i pull requestove (vidi „Zajednički način rada”), a repozitorij je javan i ne smije sadržavati tajne (odluka 20).

**Preduvjeti:** D-01 gotov, P-02 gotov (Petar te pozvao kao *collaboratora*).

> 🔁 **Predaja:** Petar predaje Karlu pristup repozitoriju (pozivnica za *collaboratora*, korak **P-02**). Tek tada ovaj korak može krenuti.

**Novi pojmovi:**
- **Kloniranje (*clone*)** je preuzimanje repozitorija s GitHuba na računalo, zajedno s poviješću.
- **Commit** je spremljena točka u povijesti projekta, s porukom što je promijenjeno.
- **Grana (*branch*)** je odvojena linija rada. Na njoj mijenjaš datoteke bez diranja glavne grane `main`. [Pro Git: Branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- **Push** šalje tvoje commitove na GitHub, a **pull** preuzima tuđe.
- **Pull request (PR)** je zahtjev da se tvoja grana spoji u `main`. Petar ga prije spajanja pregleda. [GitHub: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- **Pregled PR-a (*review*)** je čitanje tuđih promjena i ostavljanje komentara ili odobrenja. [GitHub: Reviewing changes](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- **`.gitignore`** je popis datoteka koje Git ne prati, npr. `.env` s tajnama.

**Upute:**
1. Prihvati pozivnicu u e-mailu ili na GitHubu.
2. Kloniraj repozitorij. U **GitHub Desktopu**: *File → Clone repository* i odaberi `vjecnaspomen`. U terminalu:
   ```
   git clone https://github.com/<petrov-korisnik>/vjecnaspomen.git
   cd vjecnaspomen
   ```
3. Probni krug:
   ```
   git switch -c d-02-proba
   ```
   U `docs/plan/prijatelj.md` označi D-01 kao gotov (`- [x] Gotovo`).
   ```
   git add docs/plan/prijatelj.md
   git commit -m "D-01 gotov"
   git push -u origin d-02-proba
   ```
   U GitHub Desktopu isto napraviš gumbima *Current branch → New branch*, *Commit to d-02-proba* i *Publish branch*.
4. Na GitHubu otvori PR („Compare & pull request”). U opis napiši „D-01 gotov, probni PR”. Petar ga pregleda i spoji.
5. Vrati se na `main` i povuci promjene: `git switch main && git pull` (Desktop: *Fetch origin → Pull*).
6. Pregledaj jedan Petrov PR: otvori karticu *Files changed*, ostavi barem jedan komentar i klikni *Review changes → Approve*.

**Gotovo kada:**
- tvoj probni PR je spojen u `main`;
- pregledao si i odobrio barem jedan Petrov PR;
- `git status` u tvojoj kopiji kaže „nothing to commit, working tree clean” nakon `git pull`.

**Procjena:** 2–3 sata.

**Česte greške:**
- Rad izravno na `main` umjesto na grani. GitHub će odbiti push. Napravi granu (`git switch -c ...`), pa push s nje.
- Zaboravljen `git pull` prije nove grane, pa grana kreće od stare verzije i kasnije ima sukobe (*merge conflicts*).

### D-03 Pokretanje projekta na svom računalu
- [ ] Gotovo

**Cilj:** projekt radi na tvom računalu na `http://localhost:8000`, Tailwind automatski osvježava CSS, a možeš se prijaviti u Django admin.

**Zašto:** bez lokalnog pokretanja ne možeš izrađivati ni provjeravati predloške (odluka 17).

**Preduvjeti:** D-02 gotov, P-05 gotov.

> 🔁 **Predaja:** Petar predaje Karlu projekt koji se može pokrenuti, s README uputama za macOS i Windows, strukturom mapa `templates/` i `static/`, `base.html` i `docs/predlosci.md` (korak **P-05**). Isti `base.html` kasnije preuređuješ u D-16.

**Novi pojmovi:**
- **Virtualno okruženje (*venv*)** je mapa s Pythonom i paketima samo za ovaj projekt, da se ne miješaju s drugim projektima. [Python: venv](https://docs.python.org/3/library/venv.html)
- **`requirements.txt`** je popis Python paketa koje projekt treba. `pip install -r requirements.txt` ih sve instalira.
- **`.env`** je datoteka s postavkama i tajnama za tvoje računalo. Nikad ne ide u Git. Predložak je `.env.example`.
- **SQLite** je baza podataka u jednoj datoteci, bez instalacije. Lokalno ti je dovoljna. Petar i hosting koriste PostgreSQL. [Django: Databases](https://docs.djangoproject.com/en/6.1/ref/databases/)
- **Migracije** stvaraju tablice u bazi prema modelima. Pokreneš ih naredbom `python manage.py migrate` nakon svakog `git pull` u kojem je Petar mijenjao modele. [Django: Migrations](https://docs.djangoproject.com/en/6.1/topics/migrations/)
- **Django admin** je gotovo administratorsko sučelje na `/admin/`. [Django: Admin](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)

**Upute:**
1. U mapi projekta:

   | | macOS | Windows (PowerShell) |
   |---|---|---|
   | napravi venv | `python3 -m venv .venv` | `python -m venv .venv` |
   | uključi venv | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
   | instaliraj pakete | `pip install -r requirements.txt` | isto |

2. Kopiraj `.env.example` u `.env` (macOS: `cp .env.example .env`, Windows: `copy .env.example .env`). Promijeni `DATABASE_URL=sqlite:///db.sqlite3` i upiši bilo koji dugi `SECRET_KEY`.
3. Pokreni:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py tailwind runserver
   ```
   Prvi put `tailwind` preuzima Tailwind program, pa treba malo pričekati.
4. Otvori `http://localhost:8000` i `http://localhost:8000/admin/`.
5. Probaj: promijeni jednu Tailwind klasu u `templates/javno/pocetna.html` (npr. `text-4xl` u `text-6xl`) i osvježi stranicu.
6. Zapiši u README sve što ti nije bilo jasno ili nije radilo (PR s ispravkom uputa).
7. Kasnije (od P-14) naredba `python manage.py napravi_probni_grob` daje ti probni grob, a (od P-40) `python manage.py napuni_demo` cijeli demo. Za rad s uploadom medija trebaš pristupne podatke za R2 dev spremnik (Petar ti ih šalje privatno, u tvoj `.env`). Za video trebaš i ffmpeg (macOS: `brew install ffmpeg`, Windows: `winget install Gyan.FFmpeg`) te treći terminal s `python manage.py qcluster`.

**Gotovo kada:**
- početna stranica i admin rade na tvom računalu;
- promjena Tailwind klase vidi se nakon osvježavanja;
- `git status` ne prikazuje `.env` ni `db.sqlite3`.

**Procjena:** 2–3 sata.

**Česte greške:**
- Windows: „running scripts is disabled on this system” pri uključivanju venv-a. Jednom pokreni `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- Zaboravljeno uključivanje venv-a u novom terminalu, pa javlja „No module named django”.

## Faza 2: Temelji dizajna

Korisnički tokovi, vizualni identitet, komponente u Figmi i izmišljeni demo sadržaj.

### D-04 Korisnički tokovi
- [ ] Gotovo

**Cilj:** na Figma stranici *Tokovi* (ili u FigJamu) postoje dijagrami toka za posjetitelja, vlasnika, administratora i partnera, s popisom svih ekrana koje treba dizajnirati.

**Zašto:** jedna aplikacija s tri dijela, javnim, vlasničkim i administracijom (odluka 16). Tokovi otkrivaju svaki ekran i stanje prije nego što počne crtanje.

**Preduvjeti:** D-01 gotov. Ne čeka Petra.

**Novi pojmovi:**
- **Korisnički tok (*user flow*)** je dijagram koraka kojima korisnik dolazi do cilja: ekrani su kvadrati, odluke rombovi, a strelice prijelazi. [Figma: FigJam](https://help.figma.com/hc/en-us/search?query=figjam)
- **Stanje ekrana** je varijanta istog ekrana: prazno, s greškom, učitavanje, uspjeh.

**Upute:**
1. Napravi tokove (sve iz `docs/odluke.md`, odluke 3, 4, 5, 8, 15 i 19):
   - **Posjetitelj na grobu:** skenira QR → zaključani ekran → lozinka (točna / pogrešna / previše pokušaja) → stranica groba (ako je pokojnika više) → profil → galerija / video / knjiga sjećanja / „Prijavi”.
   - **Posjetitelj na daljinu:** dobije obiteljski link porukom → profil bez lozinke. Ili nema ništa → „Zatraži pristup” → čeka vlasnika.
   - **Neaktivirana pločica:** skenira → „Upišite aktivacijski kod” → čarobnjak (kod → podaci groba i lozinka → prvi pokojnik → slike → gotovo).
   - **Vlasnik:** prijava e-mailom → link u e-pošti → popis grobova → grob → uređivanje pokojnika, srodnika i medija, odobravanje poruka, zahtjevi za pristup, lozinka, obiteljski link, javni prikaz.
   - **Administrator (Petar i ti):** Django admin → partner → nova serija → preuzimanje kodova → mjesečni izvještaj → prijave sadržaja.
   - **Partner:** prijava e-mailom → pregled → mjesečni izvještaj.
2. Uz svaki tok napiši tko je korisnik i u kakvoj je situaciji: npr. „baka od 75 godina na groblju, sunce, jedna ruka zauzeta cvijećem” ili „unuk u Njemačkoj, na kauču”.
3. Na kraju napravi tablicu svih ekrana i stanja. Ona postaje popis za D-08 do D-24.

**Gotovo kada:**
- postoje tokovi za sve četiri vrste korisnika;
- svaki ekran iz tokova ima ime i nalazi se u tablici ekrana;
- Petar je pregledao tokove (komentar u Figmi) i potvrdio da odgovaraju onome što gradi.

**Procjena:** 3–4 sata.

### D-05 Vizualni identitet
- [ ] Gotovo

**Cilj:** na Figma stranici *Identitet* postoje moodboard, paleta boja s provjerenim kontrastom, odabrani fontovi s veličinama, jednostavan logotip (tekstualni znak „Vječna spomen”) i načela tona teksta.

**Zašto:** proizvod mora biti dostojanstven, smiren i čitljiv starijima, jer je velik dio korisnika starije životne dobi (podjela posla, odluka 17). Odluke o fontu i boji idu u Tailwind temu (D-14).

**Preduvjeti:** D-04 gotov.

**Novi pojmovi:**
- **Kontrast** je omjer svjetline teksta i pozadine. Pravila pristupačnosti **WCAG** traže najmanje 4,5 : 1 za običan tekst (razina AA), a 7 : 1 za razinu AAA. [WCAG 2.2: Contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- **Moodboard** je ploča s primjerima (fotografije, boje, fontovi, tuđi ekrani) koji pokazuju željeni dojam.

**Upute:**
1. Moodboard: 15–25 primjera dostojanstvenog i smirenog dojma (spomen-knjige, tiskane osmrtnice, muzejske stranice, mirni pejzaži). Dodaj i 3–5 primjera konkurenata iz odluke 13 (LOGRO, Spominko, Gedankraum ...) i zapiši što ne želiš ponoviti.
2. Paleta:
   - topla neutralna pozadina (ne čisto bijela, ne crna);
   - tamna boja teksta;
   - jedna primarna boja za glavne gumbe;
   - boje za uspjeh, upozorenje i grešku.

   Svaki par tekst/pozadina provjeri u WebAIM Contrast Checkeru i upiši omjer u Figmu. **Cilj je 7 : 1 za tekst, a najmanje 4,5 : 1 za sve ostalo.**
3. Fontovi: jedan za tekst, izrazito čitljiv (prijedlog: **Atkinson Hyperlegible Next**, napravljen za slabovidne), i po želji jedan za naslove (npr. serifni). Provjeri da font ima sve hrvatske znakove: `č ć đ š ž Č Ć Đ Š Ž`. Font mora imati slobodnu licencu (npr. SIL Open Font License) i **poslužujemo ga sami**, a ne s Google Fonts poslužitelja, zbog privatnosti posjetitelja (GDPR).
4. Veličine teksta (mobitel): osnovni tekst najmanje **18 px** (prijedlog 19–20 px), visina retka 1,5. Naslovi 28–36 px. Ništa manje od 16 px, ni sitni tekst.
5. Ton teksta: obraćanje s „Vi”, kratke rečenice, bez tehničkih riječi („link” je u redu, „token” i „sesija” nisu), bez uskličnika i bez veselih ukrasa. Riječi iz rječnika („pokojnik”, „knjiga sjećanja”) koriste se dosljedno.
6. Preporuka: bez vjerskih simbola u osnovnom dizajnu, jer usluga služi obiteljima različitih uvjerenja. Ako se tim ne slaže, zapišite odluku u `docs/odluke.md`.
7. Logotip: zasad samo tekstualni znak i mala ikona (osnova za D-30).

**Gotovo kada:**
- svaki par boja tekst/pozadina ima zapisan omjer kontrasta ≥ 4,5 : 1, a osnovni tekst ≥ 7 : 1;
- odabrani font prikazuje `č ć đ š ž Č Ć Đ Š Ž` i ima slobodnu licencu (zapisanu u Figmi);
- osnovna veličina teksta na mobitelu je ≥ 18 px;
- Petar je komentirao i prihvatio identitet.

**Procjena:** 4–6 sati.

### D-06 Komponente u Figmi
- [ ] Gotovo

**Cilj:** na Figma stranici *Komponente* postoje sve ponovljive komponente s varijantama: gumbi, polja forme, poruke, kartice, navigacija, trake napretka i dijalog za potvrdu.

**Zašto:** iste komponente se pretvaraju u iste Django komponente (`templates/komponente/`), pa dizajn i kod ostaju dosljedni (odluka 17).

**Preduvjeti:** D-05 gotov.

**Novi pojmovi:**
- **Komponenta i varijante u Figmi:** jedna glavna komponenta (npr. gumb) s varijantama (primarni, sekundarni, onemogućen, učitavanje). Promjena glavne mijenja sve kopije. [Figma: Components](https://help.figma.com/hc/en-us/search?query=components), [Variants](https://help.figma.com/hc/en-us/search?query=variants)
- **Varijable i stilovi u Figmi** čuvaju boje, razmake i fontove pod imenom (npr. `boja/primarna`). Ta imena kasnije postaju Tailwind tema. [Figma: Variables](https://help.figma.com/hc/en-us/search?query=variables)
- **Auto layout** u Figmi slaže elemente kao što će ih slagati CSS (flex), pa je prijenos u Tailwind lakši. [Figma: Auto layout](https://help.figma.com/hc/en-us/search?query=auto%20layout)

**Upute:**
1. Boje, razmaci (koristi korake od 4 px, kao Tailwind) i fontovi kao varijable i stilovi.
2. Komponente:
   - **Gumb:** primarni, sekundarni, tekstualni i opasni (brisanje). Stanja: normalno, pritisnuto, fokus, onemogućeno, učitavanje. **Visina najmanje 48 px**, na mobitelu preko cijele širine.
   - **Polje forme:** oznaka iznad polja (nikad samo *placeholder*), pomoćni tekst, stanje greške s tekstom i ikonom. Polje lozinke ima gumb „Prikaži”.
   - **Poruka (obavijest):** uspjeh, informacija, upozorenje, greška. Nikad samo bojom, uvijek i tekstom.
   - **Kartica pokojnika** (slika, ime, godine), redak srodnika, redak poruke u knjizi sjećanja.
   - **Traka napretka** (upload) i indikator „Korak X od 4”.
   - **Dijalog za potvrdu** („Jeste li sigurni?”).
   - **Zaglavlje i podnožje** (podnožje s malim linkom „Prijavi sadržaj” i nazivom servisa).
3. Fokus mora biti jasno vidljiv (obrub od najmanje 3 px u boji visokog kontrasta).

**Gotovo kada:**
- sve navedene komponente postoje kao Figma komponente s varijantama;
- svaki gumb i polje je visok ≥ 48 px;
- nijedna obavijest ne oslanja se samo na boju;
- boje i razmaci korišteni su kao varijable, a ne kao ručno upisane vrijednosti.

**Procjena:** 4–6 sati.

### D-07 Izmišljeni demo sadržaj
- [ ] Gotovo

**Cilj:** u mapi `demo/` postoje izmišljene obitelji s pokojnicima, biografijama, srodnicima i porukama u knjizi sjećanja (u `demo/sadrzaj.json`), slike i kratki video sa slobodnom licencom te `demo/IZVORI.md` s izvorom i licencom svake datoteke.

**Zašto:** MVP mora imati izmišljeni demo grob s pokojnicima, slikama i videom, uz isključivo izmišljene osobe i slobodne fotografije (odluka 20). Dizajn je uvjerljiviji s realnim tekstovima nego s „Lorem ipsum”.

**Preduvjeti:** D-01 gotov. Ne čeka Petra.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Dvije izmišljene obitelji:
   - „Obitelj Kovačić” s 3 pokojnika (npr. djed, baka i sin) i jednim videom;
   - „Obitelj Perić” s 1 pokojnikom (tako se provjerava da grob s jednim pokojnikom odmah otvara profil).

   Provjeri pretragom da kombinacija imena, mjesta i godina ne odgovara stvarnoj osobi.
2. Biografije od 150 do 400 riječi, pisane toplo i obično, kako bi ih pisala obitelj (posao, mjesto, hobiji, obitelj). Jedna neka bude vrlo kratka (2 rečenice), da se vidi kako izgleda kratka biografija.
3. Srodnici: barem jedan povezani pokojnik (npr. „supruga” → profil bake) i jedna živuća osoba samo s imenom („unuka Ana”).
4. Poruke u knjizi sjećanja: 5 odobrenih i 2 na čekanju, različite duljine, od izmišljenih autora.
5. Slike (Unsplash, Pexels ili slično sa slobodnom licencom): 15–25 komada. **Preporuka:** za pokojnike koristi fotografije bez prepoznatljivih lica (ruke, predmeti, mjesta, krajolici, ljudi s leđa). Stvarne osobe s fotografija tako ne prikazujemo kao „pokojnike”. Dodaj i nekoliko uspravnih i vodoravnih slika te jednu vrlo veliku (> 4000 px) za provjeru smanjivanja.
6. Video: jedan isječak od 30–90 sekundi sa slobodnom licencom (npr. Pexels: more, polje, ruke).
7. `demo/sadrzaj.json`, oblik koji Petar čita u P-40:
   ```json
   {
     "grobovi": [{
       "naziv": "Obitelj Kovačić",
       "lozinka": "demo-kovacic",
       "pokojnici": [{
         "ime": "Ivan", "prezime": "Kovačić",
         "datum_rodjenja": "1931-03-12", "datum_smrti": "2019-11-02",
         "biografija": "…",
         "slike": [{"datoteka": "slike/ivan-01.jpg", "opis": "Ivanov alat u radionici"}],
         "videi": [],
         "srodnici": [{"vrsta": "supruga", "pokojnik": "Marija Kovačić"}],
         "poruke": [{"autor": "Susjeda Vesna", "tekst": "…", "odobrena": true}]
       }]
     }]
   }
   ```
8. `demo/IZVORI.md`: za svaku datoteku naziv, autor, link i licenca.

**Gotovo kada:**
- sve osobe su izmišljene i nijedna kombinacija imena i godina ne odgovara stvarnoj osobi koju si našao pretragom;
- svaka slika i video ima redak u `demo/IZVORI.md` s licencom koja dopušta korištenje;
- `demo/sadrzaj.json` je ispravan JSON (provjeri na [jsonlint.com](https://jsonlint.com/) ili u VS Codeu);
- ukupna veličina mape `demo/` je ispod 100 MB (video je kratak).

**Procjena:** 3–5 sati.

> 🔁 **Predaja:** Karlo predaje Petru `demo/sadrzaj.json`, `demo/slike/`, `demo/video/` i `demo/IZVORI.md` (PR u repozitorij). Time može krenuti **P-40**. Tekstove iz ovog koraka koristi i u Figmi (D-08 do D-11).

## Faza 3: Dizajn javnog dijela

Zaključani ekran, grob, profil, galerija, video i knjiga sjećanja u Figmi, isprobani sa starijim osobama.

### D-08 Dizajn: zaključani ekran, stranica groba i neaktivirana pločica
- [ ] Gotovo

**Cilj:** na Figma stranici *Javni dio* postoje mobilni ekrani (390 × 844 px i provjera na 360 px širine) za zaključani ekran sa svim stanjima, zahtjev za pristup, stranicu groba s popisom pokojnika i ekran neaktivirane pločice.

**Zašto:** nakon skeniranja otvara se zaključani ekran s imenom groba, poljem za lozinku i gumbom „Zatraži pristup” (odluka 5), uz ime groblja ili uprave (odluka 15). Grob s više pokojnika prikazuje popis (odluka 4). Neaktivirana pločica ne smije ništa otkriti (odluka 8).

**Preduvjeti:** D-06 gotov.

**Novi pojmovi:**
- **Mobile-first** znači da se dizajnira najprije za mobitel, a zatim se proširuje za veće zaslone. Većina posjetitelja dolazi skeniranjem na groblju (odluka 16).

**Upute:**
1. **Zaključani ekran:**
   - naziv groba (npr. „Obitelj Kovačić”), naziv partnera (npr. „Gradsko groblje Primjerovo”);
   - kratko objašnjenje („Ovu stranicu obitelj čuva lozinkom. Lozinku možete dobiti od obitelji.”);
   - polje za lozinku s gumbom „Prikaži”, primarni gumb „Otvori”, sekundarni „Zatraži pristup”.

   **Na zaključanom ekranu nema imena pokojnika, datuma ni slika.**
2. Stanja zaključanog ekrana: prazno, pogrešna lozinka, previše pokušaja („Pokušajte ponovno za 15 minuta”), obiteljski link više ne vrijedi, učitavanje.
3. **Zahtjev za pristup:** forma s poljima ime, e-mail i poruka (npr. „Ja sam Ivanov unuk iz Graza”), te ekran „Zahtjev je poslan” s objašnjenjem što slijedi.
4. **Stranica groba:** naziv groba i kartice pokojnika (slika, ime i prezime, godine), poredane kako ih je vlasnik poredao.
5. **Neaktivirana pločica:** „Ova pločica još nije aktivirana. Ako ste je dobili uz račun groblja, upišite aktivacijski kod s letka.” Polje za 8 znakova (velika slova, može s razmakom) i gumb „Nastavi”. Isti ekran prikazuje se i za kod koji ne postoji, pa nema naziva groblja ni drugih podataka.
6. Za svaki ekran napravi i verziju s povećanim tekstom (sistemska veličina fonta +30 %), da vidiš što se lomi.
7. Uz svaki ekran napiši bilješku za Petra: koji podaci dolaze iz baze, a koji su fiksni tekst.

**Gotovo kada:**
- postoje svi ekrani i stanja iz koraka 1–5 na 390 px, a provjereni su i na 360 px;
- zaključani ekran ne prikazuje nijedan podatak o pokojniku;
- svi tekstovi su stvarni (na hrvatskom), bez „Lorem ipsum”;
- polje lozinke ima gumb „Prikaži”, a svi gumbi su visoki ≥ 48 px.

**Procjena:** 3–4 sata.

### D-09 Dizajn: profil pokojnika (biografija i obitelj)
- [ ] Gotovo

**Cilj:** postoji mobilni dizajn profila pokojnika: zaglavlje sa slikom, imenom i datumima, biografija, odjeljak „Obitelj” i raspored odjeljaka za galeriju, video i knjigu sjećanja, sa svim praznim stanjima.

**Zašto:** profil je digitalna spomen-stranica s biografijom, slikama, videima, obitelji i knjigom sjećanja (rječnik, odluka 6). Odjeljak „Obitelj” prikazuje srodnike s vrstom srodstva, a živuće osobe samo imenom (odluka 3a).

**Preduvjeti:** D-08 gotov, D-07 gotov (tekstovi).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Zaglavlje: profilna slika (ili dostojanstvena zamjena ako slike nema, npr. inicijali na neutralnoj pozadini), ime i prezime, datumi („12. 3. 1931. – 2. 11. 2019.” ili samo godine ako datum nije poznat).
2. Biografija: kratka i duga (za dugu predloži „Prikaži cijelu biografiju” ili prikaži cijelu, svakako bez sitnog teksta).
3. Odjeljak „Obitelj”:
   - srodnik s vlastitim profilom je link s jasnim znakom da vodi na drugi profil;
   - živući srodnik je samo ime i vrsta srodstva, bez slike i bez linka.
4. Navigacija unutar profila: kratki izbornik ili sidra (Biografija, Slike, Video, Obitelj, Knjiga sjećanja). Kad je pokojnika više, vidljiv je i povratak na stranicu groba.
5. Mali, nenametljiv link „Prijavi” na dnu profila.
6. Prazna stanja: nema biografije, nema srodnika, nema slika ni videa. Posjetitelj tada ne vidi prazan odjeljak, nego se odjeljak ne prikazuje. Vlasnik vidi poziv „Dodajte …” (vidi D-23).

**Gotovo kada:**
- postoje profil s punim sadržajem, s kratkom biografijom i bez slika;
- živući srodnik nema sliku, datum ni link;
- najmanji tekst na profilu je ≥ 16 px, a osnovni ≥ 18 px.

**Procjena:** 3–4 sata.

### D-10 Dizajn: galerija i video
- [ ] Gotovo

**Cilj:** postoji dizajn galerije slika (mreža sličica i veliki prikaz s „Prethodna” i „Sljedeća”) i videa (kadar, reprodukcija), uz opise slika.

**Zašto:** galerija slika i video su dio profila u MVP-u (odluka 6).

**Preduvjeti:** D-09 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Galerija: mreža 2 ili 3 sličice u retku na mobitelu, s opisom ispod ili tek u velikom prikazu (odluči i obrazloži).
2. Veliki prikaz slike: slika preko širine zaslona, opis, gumbi „Prethodna”, „Sljedeća” i „Zatvori”, svi ≥ 48 px. **Ne oslanjaj se samo na povlačenje prstom**, jer ga mnogi stariji korisnici ne znaju.
3. Video: kadar s velikim gumbom za reprodukciju i trajanjem („2:14”). Reprodukcija koristi ugrađene kontrole preglednika.
4. Mnogo slika: kako izgleda galerija s 300 slika? Predloži „Prikaži još” nakon npr. 24 slike.

**Gotovo kada:**
- veliki prikaz ima vidljive gumbe za prethodnu i sljedeću sliku;
- dizajn pokriva 0, 1, 5 i 300 slika te 0, 1 i 3 videa;
- svaka slika ima mjesto za opis (koristi se i kao alternativni tekst za čitače zaslona).

**Procjena:** 2–3 sata.

### D-11 Dizajn: knjiga sjećanja i gumb „Prijavi”
- [ ] Gotovo

**Cilj:** postoji dizajn knjige sjećanja na profilu (popis odobrenih poruka i forma za novu poruku) i forme „Prijavi sadržaj”, sa svim stanjima.

**Zašto:** posjetitelj ostavlja poruku koja čeka odobrenje vlasnika (odluke 3 i 19). Gumb „Prijavi” postoji na svakom sadržaju (odluka 19).

**Preduvjeti:** D-09 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Popis poruka: ime autora, datum, tekst. Duge poruke prikazane su cijele.
2. Forma: „Vaše ime”, „Poruka”, gumb „Pošalji”. Ispod gumba piše: „Poruka će biti vidljiva kad je obitelj odobri.”
3. Stanja: nema poruka („Budite prvi koji će ostaviti poruku sjećanja.”), poruka poslana, greška (prazno polje, predugačka poruka).
4. „Prijavi”: mali link uz svaku sliku, video i poruku te na dnu profila. Forma: razlog (izbor iz popisa: uvredljiv sadržaj, netočan podatak, na slici sam ja i tražim uklanjanje, drugo), opis, e-mail za odgovor. Potvrda: „Hvala. Odgovorit ćemo u roku od 7 dana.”
5. Link „Prijavi” mora biti dovoljno velik za dodir (≥ 44 × 44 px područje dodira), ali vizualno nenametljiv.

**Gotovo kada:**
- postoje sva stanja knjige sjećanja i prijave;
- nakon slanja poruke jasno piše da čeka odobrenje;
- područje dodira linka „Prijavi” je ≥ 44 × 44 px.

**Procjena:** 2–3 sata.

### D-12 Brzi test prototipa sa starijom osobom
- [ ] Gotovo

**Cilj:** klikabilni Figma prototip javnog dijela isproban je s barem dvije starije osobe, a nalazi su zapisani i ugrađeni u dizajn.

**Zašto:** velik dio korisnika su starije osobe (podjela posla, odluka 17). Greške pronađene na prototipu najjeftinije je popraviti prije izrade predložaka.

**Preduvjeti:** D-08, D-09, D-10 i D-11 gotovi.

**Novi pojmovi:**
- **Prototip u Figmi** povezuje ekrane klikovima, pa se na mobitelu (aplikacija Figma ili link) ponaša gotovo kao prava stranica. [Figma: Prototyping](https://help.figma.com/hc/en-us/search?query=prototyping)
- **Metoda „glasnog razmišljanja”:** osoba izvodi zadatak i naglas govori što misli i što traži. Ti samo slušaš i bilježiš, bez pomaganja.

**Upute:**
1. Poveži ekrane: zaključani ekran → lozinka → profil → galerija → knjiga sjećanja.
2. Dva zadatka: „Upišite lozinku s ovog papirića i otvorite stranicu” i „Ostavite poruku obitelji”.
3. Prototip otvori na sudionikovom mobitelu ili na svom. Prije početka objasni da su sve osobe izmišljene i da testiraš dizajn, a ne osobu. Tema je osjetljiva, pa ne zovi osobe koje su nedavno izgubile nekoga bliskog.
4. Bilježi gdje zastanu, što krivo dodirnu, što ne mogu pročitati i što kažu.
5. Najvažnija 3–5 nalaza popravi u Figmi i zapiši ih na stranici *Tokovi* (odjeljak „Nalazi prototipa”).

**Gotovo kada:**
- barem dvije osobe starije od 65 godina prošle su oba zadatka;
- nalazi su zapisani, a popravci napravljeni u Figmi;
- ne čuvaš ime ni kontakt sudionika, nego samo dob (npr. „70–75”) i vrstu mobitela.

**Procjena:** 2–3 sata.

## Faza 4: Predlošci javnog dijela

Osnove Django predložaka, Tailwinda i HTMX-a, zatim pravi predlošci javnog dijela.

### D-13 Osnove Django predložaka
- [ ] Gotovo

**Cilj:** znaš čitati i mijenjati Django predloške: varijable, oznake, nasljeđivanje, uključivanje komponenti, filtre, `{% url %}`, `{% static %}` i `{% translate %}`.

**Zašto:** Karlo pretvara dizajn u HTML i Tailwind predloške (podjela posla, odluka 17). Tekstovi moraju ići kroz sustav prijevoda (odluka 18a).

**Preduvjeti:** D-03 gotov.

**Novi pojmovi:**
- **Predložak (*template*)** je HTML datoteka s posebnim oznakama. Django u njih upisuje podatke prije slanja pregledniku. [Django: Templates](https://docs.djangoproject.com/en/6.1/topics/templates/)
- **Varijabla** `{{ pokojnik.ime }}` ispisuje vrijednost koju pogled pošalje. Django sam zaštićuje ispis (*escaping*): ako netko u poruku upiše `<script>`, prikazat će se kao tekst. **Nikad ne koristi filtar `|safe`** na tekstu koji je upisao korisnik.
- **Oznaka (*tag*)** `{% if %}`, `{% for %}` ... izvodi logiku. [Built-in tags](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/)
- **Nasljeđivanje:** `{% extends "base.html" %}` i `{% block sadrzaj %}...{% endblock %}`. Okvir je u `base.html`, a stranica popunjava blokove. [Template inheritance](https://docs.djangoproject.com/en/6.1/ref/templates/language/#template-inheritance)
- **`{% include "komponente/_gumb.html" with tekst="Otvori" %}`** umeće komponentu s vlastitim vrijednostima.
- **Filtar** mijenja prikaz: `{{ datum|date:"j. n. Y." }}`, `{{ tekst|linebreaks }}`, `{{ broj|default:"0" }}`. [Built-in filters](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/#built-in-filter-reference)
- **`{% url 'pristup:grob' kod=grob.plocica.kod %}`** stvara adresu prema nazivu, pa se adrese ne pišu ručno.
- **`{% static 'img/logo.svg' %}`** daje adresu statičke datoteke. [Static files](https://docs.djangoproject.com/en/6.1/howto/static-files/)
- **`{% translate "Otvori" %}`** i `{% blocktranslate %}Dobrodošli, {{ ime }}{% endblocktranslate %}` označavaju tekst za kasniji prijevod. Na vrhu predloška treba `{% load i18n %}`. [Translation in templates](https://docs.djangoproject.com/en/6.1/topics/i18n/translation/#internationalization-in-template-code)
- **`{% csrf_token %}`** mora biti u svakoj formi koja šalje podatke (POST). Štiti od lažnih zahtjeva s tuđih stranica. Nikad ga ne briši.
- **Forma u predlošku:** polja dolaze iz pogleda kao `forma`. Koristi `{{ forma.lozinka.id_for_label }}`, `{{ forma.lozinka.errors }}` i `name="{{ forma.lozinka.html_name }}"`, da Django prepozna unos. [Rendering fields manually](https://docs.djangoproject.com/en/6.1/topics/forms/#rendering-fields-manually)

**Upute:**
1. Prođi [Django tutorial, 3. dio](https://docs.djangoproject.com/en/6.1/intro/tutorial03/) (samo dio o predlošcima) i [jezik predložaka](https://docs.djangoproject.com/en/6.1/ref/templates/language/).
2. Otvori `templates/base.html` i `templates/javno/pocetna.html` i pronađi svaki od gornjih pojmova.
3. Vježba na grani `d-13-vjezba` (ne spajaš je u `main`): u `pocetna.html` dodaj petlju koja ispisuje popis od tri stavke, uvjet `{% if %}` i jedan `{% translate %}`.
4. Pročitaj `docs/predlosci.md` i odjeljak „Ugovor između pogleda i predloška” u ovom planu.

**Gotovo kada:**
- znaš objasniti razliku između `{{ }}` i `{% %}`;
- vježba radi lokalno;
- znaš koje dijelove predloška ne smiješ mijenjati bez dogovora s Petrom.

**Procjena:** 3–4 sata.

### D-14 Osnove Tailwinda i tema iz Figme
- [ ] Gotovo

**Cilj:** boje, fontovi i razmaci iz Figme postoje kao Tailwind tema u `static/css/ulaz.css`, fontovi se poslužuju iz `static/fontovi/`, a znaš složiti mobilni raspored Tailwind klasama.

**Zašto:** izgled radimo Tailwind CSS-om prema dizajnu u Figmi (odluka 17).

**Preduvjeti:** D-03 i D-05 gotovi.

**Novi pojmovi:**
- **Tailwind CSS** stil zapisuje kratkim klasama u HTML-u: `p-4` (razmak 16 px), `text-xl`, `bg-pozadina`, `rounded-lg`. Alat čita predloške i stvara CSS samo s korištenim klasama. [Tailwind: Utility-first](https://tailwindcss.com/docs/styling-with-utility-classes)
- **Prefiksi za veličinu zaslona:** `md:grid-cols-3` vrijedi tek od 768 px širine. Bez prefiksa klasa vrijedi za mobitel. Zato se piše mobile-first. [Responsive design](https://tailwindcss.com/docs/responsive-design)
- **Prefiksi stanja:** `hover:`, `focus-visible:`, `disabled:`. [Hover, focus and other states](https://tailwindcss.com/docs/hover-focus-and-other-states)
- **Tema (`@theme`)** u Tailwindu 4 zapisuje vlastite boje i fontove u CSS datoteci. Iz `--color-primarna` nastaju klase `bg-primarna`, `text-primarna` ... [Tailwind: Theme](https://tailwindcss.com/docs/theme)
- **`@font-face`** učitava font iz naše datoteke (WOFF2). [MDN: @font-face](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face)

**Upute:**
1. Preuzmi WOFF2 datoteke odabranih fontova (npr. s [Fontsource](https://fontsource.org/) ili sa stranice autora) u `static/fontovi/`, uz datoteku licence.
2. U `static/css/ulaz.css`:
   ```css
   @import "tailwindcss";
   @source "../../templates";

   @font-face {
     font-family: "Atkinson Hyperlegible Next";
     src: url("../fontovi/AtkinsonHyperlegibleNext-Regular.woff2") format("woff2");
     font-weight: 400; font-display: swap;
   }

   @theme {
     --font-sans: "Atkinson Hyperlegible Next", system-ui, sans-serif;
     --color-pozadina: #f7f4ef;     /* primjer, uzmi vrijednosti iz Figme */
     --color-tekst: #1f1d1a;
     --color-primarna: #2f4a3f;
     --color-greska: #9b1c1c;
     --text-base: 1.1875rem;        /* 19 px osnovni tekst */
   }
   ```
3. Napravi vježbu: jedna kartica pokojnika samo Tailwind klasama, uspoređena s Figmom.
4. U VS Codeu provjeri da *Tailwind CSS IntelliSense* nudi tvoje boje (`bg-pri…`).

**Gotovo kada:**
- klase `bg-primarna`, `text-tekst` i `font-sans` rade u predlošku;
- font se učitava iz `static/fontovi/` (u alatima preglednika, kartica *Network*, nema zahtjeva prema `fonts.googleapis.com`);
- osnovni tekst na stranici je ≥ 18 px.

**Procjena:** 3–4 sata.

**Česte greške:**
- Klasa složena od dijelova (`bg-{{ boja }}`) ne radi, jer je Tailwind ne vidi. Uvijek piši cijelu klasu, a za izbor koristi `{% if %}`.

### D-15 Osnove HTMX-a
- [ ] Gotovo

**Cilj:** razumiješ HTMX atribute u predlošcima (`hx-post`, `hx-get`, `hx-target`, `hx-swap`, `hx-trigger`, `hx-indicator`) i znaš ih zadržati i stilizirati.

**Zašto:** interaktivnost radimo HTMX-om (odluka 17). Ti ne pišeš logiku, ali predlošci koje uređuješ sadrže HTMX atribute.

**Preduvjeti:** D-13 gotov.

**Novi pojmovi:**
- **HTMX** je mala biblioteka. Gumbi i forme preko atributa šalju zahtjev poslužitelju i zamjenjuju **samo dio stranice** HTML-om koji poslužitelj vrati. [htmx.org: Docs](https://htmx.org/docs/)
- **`hx-target`** određuje koji element se mijenja, a **`hx-swap`** kako (`outerHTML` zamjenjuje cijeli element, `innerHTML` samo sadržaj).
- **`hx-indicator`** prikazuje element (npr. „Šaljem…”) dok zahtjev traje. HTMX tada elementu dodaje klasu `htmx-request`. [hx-indicator](https://htmx.org/attributes/hx-indicator/)
- **Djelomični predložak (*partial*)** je mali predložak (ime počinje s `_`, npr. `_poruka_redak.html`) koji poslužitelj vraća za zamjenu.

**Upute:**
1. Pročitaj uvod HTMX dokumentacije i primjere [Click to Edit](https://htmx.org/examples/click-to-edit/) i [Inline Validation](https://htmx.org/examples/inline-validation/).
2. Pronađi HTMX atribute u Petrovim predlošcima (npr. prekidač javnog prikaza iz P-21) i objasni sebi što se događa na klik.
3. Dogovori s Petrom izgled stanja „šaljem…”: koja klasa, koji tekst, onemogućeni gumb.

**Gotovo kada:**
- za tri HTMX elementa u projektu znaš reći što se šalje, kamo i što se zamjenjuje;
- znaš da ne smiješ mijenjati `hx-*` atribute ni `id` elementa na koji pokazuje `hx-target` bez dogovora.

**Procjena:** 2–3 sata.

### D-16 Osnovni predložak i komponente
- [ ] Gotovo

**Cilj:** `templates/base.html` ima pravi izgled (zaglavlje, sadržaj, podnožje, obavijesti), a komponente iz Figme postoje kao predlošci u `templates/komponente/`.

**Zašto:** sve stranice nasljeđuju isti okvir, pa su dosljedne, a promjena na jednom mjestu mijenja sve (odluka 17).

**Preduvjeti:** D-06, D-13 i D-14 gotovi, P-05 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. `base.html`:
   - zadrži `lang="hr"`, `viewport`, `noindex`, `{% tailwind_css %}`, HTMX skriptu i `hx-headers` s CSRF-om (sve od Petra);
   - dodaj zaglavlje, `<main id="sadrzaj">`, podnožje i link „Preskoči na sadržaj” na samom početku (vidljiv kad dobije fokus);
   - dodaj prikaz Djangovih poruka (`{% for message in messages %}`) kroz komponentu obavijesti.
2. Komponente u `templates/komponente/`: `_gumb.html`, `_polje.html` (oznaka, polje, pomoćni tekst, greška, `aria-describedby`), `_obavijest.html`, `_kartica_pokojnika.html`, `_potvrda.html`, `_napredak.html`, `_korak.html` („Korak X od 4”).
3. Na vrhu svake komponente komentar s parametrima, npr. `{# Parametri: tekst, vrsta (primarni|sekundarni|opasni), type (submit|button) #}`.
4. Dodaj ih u `docs/predlosci.md` pod „Komponente”.
5. Probna stranica `templates/javno/komponente.html` prikazuje sve komponente, za brzu usporedbu s Figmom. Otvori issue s oznakom `petar` da je poveže na URL koji radi samo kad je `DEBUG=True`.

**Gotovo kada:**
- probna stranica komponenti izgleda kao Figmina stranica *Komponente* na mobitelu;
- `base.html` i dalje sadrži sve Petrove elemente (provjeri `noindex`, `hx-headers` i `lang`);
- link „Preskoči na sadržaj” pojavi se pritiskom tipke Tab.

**Procjena:** 4–5 sati.

### D-17 Predlošci: zaključani ekran, stranica groba i unos aktivacijskog koda
- [ ] Gotovo

**Cilj:** predlošci `javno/zakljucano.html`, `javno/zahtjev.html` (dio forme i potvrde), `javno/grob.html` i `aktivacija/unos_koda.html` izgledaju kao Figma dizajn iz D-08, u svim stanjima.

**Zašto:** prvo mjerilo uspjeha je tok skeniranje → lozinka → profil na iPhoneu i Androidu (odluka 20).

**Preduvjeti:** D-08 i D-16 gotovi, P-14 gotov.

> 🔁 **Predaja:** Petar predaje Karlu privremene predloške `templates/javno/zakljucano.html`, `templates/javno/grob.html`, `templates/javno/profil.html` i `templates/aktivacija/unos_koda.html`, popis varijabli u `docs/predlosci.md` i naredbu `napravi_probni_grob` (korak **P-14**). Isto vrijedi za D-18.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Napravi granu `d-17-zakljucani-ekran`.
2. Svaki predložak preuredi prema Figmi, zadržavajući varijable iz komentara na vrhu, `{% csrf_token %}`, `name` atribute i `{% url %}` nazive.
3. Polje lozinke: `type="password"`, `autocomplete="current-password"`, gumb „Prikaži” (mali `<script>` u predlošku ili Alpine.js, koji dogovori s Petrom).
4. Polje aktivacijskog koda: `autocapitalize="characters"`, `autocomplete="off"`, `inputmode="text"`, `spellcheck="false"`.
5. Stanja (pogrešna lozinka, previše pokušaja, link ne vrijedi) prikaži ih tako da lokalno izazoveš svako. Npr. šest puta upiši krivu lozinku na probnom grobu (`napravi_probni_grob`).
6. Ako je zahtjev za pristup već predan (P-24), uredi i `javno/zahtjev.html`. Ako nije, napravi to u D-26.
7. Provjeri na mobitelu u istoj Wi-Fi mreži: Petar u README opisuje kako (`runserver 0.0.0.0:8000` i IP adresa računala).
8. PR sa snimkom zaslona svakog stanja s mobitela.

**Gotovo kada:**
- svako stanje iz D-08 može se izazvati lokalno i izgleda kao u Figmi;
- forme rade (točna lozinka otvara profil);
- predlošci nemaju nijedan tekst izvan `{% translate %}` / `{% blocktranslate %}`;
- Petar je pregledao i spojio PR.

**Procjena:** 3–4 sata.

### D-18 Predložak profila pokojnika
- [ ] Gotovo

**Cilj:** `javno/profil.html` izgleda kao Figma dizajn iz D-09: zaglavlje, biografija, odjeljak „Obitelj”, navigacija po odjeljcima i prazna stanja.

**Zašto:** profil s biografijom i odjeljkom „Obitelj” (odluke 3a i 6).

**Preduvjeti:** D-09 i D-17 gotovi, P-14 gotov.

> 🔁 **Predaja:** Ulaz je isti kao za D-17: predložak `templates/javno/profil.html` i varijable iz **P-14**.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Koristi `_kartica_pokojnika.html` i druge komponente gdje se ponavljaju.
2. Biografija ide kroz `|linebreaks` (Petar je to stavio u pogled ili predložak, provjeri komentar). Bez `|safe`.
3. Odjeljak „Obitelj”: popis koji Petar šalje već sadrži samo dopuštene srodnike. Ne dodaji nikakve druge izvore podataka o živućim osobama.
4. Odjeljke za galeriju, video i knjigu ostavi kao mjesta za `{% include %}` koje dolaze u D-19 i D-20.
5. Datumi: `{{ pokojnik.datum_rodjenja|date:"j. n. Y." }}`. Ako datuma nema, ne ispisuj ništa (ne „None”).
6. Napravi semantički ispravan HTML: jedan `<h1>` (ime pokojnika), `<h2>` za odjeljke, `<nav>` za izbornik odjeljaka.

**Gotovo kada:**
- profil s punim sadržajem i profil bez biografije i srodnika izgledaju kao u Figmi;
- na stranici nigdje ne piše „None” ni prazna oznaka odjeljka;
- struktura naslova je `h1` → `h2` (provjeri proširenjem *HeadingsMap* ili u alatima preglednika).

**Procjena:** 3–4 sata.

### D-19 Predlošci galerije i videa
- [ ] Gotovo

**Cilj:** `javno/_galerija.html`, `javno/_video.html` i `javno/slika.html` izgledaju kao Figma dizajn iz D-10 i rade na iPhoneu i Androidu.

**Zašto:** galerija i video su dio profila u MVP-u (odluka 6).

**Preduvjeti:** D-10 i D-18 gotovi, P-31 gotov.

> 🔁 **Predaja:** Petar predaje Karlu `templates/javno/_galerija.html`, `templates/javno/_video.html`, `templates/javno/slika.html`, `templates/vlasnik/mediji.html`, skriptu `static/js/upload.js` i popis stanja medija (korak **P-31**). Isto vrijedi za D-27.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Sličice: `<img src="{{ slika.slicica.url }}" alt="{{ slika.opis }}" loading="lazy" width="…" height="…">`. Širina i visina sprječavaju „skakanje” stranice pri učitavanju (Petar šalje `sirina` i `visina`).
2. Video: zadrži `controls`, `playsinline` i `preload="none"` iz Petrovog predloška. Stilizira se okvir oko videa, a ne same kontrole.
3. Veliki prikaz (`slika.html`): gumbi „Prethodna”, „Sljedeća”, „Natrag na profil”, svi ≥ 48 px.
4. Prazno stanje i „Prikaži još” prema D-10, ako ih je Petar predvidio u kontekstu. Inače otvori issue s oznakom `petar`.
5. Linkovi na slike su potpisani i vrijede sat vremena. Nemoj ih kopirati u Figmu ni bilo gdje drugdje kao „trajne”.

**Gotovo kada:**
- galerija i video rade u Safariju na iPhoneu i u Chromeu na Androidu;
- video na iPhoneu ne otvara se automatski preko cijelog zaslona;
- svaka slika ima `alt` iz opisa (ili prazan `alt=""` ako opisa nema, nikad ime datoteke).

**Procjena:** 3–4 sata.

### D-20 Predlošci knjige sjećanja i prijave sadržaja
- [ ] Gotovo

**Cilj:** `javno/_knjiga.html` i `javno/prijava.html` izgledaju kao Figma dizajn iz D-11, uključujući HTMX stanje nakon slanja.

**Zašto:** knjiga sjećanja s odobravanjem je mjerilo uspjeha 4 (odluka 20), a gumb „Prijavi” je na svakom sadržaju (odluka 19).

**Preduvjeti:** D-11 i D-18 gotovi, P-34 gotov.

> 🔁 **Predaja:** Petar predaje Karlu `templates/javno/_knjiga.html`, `templates/javno/prijava.html`, `templates/vlasnik/knjiga.html` i `templates/vlasnik/_poruka_redak.html` s varijablama (korak **P-34**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Tekst poruke ispisuje se kao `{{ poruka.tekst|linebreaksbr }}`. **Nikad `|safe`.**
2. Forma za poruku šalje se HTMX-om. Zadrži `hx-post`, `hx-target` i `hx-swap`. Stilizira se stanje „šaljem…” (`hx-indicator`) i potvrda.
3. Skriveno polje „mamac” protiv botova (ako postoji u Petrovom predlošku) mora ostati skriveno i za čitače zaslona (`aria-hidden="true"`, `tabindex="-1"`).
4. Link „Prijavi” uz svaku sliku, video i poruku vodi na `javno/prijava.html` s pravim parametrom (`?medij=` ili `?poruka=`), prema Petrovom predlošku.

**Gotovo kada:**
- poslana poruka prikazuje potvrdu bez ponovnog učitavanja stranice;
- poruka s tekstom `<b>test</b>` prikazuje se doslovno, a ne podebljano;
- prijava slike stiže u admin (provjeri lokalno).

**Procjena:** 2–3 sata.

## Faza 5: Aktivacija i vlasnički dio

Dizajn i predlošci čarobnjaka, vlasničkog dijela, grešaka, e-mailova i pregleda za partnera.

### D-21 Dizajn: čarobnjak za aktivaciju
- [ ] Gotovo

**Cilj:** na Figma stranici *Aktivacija* postoje svi koraci čarobnjaka (aktivacijski kod → podaci groba i lozinka → prvi pokojnik → slike → gotovo) sa svim stanjima grešaka.

**Zašto:** obitelj sama skenira kod i prolazi čarobnjak (odluka 8). Čarobnjak traži oznaku grobnog mjesta s računa (odluka 11) i „e-mail osobe koja će voditi profil” (odluka 19). Aktivacija od početka do kraja je mjerilo uspjeha 2.

**Preduvjeti:** D-06 i D-08 gotovi.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Svaki korak ima jedan zadatak, indikator „Korak X od 4”, gumb „Nastavi” i, gdje ima smisla, „Natrag”.
2. **Korak 1, aktivacijski kod:** kao ekran neaktivirane pločice (D-08), uz sliku letka koja pokazuje gdje je kod. Stanja: pogrešan kod, previše pokušaja.
3. **Korak 2, grob:**
   - naziv groba („npr. Obitelj Horvat. Ovo vide posjetitelji.”);
   - oznaka grobnog mjesta („Prepišite s računa groblja, npr. Polje C, red 4, br. 12. Posjetitelji ovo ne vide.”);
   - ime vlasnika („Osoba na koju glasi grobno mjesto”);
   - „E-mail osobe koja će voditi profil” (s objašnjenjem da to može biti i dijete ili unuk);
   - lozinka groba dvaput (najmanje 6 znakova, s gumbom „Prikaži” i savjetom „Lozinku ćete dati obitelji. Odaberite nešto što se lako izgovori i zapiše.”).
4. **Korak 3, prvi pokojnik:** ime, prezime, datum rođenja i smrti (kalendar na mobitelu), kratka biografija („Možete je napisati i kasnije.”).
5. **Korak 4, slike:** veliki gumb „Dodaj slike s mobitela” i „Preskoči, dodat ću kasnije”.
6. **Gotovo:** što je sada moguće (podijelite lozinku, obiteljski link, kako se ponovno prijaviti putem e-maila) i gumb „Otvori stranicu groba”.
7. Za svako polje pokaži stanje greške (prazno, prekratka lozinka, lozinke se ne podudaraju, neispravan e-mail).

**Gotovo kada:**
- postoje svi koraci i stanja na 390 px i provjereni su na 360 px;
- svako polje ima oznaku iznad i pomoćni tekst gdje je potrebno;
- tekst „E-mail osobe koja će voditi profil” je doslovno takav (odluka 19);
- Petar je pregledao i potvrdio da dizajn odgovara poljima koja sprema.

**Procjena:** 3–5 sati.

### D-22 Dizajn: vlasnički dio, prvi dio (prijava, grobovi, postavke, pristup)
- [ ] Gotovo

**Cilj:** na Figma stranici *Vlasnik* postoje ekrani prijave e-mailom, „link je poslan”, popisa grobova, pregleda groba, postavki (lozinka, odjava uređaja, javni prikaz), obiteljskog linka i zahtjeva za pristup.

**Zašto:** vlasnik se prijavljuje linkom na e-mail (odluka 3), postavlja i mijenja lozinku, uključuje javni prikaz te upravlja obiteljskim linkom i zahtjevima za pristup (odluka 5, OP-1).

**Preduvjeti:** D-06 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. **Prijava:** polje e-mail i „Pošalji mi link”. **Link je poslan:** „Ako je adresa upisana, poslali smo vam link. Provjerite i mapu neželjene pošte. Link vrijedi 15 minuta.”
2. **Popis grobova:** kartice s nazivom groba, brojem pokojnika i oznakama poput „2 nove poruke čekaju odobrenje” i „1 zahtjev za pristup”.
3. **Pregled groba:** pokojnici, brzi linkovi (Mediji, Knjiga sjećanja, Zahtjevi, Postavke), poveznica „Pogledaj kako stranicu vide posjetitelji”.
4. **Postavke:**
   - promjena naziva groba;
   - promjena lozinke (nova lozinka dvaput i kvačica „Odjavi sve uređaje koji su upisali staru lozinku”);
   - javni prikaz s jasnim objašnjenjem i potvrdom;
   - oznaka grobnog mjesta i ime vlasnika samo za čitanje („Za promjenu nam se javite.”).
5. **Obiteljski link:** link, gumbi „Podijeli” (izbornik mobitela) i „Kopiraj”, upozorenje „Šaljite ga samo obitelji”, „Poništi link i napravi novi” s potvrdom.
6. **Zahtjevi za pristup:** popis (ime, poruka, datum) s gumbima „Pošalji obiteljski link” i „Odbij”, te prazno stanje.
7. Vlasnički dio je i na računalu, pa za popis grobova i postavke napravi i jednu verziju na 1280 px.

**Gotovo kada:**
- postoje svi navedeni ekrani i stanja (uključujući potvrde i prazna stanja);
- svaka opasna radnja (poništavanje linka, javni prikaz) ima korak potvrde;
- postoji verzija za računalo za popis grobova i postavke.

**Procjena:** 3–4 sata.

### D-23 Dizajn: vlasnički dio, drugi dio (pokojnici, srodnici, mediji, odobravanje)
- [ ] Gotovo

**Cilj:** postoje ekrani uređivanja pokojnika, dodavanja i poretka srodnika, slanja medija s napretkom, popisa medija s potrošnjom prostora i odobravanja poruka u knjizi sjećanja.

**Zašto:** vlasnik uređuje sve i odobrava tuđe priloge (odluka 3), upravlja srodnicima uz pristanak živućih osoba (odluka 3a, OP-6), šalje slike i video s mobitela (mjerilo uspjeha 3) unutar ograničenja po grobu (odluke 12 i 18) i odobrava poruke (mjerilo uspjeha 4).

**Preduvjeti:** D-22 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. **Pokojnik:** forma (kao korak 3 čarobnjaka) i „Obriši pokojnika” s potvrdom upisom imena.
2. **Srodnici:** popis s gumbima „Gore”, „Dolje” i „Ukloni”. Dodavanje: vrsta srodstva, zatim izbor „Pokojnik u ovom grobu” ili „Živuća osoba”. Za živuću osobu samo ime i obavezna kvačica „Osoba je pristala da se njezino ime prikaže na profilu”.
3. **Slanje medija:**
   - veliki gumb „Dodaj slike ili video”;
   - popis odabranih datoteka, svaka sa svojom trakom napretka;
   - stanja: šalje se (postotak), obrađuje se („Video se priprema, to može potrajati nekoliko minuta. Možete zatvoriti stranicu.”), gotovo, greška (prevelika datoteka, video dulji od 5 minuta, ograničenje groba dosegnuto).
4. **Popis medija:** sličice, opis (uređivanje na mjestu), „Gore”, „Dolje”, „Postavi kao profilnu”, „Obriši”, te traka potrošnje („124 od 300 slika · 6 od 20 minuta videa”).
5. **Knjiga sjećanja:** poruke na čekanju s gumbima „Odobri” i „Odbij”, ispod njih odobrene s „Ukloni”, te prazna stanja.
6. Sve radnje rade dodirom gumba. Nema povlačenja i nema skrivenih gesti.

**Gotovo kada:**
- postoje svi ekrani i stanja iz koraka 1–5;
- poruke grešaka uploada kažu što učiniti, a ne samo što ne valja;
- živućeg srodnika nije moguće dodati bez kvačice pristanka (u dizajnu je gumb onemogućen ili se prikazuje greška).

**Procjena:** 4–6 sati.

### D-24 Dizajn: prazna stanja, greške, e-mail poruke, pregled za partnera
- [ ] Gotovo

**Cilj:** postoje ekrani 404, 500 i „previše pokušaja”, sva prazna stanja koja nedostaju, tekstovi svih e-mail poruka, uputa „Dodajte na početni zaslon” te jednostavan pregled i mjesečni izvještaj za partnera.

**Zašto:** prazna stanja i poruke o greškama su dio MVP ekrana (opseg dizajna). Pregled za partnera je u MVP-u (odluka 15), a dodavanje na početni zaslon za vlasnike također (odluka 16).

**Preduvjeti:** D-06 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Greške: 404 („Stranica nije pronađena. Provjerite link ili skenirajte kod ponovno.”), 500 („Nešto nije u redu na našoj strani. Pokušajte ponovno za nekoliko minuta.”), previše pokušaja. Na svakoj neka bude jasan put dalje.
2. E-mail poruke (običan tekst, kratko, s „Vi”): link za prijavu, dobrodošlica nakon aktivacije, novi zahtjev za pristup, nova poruka u knjizi sjećanja, obiteljski link posjetitelju. Za svaku napiši predmet i tekst u Figmi ili u `docs/emailovi.md`, s oznakama gdje dolaze podaci (npr. `[naziv groba]`).
3. **Pregled za partnera** (na računalu 1280 px i na mobitelu): tri broja (na zalihi, aktivirane, ukupno), tablica po mjesecima, mjesečni izvještaj s tablicom pločica i gumbom „Preuzmi CSV”. Partner ne vidi sadržaj profila.
4. **Uputa za početni zaslon** (vlasnički dio): kratka kartica s koracima za iPhone (Dijeli → Dodaj na početni zaslon) i Android (izbornik → Instaliraj aplikaciju), s gumbom „Razumijem”.

**Gotovo kada:**
- postoje svi ekrani i svih 5 e-mail tekstova;
- svaka greška ima tekst koji kaže što dalje;
- pregled za partnera ne prikazuje imena pokojnika ni e-mailove.

**Procjena:** 3–4 sata.

### D-25 Predlošci čarobnjaka za aktivaciju
- [ ] Gotovo

**Cilj:** `aktivacija/korak_kod.html`, `korak_grob.html`, `korak_pokojnik.html`, `korak_slike.html` i `gotovo.html` izgledaju kao Figma dizajn iz D-21, u svim stanjima.

**Zašto:** aktivacija nove pločice od početka do kraja je mjerilo uspjeha 2 (odluka 20).

**Preduvjeti:** D-21 i D-16 gotovi, P-20 gotov.

> 🔁 **Predaja:** Petar predaje Karlu predloške `templates/aktivacija/*.html` s varijablama (`korak`, `ukupno_koraka`, greške forme) i CSV s demo aktivacijskim kodovima (korak **P-20**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Koristi `_korak.html` s varijablama `korak` i `ukupno_koraka` iz Petrovog konteksta.
2. Polja:
   - e-mail: `type="email" autocomplete="email" inputmode="email"`;
   - nova lozinka: `type="password" autocomplete="new-password"`;
   - datumi: `type="date"`.
3. Greške forme prikazuj uz polje (`{{ forma.polje.errors }}`) i jednom na vrhu (`{{ forma.non_field_errors }}`). Polje s greškom dobiva `aria-invalid="true"`.
4. Provjeri cijeli tok lokalno s aktivacijskim kodom iz Petrovog demo CSV-a.

**Gotovo kada:**
- cijeli čarobnjak prolazi na mobitelu i izgleda kao u Figmi;
- svako stanje greške može se izazvati i prikazano je uz polje;
- predlošci imaju sve tekstove u `{% translate %}`.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Karlo predaje Petru PR s pravim predlošcima iz ovog koraka. Petar ih pregledava i spaja u **P-43**.

### D-26 Predlošci vlasničkog dijela, prvi dio
- [ ] Gotovo

**Cilj:** predlošci prijave, popisa grobova, pregleda groba, postavki, obiteljskog linka i zahtjeva za pristup (`vlasnik/prijava.html`, `popis.html`, `postavke.html`, `zahtjevi.html` i `javno/zahtjev.html`) izgledaju kao Figma dizajn iz D-22.

**Zašto:** vlasnik upravlja lozinkom, javnim prikazom, obiteljskim linkom i zahtjevima (odluka 5).

**Preduvjeti:** D-22 i D-16 gotovi, P-24 gotov.

> 🔁 **Predaja:** Petar predaje Karlu predloške vlasničkog dijela iz koraka P-21 do P-24 (`vlasnik/prijava.html`, `popis.html`, `postavke.html`, `zahtjevi.html`, `javno/zahtjev.html`) s varijablama (korak **P-24**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. HTMX prekidač javnog prikaza i HTMX gumbe zahtjeva zadrži točno kako ih je Petar postavio, a stiliziraj ih.
2. „Podijeli” koristi `navigator.share` ako postoji, a inače se prikazuje samo „Kopiraj”. Dogovori s Petrom tko piše tih nekoliko redaka JavaScripta (prijedlog: ti, u `static/js/dijeli.js`, a Petar pregledava).
3. Dijalog potvrde (`_potvrda.html`) koristi `<dialog>` ili zasebnu stranicu potvrde. Odluči s Petrom, ali mora raditi i tipkovnicom.
4. Verzija za računalo: `md:` i `lg:` klase prema dizajnu na 1280 px.

**Gotovo kada:**
- svi ekrani iz D-22 rade lokalno i izgledaju kao u Figmi na mobitelu i računalu;
- poništavanje obiteljskog linka i javni prikaz traže potvrdu;
- „Kopiraj” radi na iPhoneu i Androidu.

**Procjena:** 3–5 sati.

> 🔁 **Predaja:** Karlo predaje Petru PR s pravim predlošcima iz ovog koraka. Petar ih pregledava i spaja u **P-43**.

### D-27 Predlošci vlasničkog dijela, drugi dio
- [ ] Gotovo

**Cilj:** predlošci uređivanja pokojnika, srodnika, slanja i popisa medija i odobravanja poruka (`vlasnik/pokojnik.html`, `_srodnik_redak.html`, `mediji.html`, `knjiga.html`, `_poruka_redak.html`) izgledaju kao Figma dizajn iz D-23.

**Zašto:** upload slike i videa s mobitela (mjerilo uspjeha 3), knjiga sjećanja s odobravanjem (mjerilo uspjeha 4) i odjeljak „Obitelj” (odluka 3a).

**Preduvjeti:** D-23 i D-26 gotovi, P-24, P-31 i P-34 gotovi.

> 🔁 **Predaja:** Petar predaje Karlu `vlasnik/pokojnik.html` i `_srodnik_redak.html` (**P-24**), predloške medija i `upload.js` (**P-31**) te predloške knjige sjećanja u vlasničkom dijelu (**P-34**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Upload: `static/js/upload.js` je Petrov i ne mijenjaš ga. Stiliziraš elemente koje skripta koristi (popisani u `docs/predlosci.md`, npr. `data-upload-popis`, `data-upload-napredak`). Ako ti treba druga struktura HTML-a, otvori issue s oznakom `petar`.
2. Traka napretka: `<progress>` ili `role="progressbar"` s `aria-valuenow`, da je čitač zaslona može pročitati.
3. Popis medija se dok traje obrada osvježava sam (HTMX `hx-trigger="every 5s"`). Ne uklanjaj taj atribut.
4. Redak poruke i redak srodnika su djelomični predlošci koje HTMX zamjenjuje. Moraju imati isti vanjski element s istim `id`-om kao kod Petra.

**Gotovo kada:**
- slanje slike i videa s mobitela pokazuje napredak i stanje obrade kao u Figmi;
- odobravanje poruke mijenja samo njezin redak, bez ponovnog učitavanja stranice;
- dodavanje živućeg srodnika bez kvačice pristanka prikazuje grešku.

**Procjena:** 4–6 sati.

> 🔁 **Predaja:** Karlo predaje Petru PR s pravim predlošcima iz ovog koraka. Petar ih pregledava i spaja u **P-43**.

### D-28 Predlošci grešaka, e-mail poruka i pregleda za partnera
- [ ] Gotovo

**Cilj:** `greske/404.html`, `greske/500.html`, `greske/zakljucano.html`, `emailovi/*.txt` i `partner/*.html` izgledaju i glase kao u D-24.

**Zašto:** prazna stanja i greške su dio MVP ekrana, a pregled za partnera je u MVP-u (odluka 15).

**Preduvjeti:** D-24 i D-16 gotovi, P-38 gotov.

> 🔁 **Predaja:** Petar predaje Karlu `templates/partner/*.html`, `templates/emailovi/*.txt` i `templates/greske/*.html` s varijablama (korak **P-38**).

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. `500.html` ne smije koristiti varijable iz baze ni složene oznake, jer se prikazuje i kad baza ne radi. Koristi samo statički HTML i `{% static %}`.
2. E-mail predlošci su običan tekst. Zadrži varijable (npr. `{{ link }}`, `{{ grob.naziv }}`) i ne dodaji HTML.
3. Pregled za partnera: tablice s `<th scope="col">`, brojevi poravnati udesno, iznosi s dvije decimale i oznakom €.
4. Grešku 404 provjeri lokalno: u `.env` privremeno postavi `DEBUG=False`, pokreni `python manage.py collectstatic --noinput` i otvori nepostojeću adresu. Nakon provjere vrati `DEBUG=True`.

**Gotovo kada:**
- nepostojeća adresa uz `DEBUG=False` prikazuje tvoj dizajn 404;
- e-mailovi u terminalu (lokalno) imaju tekst iz D-24;
- pregled za partnera izgleda kao u Figmi na računalu i mobitelu.

**Procjena:** 2–3 sata.

> 🔁 **Predaja:** Karlo predaje Petru PR s pravim predlošcima iz ovog koraka. Petar ih pregledava i spaja u **P-43**.

## Faza 6: Pristupačnost i materijali

Provjera pristupačnosti, ikone za početni zaslon, demo QR pločica i letak.

### D-29 Provjera pristupačnosti
- [ ] Gotovo

**Cilj:** svi predlošci prošli su provjeru kontrasta, veličina, tipkovnice i čitača zaslona (VoiceOver na iPhoneu, TalkBack na Androidu), a pronađeni problemi su popravljeni ili zapisani kao issue.

**Zašto:** velik dio korisnika su starije osobe, a pristupačnost (kontrast, veličine, čitači zaslona) je dio Karlovog posla (podjela posla, odluka 17).

**Preduvjeti:** D-17 do D-28 gotovi.

**Novi pojmovi:**
- **WCAG 2.2** su međunarodne smjernice za pristupačnost weba. Cilj je razina AA, a za tekst AAA (kontrast 7 : 1). [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- **Čitač zaslona** je program koji slijepim i slabovidnim osobama naglas čita sadržaj: **VoiceOver** na iPhoneu (*Postavke → Pristupačnost → VoiceOver*) i **TalkBack** na Androidu. [Apple: VoiceOver](https://support.apple.com/guide/iphone/turn-on-and-practice-voiceover-iph3e2e415f/ios), [Google: TalkBack](https://support.google.com/accessibility/android/answer/6283677)
- **Lighthouse** i **axe DevTools** su alati u pregledniku koji automatski pronalaze dio problema pristupačnosti. [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview), [axe DevTools](https://www.deque.com/axe/devtools/)

**Upute:**
1. Za svaki predložak prođi popis:
   - kontrast teksta ≥ 7 : 1, a ostalog ≥ 4,5 : 1;
   - osnovni tekst ≥ 18 px;
   - područja dodira ≥ 44 × 44 px (gumbi ≥ 48 px);
   - svako polje ima `<label>`;
   - greške su povezane s poljem (`aria-describedby`);
   - fokus je vidljiv;
   - redoslijed fokusa tipkom Tab je logičan;
   - sve se može napraviti tipkovnicom;
   - slike imaju `alt`;
   - nijedna informacija nije samo u boji;
   - stranica radi kad je tekst povećan na 200 %;
   - animacije poštuju `prefers-reduced-motion`.
2. Pokreni Lighthouse (kategorija *Accessibility*) i axe na zaključanom ekranu, profilu, čarobnjaku i popisu medija.
3. Prođi tok „lozinka → profil → poruka u knjizi sjećanja” s VoiceOverom i TalkBackom zatvorenih očiju (ili bez gledanja u zaslon).
4. Na mobitelu u postavkama povećaj sistemsku veličinu teksta na najveću i provjeri da se ništa ne preklapa.
5. Rezultat zapiši u `docs/pristupacnost.md` (tablica: ekran, provjera, rezultat, issue).

**Gotovo kada:**
- Lighthouse *Accessibility* ≥ 95 na četiri navedena ekrana;
- tok lozinka → profil → poruka može se proći s VoiceOverom i TalkBackom;
- nema otvorenih problema ozbiljnosti 1 (blokira korištenje);
- `docs/pristupacnost.md` postoji i spojen je u `main`.

**Procjena:** 3–5 sati.

### D-30 Ikone za početni zaslon i favicon
- [ ] Gotovo

**Cilj:** u `static/img/ikone/` postoje ikona za početni zaslon (180, 192, 512 px i *maskable* 512 px) i favicon (SVG i 32 px PNG), uz boje teme.

**Zašto:** dodavanje na početni zaslon (PWA) za vlasnike (odluka 16).

**Preduvjeti:** D-05 gotov.

**Novi pojmovi:**
- **Maskable ikona** ima sadržaj u sigurnoj zoni u sredini (oko 80 %), jer je Android može izrezati u krug ili kvadrat. [web.dev: Maskable icons](https://web.dev/articles/maskable-icon), [maskable.app](https://maskable.app/)
- **Favicon** je mala ikona u kartici preglednika.

**Upute:**
1. Iz znaka iz D-05 napravi ikonu koja je jasna i na 32 px: jednostavan oblik, bez sitnog teksta.
2. Izvezi PNG datoteke u navedenim veličinama i `favicon.svg`.
3. Provjeri *maskable* verziju na maskable.app.
4. Uz datoteke zapiši `theme_color` i `background_color` (heksadecimalno) u opis PR-a.

**Gotovo kada:**
- sve datoteke su u `static/img/ikone/`;
- *maskable* ikona izgleda dobro u krugu i kvadratu na maskable.app;
- favicon je prepoznatljiv na 32 px.

**Procjena:** 1–2 sata.

> 🔁 **Predaja:** Karlo predaje Petru ikone u `static/img/ikone/` i boje teme (PR). Time može krenuti **P-39**.

### D-31 Dizajn demo QR pločice i letka
- [ ] Gotovo

**Cilj:** na Figma stranici *Pločica i letak* postoje dizajn pločice 5 × 5 cm (QR kod, kratki kod ispod, naziv servisa) i letak (A6 ili A5) s uputama i mjestom za aktivacijski kod, spremni za ispis na papir za demo.

**Zašto:** QR s korekcijom H i kratki kod za ručni upis ispod koda (odluka 7), aktivacijski kod na papiru uz pločicu i letak koji obitelj dobiva (odluka 8), nekoliko demo QR kodova ispisanih na papiru (odluka 20). **Ovo je samo za demo. Ne naručuje se izrada i ne kontaktira se radionica.**

**Preduvjeti:** D-05 gotov, P-10 gotov (primjer QR SVG datoteke i koda).

> 🔁 **Predaja:** Petar predaje Karlu primjer QR SVG datoteke i 6-znakovnog koda iz demo serije (korak **P-10**).

**Novi pojmovi:**
- **Tihi rub (*quiet zone*)** je obavezni prazni (bijeli) rub oko QR koda, širok najmanje 4 modula. Bez njega mobitel teže čita kod.
- **Vektorska datoteka (SVG)** se može povećavati bez gubitka oštrine. QR kod se nikad ne umeće kao mutna slika.

**Upute:**
1. **Pločica 5 × 5 cm:**
   - QR kod (SVG iz P-10, ne mijenjaj mu proporcije, boje ni rub);
   - ispod kratki kod velikim, jasnim slovima (npr. `K7M4QX`);
   - po želji sitno `vjecnaspomen.hr`.

   Kontrast tamno na svijetlom (laser na inoxu daje tamno na svijetlom).
2. **Letak** (A6 ili A5):
   - naslov („Digitalna stranica sjećanja za Vaš grob”);
   - tri koraka sa slikom („1. Skenirajte kod kamerom mobitela. 2. Upišite aktivacijski kod s ovog letka. 3. Postavite lozinku i dodajte prvog pokojnika.”);
   - polje za aktivacijski kod (za demo upiši izmišljeni);
   - kratka adresa za ručni upis;
   - napomena da usluga uključuje postavljanje sadržaja ako to obitelj ne želi sama (odluka 3).

   Ne navodi stvarno groblje ni cijenu (odluka 20).
3. Izvezi PDF za ispis u stvarnoj veličini (100 %, bez skaliranja): jedan A4 list sa 6–9 demo pločica i jedan list s letkom.
4. Ispiši probno na kućnom pisaču i skeniraj QR s iPhonea i Androida s udaljenosti od 30–50 cm.

**Gotovo kada:**
- ispisana pločica ima QR točno 5 × 5 cm s tihim rubom (izmjeri ravnalom);
- QR se skenira s oba mobitela s 30–50 cm;
- kratki kod ispod QR-a čitljiv je s 50 cm;
- na letku nema stvarnog groblja, stvarnih osoba ni cijene.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Karlo predaje Petru PDF za ispis demo pločica i letka (`docs/demo-ispis/`) i Figma predložak u koji Petar ili Karlo umeću QR kodove demo serije. Time Petar može dovršiti **P-44**.

## Faza 7: Testiranje

Plan testiranja, testiranje na mobitelima i sa starijim osobama, popravci nalaza.

### D-32 Plan testiranja
- [ ] Gotovo

**Cilj:** u `docs/testiranje/plan.md` postoje scenariji testiranja za posjetitelja i vlasnika, popis uređaja, protokol razgovora sa starijim osobama i obrazac za bilježenje nalaza, a na GitHubu postoji predložak issuea „Nalaz testiranja”.

**Zašto:** testiranje na stvarnim mobitelima i sa starijim osobama je dio Karlovog posla (podjela posla, odluka 17). Mjerilo uspjeha 1 traži da tok radi na iPhoneu i Androidu (odluka 20).

**Preduvjeti:** D-04 gotov.

**Novi pojmovi:**
- **Scenarij** je zadatak opisan kao stvarna situacija, bez otkrivanja gdje treba kliknuti („Vaša sestrična vam je poslala lozinku. Pogledajte slike djeda Ivana.”).
- **Ozbiljnost nalaza:** 1 = osoba ne može završiti zadatak, 2 = završi uz muku ili pomoć, 3 = sitnica.
- **Predložak issuea** je obrazac koji GitHub ponudi pri otvaranju novog issuea. [GitHub: Issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)

**Upute:**
1. **Scenariji za posjetitelja:**
   - P1 skeniraj QR s papira i otvori profil lozinkom s papirića;
   - P2 pogledaj slike i pusti video;
   - P3 ostavi poruku u knjizi sjećanja;
   - P4 otvori obiteljski link iz poruke (WhatsApp ili Viber);
   - P5 nemaš lozinku: zatraži pristup.
2. **Scenariji za vlasnika:**
   - V1 aktiviraj pločicu s letkom;
   - V2 dodaj sliku i video s mobitela;
   - V3 odobri poruku;
   - V4 promijeni lozinku;
   - V5 pošalji obiteljski link rođaku;
   - V6 ponovno se prijavi putem e-maila.
3. **Uređaji i uvjeti:**
   - iPhone (Safari, aktualni iOS) i po mogućnosti stariji iPhone;
   - Android (Chrome) i Samsung (Samsung Internet);
   - zaslon širine 360 px ili manje;
   - povećan sistemski tekst;
   - tamni način rada;
   - spora mreža (u Chromeu na računalu: DevTools → Network → *Slow 4G*);
   - skeniranje ugrađenom kamerom i Google Lensom.
4. **Protokol za starije osobe:**
   - sudionici: 5 osoba starijih od 65 godina, po mogućnosti na vlastitom mobitelu, i 2–3 mlađe osobe kao „unuci” za vlasničke scenarije;
   - ne pozivaj osobe koje su nedavno izgubile nekoga bliskog;
   - na početku objasni da su sve osobe na stranici izmišljene, da testiraš stranicu a ne njih, da mogu prekinuti kad god žele i da ne snimaš lice;
   - usmeni pristanak; zvuk snimaš samo ako pristanu;
   - metoda „glasnog razmišljanja”, ti ne pomažeš osim ako osoba zapne dulje od 2 minute (to se bilježi kao ozbiljnost 1);
   - na kraju tri pitanja: što je bilo najteže, što vam se svidjelo, biste li ovo koristili za svoju obitelj.
5. **Što se promatra:** je li zadatak završen (da / uz pomoć / ne), koliko je trajao, gdje je osoba zastala, što je krivo dodirnula, što nije mogla pročitati, doslovni citati.
6. **Obrazac nalaza** (`.github/ISSUE_TEMPLATE/nalaz-testiranja.md`): scenarij, uređaj i preglednik, sudionik (samo dobna skupina, npr. „70–75”, bez imena), ozbiljnost, što se dogodilo, citat, prijedlog. Oznaka `nalaz-testiranja` dodaje se automatski.

**Gotovo kada:**
- `docs/testiranje/plan.md` sadrži sve scenarije, uređaje, protokol i obrazac;
- predložak issuea „Nalaz testiranja” pojavljuje se pri otvaranju novog issuea;
- plan nigdje ne traži prikupljanje imena, kontakata ni snimki lica sudionika;
- Petar je pregledao plan (PR).

**Procjena:** 3–4 sata.

### D-33 Prva runda testiranja na mobitelima
- [ ] Gotovo

**Cilj:** svi scenariji iz plana prošli su na svim uređajima i uvjetima s popisa (testira Karlo sam ili s Petrom), a svaki problem je zapisan kao issue.

**Zašto:** mjerilo uspjeha 1: tok skeniranje → lozinka → profil mora raditi na iPhoneu i Androidu (odluka 20). Tehničke probleme bolje je naći prije testiranja sa starijim osobama.

**Preduvjeti:** D-32 gotov, D-25, D-26 i D-27 gotovi, P-42 gotov (javni demo).

> 🔁 **Predaja:** Petar predaje Karlu javnu adresu demoa, demo kodove i lozinke te neaktivirane demo pločice s aktivacijskim kodovima, privatnom porukom (korak **P-42**). Isto vrijedi za D-34, D-37 i D-38.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Ispiši nekoliko demo QR kodova (dok D-31 nije gotov, dovoljan je QR iz ZIP-a demo serije na običnom papiru).
2. Svaki scenarij prođi na svakom uređaju iz D-32 i u svakom uvjetu (povećan tekst, tamni način, spora mreža).
3. Posebno provjeri:
   - HEIC fotografiju s iPhonea;
   - video snimljen u uspravnom položaju;
   - otvaranje obiteljskog linka iz WhatsAppa ili Vibera (otvaraju li ga u vlastitom pregledniku i ostaje li pristup zapamćen);
   - povratak na profil nakon 24 sata bez lozinke.
4. Svaki problem kao issue po predlošku „Nalaz testiranja”, sa snimkom zaslona.
5. Na kraju u `docs/testiranje/runda-1.md` napravi tablicu scenarij × uređaj s ✅ / ⚠️ / ❌.

**Gotovo kada:**
- tablica u `docs/testiranje/runda-1.md` je popunjena za sve scenarije i uređaje;
- svaki ⚠️ i ❌ ima issue;
- P1 (skeniranje → lozinka → profil) prolazi na barem jednom iPhoneu i jednom Androidu.

**Procjena:** 3–5 sati.

> 🔁 **Predaja:** Karlo predaje Petru issue nalaze s oznakom `nalaz-testiranja` (i `petar` za backend probleme) i tablicu `docs/testiranje/runda-1.md`. Time Petar može raditi **P-43**.

### D-34 Testiranje sa starijim osobama
- [ ] Gotovo

**Cilj:** pet starijih osoba prošlo je posjetiteljske scenarije, a dvije do tri mlađe osobe vlasničke scenarije, prema protokolu iz D-32, uz zapisane bilješke.

**Zašto:** velik dio budućih korisnika je starije životne dobi, a testiranje s bakama, djedovima i roditeljima je dio Karlovog posla (podjela posla, odluka 17).

**Preduvjeti:** D-32 i D-33 gotovi, D-31 gotov (ispisane demo pločice i letak), P-42 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Pripremi za svakog sudionika: ispisanu pločicu, papirić s lozinkom, za vlasnike letak s aktivacijskim kodom (neaktivirana demo pločica, svaki sudionik dobiva svoju), te praznu tablicu bilješki.
2. Susret traje 30–45 minuta. Najbolje u mirnom prostoru i po danu, a jedan scenarij po mogućnosti vani (sunce, odsjaj).
3. Slijedi protokol iz D-32 doslovno. Kad osoba zapne, zapiši točno gdje i što je rekla.
4. Bilješke piši odmah nakon svakog susreta, dok se sjećaš detalja.
5. Nakon svih susreta zamoli Petra da u adminu obriše grobove stvorene tijekom testiranja ili ponovno pokrene `napuni_demo`.

**Gotovo kada:**
- najmanje 5 starijih osoba i 2 mlađe osobe prošlo je scenarije;
- bilješke postoje za svaki susret, bez imena i kontakata sudionika;
- testni grobovi su obrisani ili je demo vraćen u početno stanje.

**Procjena:** 5–6 sati.

### D-35 Sažetak nalaza testiranja
- [ ] Gotovo

**Cilj:** u `docs/testiranje/nalazi.md` postoji sažetak nalaza testiranja sa starijim osobama, poredanih po ozbiljnosti i učestalosti, a svaki nalaz postoji kao issue.

**Zašto:** nalazi se moraju pretvoriti u konkretne popravke (D-36 i P-43), a sažetak ulazi u studiju slučaja (D-39).

**Preduvjeti:** D-34 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Grupiraj slične nalaze (npr. „4 od 5 osoba nije pronašlo gumb Prikaži lozinku”).
2. Za svaku grupu: ozbiljnost, broj osoba, citati, prijedlog popravka i tko ga radi (ti = izgled i tekst, Petar = ponašanje i logika).
3. Otvori issue za svaku grupu (oznaka `nalaz-testiranja`, plus `prijatelj` ili `petar`).
4. Zapiši i 3–5 stvari koje su dobro prošle, jer i to ide u studiju slučaja.

**Gotovo kada:**
- `docs/testiranje/nalazi.md` je spojen u `main`;
- svaki nalaz ozbiljnosti 1 i 2 ima issue s oznakom osobe koja ga popravlja.

**Procjena:** 2–3 sata.

> 🔁 **Predaja:** Karlo predaje Petru issue nalaze s oznakom `petar` i sažetak `docs/testiranje/nalazi.md`. Time Petar može dovršiti **P-43**.

### D-36 Popravci nalaza u dizajnu i predlošcima
- [ ] Gotovo

**Cilj:** svi nalazi ozbiljnosti 1 i 2 s oznakom `prijatelj` popravljeni su u Figmi i u predlošcima, a issuei su zatvoreni.

**Zašto:** mjerilo uspjeha 1 i čitljivost za starije korisnike (odluke 17 i 20).

**Preduvjeti:** D-35 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Najprije popravi u Figmi, zatim u predlošku. Figma i kod moraju ostati usklađeni.
2. Jedan PR po skupini srodnih nalaza, s `Popravlja #broj` u opisu.
3. Svaki popravak provjeri na mobitelu prije PR-a.

**Gotovo kada:**
- nema otvorenih issuea `nalaz-testiranja` ozbiljnosti 1 ili 2 s oznakom `prijatelj`;
- Figma odgovara spojenim predlošcima.

**Procjena:** 4–6 sati (ako je nalaza više, ponovi korak).

### D-37 Druga runda testiranja na javnom demou
- [ ] Gotovo

**Cilj:** nakon popravaka (D-36 i P-43) svi scenariji ponovno su prošli na iPhoneu i Androidu na javnom demou, s ispisanim demo pločicama, a rezultat je zapisan.

**Zašto:** potvrda mjerila uspjeha 1 do 4 na stvarnim mobitelima (odluka 20).

**Preduvjeti:** D-36 gotov, P-43 gotov.

> 🔁 **Predaja:** Petar javlja da su popravci iz **P-43** spojeni i objavljeni na demou.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Ponovi tablicu iz D-33 u `docs/testiranje/runda-2.md`.
2. Pokaži demo jednoj ili dvjema starijim osobama iz D-34 (ako žele) i provjeri jesu li glavni problemi nestali.
3. Novi problemi idu u Issues, a za ozbiljnost 1 dogovori s Petrom hitni popravak.

**Gotovo kada:**
- svi scenariji imaju ✅ na barem jednom iPhoneu i jednom Androidu;
- nema otvorenih nalaza ozbiljnosti 1.

**Procjena:** 2–3 sata.

> 🔁 **Predaja:** Karlo predaje Petru `docs/testiranje/runda-2.md`. Uz ispisane pločice iz D-31 to su ulazni podaci za zajedničku provjeru mjerila u **P-44**.

## Faza 8: Prezentacija za CV

Snimke zaslona, video demo i dizajnerski dio studije slučaja.

### D-38 Snimke zaslona i kratki video demo
- [ ] Gotovo

**Cilj:** u `docs/slike/` postoje uredne snimke zaslona glavnih ekrana s mobitela, a kratki video demo (60–120 sekundi) prikazuje tok skeniranje → lozinka → profil → knjiga sjećanja → vlasničko odobravanje.

**Zašto:** javno dostupan demo i uredan repozitorij za CV (odluka 20, mjerilo uspjeha 6).

**Preduvjeti:** D-37 gotov.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Snimke zaslona (samo demo podaci): zaključani ekran, profil, galerija, knjiga sjećanja, čarobnjak (2 koraka), popis medija s uploadom, odobravanje poruke, pregled za partnera. Po želji ih umetni u okvir mobitela u Figmi.
2. Video: snimanje zaslona na iPhoneu (*Kontrolni centar → Snimanje zaslona*) ili Androidu. Uvodni kadar može biti skeniranje ispisane pločice drugim mobitelom. Natpisi na hrvatskom, a po želji i engleski titlovi zbog CV-a.
3. Provjeri da se nigdje ne vide obavijesti, imena kontakata, e-mailovi ni lozinke osim demo lozinki.
4. Video stavi tamo gdje ga je lako otvoriti iz README-a (npr. kao privitak na GitHubu ili kao neizlistani YouTube video) i link zapiši u PR.

**Gotovo kada:**
- postoji najmanje 8 snimki zaslona u `docs/slike/` (svaka manja od 500 kB, u formatu WebP ili PNG);
- video traje 60–120 sekundi i prikazuje sva četiri koraka toka;
- ni na jednoj snimci ni u videu nema stvarnih osoba ni privatnih podataka.

**Procjena:** 3–4 sata.

> 🔁 **Predaja:** Karlo predaje Petru snimke u `docs/slike/` i link na video. Time Petar može dovršiti **P-45**.

### D-39 Studija slučaja: dizajn i testiranje
- [ ] Gotovo

**Cilj:** u zajedničkoj studiji slučaja postoji tvoj dio: proces dizajna, odluke o vizualnom identitetu i pristupačnosti, testiranje sa starijim osobama i promjene koje je ono donijelo (prije i poslije).

**Zašto:** primarni cilj MVP-a je portfolio i CV za oba člana tima (odluka 20).

**Preduvjeti:** D-38 gotov, P-45 gotov.

> 🔁 **Predaja:** Karlo predaje Petru svoj dio studije slučaja (PR). Time Petar može dovršiti **P-46**.

**Novi pojmovi:** nema novih; svi potrebni pojmovi objašnjeni su u ranijim koracima.

**Upute:**
1. Odjeljci:
   - korisnici (posebno stariji);
   - tokovi;
   - identitet (zašto ove boje i fontovi);
   - pristupačnost (brojke: kontrast, veličine, Lighthouse);
   - testiranje (metoda, broj sudionika, 3 glavna nalaza i kako ste ih riješili, sa snimkama prije i poslije);
   - što biste napravili drugačije.
2. Link na Figmu samo za gledanje: provjeri da Figma datoteka ne sadrži bilješke s testiranja s osobnim podacima.
3. Bez stvarnog groblja i stvarnih osoba (OP-9).

**Gotovo kada:**
- tvoj dio je spojen u `docs/studija-slucaja.md` (ili gdje se dogovorite u P-46);
- Petar je pregledao tekst;
- nema stvarnih osoba ni podataka sudionika testiranja.

**Procjena:** 3–4 sata.

## Kasnije, ako krenemo u pilot

Ništa od ovoga ne radi se prije veljače 2027. ni prije zajedničke odluke o pilotu (odluka 20). Popis služi da se ne zaboravi.

- **Pločica za stvarnu izradu:** vektorska datoteka pločice u točnoj veličini za lasersku radionicu, upute za izvedbu (odluke 7 i 9) i, kad se odabere izvođač, provjera probnog uzorka.
- **Upute za klesara:** kratki dokument s veličinom QR koda, tihim rubom i preporukom za tamni ili svijetli kamen (odluka 7).
- **Letak za tisak:** konačni letak s cijenom i nazivom groblja, nakon dogovora s upravom. Tiskanje u tiskari.
- **Test izdržljivosti uzoraka** (sol, mraz, ribanje kroz 2 do 3 mjeseca) zajedno s Petrom: fotografiranje i provjera skeniranja svaka 2 tjedna (odluka 7).
- **Razgovori s obiteljima u pilotu** (cilj iz odluke 20: 10 razgovora), s istim protokolom kao u D-32 i pisanim pristankom.
- **Materijali za upravu groblja:** kratka uputa za djelatnike šaltera („predajte pločicu i letak uz plaćeni račun”, odluke 8 i 10).
- **Vizualni materijali za Sve svete** (1. studenoga) kao trenutak za vidljivost (odluka 20).
- **Uvjeti korištenja i politika privatnosti:** dizajn stranica za tekstove koje pregledava pravnik (odluka 19).

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

Svaka MVP odluka iz `docs/odluke.md` pokrivena je barem jednim korakom. Petrovi koraci navedeni su radi potpunosti.

| Odluka | Što iz nje ulazi u MVP | Koraci (Karlo) | Koraci (Petar) |
|---|---|---|---|
| 1. Tko plaća i tko prodaje | partner, obračun | D-24, D-28 (pregled za partnera) | P-06, P-37 |
| 2. Pilot lokacija | rad na daljinu (obiteljski link) | D-04, D-08, D-22 | P-23, P-42 |
| 3. Uloge i uređivanje | vlasnik, posjetitelj, prijava linkom, odobravanje, usluga postavljanja | D-04, D-22, D-23, D-26, D-27, D-31 | P-17, P-21, P-22, P-33, P-35 |
| 3a. Obiteljsko stablo | odjeljak „Obitelj”, živuće osobe samo ime uz pristanak | D-09, D-18, D-23, D-27 | P-07, P-14, P-22 |
| 4. QR kod po grobu | stranica groba s popisom, izravni profil kad je pokojnik jedan | D-07, D-08, D-17 | P-07, P-11, P-22 |
| 5. Privatnost i pristup | zaključani ekran, lozinka, obiteljski link, zahtjev za pristup, zaključavanje, javni prikaz | D-08, D-17, D-22, D-26 | P-12, P-13, P-15, P-21, P-23, P-24, P-26 |
| 6. Opseg profila | biografija, galerija, video, obitelj, knjiga sjećanja | D-09, D-10, D-11, D-18, D-19, D-20 | P-14, P-31, P-33 |
| 7. Fizička oznaka | QR s korekcijom H, kratki kod ispod koda (demo na papiru) | D-31 | P-10 |
| 8. Izrada i aktivacija kodova | aktivacijski kod na letku, čarobnjak, neaktivirana pločica ne otkriva ništa | D-08, D-21, D-25, D-31 | P-10, P-11, P-18 do P-20 |
| 9. Odnos s izvođačima | – (samo demo) | D-31 (ostalo „Kasnije”) | P-10 |
| 10. Naplata | bez plaćanja u aplikaciji, mjesečni izvještaj | D-24, D-28 | P-37 |
| 11. Lokacija groba | oznaka grobnog mjesta u čarobnjaku, nevidljiva posjetiteljima | D-21, D-22 | P-07, P-19, P-37 |
| 12. Jednokratna cijena i čuvanje | ograničenja po grobu prikazana vlasniku | D-23, D-27 | P-08, P-28, P-30, P-31, P-36 |
| 13. Cijena | – (cijena se ne prikazuje u demou) | – | P-06, P-37 |
| 14. Financiranje | bez troškova osim hostinga i domene | – | P-42, P-47 |
| 15. Strategija rasta | ime partnera na zaključanom ekranu, pregled za partnera | D-08, D-24, D-28 | P-06, P-12, P-38 |
| 16. Web aplikacija | mobile-first, tri dijela, PWA za vlasnike | D-04 do D-28, D-30 | P-05, P-11, P-21, P-39 |
| 17. Tim i tehnologije | Figma, Django predlošci, Tailwind, HTMX, testiranje sa starijima | D-01 do D-03, D-13 do D-16, D-29, D-32 do D-36 | P-03 do P-05 |
| 18. Naziv, domena i format koda | 6-znakovni kod velikim slovima, aktivacijski kod od 8 znakova, ograničenja datoteka u porukama | D-08, D-21, D-23, D-31 | P-06, P-10, P-11, P-18, P-28 do P-30, P-47 |
| 18a. Jezik | samo hrvatski, tekstovi kroz `{% translate %}` | D-13, D-16 do D-28 | P-05, P-43 |
| 19. Vlasništvo i moderacija | „e-mail osobe koja će voditi profil”, knjiga uz odobrenje, „Prijavi”, GDPR | D-11, D-20, D-21, D-23 | P-07, P-19, P-33, P-34 |
| 20. Tempo i cilj | izmišljeni demo, ispisani QR, snimke, studija slučaja | D-07, D-31, D-37, D-38, D-39 | P-02, P-40, P-42, P-44 do P-46 |

### Mjerila uspjeha MVP-a (odluka 20) → koraci

| Mjerilo | Koraci |
|---|---|
| 1. skeniranje demo koda → lozinka → profil na iPhoneu i Androidu | D-08, D-17, D-18, D-31, D-33, D-37 (+ P-10 do P-14, P-42, P-44) |
| 2. aktivacija nove pločice od početka do kraja | D-21, D-25, D-34 (+ P-18 do P-20) |
| 3. upload slike i videa s mobitela uz automatsku obradu | D-23, D-27, D-33 (+ P-26 do P-32) |
| 4. knjiga sjećanja s odobravanjem | D-11, D-20, D-23, D-27 (+ P-33) |
| 5. administracija: partneri, serije pločica, mjesečni izvještaj | D-24, D-28 (+ P-09, P-10, P-35, P-37, P-38) |
| 6. javno dostupan demo i uredan repozitorij za CV | D-38, D-39 (+ P-42, P-45, P-46) |
