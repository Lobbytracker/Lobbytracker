# Asiakastapaaminen 4
Esiteltiin aluksi mitä ollaan saatu sprintin aikana valmiiksi. Saatiin yllättävän paljon tehtyä sprintin alussa, joten tekeminen tuntui vähän jopa loppuvan kesken. Sovellukseen on tehty viime tapaamisessa sovitut asiat ja tehty huomattava määrä refaktorointia, sekä kehitystiimille hyödyllisiä apuskriptejä.

## Tulevaisuuden näkymistä keskustelua

Asiakas oli ensinnäkin tyytyväinen tämän hetkiseen edistykseen.

Puhetta, että tulevaisuudessa voidaan testailla eri prompteilla. Kenties mallille voisi antaa enemmän kontekstia myös. Olisi kiinnostavaa nähdä mitä eroja tulosteeseen tulee kun ajetaan samat asiat eri prompteilla. Mutta tämä vasta myöhemmillä sprinteillä.

Web-käyttöliittymästä myös puhuttiin, kehitystiimi pitää sovelluksen sisäisen rakenteen joustavana ja valmiina mahdollisen web-käyttöliittymän kehittämiseen. Diff-tyyppinen vertailunäkymä olisi mielekäs, jos kehitystiimillä on aikaa viimeisillä sprinteillä. Nyt ei tehdä vielä mitään graafista käyttöliittymää, vaan mennään tekstikäyttöliittymällä.

Puhetta sovelluksen roolista oikeassa tuotantokäytössä. Tärkeintä nyt on saada dataa tästä projektista, että osaako mallit edes evaluoida dataa oikein.

Tulevaisuudessa voisi laskea kuinka hyvin kielimalli selviytyy konseptien löytämisestä vs. ihmiskoodari. Jotain testejä tästä voi jo miettiä, jos aikaa riittää.

Yksi tulevaisuuden keskeinen feature olisi isompi ajo. Tyyliä "Aja kaikki konseptit läpi kaikilla dokkareilla yön läpi", eli tarvetta on jonkinlaiselle batch processing-mallille. Tämä olisi mielekkäämpi feature myös testejä varten, koska sillä saa parempaa dataa. Ryhmä alkaa valmistautumaan tämän featuren kehitykseen alkavalla sprintillä.

Puhuttiin myös mahdollisesta tuesta eri Batch-rajapinnoille. Ei ehkä mene syksyn tavoitteisiin, mutta ryhmä voi myös tähän vähän perehtyä jos on aikaa. Mahdollisesti palataan tähän myös tulevilla sprinteillä. Oikeassa tuotannossa tulee kuitenkin olemaan jokin muu rajapinta, kuin AITTA.

Akademiassa ja muualla kovaa hypeä sovelluksesta ja ennenkaikkea asiakas on erittäin innoissaan! Kenties vuoden lopussa tehdään myös jotain kalliita ajoja Frontier-malleilla!

Sovittiin seuraava asiakastapaaminen 21.10.2026 klo 10.

## Pohdintaa seuraavasta sprintistä

F1 vertailusta ei asiakkaalla aiempaa kokemusta. Preferenssinä kuitenkin, että Golden Standard-kysely palauttaa listan vain jos jotain löytyy (yes). Mikäli mitään ei löydy (no), niin sitä ei tarvitse näyttää tai palauttaa, koska se tuskin vaikuttaa tunnuslukujen laskemiseen. Asiakas perehtyy mitä halutaan vertailla jatkoa varten. F1 laskee keskiarvon, kuinka hyvin kaksi tulostetta vastaa toisiaan. Ryhmä voi myös miettiä etukäteen ehdotuksia näistä.

Puhetta myös mallien lomittaisista ajoista ja toiminnoista. Ryhmä pohtii tätä sprintin aikana ja myös jos käyttäisi isompia valmiita kirjastoja virheenhallintaa ja automaatiota varten (retry yms.). Olisi hyvä selvittää saatavilla olevat vaihtoehdot, ennenkuin ryhmä alkaa rakentamaan omia. Vaihtoehtona kenties LightLLM?

Prioriteettinä nyt on saada tuki useampaa ajoa varten. Toiveena myös jos saisi prompteista eri versioita ja testattua niiden ajoja. Tyyliä: "Ensi yön aikana aja promptit 1.1 ja 1.2, ja laske tästä [jotain]", minkä avulla voidaan selvittää esimerkiksi paras prompti tälle kyseiselle tekoälymallille.

Laitetaan työn alle ekstraktointi-komento, joka paluttaa JSONin Golden Standardista, jolla voi laskea ja vertailla.

Sovellukseen olisi myös hyvä saada loki, jota voi tarkistella ajojen jälkeen ja käyttöliittymästä ajojen aikana.

## Seuraavan sprintin tehtävät
- Golden standard tietokantaan ja sovelluksen käyttöön.
- Loki sovellukseen ja käyttäjän näkyville.
- Virheenhallinnan tutkimista batch processing featurea varten.
- Batch processing featuren aloittaminen.
- Vertailua (F1 testejä) voi myös vähän miettiä ja perehtyä asiaan. Asiakas laittaa viestiä ensi viikolla, että millaisia haluaisi.