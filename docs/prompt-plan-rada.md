# Zadatak: izradi dva detaljna plana rada za projekt „Vječna spomen”

## 1. Tvoja uloga

Ti si iskusan tehnički voditelj i mentor koji vodi mali studentski tim kroz izradu prvog ozbiljnog web proizvoda. Znaš Django, HTMX, Tailwind CSS i proces dizajna u Figmi. Odlično objašnjavaš složene stvari jednostavnim jezikom, bez preskakanja koraka i bez pretpostavke da čitatelj „to već zna”.

## 2. Što trebaš pročitati prije bilo čega drugog

1. **Najprije pročitaj cijeli ovaj prompt.**
2. **Zatim pročitaj cijelu datoteku `docs/odluke.md`, od prve do zadnje linije.** U njoj su sve dogovorene odluke o proizvodu, poslovnom modelu, tehnologiji i pravilima, uz rječnik pojmova. To je jedini izvor istine o projektu.
3. Pogledaj što još postoji u repozitoriju (`ls`, `git log`). U trenutku pisanja ovog prompta repozitorij sadrži samo mapu `docs/`. Kod još ne postoji.

Ne počinji pisati planove dok ne pročitaš oba dokumenta. Pojmove koristi točno onako kako su definirani u rječniku u `docs/odluke.md` (grob, QR oznaka, pločica, pokojnik, profil, vlasnik, kontakt za prijavu, posjetitelj, partner, aktivacija, aktivacijski kod, knjiga sjećanja, srodnik).

## 3. Kontekst koji NIJE zapisan u `odluke.md`

Ove informacije su jednako obavezujuće kao i one u dokumentu:

- **Tim čine dvije osobe s udjelom 50/50:**
  - **Petar** (vlasnik repozitorija) radi **arhitekturu i sav razvoj**: Django modele, poglede i URL-ove, aktivaciju, lozinke i sigurnost, upload i obradu slika i videa (ffmpeg), pozadinske zadatke, Django admin, pregled za partnera i obračun, objavu na hosting i povezivanje s Cloudflare R2. Radi na macOS-u.
  - **Prijatelj** (dizajner i tester) radi **dizajn svih ekrana u Figmi**, pretvara dizajn u **HTML i Tailwind CSS predloške** (Django templates), radi **testiranje na stvarnim mobitelima** (iPhone i Android) i **testiranje sa starijim osobama** (bake, djedovi, roditelji), jer je velik dio budućih korisnika starije životne dobi. Operativni sustav prijatelja nije poznat, pa upute za instalaciju napiši za macOS i Windows.
- **Oba člana su prije radila s Pythonom i Djangom, ali je to znanje zahrđalo.** Svaki korak koji uvodi Django pojam (projekt i aplikacija, modeli, migracije, URL-ovi, pogledi, predlošci, forme, admin, statičke datoteke, postavke, upravljačke naredbe...) mora ukratko objasniti **što je to i zašto postoji**, uz link na odgovarajući dio službene Django dokumentacije. HTMX, Tailwind, Git, GitHub, `.env`, pozadinski zadaci i ffmpeg objasni od nule.
- **Petar je na Erasmusu do veljače 2027.** Projekt se radi **bez rokova i bez pritiska**, uz fakultet. **Ne zadaj datume.** Koristi faze i procjenu trajanja svakog koraka u satima, da tim sam rasporedi rad.
- **Primarni cilj je MVP spreman za demonstraciju, za portfolio i CV.** Pilot s upravom groblja, prodaja i investitori dolaze tek kasnije, i to samo ako tim tako odluči.
- **Do veljače 2027. nema nikakve komunikacije** s upravom groblja, klesarima, laserskim radionicama, pravnicima ni knjigovođama. Sve takve zadatke stavi u zaseban odjeljak „Kasnije, ako krenemo u pilot” na kraju odgovarajućeg plana. Neka ne budu pomiješani s razvojnim koracima.
- **GitHub repozitorij je javan.** Od prvog koraka vrijedi: nikakve lozinke, ključevi ni tokeni u Gitu. Sve ide u `.env` datoteku, koja je u `.gitignore`. U README ide napomena „Sva prava pridržana”, bez open-source licence.
- **Demo sadržaj koristi isključivo izmišljene osobe** i fotografije sa slobodnom licencom (npr. Unsplash, Pexels). Nikad stvarne pokojnike ni stvarne obitelji.
- **Aplikacija je samo na hrvatskom**, ali se svi tekstovi u predlošcima od početka pišu kroz `{% translate %}` / `gettext`, da se kasnije mogu dodati njemački i engleski.
- **U MVP-u nema online plaćanja.** Prodaju obavlja uprava na šalteru, a aplikacija samo bilježi aktivacije.
- **Domena vjecnaspomen.hr još nije registrirana.** Razvoj ide lokalno, a demo na besplatnu ili jeftinu poddomenu hostinga (Render ili Railway). Registracija domene je neobavezan korak koji Petar može napraviti u bilo kojem trenutku.

## 4. Tvoj zadatak

Izradi **dva odvojena dokumenta**:

1. `docs/plan/petar.md`: plan rada za Petra (arhitektura i razvoj)
2. `docs/plan/prijatelj.md`: plan rada za prijatelja (dizajn, predlošci, testiranje)

Svaki dokument mora biti **samodostatan**: osoba ga čita bez drugog dokumenta i zna točno što radi, kojim redom i kad je korak gotov. Ondje gdje rad jedne osobe ovisi o radu druge, to izričito navedi (vidi točku 6).

Planovi zajedno moraju pokriti **sve** što treba za ispunjenje svih šest mjerila uspjeha MVP-a iz odjeljka „20. Tempo i cilj” u `docs/odluke.md`, i **sve funkcije označene kao MVP** u tom dokumentu. Funkcije označene kao „faza 2” ili „izvan opsega” **ne planiraj**, nego ih samo navedi na kraju u odjeljku „Nije u MVP-u (namjerno)”.

## 5. Struktura svakog dokumenta

```
# Plan rada: <ime>

## Kako koristiti ovaj plan
(2–4 rečenice: redoslijed, kako označiti gotov korak, gdje tražiti pomoć)

## Pregled
(tablica svih faza: naziv faze, cilj, broj koraka, ukupna procjena sati)

## Faza 1: <naziv>
### <ID> <naziv koraka>
...

## Kasnije, ako krenemo u pilot
## Nije u MVP-u (namjerno)
## Otvorena pitanja
```

**Svaki korak ima točno ove dijelove:**

```
### P-07 Model Pločice i Serije pločica
- [ ] Gotovo

**Cilj:** jedna rečenica o tome što postoji nakon ovog koraka.
**Zašto:** jedna do dvije rečenice o tome kako korak služi proizvodu (s pozivom na točku u odluke.md, npr. „odluka 8”).
**Preduvjeti:** ID-ovi prethodnih koraka, uključujući korake druge osobe (npr. „D-04 gotov”).
**Novi pojmovi:** kratko i jednostavno objašnjenje svakog novog tehničkog pojma, uz link na službenu dokumentaciju.
**Upute:**
1. Konkretan korak, s naredbom ili isječkom koda gdje pomaže.
2. ...
**Gotovo kada:** provjerljivi kriteriji (npr. „u adminu mogu stvoriti seriju od 5 pločica i svaka ima jedinstven 6-znakovni kod bez znakova 0, O, 1, I, L”).
**Procjena:** X–Y sati.
**Česte greške:** 1–3 stvari na koje početnici obično nalete (neobavezno, samo kad je korisno).
```

ID-ovi: `P-01, P-02...` za Petra, `D-01, D-02...` za prijatelja. Numeriraj ih redom kojim se izvode.

## 6. Usklađivanje dvaju planova

- Gdje se rad predaje između dvije osobe, u oba dokumenta dodaj blok **„🔁 Predaja”**: tko predaje što, u kojem obliku (npr. Figma link, HTML predložak u `templates/...`, popis varijabli koje pogled šalje predlošku), te koji korak druge osobe time može krenuti.
- Organiziraj rad tako da **nitko dugo ne čeka**. Prijatelj može dizajnirati u Figmi dok Petar radi modele. Petar može raditi na „ružnim” privremenim predlošcima dok prijatelj ne preda prave.
- Dogovori zajednički način rada i opiši ga u oba dokumenta jednako: Git grane, pull requestovi koje drugi član pregleda, struktura mapa `templates/` i `static/`, gdje se prijavljuju bugovi (npr. GitHub Issues). Neka bude jednostavno, primjereno dvočlanom studentskom timu.
- Prvi korak u **oba** plana je zajednički: postavljanje alata (Git, GitHub pristup, Python ili Node po potrebi, uređivač koda, Figma) i kratki zajednički sastanak (može i video poziv) na kojem oba člana pročitaju `docs/odluke.md`.

## 7. Što plan mora obuhvatiti (minimalni popis)

Ovaj popis nije redoslijed. Redoslijed odredi ti, tako da se što prije dobije prva radna verzija „QR → lozinka → profil”, a ostalo se nadograđuje.

**Petar:** kostur Django projekta i postavke iz `.env`; PostgreSQL lokalno; Tailwind i HTMX u Djangu; modeli podataka i njihove veze za sve pojmove iz rječnika (uključujući partnera s postotkom provizije, serije pločica, pločicu sa statusom neaktivirana/aktivirana, grob s tekstualnom oznakom grobnog mjesta, vlasnika i kontakt za prijavu kao odvojena polja, pokojnika, srodnika s vrstom srodstva, medij s ograničenjima, poruku u knjizi sjećanja sa statusom odobrenja, prijavu sadržaja); dijagram modela u `docs/`; generiranje kodova i QR slika (velika slova, korekcija H); zaključani ekran, lozinka groba, pamćenje uređaja, zaključavanje nakon više pogrešnih pokušaja; obiteljski link koji se može poništiti; zahtjev za pristup; čarobnjak za aktivaciju; prijava vlasnika linkom na e-mail; upload s mobitela, pretvorba HEIC→JPEG/WebP, smanjivanje slika, video u 720p kroz pozadinski zadatak, ograničenja po datoteci i po grobu; privremeni potpisani linkovi za medije (Cloudflare R2); knjiga sjećanja s odobravanjem; gumb „Prijavi”; zaštita od indeksiranja (`noindex`, `robots.txt`); Django admin za partnere, serije i izvještaje; mjesečni izvještaj o aktivacijama po partneru; demo podaci kroz upravljačku naredbu; automatski testovi za kritične dijelove (aktivacija, lozinka, dozvole); objava na Render ili Railway; README i javna studija slučaja za CV.

**Prijatelj:** korisnički tokovi (posjetitelj, vlasnik, administrator); vizualni identitet (dostojanstven, smiren, čitljiv za starije: veliki fontovi, jak kontrast, velike tipke); dizajn svih MVP ekrana mobile-first u Figmi (stranica groba s popisom pokojnika, zaključani ekran, profil, galerija, video, odjeljak „Obitelj”, knjiga sjećanja, čarobnjak za aktivaciju, vlasnički dio za uređivanje i odobravanje, prazna stanja i poruke o greškama); osnove Django predložaka, Tailwinda i HTMX-a, toliko koliko treba za njegov dio; izrada predložaka; pristupačnost (kontrast, veličine, čitači zaslona); dizajn QR pločice i letka za upravu (samo za demo, bez naručivanja); izmišljeni demo sadržaj; plan i provedba testiranja na mobitelima i sa starijim osobama (scenariji, što se promatra, kako se bilježe nalazi); snimke zaslona i kratki video demo za studiju slučaja.

## 8. Pravila pisanja

- **Jezik:** hrvatski standardni jezik, jednostavan i izravan. Obraćaj se čitatelju u drugom licu („otvori”, „pokreni”). Tehnički pojmovi i naredbe ostaju na engleskom, ali ih objasni.
- **Ne izmišljaj nove poslovne ili produktne odluke.** Ako naiđeš na nešto što `odluke.md` ne pokriva, a za izvedbu je potrebno, upiši to u „Otvorena pitanja” sa svojim prijedlogom i obrazloženjem. Za sitne tehničke odluke (npr. naziv Django aplikacije) odluči sam i ukratko obrazloži.
- **Budi konkretan.** Umjesto „postavi bazu” napiši točne naredbe. Umjesto „napravi lijep dizajn” napiši koje ekrane, za koje stanje i s kojim zahtjevima.
- **Koraci moraju biti mali:** jedan korak traje 1 do 6 sati. Veće cjeline razbij.
- **Ne piši cijelu aplikaciju unutar plana.** Isječci koda smiju pokazati ključnu ideju (do ~25 linija). Plan nije zamjena za kod.
- **Verzije alata:** navodi aktualne stabilne verzije i provjeri ih ako imaš pristup webu. Ako nemaš, napiši „provjeri najnoviju stabilnu verziju” umjesto da pogađaš.
- **Sigurnost je dio koraka, a ne zaseban dodatak na kraju.** Svaki korak koji dira lozinke, medije, prijavu ili dozvole mora u „Gotovo kada” imati sigurnosni kriterij.

## 9. Provjera prije predaje

Prije nego završiš, prođi ovu listu i popravi što ne valja:

- [ ] Pročitao sam cijeli `docs/odluke.md` i svaka MVP odluka iz njega pokrivena je barem jednim korakom (dodaj na kraj svakog dokumenta tablicu „Odluka → koraci”).
- [ ] Svih šest mjerila uspjeha MVP-a (odluka 20) ostvarivo je kad se svi koraci završe.
- [ ] Nijedan korak ne uključuje kontakt s upravom, klesarima, radionicama, pravnicima ni troškove osim hostinga i neobavezne domene.
- [ ] Svaki korak ima sve obavezne dijelove, a „Gotovo kada” je provjerljiv.
- [ ] Svaka ovisnost o drugoj osobi navedena je u oba dokumenta s istim ID-ovima.
- [ ] Nema datuma, samo faze i procjene u satima.
- [ ] Nema lozinki ni ključeva u primjerima koda (koriste se `os.environ` / `.env`).
- [ ] Novi pojmovi objašnjeni su na prvom mjestu gdje se pojave.
- [ ] Pojmovi su usklađeni s rječnikom u `docs/odluke.md`.

## 10. Završna poruka

Kad zapišeš obje datoteke, u odgovoru navedi samo:
1. putanje obiju datoteka;
2. broj faza i koraka te ukupnu procjenu sati za svaku osobu;
3. popis otvorenih pitanja (ako ih ima).

Ne ponavljaj sadržaj planova u odgovoru.
