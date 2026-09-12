# Quick Start - Signal Desk v0

Get the full Signal Desk v0 implementation running in 5 minutes.

## 1️⃣ Start PostgreSQL (30 seconds)

```bash
docker compose up -d postgres
```

Or if using local PostgreSQL:
```bash
createdb signal_desk
```

## 2️⃣ Start Message Service (1 minute)

```bash
cd messages
uv sync
uv run fastapi run src/messages/main.py --host 0.0.0.0 --port 8000
```

✅ API available at: http://localhost:8000/docs

## 3️⃣ Start Web Interface (1 minute)

In a new terminal:

```bash
cd web
npm install
npm start
```

✅ Web app available at: http://localhost:4200

## 🎉 Done!

1. Open http://localhost:4200
2. Click "Messages" button
3. Type a message and send
4. See your message appear in the list!

## 📚 Full Documentation

- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Complete setup guide with troubleshooting
- **[web/README.md](./web/README.md)** - Angular web interface documentation
- **[messages/README.md](./messages/README.md)** - FastAPI service documentation
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture overview

## 🔧 Common Commands

```bash
# View API documentation
curl http://localhost:8000/docs

# Get all messages
curl http://localhost:8000/api/messages

# Send a message
curl -X POST http://localhost:8000/api/messages \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello!"}'

# Stop PostgreSQL
docker compose down
```

## ✨ What's Implemented (v0)

### Web Interface (Angular)
- ✅ Header with Messages button
- ✅ Modal for composing messages
- ✅ Message list display with timestamps
- ✅ HTTP client for API communication
- ✅ DaisyUI styling
- ✅ Responsive design

### Message Service (FastAPI)
- ✅ REST API endpoints (GET, POST)
- ✅ PostgreSQL persistence
- ✅ CORS support
- ✅ Health check endpoint
- ✅ Automatic database setup
- ✅ Error handling and validation

### Infrastructure
- ✅ Docker Compose for PostgreSQL
- ✅ Monorepo structure
- ✅ Development documentation

## 🚀 Next Steps

See [DEVELOPMENT.md](./DEVELOPMENT.md) for:
- Troubleshooting guide
- Database access instructions
- Testing and linting
- Production build steps
- Performance tips

## 📝 Project Files

Key files you should know about:

**Web Interface:**
- `web/src/app/components/header/` - Header with Messages button
- `web/src/app/components/message-list/` - Message modal and list
- `web/src/app/services/message.service.ts` - API client

**Message Service:**
- `messages/main.py` - REST API endpoints
- `messages/database.py` - Database configuration
- `messages/schemas.py` - Data models

**Configuration:**
- `docker-compose.yml` - PostgreSQL setup
- `.github/` - GitHub Actions (for future CI/CD)
