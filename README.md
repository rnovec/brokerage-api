# Brokerage API

API REST services for Brokerage firm to process a set of buy/sell orders.

## Features

- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework, high performance, easy to learn, fast to code, ready for production.
- [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL Toolkit and Object Relational Mapper with SQLite3 implementation.
- [Pytest](https://docs.pytest.org/en/7.1.x/) - The **pytest** framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.
- [Mangum](https://mangum.io/) - Mangum is an adapter for running ASGI applications in AWS Lambda to handle Function URL, API Gateway, ALB, and Lambda@Edge events.
- [Pyscopg2](https://www.psycopg.org/) - Python interface to PostgreSQL database server.

## Requirements

- Python 3.8+
- Postgres 12.0
- Docker
- Docker Compose

#### Environment variables

- `DATABASE_URL` - database uri (postgresql+pyscopg2://user:password@host:port/database)
- `OPENAPI_URL` - relative path to openapi.json, default is `/openapi.json`
- `OPEN_MARKET_AT` - open market time, default is `06:00`
- `CLOSE_MARKET_AT` - close market time, default is `15:00`

### Disclaimer

There is currently a lot of flexibility with the installation.

Many of the developers use docker compose with visual studio code to test the functionality of the backend in a way that is similar to our deployed environments.
Details regarding docker setup are listed later in this document.

You will need to install Postgres and this can be done with docker, a direct system install, or any other typical Postgres install.

These instructions will try to cover setup for both Windows and Linux/Mac.

### Install package requirements

For the next 2 commands, replace `python` with the full path to your Python 3.8+ installation.

- Install virtualenv

```bash
python -m pip install --user virtualenv
```

- Create environment

```bash
python -m virtualenv venv # or python -m venv venv
```

- Activate your virtual environment

#### Windows

```bash
venv/Scripts/activate.ps1
```

#### Mac/Linux

```bash
source venv/bin/activate
```

You should now be in the virtual environment and see the `(venv)` tag as part of your prompt. If you are not using Python 3.7, the next command will fail.

- Install package requirements

```bash
pip install -r etc/pip/requirements-dev.txt
```

*Please keep in mind that for any local system commands that you run regarding this project and Python, you need to be in the virtual environment. Always re-enter the virtual environment before trying to do anything.*

## Run locally

Start dev server on your local machine:

```bash
uvicorn app.main:app --reload 
```

Then open your browser to <http://localhost:8000/docs>

# Run Formatting

We are using the `black` <https://pypi.org/project/black/> and `isort` auto-formatting tools.

Usage: `black dir_name` and/or `isort dir_name` to format the code.

```
isort app && black app
```

# Docker Setup

Docker allows for development within an environment that is similar to our dev and production environments in ECS.

## Install Docker

To install docker, Docker desktop is recommended for Windows and Mac. <https://www.docker.com/products/docker-desktop>

### Run Docker Compose

Navigate to the location of the docker-compose.yml file and run the following command.

```bash
docker-compose up
```

#### Open Swagger docs

- [http://localhost:8000/docs](http://localhost:8000/docs)

#### Run tests

```bash
docker-compose run --rm api pytest
```

# Directory Structure

The following is an overview of the directory structure. It should be noted that since this uses tenant settings, the directory structure differs from traditional Django in certain aspects.

Deployment and build related files can be found in the `etc` folder.

- `etc\docker` contains docker files.
- `etc\pip` contains requirements.txt files for python requirements

## App folder

Source code is located in the `app` folder.

- `app\api` contains the API code (routes, controllers and schemas).
- `app\database` contains the database configuration and models.
- `app\tests` contains the unit and integration tests.
- `app\main.py` is the entry point for the application.
- `app\settings.py` contains the global settings for the project.

## Live example

Walk through the live example and test the API:

- [stg - https://gongwy0jx2.execute-api.us-west-1.amazonaws.com/dev/docs](https://gongwy0jx2.execute-api.us-west-1.amazonaws.com/dev/docs)
- [dev - https://brokerage-api.herokuapp.com/docs](https://brokerage-api.herokuapp.com/docs)

## Notes and restrictions

## Author ✒

- **Raul Novelo** - [@rnovec](https://github.com/rnovec)
