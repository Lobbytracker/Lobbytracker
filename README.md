# Lobbytracker

## Description
Lobbytracker is a tool for analyzing legal and policy documents with LLMs. The goal of this project is to find out how well LLMs can analyze Finnish language policy documents and find stances in them. This tool is made mainly for political and social scientists to streamline their research. Reliable stance data can then be aggregated into networks of organisations' policy positions.

Other similar tools have been developed for other languages (for e.g. German & English), but this is the first one in Finnish. The project is developed as a university course project for a researcher at the University of Helsinki.


## Features
- **Choosing a Model:** pick an LLM from a list of available models
- **Document selection:** analyse one or several documents
- **Concept-based coding:** the LLM receives a list of concepts (the stances a human
  coder looks for) and decides for each one whether the document mentions it
- **Stance detection:** for each concept found, the output states whether the document supports or opposes it
- **Output inspection:** view the LLM's output for each document and concept
- **Batch processing:** run all document-concept pairs in one go
- **Evaluation:** compute F1 scores for concept and stance detection against the
  human researchers' labels

## Installation

First navigate to the command line interface.

**1.** Clone the project
```
$ git clone git@github.com:Lobbytracker/Lobbytracker.git
```

**2.** Configure the local .env file
```
cp .env.example .env
```
Then edit `.env`:

| Variable | Description |
|---|---|
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Database name and credentials |
| `AITTA_API_KEY` | API key for the LLM service |

**3.** Install ```make``` utility
```
sudo apt install make
``` 

 **4.** Upload your data
 **TO DO**

**5.** Start the application

* Start the Docker container
```
make start
```
* Start the application
```
make app
```

## Documentation

- [Architecture](documentation/architecture.md): project structure, technologies, and database.
- [User guide](documentation/user_guide.md): terminology, starting the application, menu commands, and interpreting results.

## Links
[Backlog.](https://github.com/orgs/Lobbytracker/projects/1)


## Definition of Done

* Acceptance criteria have been defined for user stories and are documented in the description of each user story.
* User stories and their acceptance criteria can be found in the product backlog.
* The test coverage of the implemented code must be reasonable.
* The customer can view the status of the code and tests at all times via the CI service.
* The code is as maintainable as possible: naming conventions and architecture are sensible,
* A consistent coding style is followed (enforced using Pylint).
