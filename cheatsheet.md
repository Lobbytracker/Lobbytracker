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