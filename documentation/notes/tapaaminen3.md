# Asiakastapaaminen 3

Selitetään, mitä tehty tällä sprintillä: staging ympäristön pystytys (tekniset ongelmat), tietokanta pystyssä, plain txt tiedostot, ekat promptit ajaettu komentoriviltä käsin. 

## Heikin kommentteja ja neuvoja puheesta tekstiksi

Heikki: Asennettaan alkuun Linux-työasema lokaalisti - ei kannata laittaa virtuaaliserverin asentamiseen liikaa aikaa nyt alkuun.


Heikki:

Gemma parhaita monikielisiä malleja, joilla toimii suomi.
Litteroidaan yksi politiinnen väite kerrallaan
Aluksi yksi claim kerrallaan, monta toistoa kerralla--> vähemmän randomeita tuloksia.
Ollaan ongelman ytimessä: alkuperäiset claimit ovat vain yhden ihmisen koodaus. Voi olla sattumia. Muutetaan lennossa spekseja? Voisi tulla järkevää outputtia. Tilastoja varten pitäisi saada rakenteisttua outputtia jsoniin. Frontier malleilla voi system levelillä pyytää, että inputista tulee jsonia, mutta joissain malleissa voi tulla puhdasta jsonia, joskus ei. 

Seuraava luonnollinen steppi saada vähän iterointia: nämä lausunnot, nämä claimit, nämä ajot. EI turhaa aikaa käyttiksen säätöön. 

Kovakoodataan promptit toistaseks, ettei käyttäjän tarvitse itse antaa prompteja. Testatkaa heittämällä codebookin kontekstiin tai pilkkokaa erillisiin kyselyihin rajapinnasta claimi kerrallaan. Pikkuhiljaa rakennatte, että lähtee kyselyitä rajapintaan. 

Oisko tässä vaiheessa järkevää saada outputista rakenteistetumpaa, jos tulisi jsonia? Voi mennä paljon aikaa sprintistä outputin siistimseen.

Ryhmä: ei prio, jos ehditään tehdään

Heikki: 

Käyttikseen tulii 'valitse lausuntotiedostot, vaikka csv id:t tai 1-10, joku simppeli tapa spesiofioida, mitä lausuntoja chekataan. Sit valitse, mitkä politiikkaväitteet chekataan. Sit kaikki kirjoitetaan promptiin. EI iteroida väite kerrallaan. Minimi voisi olla: mitkä lausuntodokkarit, mitkä poliittiset väitteet, ajo jokaista dokkaria varten. 

Valitaan pieni subset codebookista, etsitään goldielocks zone. Valitaan claimien väärä ja mihin lähdedokkariin testataan. Ehkä vois olla oikea palanen seuraavaan sprinttiin.

Ja sitten stretch goals: joko se, että vois valita tehdätäänkö jokaista claimia varten joka ajo vai laitetanko samaan promptiin kaikki politiikkaväitteet.  Olisi parempi pitää kova focus niihin, että 'löytyykö tätä väitettää tästä lausunnosta, seuraava claimi, seuraava ajo'.

Kauri: ehkä ai:lle tämä helpompi/parempi

Heikki: 

jokaista politiikkaväitettä kohdi tehdään oma pääättely inferenssiajapinnasta, mutta prompti voi olla sama. Se mahdollistaa kiinnostavan tilastollisen päättelyn claimi kerraallaan ja voi laskea keskiarvon jokaiselle claimille.
    
Toi NO/YES pitää selittää mallille, koska se nyt hämäää mallia. 
Lähetetään claimi ilman NO/YES ja kysytään: löydätkö tätä väitettä dokumentista.


Voidaan itse päättää, onko promptit suomeksi vai englanniksi. Myöhemmin voidaan vertailla, kumpi parempi. 


## Seuraavan sprintin tehtävät (Heikin kommenttien pohjalta)

### 1. Promptin korjaus — NO/YES pois
- Nykyinen ongelma: promptissa esiintyvä NO/YES-merkintä hämää mallia.
- Muutos: lähetetään malliille pelkkä väite (esim. "climate law could weaken economic growth"), 
  ilman NO/YES-etuliitettä.
- Kysymyksenasettelu: "Löytyykö tätä väitettä tästä dokumentista?" (kyllä/ei tai asteikko)

### 2. Yksi väite, yksi inferenssikutsu
- Jokaista politiikkaväitettä kohden tehdään **oma erillinen kutsu** rajapintaan.
- Prompti-pohja voi pysyä samana joka kutsulla — vain väite ja dokumentti vaihtuvat.
- Tämä mahdollistaa tilastollisen käsittelyn myöhemmin: jokaiselle väitteelle voidaan
  laskea keskiarvo/luottamus useiden ajojen yli.
- EI lähetetä kaikkia väitteitä samassa promptissa (tätä harkittiin stretch goalina,
  mutta fokus pidetään yksinkertaisena aluksi).

### 3. Kovakoodatut promptit (toistaiseksi)
- Käyttäjän ei tarvitse itse syöttää tai muokata prompteja tässä vaiheessa.
- Kaksi vaihtoehtoa testattavaksi:
  a) koko codebook kontekstiin kerralla, TAI
  b) pilkotaan erillisiksi kyselyiksi, yksi claim kerrallaan
- Kokeilkaa kumpi toimii paremmin, ei tarvitse päättää lopullisesti vielä.

### 4. Minimi-käyttöliittymä (MVP tälle sprintille)
Käyttäjä pystyy valitsemaan:
- **Mitkä lausuntodokumentit** tarkistetaan (esim. CSV id:t tai yksinkertainen 1–10-valinta)
- **Mitkä politiikkaväitteet** tarkistetaan
- Ajo suoritetaan jokaista dokumenttia kohden valituilla väitteillä
- EI iteroida käyttöliittymässä väite kerrallaan — kaikki valinnat kerralla, sitten ajo

### 5. Goldilocks-subset ensimmäiseksi testiksi
- Valitaan **pieni osajoukko** codebookista (ei koko settiä)
- Valitaan muutama tunnettu "väärä"/haastava claim + lähdedokumentti, jota vasten testataan
- Tavoite: löytää sopivan kokoinen testitapaus, joka ei ole liian helppo eikä liian laaja
- Tämä voisi olla konkreettinen palanen tulevaan sprinttiin

### 6. Rakenteistettu output (matala prioriteetti, "jos ehditään")
- Tavoite: mallin output JSON-muodossa tilastojen laskemista varten
- Huomio: frontier-malleilla voi pyytää JSON-outputtia system-tasolla, mutta ei taattu
  kaikilla malleilla (osa palauttaa puhdasta JSONia, osa ei)
- Heikki: tähän voi mennä paljon aikaa siistimiseen — **ei prioriteetti tälle sprintille**,
  tehdään vain jos aikaa jää muun jälkeen

### 7. Kieli: suomi vs. englanti promptissa
- Ei tarvitse päättää nyt — voidaan kokeilla molempia
- Myöhemmässä sprintissä vertaillaan, kumpi antaa parempia tuloksia

### Stretch goal (ei tämän sprintin fokus)
- Valinta: ajetaanko jokaista claimia varten erillinen ajo, vai kaikki politiikkaväitteet
  samassa promptissa? → Heikki suosittelee pitämään fokuksen yksinkertaisena:
  "löytyykö tätä väitettä tästä lausunnosta, seuraava claimi, seuraava ajo"


