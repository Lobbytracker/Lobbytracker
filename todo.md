# Todo lista projektille

## To be done

- Tietokannan alustus omanaan (schema.sql/oma ajettava skripti "init_db.py", joka ajetaan skeeman muutoksen jälkeen.)
  - db schema muuttuu --> docker vois hoitaa kontin käynnistyessä init_db:n voluumin poiston jälkeen
- Ai tiedoston yhdenmukaistaminen
- BUG: Alarajan poistaminen rikkoo sovelluksen komennon 2 (Esim. alarajan poistaminen ai.py-tiedostosta)
- Pylint virheiden korjaaminen
- Testipipeline GitHubiin
- Nimeämisen yhteinäistäminen ja järkevöittäminen
- Kaikki app-tiedostossa tapahtuva printtaaminen tuihin.

## Done

- :white_check_mark: App alustaa managerit ohjelman käynnistyessä.
  - :white_check_mark: App alustaa Manager luokat ja hoitaa injektiot.
    - :white_check_mark: Lausunnot, käsitteet ja golden standards DONE
  - :white_check_mark: Turhat kommentit pois.
  - :white_check_mark: Instructionsit kanssa Tui:lle
- :white_check_mark: Tui hoitaa vain IO:n (printtaus, käyttäjän syötteet) ja formatoinnin
- :white_check_mark: Kaikki toiminnallisuus muihin luokkiin.
- :white_check_mark: Argumentin kanta (Yes/No) kielimallille. Eli puoltaako dokumentin lause annettua konseptia.
- :white_check_mark: Agreement arvo kielimallin tulosteeseen.
- :white_check_mark: Golden standardin agreement tietokantaan. (Ei saa antaa kielimallille --> annetaan valitut sarakkeet)
- :white_check_mark: db-tiedoston jakaminen pienempiin tiedostoihin.
