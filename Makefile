.PHONY: start app stop status db tables logs

start:
	docker compose up -d --build

app:
	uv run src/app.py

stop:
	docker compose down

status:
	docker compose ps

db:
	docker compose exec db psql -U postgres -d lobbytracker

tables:
	docker compose exec db psql -U postgres -d lobbytracker -c '\dt'

logs:
	docker compose logs backend
