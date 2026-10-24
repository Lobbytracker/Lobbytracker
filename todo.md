# Todo lista projektille

- App alustaa managerit ohjelman käynnistyessä.
  - App alustaa Manager luokat ja hoitaa injektiot.
    - :white_check_mark: Lausunnot ja käsitteet DONE
    - :x: Golden standards tekemättä!
  - :white_check_mark: Turhat kommentit pois.
  - :white_check_mark: Instructionsit kanssa Tui:lle
- :white_check_mark: Tui hoitaa vain IO:n (printtaus, käyttäjän syötteet) ja formatoinnin
  - :white_check_mark: Kaikki toiminnallisuus muihin luokkiin.
- db-tiedoston jakaminen pienempiin tiedostoihin. Tietokannan alustus omanaan (schema.sql/oma ajettava skripti "init_db.py", joka ajetaan skeeman muutoksen jälkeen.)
  - db schema muuttuu --> docker vois hoitaa kontin käynnistyessä init_db:n voluumin poiston jälkeen
- Ai tiedoston yhdenmukaistaminen
- Argumentin kanta (Yes/No) kielimallille. Eli puoltaako dokumentin lause annettua konseptia.
- Agreement arvo kielimallin tulosteeseen.
- Golden standardin agreement tietokantaan. (Ei saa antaa kielimallille --> annetaan valitut sarakkeet)
