# Asiakastapaaminen 2

Aloitettiin tapaaminen demolla. Esiteltiin tähän mennessä luodut tietokantataulukot, jotka pyörivät tällä hetkellä Dockerissa sekä terminaalissa oleva käyttöliittymä. 
## Demoon liittyen kommentteja:
- Otettiin Aitasta OpenAI käyttöön, ja siihen liittyen ollaan kovakoodattu prompti. Mikä backend meillä on Aittan kautta? Aittassa on status sivu, josta näkee onks ne mallit pystyssä vai ei, eikä Aitassa ole mitään palvelupalstaa koska ne on pystyssä ja koska ei. Aittassa ei oo mitään lupauksia miten mallit toimii, voi vaihtaa aina mallii ku alussa ei oo mitää väliä. Eli jos Aitta ei vastaa niin kannattaa käydä tarkistaa sieltä sivulta onko kyseinen malli edes pystyssä sillä hetkellä. 
- Alunperin kovakoodataan promptit toistaseks, ettei käyttäjän tarvitse itse antaa prompteja.
- Turku nlp ideoita: palataan niihin loppusyksyllä jos on aikaa. 
- Mahtavaa, että saimme jo infrastruktuurin pystyyn.

## Tavoite:
Mihin me yritetään on se, että me voidaan ajaa joko terminaalissa tai nettisivulla. Jos saa rahoituksen, niin komentorivi on agenteille tehokkain niin suurinpiirtein samat featuret tai ainakin perus featuret myös komentorivin kautta.

## Seuraavaks:
- Datan saaminen tietokantaan, yks kerrallaan. Alkuun raakadata ja myöhemmin voidaan hyödyntää codebookin kautta. 
- Codebook tietokantaan
- Datassa oleva ongelma: osa tiedostoista on tosi kämäsellä ocr:llä vedetty ja Heikki yritti sitä vähän fiksailla, mutta se ei edelleenkään ole kauheen hyvä ja saattaa hämää jotain malleja, erityisesti niitä jotka eivät ole parhaita suomessa, mutta nyt on kyselyt käynnissä jos saatais pdf et ois paremmat ocr. Toistaseks menee, mut jos halutaan konkreettiset tulokset niin eivät ole parhaita. 
- Jos ehtii niin tekis funktion, jolla vertaa aitassa jo yhtä tiedostoo siihen codebookiin ja niiku ettii ne conceptit.  
- Staging ympäristön pystyttäminen

## Kyssäreitä:
- Datassa on concepteilla omat id, onks sillä väliä? Jotain tippunu välistä, tutkija lukenu ja sit tehny alustavan koodauksen ja huomannu et joku id 20 on esim vaa yhes niin ottanu pois. Tullaan tuomaan lisää samantyyppisiä listoja. Jos tuonti tiedostosta tulee joku id ja skeemassa oma id, ei vissiin ihan hirveesti relevanttia. Tuodaanko noi tietokantaan? Toi ei menis mut luodaan oma id. Jos tulevaisuudessa tuodaan useesta eri lähteestä, mut nyt dumpataan pois toi concept_id
- Miten on järkevin tallentaa eri dokumentit? Ja mitkä kentät tarvitaan esim documentsissä:
1. Kuvittelee monimutkaisemman codebookin, kuka sen on laatinut? Eli tekijä kenttä
2. Tiedostoissa itsessään ei ole title, joten title kenttä on huono
3. Skeemassa title ja author ois hyvä olla
- Nyt koko syksy Aittan kautta, protoilua ja sit jos ne saa rahaa nii ne voi yleistää sen, mutta for now näin

Ehdotus seuraavasta tapaamisesta: 10.00 A319, tasan kahden viikon päästä.