# Signal Desk architecture
 
 ```text
 Browser -> Nginx (Reverse Proxy) -> Angular frontend / FastAPI messages API -> SQLAlchemy ORM -> PostgreSQL
 ```
 
 ## Responsibilities
 
 - Nginx: Reverse proxy, static asset serving, and API routing
 - Angular frontend: user interface and transient browser state
 - FastAPI service: API contract and business logic (separated into controllers and services)
 - SQLAlchemy ORM: database-access layer (centralized in a dedicated database package)
 - PostgreSQL: durable storage
 - Alembic: schema versioning under messages/migrations
 
 ## Network Flow
 
 - **External Entry**: Traffic enters via Nginx (mapped port 80 -> internal port 8080).
 - **Static Content**: Nginx serves the Angular production build from `/usr/share/nginx/html`.
 - **API Proxy**: Requests starting with `/api/` are proxied to the `signal-desk-messages` service on port 8000.
 - **Internal Communication**: Services communicate over the `signal-desk-network` bridge.
 
 ## Boundaries
 
 - The browser does not connect to PostgreSQL.
 - The FastAPI service owns validation and persistence logic.
 - Database schema changes are managed through Alembic migration files, not ad hoc runtime SQL.
 - Pydantic models validate request/response payloads; SQLAlchemy models define the database schema.
