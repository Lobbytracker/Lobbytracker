# Aloitustapaaminen

## Pääpiirteitä
- Mistä kyse: liittyy valtsikan politiikantutkijan proffiin. Politiikkaverkostoja. Miten eri lobbaritoimija tpystyy vaikuttamaan politiikkaan. Verkostograafeja miten saadaan ääni kuuluviin. Tehdään avoin palvelu, jossa mahdolisimman avoin palvelu

- miten tietyt lobbarit on saaneet oman kantansa läpi lakivedokseen
- kielimalleja politiikkajuttujen havainnointiin
- MEIDÄN TEHTÄVÄ arvioida miten erilaiset mallit selviävät eri politiikkamallien tekstiarvioinnissa. Eli pitää selvittää mikä on poliitikon kanta/näkemys aiheessa. Ei ole stabiilia rajapintaa
- Voimme osoittaa minkä arvion mikäkin malli teki
- Tarvitaan jokin politikka kartoitus aiheesta ja kokeillaan siihen eri malleja, miten ne päsevät yhtä lähelle ihmisen arviota. Eli meidän tehtävä arvioida miten lähelle ne pääsee
- Kysyntää on tosi paljon
- Kielimallien kyvyn kriittinen arviointi
- Kyvyt täysin meidän hyppysissä
- Kukaan ei vielä ole suomessa tehnyt samanlaista
- Turun ihmisillä ideoita (päivitetään lappuseen)
- Palautetta on turussa
- Nettisivu? JOka tapauksessa joskus tarvitaan
- Syötetään corpus ja gaol standard ja ohjelma luo raportin mallin ajoista
- Bare bones nettisivu ei olennaisin
- csv raportti jonka muuntaa ajoiksi
- corpus valmiina, polintologeilla on ilmastopolitiikka aineisto johon on analysoitu aiheita. Aineistoa ei vielä ole saatu.
- nettisivu eli kämänen web käyttöliittymä
- pääasia, että codebook data on hyvää
- Käyttöliittymä ei ole olennainen, ei tarvitse käyttää aikaa siihen
- Ajojen promptit
- Voidaan käyttää mitä vain backendiä
- jotain dataa edes ja nähdään että menee päästä päähän
- csc rajapinta käyttöoikeudet ja sieltä muutama malli
- AllLLM
- Google gemma
- tokeneita tulee pari sekunnissa
- Codebookista tehdään pieni siivu, jolla testataan mekaanisesti voiko ohjelma tekemään vertailut
- LiteLLM
- Miten hyvin evaluoi mun prompteilla dataa mikä on politiikan näkökulmasta mielenkiintoinen juttu
- KÄyttöliittymä, jossa voisi tehdä koodausta (BOONUS) (ei välttis niin tärkeä)
- DNA (discourse network analysis) jutulla tehty data
- Aja sama asia monesti ja arvioi
- Luokittelumalli eli kuinka varma se on tuloksesta. Jos ei ole varma millaista lobbausta on niin nostaisi ihmisen arviointiin mahdolliset epävarmuudet.
- Confidence luokittelu
- Inferenssihinnat nousee koko ajan ja niitä pidetään hallussa batch API:eilla. Mahdollinen lisädevilerable. Samoin autentikaatio
- Teknologioilla ei vaatimuksia
- Pythonia asiakas osaisi kanssa lukea
- ollama
- Ensimmäisen kahden viikon aikana: Lähdetään liikkeelle siitä, että corpuksen uploadaus ja prosessointi. Joku katselunäkymä siihen. Tietokantarakenne sen jälkeen. Tietokannassa corpus ja miten se rakenteistetaan. Data eritelty paremmin alkuperäisessä
- Jos iso corpus niin se pitää palastella. Miten palastellaan?
- Rajapintaan lähetään palanen ja pyydetään mikä policyclaim kyseisessä palasessa on. Palasten täytyy olla lomittaisia jos ne on liian pieniä. Vertailu alustalle muutama valinta kuinka suuriksi palasiksi data jaetaan.
- Jos konteksti liian iso niin arvio saattaa olla ihan metsään
- Input ei saa olla liian iso eikä liian pieni vaan juuri sopiva :D (kultakutrivyöhyke)


- MVP kuvio: corpus, tutkijan löytämät evaluaatiot ja codebook minkä avulla näkee tutkijan politiikkaväitteet tarkemmin eli miten ne on havainnoitu, jotka uploadataan kielimallirajapintaan. Corpuksesta läheteään pala sekä codebook kielimallille joka antaa tuloksia. NÄmä pisteytetään ja annetaan arviot gold standardiin (eli ihmisen arvioon).

- rajapintojen taustatyötä
- OpenAI:lla rajoituksia (suurin osa palveluntarjoajista käyttää samaa formaattia)
- Pisteytyksen tietokantamalli, uploadaus vaihe eli miten data menee kantaan corpuksena, codebookkina ja gold standardina, sekä mitä datalle pitää tehdä kun se käy kielimallin rajapinnan kautta.
- Heikkiin tarvittaessa yhteydessä
- Jos lähdetään tekemään niin saadaan haluttu prototyyppi, jolla saadaan lähetettyä data kielimallille jonka tulos saadaan pisteytettyä
- Codebook = Arvioi näiden ohjeiden mukaisesti
- Pseudoaineisto tarvittaessa
- Datamallit oikeat
- Projektin nimi
- Lobbytracker aiheen nimi
- Lopputulos julkinen

- Datan parsiminen
- Arviointi
- Raportin koostaminen

heikki.wilenius@iki.fi

## Esille tulleita user storyja
- Datan parsiminen
- Kielimalli analysoi dataa
- Kielimallin analyysin arviointi gold standardiin verrattuna
- Staging palvelin pystyyn
- Codebookin rekonstruktointi
- Ajon testaus annetuilla prompteilla
- Testaus jollakin keilimalli rajapinnalla
- MVP käyttöliittymä
- Comparison dashboard
- Ohjelman ajaminen monesti (lopullisessa versiossa)
- Confidence luokittelu eli kuinka varma LLM on tuloksesta
- Miten dokumentti jaetaan pienempiin osiin, jotka laitetaan kielimallille analysoitavaksi.

## Teknkologiat:
- python
- PostgreSQL
- React

## Definition of Done
- Pienin mahdollinen, joka toimii
- Testattavissa ja toimiva

