# Todo lista projektille

- App alustaa dokumentit ja konseptit.
  - App alustaa Manager luokat ja hoitaa injektiot.
- Tui hoitaa vain printtauksen.
  - Kaikki toiminnallisuus muihin luokkiin.
- db-tiedoston jakaminen pienempiin tiedostoihin. Tietokannan alustus omanaan (schema.sql/oma ajettava skripti "init_db.py", joka ajetaan skeeman muutoksen jälkeen.)
  - db schema muuttuu --> docker vois hoitaa kontin käynnistyessä init_db:n voluumin poiston jälkeen
- Ai tiedoston yhdenmukaistaminen
- Argumentin kanta (Yes/No) kielimallille. Eli puoltaako dokumentin lause annettua konseptia.
- Agreement arvo kielimallin tulosteeseen.
- Golden standardin agreement tietokantaan. (Ei saa antaa kielimallille --> annetaan valitut sarakkeet)
