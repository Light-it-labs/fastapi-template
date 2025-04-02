# fast-api-template

Auth Service in FastAPI

### Install dependencies

1. Install [Poetry](https://python-poetry.org/).
   `pip install poetry`
2. Access Poetry shell.
   `poetry shell`
3. Install dependencies.
   `poetry install`

### Run dockerized project

Run `cp .env.example .env`
Run `docker-compose up -d`

### Migrations

Migrations can be autogenerated using the `generate_migrations.sh` script.

### Linters

We use ruff as linter, to run them on pre-commit please run `pre-commit install`.

### Tests

- You can run tests locally by running `./tests-start.sh` (this will use your local database).
- Tests can also run in docker container with the following command: `docker-compose exec api ./tests-start.sh`.

### Seed db

Run `./scripts/seed-db.sh`
