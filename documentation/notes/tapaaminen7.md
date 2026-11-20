# Asiakastapamainen 7
Esiteltiin aluksi mitä ollaan saatu sprintin aikana valmiiksi. Kehitystä F1-laskentaan, batch-prosessointiin, dokumentaatioon ja muuta pientä.

Asiakas oli jälleen kovin tyytyväinen.

## Keskustelua projektin tulevaisuudesta ja tulevasta sprintistä

Asiakas toivoo, että lisättäisiin sovellukseen lisää virheenhallintaa, erityisesti ajoihin. Toivelistalla kärjessä oli myös eri ajojen tarkastelu, vertailu ja oman promptin lisäys. Mielekästä olisi esimerkiksi selvittää, toimiiko jotkut mallit paremmin toisenlaisilla prompteilla. Pöydättiin keskustelu siitä, huomioidaanko agreement vielä laskuissa tai muualla, asiakas selvittää ja palaa asiaan.

Mikäli aikaa ja intoa riittää, niin "tilastomatikan" lisääminen ajojen vertailuun olisi yleisesti hyvä. Etenkin luottamusvälit ja confusion matrix konsepteille.

Tuotantokäytössä olisi hyvä, jos sovelluksen käyttäjä voisi ladata omat datansa sovelluksen käyttöön. On kuitenkin huomattu, että nykyinen golden standard, ei ole tarpeeksi hyvä tuotantokäyttöön. Joten ryhmä ei nyt tuota toiminnallisuutta, jolla tämä tulevaisuuden unelma toteutuisi. Se jätetään projektin tuleville kehittäjille tehtäväksi.

Keskusteltiin myös sovelluksen kielestä. Päätettiin pitää sovelluksen kieli suomena. Käytiin läpi myös vähän ryhmän tuottamia käyttöohjeita. Sinne voi halutessaan lisätä Linux-ohjeiden lisäksi ohjeistusta Windowsille ja Macille, jos aikaa riittää (ei varmaan riitä). Logon toteutuksesta vaihdettiin myös muutama sana. Siiterakseni asiakasta "Go crazy! But not too crazy." 

Loppu lähestyy, joten pohdimme myös miten merkitsemme projektin tekijät projektiin, jotta Asiakas voi esimerkiksi viitata projektiin tai ryhmään. Asiakkaalta täten ehdoton vaatimus, että ryhmä selvittää miten ryhmää siteerataan. Myös loppudokumentaatio olisi hyvä saada aluille. Sinne kirjataan ylös kaikki featuret mitä ryhmä ei ehdi tekemään. Esimerkiksi confusion matrix, muut tilastomatikka-asiat, käli, yms. Ryhmä antaa lopuksi vielä asiakkaalle tarkistettavaksi kyseisen dokumentin.

## Seuraavan sprintin tehtävät
- Viittauskäytänteiden selvittäminen (miten projektiin ja sen tekijöihin viitataan tulevaisuudessa)
- F1-laskennan voi suorittaa valitulle ajolle (eikä vain viimeisimmälle)
- Käyttäjä voi vertailla eri ajojen tuloksia keskenään
- Epäonnistuneiden API-kutsujen käsittelyä ja muuta lisäystä virheenhallintaan
- Käyttäjä voi lisätä sovellukseen uuden promptin
- Loppudokumentaation aloittaminen
- Logo
