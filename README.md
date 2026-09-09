# Lobbytracker
This is the repository for Lobbytracker, a public platform that will aggregate and analyse Finnish lobbying data. It's goal is to be an web application that lets a researcher answer the question *"which model and which prompting strategy should I use for this coding task?"* without writing code.

## Installing the application

### Clone the project on your own computer

```
$ git clone git@github.com:Lobbytracker/Lobbytracker.git
```

### Update the project's environment:
```
uv sync
```

### Create local environment file
```
cp .env.example .env
```
Fill required fields with your own credentials.

### Start the application with Docker Compose
```
docker compose up -d --build
```
The application is available at: http://localhost:8000

### Checking running containers
```
docker compose ps
```

### How to see current postgres tables
```
docker compose exec db \
  psql -U postgres -d lobbytracker -c '\dt'
```

### Stopping the application
```
docker compose down
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
