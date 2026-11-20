.PHONY: start app stop status db tables logs init-db reset-db

init-db:
	PYTHONPATH=src uv run src/db/initialize_db.py

reset-db:
	docker compose exec db psql -U postgres -d lobbytracker -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;'
	PYTHONPATH=src uv run src/db/initialize_db.py
	uv run python scripts/import_documents.py
	uv run python scripts/import_concepts.py
	uv run python scripts/import_goldenstandard.py

start:
	docker compose up -d --build

data:
	uv run python scripts/import_documents.py
	uv run python scripts/import_concepts.py
	uv run python scripts/import_goldenstandard.py

app:
	uv run src/index.py

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

autofix:
	uv run ruff check --fix .
	uv run ruff format .