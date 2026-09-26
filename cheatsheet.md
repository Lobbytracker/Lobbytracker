# Cheat sheet

## Local development

### Start the application

```bash
make start
```

Application:

http://localhost:8000

FastAPI documentation:

http://localhost:8000/docs

### run src/app.py (MVP)

```bash
make app
```

### Check running containers

```bash
make status
```

### View backend logs

```bash
make logs
```

### Stop the application

```bash
make stop
```

---

## PostgreSQL

### Access the database

```bash
make db
```

Inside PostgreSQL:


Show all tables.

```sql
\dt
```


Show the first 10 concepts.

```sql
SELECT * FROM concepts LIMIT 10;
```


Show the first 10 files.

```sql
SELECT * FROM files LIMIT 10;
```

Show the row where `id` is 3.

```sql
SELECT * FROM files WHERE id = 3;
```

Exit PostgreSQL:

```sql
\q
```

### If database tables are missing

First restart/rebuild the application:

```bash
make stop
make start
```

Then check the tables:

```bash
make tables
```

If the tables are still missing, check the backend logs:

```bash
make logs
```

---

## Development workflow

```text
make start
    ↓
open http://localhost:8000/docs
    ↓
write/change Python code
    ↓
test through /docs
    ↓
check PostgreSQL if necessary
    ↓
git add .
    ↓
git commit -m "describe your changes"
    ↓
git push
```

---

## OKD-klusteri

### Kooste tärkeimmistä komennoista

| Komento                         | Kuvaus                                                                                |
| :------------------------------ | :------------------------------------------------------------------------------------ |
| `oc get po`                     | listaa podit                                                                          |
| `oc get svc`                    | listaa servicet                                                                       |
| `oc describe po <pod>`          | katso podin tarkemmat tiedot, toimii myös muille resursseille, esim. svc, deployments |
| `oc exec -it <pod> -- bash`        | suorita podilla komento bash eli komentotulkki                                        |
| `oc apply -f manifest.yaml`     | luo/päivitä manifestin määrittelemät objektit                                         |
| `oc delete -f manifest.yaml`    | tuhoa manifestin määrittelemät objektit                                               |
| `oc import-image image:tagi`    | päivitä imagestream heti                                                              |
| `oc logs <pod>`                 | näytä sovelluksen lokit                                                               |
| `oc logs -f <pod>`              | seuraa sovelluksen lokeja                                                             |
| `oc port-forward <pod>`         | ohjaa lokaalin koneen portin liikenne podiin                                          |
| `oc port-forward svc/<service>` | ohjaa lokaalin koneen portin liikenne palveluun                                       |

### Staging
https://lobbytracker-ohtuprojekti-staging.ext.okd-cs-test-0.k8s.cs.helsinki.fi/

Kirjautuminen oc:
`oc login` 
palauttaa linkin, jonka kautta voi kirjautua HY -tunnuksilla. Sieltä kopioi 'Display token' takaata paljastuvat komennon terminaaliin. 