# Lobbytracker
Lobbytracker is a prototype for analysing legal documents with AI. It lets a user select documents and predefined concepts, asks an AI model whether each concept appears in the document, and returns the answer together with an exact supporting passage.

## Installing the application

### Clone the project
```
$ git clone git@github.com:Lobbytracker/Lobbytracker.git
```

### Update the project's environment
```
uv sync
```

### Create local environment file
```
cp .env.example .env
```

*Fill required fields with your own credentials.*

### Install `make` utility
```
sudo apt install make
```

### Start docker
```
make start
```

### Run data import scripts

```
uv run python scripts/import_concepts.py
uv run python scripts/import_documents.py
uv run python scripts/import_goldenstandard.py
```

### Run the application locally

```
uv run python src/app.py
```

Web-version is available at [http://localhost:8000](http://localhost:8000)

## Docker commands

### Check running containers
```
make status
```
### View backend logs
```
make logs
```
### Stop the application
```
make stop
```

## Database commands

### Access PostgreSQL

Open an interactive PostgreSQL session:
```
make db
```

### Show the tables
```
\dt
```

### Show the first 10 concepts
```
SELECT * FROM concepts LIMIT 10;
```

### Show PostgreSQL tables directly
```
make tables
```

### Exit PostgreSQL
```
\q
```

## Backlog

Product backlog and sprint backlog can be found [here.](https://github.com/orgs/Lobbytracker/projects/1)

## Data

Data can be found [here.](https://github.com/Lobbytracker/ilmastolaki_lausunnot)

## Definition of Done

* Acceptance criteria have been defined for user stories and are documented in the description of each user story.
* User stories and their acceptance criteria can be found in the product backlog.
* The test coverage of the implemented code must be reasonable.
* The customer can view the status of the code and tests at all times via the CI service.
* The code is as maintainable as possible: naming conventions and architecture are sensible,
* A consistent coding style is followed (enforced using Pylint).
