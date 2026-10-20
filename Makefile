.PHONY: start app stop status db tables logs

start:
	docker compose up -d --build

data:
	uv run python scripts/import_concepts.py
	uv run python scripts/import_documents.py
	uv run python scripts/import_goldenstandard.py

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

tests:
	uv run pytest src

coverage:
	uv run coverage run -m pytest src
	uv run coverage report

pylint:
	uv run pylint src
