# Odluke projekta

Studentski projekt koji potencijalno prerasta u startup: QR kod na grobu otvara digitalnu stranicu sjećanja na pokojnika.

Odluke se bilježe redom kako se donose.

## Proizvod i korisnici

### 1. Tko plaća i tko prodaje
- **Plaća obitelj pokojnika. Prodajni kanal je uprava groblja** (B2B2C): uprava nudi uslugu obitelji pri ugovaranju ukopa.
- **Podjela prihoda (prijedlog za pregovore):** 25 % upravi, 75 % nama, računato od bruto cijene. Ako uprava preuzme i montažu pločice, ide do 35 % uprave.
  - Naših 75 % pokriva proizvodnju pločice, hosting, razvoj i podršku.
  - Provizija ide poduzeću, a ne pojedinim djelatnicima (sukob interesa u javnom poduzeću).
- **Vremenski tok:** prodaja u trenutku ugovaranja ukopa, profil se aktivira odmah, pločica se postavlja na privremeno obilježje ili kasnije na spomenik.
- **Sporedni kanali (kasnije):** klesari i izravna web narudžba za postojeće grobove.

### 2. Pilot lokacija
- **Groblje u Crikvenici.** Postoji izravan kontakt s direktorom uprave.
- Ponuda: besplatni pilot na 6 mjeseci, uprava ne snosi trošak i dobiva proviziju od svake prodaje.
- Prije sastanka pročitati gradski pravilnik o grobljima (što je dopušteno postaviti na grob).
- Uočeno: dio obitelji živi izvan Crikvenice ili u inozemstvu, pa stranica mora raditi i na daljinu, ne samo uz skeniranje na grobu.

### 3. Uloge i uređivanje sadržaja
- **Vlasnik profila** (MVP): jedan član obitelji, kupac usluge. Uređuje sve i odobrava tuđe priloge.
- **Posjetitelj** (MVP): gleda sadržaj i ostavlja poruku u knjizi sjećanja, koja čeka odobrenje vlasnika.
- **Urednik** (faza 2): član obitelji kojeg vlasnik pozove.
- Prijava bez lozinke, linkom poslanim e-mailom.
- Usluga u pilotu: „pošaljite nam slike, mi postavimo” za vlasnike koji to ne mogu sami.

### 3a. Obiteljsko stablo
- **MVP:** odjeljak „Obitelj” sa srodnicima pokojnika i vrstom srodstva (supruga, sin, otac...). Srodnik koji i sam ima profil povezuje se na njega klikom.
- **Faza 2:** interaktivni vizualni prikaz stabla kroz više generacija.
- **Živuće osobe:** prema van se prikazuje samo ime, uz pristanak. Bez datuma rođenja, kontakata i slika (GDPR).

### 4. QR kod po grobu
- **Jedan QR po grobu**, ne po osobi. Kod otvara stranicu groba s popisom pokojnika, a svaki pokojnik ima svoj profil.
- Ako je u grobu samo jedan pokojnik, kod odmah otvara njegov profil.
- Novi ukop u isti grob znači novi profil bez nove pločice, uz dodatni prihod „dodaj profil u postojeći grob”.
- Uprava groblja već vodi evidenciju po grobnim mjestima, pa je logika usklađena s njihovom.

### 5. Privatnost i pristup
- **Zadano je sve privatno**, iza lozinke. Javni prikaz je opcija koju vlasnik može uključiti.
- Nakon skeniranja otvara se **zaključani ekran**: ime groba ili obitelji, polje za lozinku i gumb „Zatraži pristup” (šalje zahtjev vlasniku).
- **Jedna lozinka po grobu.** Postavlja je i mijenja vlasnik, a obitelj je prenosi usmeno ili porukom.
- **Uređaj se pamti** (oko 12 mjeseci) pa se lozinka ne upisuje kod svakog posjeta.
- **Obiteljski link** s ugrađenim pristupom (bez upisa lozinke) za rođake na daljinu. Vlasnik ga može poništiti.
- **Sigurnost:** zaključavanje nakon više pogrešnih pokušaja, lozinka od najmanje 6 znakova, mediji dostupni samo preko privremenih potpisanih linkova (nikad javni URL), profili se ne indeksiraju na tražilicama.

### 6. Opseg profila
- **MVP:** biografija, galerija slika, video, odjeljak „Obitelj”, knjiga sjećanja.
- **Faza 2:** audio, vremenska crta života, virtualna svijeća, podsjetnici na godišnjice.
- **Izvan opsega:** navigacija do groba.

### 7. Fizička oznaka: dvije opcije
- **Osnovna: inox pločica** (AISI 316, laserska gravura, oko 5 × 5 cm, lijepljena dvokomponentnim ljepilom za kamen).
- **Premium: gravura izravno u kamen** (skuplje, nema pločice, grob izgleda urednije).
  - Najbolje radi na tamnom granitu (laser posvjetljava kamen). Na svijetlom kamenu treba pjeskarenje i ispunu bojom.
  - Gravura je nepovratna, pa link u kodu mora zauvijek ostati isti (kratki trajni ID na našoj domeni).
  - Spomenik se postavlja mjesecima nakon ukopa. Do tada grob dobiva privremenu oznaku (inox pločicu ili naljepnicu), a profil radi od prvog dana.
- **Za obje opcije:** QR s korekcijom pogrešaka razine H, kratki link, ispod koda ugraviran kratki kod za ručni upis. NFC izvan opsega.
- **Prije pilota:** test izdržljivosti 3 do 5 uzoraka (sol, mraz, ribanje) kroz 2 do 3 mjeseca.
- **Izvođači: otvoreno.** Pretraga weba nije dala potvrđenu radionicu na potezu Rijeka–Crikvenica–Senj. Sljedeći koraci:
  1. pitati direktora groblja koji klesari rade na crikveničkom groblju;
  2. Google Maps / eMajstor: „lasersko graviranje Rijeka”, „CNC obrada metala Rijeka”, „klesar Crikvenica / Novi Vinodolski”;
  3. Tehnički fakultet u Rijeci (RITEH): laboratorij ili kontakt preko profesora za izradu testnih uzoraka.

### 8. Izrada i aktivacija kodova
- **Inox: unaprijed izrađene prazne pločice** u serijama (npr. 50 komada) sa slučajnim kodovima. Uprava ih drži na zalihi.
- Uz svaku pločicu ide **aktivacijski kod** na papiru (kao PIN na bonu). Bez njega se pločica ne može aktivirati.
- Djelatnik uprave samo preda pločicu i letak. Obitelj sama skenira kod i prolazi čarobnjak: aktivacijski kod → lozinka groba → prvi pokojnik → slike.
- Skeniranje neaktivirane pločice bez aktivacijskog koda ne otkriva ništa.
- Svaka pločica u sustavu nosi podatak koja ju je uprava dobila. Provizija se iz toga obračunava automatski.
- **Gravura u kamen:** klesar ugravira isti kod koji je obitelj već aktivirala na privremenoj pločici.

### 9. Odnos s izvođačima
- **Laserska radionica je čisti dobavljač:** fiksna cijena po komadu za seriju, nema kontakta s obiteljima. Radionica čuva datoteku s dizajnom, a za novu seriju dobiva samo popis kodova.
- **Klesar naplaćuje gravuru izravno obitelji**, kao stavku uz spomenik. Mi ne posredujemo novcem i ne odgovaramo za klesarski posao.
- Klesaru dajemo gotovu vektorsku datoteku QR koda u točnoj veličini i kratke upute za izvedbu.
- **Faza 2:** klesar kao sporedni prodajni kanal za grobove bez QR oznake, uz proviziju od 15 do 20 %.

### 10. Naplata
- **Uprava naplaćuje obitelji** na svojoj blagajni, uz ostale troškove ukopa. Pretpostavka je da će uprava lakše pristati na ovaj model.
- **Model veleprodaje:** mi upravi prodajemo uslugu po veleprodajnoj cijeni (75 % maloprodajne), a uprava je preprodaje obitelji. Razlika od 25 % je zarada uprave. Pravno i knjigovodstveno je to jednostavnije od provizije.
- **Pločice u komisiji:** uprava drži zalihu, a mi fakturiramo samo prodane komade.
- Uprava predaje obitelji **pločicu i aktivacijski kod tek uz plaćeni račun.** Aplikacija zato nema plaćanje u MVP-u.
- **Mjesečni obračun:** sustav generira izvještaj o aktiviranim pločicama. Usklađujemo ga s prodajom uprave i izdajemo račun, s rokom plaćanja od npr. 15 dana.
- Za izdavanje računa treba pravni subjekt (paušalni obrt ili j.d.o.o.) prije prve prodaje. Za pilot je dovoljan sporazum o suradnji.
- Uprava će možda morati uvesti novu stavku u cjenik. Treba provjeriti s direktorom tko to odobrava.

### 11. Lokacija groba
- Pri aktivaciji se upisuje **tekstualna oznaka grobnog mjesta** (npr. „Polje C, red 4, br. 12”), prepisana s računa uprave.
- Oznaka se ne prikazuje posjetiteljima. Služi upravi i nama za održavanje (oštećene pločice, premještanje na spomenik, popisi).
- **Bez integracije** s programom uprave u MVP-u. Integracija i karta groblja dolaze u fazi skaliranja.

## Poslovni model

### 12. Jednokratna cijena s trajnim čuvanjem
- Obitelj plaća **jednom**, a cijena uključuje trajno čuvanje sadržaja. Nema pretplate, jer uprava naplaćuje na šalteru.
- **Ograničenje po grobu:** oko 300 slika i 20 minuta videa (oko 2 GB nakon kompresije).
- **Fond za čuvanje:** oko 15 € od svake prodaje odvaja se za dugoročnu pohranu. Procijenjeni trošak je oko 0,40 € godišnje po grobu.
- **Dodatna pohrana** kao jednokratna nadoplata (faza 2, online plaćanje).
- **Gašenje servisa:** obavijest 6 mjeseci unaprijed i izvoz svih sadržaja (ZIP). Ta obveza ulazi u uvjete korištenja.
- **Domena** se plaća 10 godina unaprijed, ako registar to dopušta.
- Video se pri postavljanju automatski kompresira.

### 13. Cijena

**Odluka:**

| Paket | Cijena | Uprava (25 %) | Nama |
|---|---|---|---|
| **Osnovni, sve uključeno** (grob, prvi pokojnik, inox pločica, postavljanje sadržaja po želji obitelji) | **119 €** | ~30 € | ~89 € |
| **Dodatni pokojnik u postojeći grob** (uključeno postavljanje sadržaja) | **49 €** | ~12 € | ~37 € |
| **Pilot** (prvih 10 do 15 obitelji, u zamjenu za povratne informacije) | **49 €** | ~12 € | ~37 € |
| **Gravura u kamen** | prema cijeni klesara | – | – |

- Nama od osnovnog paketa ostaje: 89 € − pločica ~10 € − fond za čuvanje 15 € = **~64 €** (prije troška rada na postavljanju sadržaja).
- Argument prema tržištu: jednokratno i trajno, dok domaći konkurent (LOGRO) s godišnjom obnovom kroz 10 godina stoji oko 210 €.

**Istraživanje konkurencije (studeni 2026.)**

Prosječne neto plaće: Hrvatska ~1.555 € (Primorsko-goranska ~1.564 €, DZS, 2026.), Slovenija ~1.720 €, Njemačka ~3.000 €, Austrija ~2.700 € (procjena, izvori nisu usklađeni).

| Konkurent | Država | Ponuda | Cijena | Prilagođeno HR plaći |
|---|---|---|---|---|
| LOGRO | HR | QR + profil, 1. godina, zatim godišnja obnova | 720 kn (~96 €) + 100 kn (~13 €) godišnje (stari cjenik) | – |
| Spominko | SI | QR pločica + stranica | 49,99 € (redovno 99,99 €) | ~45–90 € |
| Candlebook | SI | aluminijska pločica + pretplata | 24,40 € + 3,05 € mjesečno | – |
| digitale-gedenkseite.at | AT | inox pločica + stranica, bez pretplate | od 169 € | ~96 € |
| InErinnerung.at | AT | paket na 5 / 10 godina | 180 / 250 € | ~103 / 143 € |
| Gedankraum | DE | aluminijska pločica + 10 godina | 155 € | ~81 € |
| Monumeo | DE | premium stranica + aluminijska pločica | 165 € | ~86 € |
| Living Headstones | SAD | preko klesara | 125–156 $ | – |

Zaključak: usporedive usluge, prilagođene hrvatskom standardu, stoje oko **85–100 €**. Jedini poznati domaći konkurent (LOGRO) naplaćuje godišnju obnovu, pa kroz 10 godina stoji oko 210 €.

### 14. Financiranje
- **MVP i pilot financiramo sami.** Procjena: ~800–1.000 € bez troškova pravnog subjekta (domena, hosting, testne pločice, prva serija od 50 pločica, letci).
- **Investitore tražimo tek nakon pilota** (cilj: 30+ prodaja i zadovoljna uprava), da bi se pregovaralo s brojkama.
- **Besplatni izvori prije investitora:** STEP RI (inkubacija i mentorstvo), studentska natjecanja i natjecanja poslovnih ideja, programi za rane faze (npr. HAMAG-BICRO; provjeriti dostupnost).
- **Poželjan profil investitora:** netko iz struke (pogrebno poduzeće, klesarska tvrtka, lokalni poduzetnik) s kontaktima na drugim grobljima.
- **Otvoreno, rizik:** oblik pravnog subjekta za studente (mjesečni doprinosi kod obrta, status studenta). Prije otvaranja potrebno je savjetovanje s knjigovođom ili Obrtničkom komorom.

### 15. Strategija rasta
- **Cilj: širenje na druga groblja** (Rijeka, Novi Vinodolski, Senj, pa cijela Hrvatska i regija), s istim modelom prodaje preko uprave.
- **Sustav od prvog dana podržava više partnera.** Svaka pločica i svaki grob pripadaju partneru. Partner ima naziv, kontakt i vlastiti postotak provizije.
- **Pregled za partnera** (MVP): broj prodanih i aktiviranih pločica te mjesečni izvještaj.
- Ime groblja ili uprave prikazuje se na zaključanom ekranu.
- **Mogući izlaz:** prodaja tvrtke strateškom kupcu. Vrijednost čine ugovori s grobljima i broj aktivnih grobova.
- **White-label licenca:** ne zasad, tek ako se javi konkretan interes.

## Tehnologija

### 16. Web aplikacija
- **Web aplikacija bez instalacije, prilagođena prvenstveno mobitelu.** Skeniranje QR koda vodi izravno na zaključani ekran.
- Mogućnost dodavanja na početni zaslon (PWA) za vlasnike.
- Jedna aplikacija s tri dijela: **javni** (posjetitelji), **vlasnički** (obitelj), **administracija** (mi i partneri).
- Nativna aplikacija: ne u MVP-u, a kasnije eventualno samo za vlasnike (obavijesti).

### 17. Tim i tehnologije
- **Tim (2 osobe):** Petar (arhitektura i razvoj), prijatelj (dizajn i testiranje).
- Tim ima prethodno iskustvo s Pythonom i Djangom, ali ga treba osvježiti.
- **Tehnologije** (odabrane prema iskustvu tima):

| Dio | Tehnologija |
|---|---|
| Backend i stranice | Django + Django templates |
| Interaktivnost | HTMX (+ Alpine.js po potrebi) |
| Izgled | Tailwind CSS (dizajn u Figmi) |
| Baza | PostgreSQL |
| Administracija | Django admin; jednostavan pregled izvještaja za partnere |
| Prijava vlasnika | link na e-mail (`django-sesame`) |
| Pohrana medija | Cloudflare R2 preko `django-storages` |
| Obrada videa | ffmpeg (pretvorba u 720p) u pozadinskom zadatku (`django-q2` ili Huey) |
| Hosting | Render ili Railway, ~15–25 € mjesečno za pilot |

- Specijalizirani video servisi (Mux, Cloudflare Stream) odbačeni su zbog mjesečne naplate po minuti, koja nije održiva uz jednokratnu cijenu.
- **Udjeli: 50/50.** Detalje (vlasništvo koda, dizajna i naziva, odlazak iz projekta, odluka o prodaji, troškovi) dogovaraju dvojica članova tima u kratkom pisanom dogovoru. Taj dogovor postaje temelj za udjele u budućem j.d.o.o.-u.
- **Podjela posla:** Petar radi modele, aktivaciju, sigurnost, medije, administraciju i obračun. Prijatelj radi dizajn u Figmi, HTML/Tailwind predloške i testiranje na mobitelima, uključujući starije korisnike.

### 18. Naziv, domena i format koda
- **Naziv i domena: vjecnaspomen.hr** (+ vjecnaspomen.com zbog zaštite). Plaćaju se više godina unaprijed. **Dostupnost treba provjeriti i registrirati domenu prije narudžbe pločica.**
- **Format linka:** `https://vjecnaspomen.hr/g/K7M4QX`
  - 6 znakova iz abecede bez dvosmislenih znakova (bez 0/O, 1/I/L).
  - Link se u QR kod upisuje **velikim slovima** (`HTTPS://VJECNASPOMEN.HR/G/K7M4QX`), pa QR koristi alfanumerički način i stane u verziju 3 (29 × 29 modula) uz korekciju H. Na pločici od 5 cm, uz obavezni bijeli rub, to daje module od oko 1,3 mm, koji se lako skeniraju i dugo traju.
  - Rute u aplikaciji ne razlikuju velika i mala slova.
- **Aktivacijski kod:** 8 znakova, samo na papiru uz pločicu.
- **Ograničenja datoteka:** video do 5 minuta i 1 GB po isječku (pretvara se u 720p). Slike se pretvaraju iz HEIC u JPEG ili WebP i smanjuju na ~2048 px.

### 18a. Jezik
- **MVP je samo na hrvatskom.** Njemački i engleski dolaze kasnije.
- Tekstovi u predlošcima ipak se od početka pišu kroz Djangov sustav prijevoda (`{% translate %}`), da bi se kasnije dodao jezik bez prerade.
- Sadržaj (biografije, poruke) obitelj piše na jeziku koji želi i on se ne prevodi.

## Pravila i pravno

### 19. Vlasništvo, sporovi i moderacija
- **Vlasnik profila je osoba koju uprava vodi kao korisnika grobnog mjesta**, ili osoba koju ona ovlasti. U sporu odlučuje evidencija uprave, a ne mi.
- **Prijenos vlasništva:** uz potvrdu uprave ili pisani pristanak dosadašnjeg vlasnika.
- **Vlasnik i kontakt za prijavu su odvojeni.** Vlasnik je osoba iz evidencije uprave (ime, zbog sporova). Kontakt za prijavu je e-mail osobe koja vodi profil, npr. djeteta ili unuka. Čarobnjak traži „e-mail osobe koja će voditi profil”.
- Promjena kontakta za prijavu ide uz potvrdu vlasnika ili uprave.
- Prijava SMS-om nije u MVP-u. Starijima bez pomoći služi usluga postavljanja sadržaja (uključena u cijenu).
- **Knjiga sjećanja:** objava tek uz vlasnikovo odobrenje.
- **Gumb „Prijavi”** na svakom sadržaju. Odgovaramo u roku od 7 dana. Ne pregledavamo sadržaj unaprijed, nego reagiramo na prijave.
- **Zahtjev živuće osobe za uklanjanje vlastite slike** (GDPR) ima prednost pred željom vlasnika.
- **Dokumenti prije pilota:** uvjeti korištenja, politika privatnosti (GDPR, podaci na EU poslužiteljima), ugovor s upravom. Nacrte radimo sami, a pregledava ih pravnik (pravna klinika PFRI, STEP RI ili poznanik).

## Plan

### 20. Tempo i cilj
- **Bez rokova i pritiska.** Petar je na Erasmusu do veljače 2027.
- **Primarni cilj: funkcionalan MVP za portfolio i CV**, uz mogućnost kasnije prodaje ili pokretanja pilota.
- **Do veljače 2027.:** samo razvoj. Nema komunikacije s upravom, klesarima ni radionicama.
- **MVP mora biti spreman za demonstraciju:** izmišljeni demo grob s pokojnicima, slikama i videom, nekoliko demo QR kodova (ispisanih na papiru), čarobnjak za aktivaciju i administracija koji rade od početka do kraja. Javno dostupan na webu, uz README s opisom arhitekture.
- **Odgođeno do odluke o pilotu:** sastanak s direktorom, test izdržljivosti pločica, pravni subjekt, pravni dokumenti, narudžba pločica.
- **Neobavezno:** registrirati vjecnaspomen.hr ranije (mali trošak) kako bi se zadržao naziv.
- **Mjerila uspjeha MVP-a:**
  1. skeniranje demo koda → lozinka → profil radi na iPhoneu i Androidu;
  2. aktivacija nove pločice od početka do kraja;
  3. upload slike i videa s mobitela uz automatsku obradu;
  4. knjiga sjećanja s odobravanjem;
  5. administracija: partneri, serije pločica, mjesečni izvještaj;
  6. javno dostupan demo i uredan repozitorij za CV.
- **Repozitorij je zasad javan** (GitHub), radi CV-a.
  - Bez open-source licence. U README stoji „Sva prava pridržana”, pa drugi kod smiju gledati, ali ga ne smiju koristiti.
  - Repozitorij se kasnije može prebaciti u privatni (npr. prije prodaje ili pilota), ali kopije napravljene do tada ostaju vani.
  - Tajni podaci (ključevi, lozinke) nikad ne idu u Git. Koristi se `.env` uz `.gitignore`.
  - Demo sadržaj koristi samo izmišljene osobe i slobodne fotografije.
- **Mjerila pilota** (ako se pokrene): 30 prodaja u 6 mjeseci, ≥ 80 % aktivacija, 10 razgovora s obiteljima, uprava želi nastaviti, jedno novo zainteresirano groblje. Dobar trenutak za vidljivost su Svi sveti (1. studenoga).

## Rječnik pojmova

| Pojam | Značenje |
|---|---|
| **Grob** | Fizičko grobno mjesto (i obiteljska grobnica). Ima točno jednu QR oznaku i jednog ili više pokojnika. |
| **QR oznaka** | Fizički QR kod na grobu s trajnim kratkim ID-om. Izvodi se kao inox pločica (osnovna opcija) ili gravura u kamen (premium). |
| **Aktivacijski kod** | Tajni kod isporučen uz pločicu. Njime obitelj pločicu veže uz svoj grob i postaje vlasnik. |
| **Aktivacija** | Trenutak kad neaktivirana pločica postaje QR oznaka određenog groba. |
| **Partner** | Organizacija koja prodaje uslugu i dobiva proviziju (u pilotu uprava groblja Crikvenica). |
| **Pokojnik** | Preminula osoba ukopana u grob. |
| **Profil** | Digitalna spomen-stranica jednog pokojnika: biografija, slike, videi, obitelj, knjiga sjećanja. |
| **Vlasnik** | Osoba koja upravlja profilima groba. To je korisnik grobnog mjesta prema evidenciji uprave ili osoba koju on ovlasti. |
| **Kontakt za prijavu** | E-mail osobe koja stvarno vodi profil u ime vlasnika. Na njega stiže link za prijavu. Može biti različit od vlasnika. |
| **Posjetitelj** | Bilo tko tko skenira kod ili otvori link. |
| **Knjiga sjećanja** | Poruke posjetitelja na profilu, vidljive tek nakon odobrenja vlasnika. |
| **Srodnik** | Osoba povezana s pokojnikom vrstom srodstva. Može biti drugi pokojnik s vlastitim profilom ili živuća osoba (samo ime). |
