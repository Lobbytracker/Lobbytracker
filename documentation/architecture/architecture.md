# Architecture

This document describes the application structure, main technologies, and database.

## Project structure

| File or directory | Responsibility |
| --- | --- |
| `src/index.py` | Entry point: creates the interface and data managers, constructs `App`, and starts its main loop. |
| `src/app.py` | Dispatches menu commands, holds the selected model, and handles returns to the menu and interrupted operations. |
| `src/tui/` | User input and output rendered with Rich. |
| `src/documents/`, `src/concepts/`, `src/goldenstandards/` | Work with documents, concepts, and reference annotations loaded from the database. |
| `src/ai/ai.py` | Aitta connection, model catalogue, prompts, response schema, and result collection. |
| `src/ai/batch.py` | Processes a limited set of document-concept pairs through sequential requests. |
| `src/db/initialize_db.py` | Defines and runs database initialization when executed as a script. |
| `src/db/db_calls.py` | Database reads and model result persistence using asyncpg. |
| `src/evaluations/` | Encodes document-concept pairs and calculates scikit-learn metrics. |
| `src/error_handling.py` | Defines the exception used to return from selection prompts to the main menu. |
| `src/main.py` | FastAPI backend with example routes; analysis is currently accessed through the terminal. |
| `src/tests/` | Automated tests. |

## Technologies

| Technology | Role |
| --- | --- |
| Python | Application language. Requires Python 3.12 or newer. |
| Rich | Terminal interface and formatted output. |
| PostgreSQL and asyncpg | Data storage and database access. |
| Aitta and OpenAI Python SDK | Language model service and API client. |
| Pydantic | Structured model response schema and validation. |
| pandas | Reading CSV datasets during import. |
| scikit-learn | Evaluation metrics. |
| FastAPI | Web backend skeleton. |
| Docker Compose | Runs the database and web backend locally. |
| uv | Python dependency management and command execution. |
| pytest and coverage | Automated testing and coverage reporting. |
| Pylint and Ruff | Code checks and formatting. |

Dependency requirements are listed in `pyproject.toml` and locked versions in `uv.lock`.

## Database

Tables are defined in `src/db/initialize_db.py`.

Docker Compose initializes the tables after the database is healthy.

| Table | Main fields |
| --- | --- |
| `concepts` | `id` (primary key), `stance_label`, `concept`. |
| `files` | `id` (primary key), `document_id` (source dataset ID), `filename`, `author`, `content`. |
| `goldenstandard` | `id`, `document_id` (references `files.id`), `concept_id` (references `concepts.id`), `passage`, `agreement`. |
| `llmoutput` | `id`, `document_id` (references `files.id`), `concept_id` (references `concepts.id`), `present` (boolean), `passage`, `agreement` (boolean or null). |

Initialization creates missing tables but does not migrate existing table structures.
