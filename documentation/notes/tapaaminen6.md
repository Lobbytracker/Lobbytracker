# Asiakastapaaminen 6

Tapaamisen alussa demotaan asiakkaalle mitä ollaan saatu sprintin aikana valmiiksi:

- Tehty F1 laskennan MVP feikkidatalla
- Enkoodaus filu golden standardin ja kielimallin tulosteelle
- Refaktorointia
- Testejä
- Paluu komento terminaalin valikkoihin

## Asiakkaan toiveet ja kysymyksiä asiakkaalle

### Batch processing

Asiakas kysyy, tuleeko eräajosta tulostetta konsolille tai käyttäjälle? Ei tällä hetkellä, ollaan mietitty. Lokitus on hyvä ja tärkeä ominaisuus; nähdään miksi feilas.

### F1-laskenta

Nykyinen laskenta tarkastelee binäärisesti, esiintyykö käsite dokumentissa. Se ei huomioi käsitteen esiintymiskertojen määrää eikä tuota erillisiä käsitekohtaisia tuloksia. Miten halutaan? Mikro ja makro eri tavalla? Lasketaanko dokumentti kohtaisesti vai konsepti kohtaisesti?

Asiakas toivoo, että lasketaan eri komboille. Jokaiselle käsitteelle lasketaan erikseen precision- ja recall-arvot. Näin voidaan vertailla, mitkä käsitteet kielimalli tunnistaa hyvin ja minkä kohdalla se tekee enemmän virheitä. Lisäksi tarvitaan koko ajon tuloksia kuvaavat mittarit. 

Asiakas katselee Angstin duuneja ja kaivelee muiden implementaatioita siitä, miten F1 kannattaa laskea eri komboista. Ehkä tehdään samaan dokumenttiin 10 eri ajoa, ajokohtainen F1, lasketaan lopuksi niiden keskiarvo. Tai koko ajo, kaikki käsiteparit: Tehdään ajo jokaiselle käsitteelle -> jokaiselle f1 erikseen, otetaan siitä tavallinen keskiarvo --> tämä joukon f1

1 konsepti, 1 dokumentti, 1 ajo: siitä mikro ja makro f1 ei ole mitään eroa. Yhden setin f1 on koko setin f1. lisätäään 2 käsitettä, 2 dokumenttia, 1 ajo, ajo per käsite, saadaan 2 eri precision ja recall lukua molemmille käsitteelle. makro-F1 saadaan käsitekohtaisten F1-arvojen keskiarvona.

## Seuraavan sprintin tehtävät

- F1 laskenta oikeilla syötteillä (vaatii muutoksia nykyiseen dataan)
- Batch processing valmiiksi
- Tekemättä jääneet taskit valmiiksi

## Tietokannan skeema

- evaluationRuns: Tähän hätään ei lisättävää.

Myöhemmin virheenkäsittelyä sovellukseen, että pystytään jatkamaan samasta kohdasta.

Seuraava tapaaminen 18.11. klo 9.