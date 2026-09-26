start:
	docker compose up -d --build

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
