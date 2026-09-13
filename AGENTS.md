# Signal Desk agent notes

## Architecture

```text
Browser -> Angular frontend -> FastAPI messages API -> SQLAlchemy ORM -> PostgreSQL
```

- Angular app: UI and transient browser state
- FastAPI service: API contract and business logic
- SQLAlchemy ORM: database access layer
- PostgreSQL: durable storage
- Alembic: schema versioning under messages/migrations

## Rules

- Keep scope to the current milestone.
- Prefer the smallest relevant fix and validation.
- Do not add extra architecture or deployment patterns unless asked.
- Treat Alembic migration files as the source of truth for schema changes.
- Keep Pydantic models for API validation only; use SQLAlchemy models for database mapping.

## Validation

```bash
cd messages
source .venv/bin/activate
PYTHONPATH=src pytest tests -q
```

For DB migration checks:

```bash
cd messages
source .venv/bin/activate
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/signal_desk PYTHONPATH=src alembic current
```

## Canonical sources

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [docs/devops-study-guide.md](docs/devops-study-guide.md)
- [messages/migrations](messages/migrations)
