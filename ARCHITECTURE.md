# Signal Desk architecture

```text
Browser -> Angular frontend -> FastAPI messages API -> SQLAlchemy ORM -> PostgreSQL
```

## Responsibilities

- Angular frontend: user interface and transient browser state
- FastAPI service: API contract and business logic
- SQLAlchemy ORM: database-access layer
- PostgreSQL: durable storage
- Alembic: schema versioning under messages/migrations

## Boundaries

- The browser does not connect to PostgreSQL.
- The FastAPI service owns validation and persistence logic.
- Database schema changes are managed through Alembic migration files, not ad hoc runtime SQL.
- Pydantic models validate request/response payloads; SQLAlchemy models define the database schema.
