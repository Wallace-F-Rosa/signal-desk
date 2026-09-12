# Development Guide - Signal Desk v0

This guide walks you through setting up and running the v0 implementation of Signal Desk.

## Architecture Overview

Signal Desk v0 implements a simple 3-tier architecture:

1. **Web Interface (Angular)** - User-facing UI for composing and viewing messages
2. **Message Service (FastAPI)** - REST API server for message persistence
3. **Database (PostgreSQL)** - Message storage

## Prerequisites

- **Node.js 18+** - For Angular frontend
- **Python 3.10+** - For FastAPI backend
- **PostgreSQL 12+** - For message storage
- **Docker & Docker Compose** (optional) - For PostgreSQL container

## Step 1: Start PostgreSQL

### Option A: Using Docker Compose (Recommended)

```bash
# From the root directory
docker compose up -d postgres

# Verify it's running
docker compose ps
```

### Option B: Using Local PostgreSQL

```bash
# Create the database
createdb signal_desk

# Verify connection
psql -U postgres -d signal_desk -c "SELECT 1;"
```

## Step 2: Start the Message Service

```bash
cd messages

# Install dependencies and run the service
uv sync
uv run fastapi run src/messages/main.py --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify the service is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"ok"}
```

**View API docs:**
Visit http://localhost:8000/docs in your browser for interactive Swagger documentation.

## Step 3: Start the Web Interface

In a new terminal:

```bash
cd web

# Install dependencies
npm install

# Start development server
npm start
```

**Expected output:**
```
✔ Compiled successfully.

Application bundle generated successfully.
✔ Compiled successfully.
```

**Access the application:**
Visit http://localhost:4200 in your browser.

## Using the Application

1. Click the **"Messages"** button in the header (top right)
2. Type your message in the text area
3. Click **"Send"**
4. Your message appears in the list below

## Troubleshooting

### "Connection refused" on Message Service

**Problem:** The web interface can't connect to the API
**Solution:** 
- Ensure the message service is running on port 8000
- Check that CORS is configured correctly in `messages/main.py`

### "Database connection error"

**Problem:** Message Service can't connect to PostgreSQL
**Solution:**
- Verify PostgreSQL is running: `docker-compose ps`
- Check DATABASE_URL in `.env` matches your setup
- For Docker Compose: `postgresql://postgres:postgres@localhost:5432/signal_desk`

### Port already in use

**Problem:** "Port 4200 already in use" or "Port 8000 already in use"
**Solution:**
```bash
# Kill process using port (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or on macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

## Project Structure

```
signal-desk/
├── web/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── header/          # Header with Messages button
│   │   │   │   └── message-list/    # Message list and modal
│   │   │   ├── services/
│   │   │   │   └── message.service.ts  # HTTP client
│   │   │   ├── app.component.ts
│   │   │   └── app.routes.ts
│   │   ├── main.ts
│   │   └── index.html
│   ├── package.json
│   ├── angular.json
│   └── tsconfig.json
│
├── messages/
│   ├── main.py              # FastAPI application & endpoints
│   ├── database.py          # SQLAlchemy ORM setup
│   ├── schemas.py           # Pydantic models
│   ├── run.py               # Server runner
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── docker-compose.yml       # PostgreSQL container
└── README.md               # Main documentation
```

## Next Steps (Milestones)

- **Milestone 1**: Add authentication, input validation, error handling
- **Milestone 2**: Add Docker images for services and deployment
- **Milestone 3**: Set up GitHub Actions CI/CD pipeline
- **Milestone 4**: Deploy to Kubernetes cluster

## Useful Commands

### Message Service

```bash
# View API docs
curl http://localhost:8000/docs

# Get all messages
curl http://localhost:8000/api/messages

# Send a message
curl -X POST http://localhost:8000/api/messages \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from curl!"}'

# Health check
curl http://localhost:8000/health
```

### Web Interface

```bash
# Build for production
npm run build

# Run tests
npm test

# Lint code
ng lint
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f postgres

# Stop all services
docker-compose down

# Remove volumes (including data)
docker-compose down -v
```

## Database Access

Access PostgreSQL directly:

```bash
# Using psql
psql -U postgres -d signal_desk

# View messages table
SELECT * FROM messages;

# Using Docker
docker-compose exec postgres psql -U postgres -d signal_desk
```

## Performance Tips

- The Angular app caches messages in memory. Refresh the page to see updates from other clients.
- For production, consider adding Redis caching for frequently accessed messages.
- Set up database connection pooling with SQLAlchemy for better performance.

## Additional Resources

- [Angular Documentation](https://angular.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [DaisyUI Documentation](https://daisyui.com/)
