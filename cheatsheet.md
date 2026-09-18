# Cheat sheet

## CHECK DATABASE 

docker exec -it lobbytracker-postgres psql -U postgres -d lobbytracker

Inside PostgreSQL: 
 show tables
\dt SELECT * FROM concepts LIMIT 10;  

Exit: 

\q  

### DATABASE TABLES MISSING? 

uv run python app/db.py  

Then: 

docker exec -it lobbytracker-postgres psql -U postgres -d lobbytracker 


## Workflow

START  
↓ 
docker start lobbytracker-postgres  
↓
uv run fastapi dev app/main.py  
↓ 
write/change Python code  
↓
test through /docs  
↓ 
check database if necessary  
↓ 
git add, commit, push

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

https://lobbytracker-ohtuprojekti-staging.ext.okd-cs-test-0.k8s.cs.helsinki.fi/
