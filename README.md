# Brokerage API

## Features

- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework, high performance, easy to learn, fast to code, ready for production
- [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL Toolkit and Object Relational Mapper with SQLite3 implementation
- [Pytest](https://docs.pytest.org/en/7.1.x/) - The **pytest** framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.

## Requirements

- Python 3.8+
- Docker
- Docker Compose

### Run locally

```bash
docker-compose up
```

#### OpenSwagger docs

- [http://localhost:8000/docs](http://localhost:8000/docs)

#### Run tests

```
docker-compose run --rm api pytest
```