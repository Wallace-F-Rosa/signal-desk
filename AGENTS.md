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

## Project Map
- `/messages/src/main.py`: FastAPI Application Entry
- `/messages/src/messages/main.py`: Message API Controllers (Routers)
- `/messages/src/messages/service.py`: Message Business Logic
- `/messages/src/database/`: Shared Database Infrastructure & Models
- `/messages/migrations/`: Alembic Schema Versions

## Rules
 
 - Keep scope to the current milestone.
 - Prefer the smallest relevant fix and validation.
 - Do not add extra architecture or deployment patterns unless asked.
 - Treat Alembic migration files as the source of truth for schema changes.
 - Keep Pydantic models for API validation only; use SQLAlchemy models for database mapping.
 - **Documentation Sync**: Any structural update to project files (new packages, renamed services, architectural shifts) must be immediately reflected in `AGENTS.md` and `ARCHITECTURE.md`.
 - **Diagramming**: All architectural and flow diagrams must be created using Mermaid.js syntax instead of ASCII art.
 - **Optimize token usage**:
    - Restrict `grep` and `read` operations to source directories (e.g., `src/`).
    - Never scan or read build artifacts, `node_modules`, `.venv`, `.angular`, or `dist/` folders.
    - Use `grep -n` to find line numbers and read specific offsets/limits instead of whole files.
    - Combine multiple filesystem operations (e.g., `mkdir`, `mv`, `rm`) into single `bash` calls.
    - Prefer `edit` over `write` to avoid transferring large file contents. If `edit` fails due to whitespace, do not repeat the call; instead, read the file again or rewrite it.
    - Summarize long tool outputs; avoid pasting raw logs into the prompt.
    - Update `todo_write` only after completing logical phases.
 - **Operational Discipline**:
    - If a tool call fails twice with the same error, stop and re-examine the raw output of the previous `read` or `grep` before attempting a third time.
    - For complex refactors, use phase-based planning (Infrastructure -> Logic -> Validation).
    - Always ensure `PYTHONPATH=src` and `DATABASE_URL` are set when running alembic or pytest manually in bash.

## Validation
 
- **Criteria for completion**: 1. Happy path (2xx), 2. Validation errors (422), 3. Infrastructure failures (5xx), 4. Unit tests for service logic.

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
