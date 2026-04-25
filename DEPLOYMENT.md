"""Deployment guide for KINOBOT."""

# KINOBOT DEPLOYMENT GUIDE

## Prerequisites

- Docker & Docker Compose
- Railway.io account (for production)
- Telegram Bot Token from @BotFather
- PostgreSQL credentials (auto-provided by Railway)

## Local Development Setup

### 1. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env`:
```env
BOT_TOKEN=<your_telegram_bot_token>
BOT_USERNAME=<your_bot_username>
SUPER_ADMIN_IDS=<your_telegram_id>,<other_admin_ids>

# Local development
DATABASE_URL=postgresql+asyncpg://kinobot_user:kinobot_password@localhost:5432/kinobot_db
REDIS_URL=redis://localhost:6379/0

# Channels
BASE_CHANNEL_ID=-1001234567890
LOG_CHANNEL_ID=-1001234567890
COMMENT_GROUP_ID=-1001234567890

# Optional: Pyrogram for userbot
API_ID=<your_api_id>
API_HASH=<your_api_hash>
USERBOT_SESSION_STRING=<your_session_string>
```

### 2. Start Services Locally

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Verify services are running
docker-compose ps

# Check database health
docker-compose exec postgres pg_isready -U kinobot_user -d kinobot_db

# Check Redis health
docker-compose exec redis redis-cli ping
```

### 3. Run Bot Locally

```bash
# Option A: Docker
docker-compose up bot

# Option B: Local environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -e .
python main.py
```

### 4. Verify Deployment

```bash
python verify_deployment.py
```

Expected output:
```
✓ File Structure: PASS
✓ Database Config: PASS
✓ Imports: PASS
🚀 READY FOR DEPLOYMENT!
```

## Production Deployment (Railway.io)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial KINOBOT deployment"
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

### 2. Create Railway Project

1. Go to https://railway.app
2. Create new project
3. Connect GitHub repository
4. Select this repository

### 3. Add Services

#### PostgreSQL Service:
- From Railway Marketplace → Add PostgreSQL
- Railway auto-provides DATABASE_URL

#### Redis Service:
- From Railway Marketplace → Add Redis
- Railway auto-provides REDIS_URL

#### Bot Service:
- Create from GitHub repo
- Build: Dockerfile
- Entrypoint: `python -u main.py`

### 4. Set Environment Variables

In Railway dashboard, go to project settings and add:

```
BOT_TOKEN=<your_telegram_bot_token>
BOT_USERNAME=<your_bot_username>
SUPER_ADMIN_IDS=<admin_ids>
BASE_CHANNEL_ID=<channel_id>
LOG_CHANNEL_ID=<channel_id>
COMMENT_GROUP_ID=<group_id>
LOG_LEVEL=INFO
FORCE_SUBSCRIPTION=true

# Pyrogram (optional)
API_ID=<optional>
API_HASH=<optional>
USERBOT_SESSION_STRING=<optional>
```

### 5. Deploy

- Railway auto-detects from GitHub push
- Or manually trigger deployment from dashboard
- View logs: `railway logs bot`

### 6. Verify Production

```bash
# Check bot is running (from Railway logs)
railway logs bot

# Check database connection
# Should show: "✓ Database schema created/verified"

# Send /start to bot via Telegram
# Should respond with welcome message
```

## Database Initialization

### First Run (Auto)
- On bot startup, `setup_database()` runs automatically
- Creates all 13 tables
- Sets default settings

### Manual Initialization
```bash
python -c "import asyncio; from db.init_db import setup_database; asyncio.run(setup_database())"
```

## Backup & Restore

### Automatic Daily Backup
- Runs at 3 AM UTC+5 (22:00 UTC)
- Saves to `backups/kinobot_backup_YYYYMMDD_HHMMSS.json.gz`

### Manual Backup
```python
from db.base import AsyncSessionLocal
from services.backup import BackupService
import asyncio

async def backup():
    async with AsyncSessionLocal() as session:
        service = BackupService(session)
        await service.backup_now()

asyncio.run(backup())
```

### Restore Backup
```python
async def restore(backup_file):
    async with AsyncSessionLocal() as session:
        service = BackupService(session)
        await service.restore(backup_file)
```

## Monitoring

### Logs
- Local: stdout
- Railway: Dashboard → Logs

### Key Log Patterns
```
✓ Database initialized
✓ Dispatcher created
Starting polling...
```

### Check Bot Status
```bash
# In Telegram
/start          # Should respond
/admin          # Should show admin menu (if admin)
search_query    # Should search movies
```

## Troubleshooting

### Bot not responding
1. Check `BOT_TOKEN` is correct: `https://api.telegram.org/bot<TOKEN>/getMe`
2. Check logs: `docker-compose logs bot` or Railway logs
3. Verify database is running: `docker-compose ps`

### Database connection failed
```
Error: could not connect to server
Solution: Check DATABASE_URL format, PostgreSQL is running
```

### Redis connection failed
```
Error: Cannot connect to Redis
Solution: Check REDIS_URL, Redis container is running
```

### Userbot not working
```
Solution: Optional feature - bot falls back to bot API
Set API_ID, API_HASH, and USERBOT_SESSION_STRING to enable
```

## Performance Tuning

### Database
- Connection pool: 50 (20 base + 30 overflow)
- Adjust in `db/base.py` if needed
- Indices on: broadcast(status, updated_at), user(banned, blocked), movie_view(user_id, viewed_at)

### Broadcast
- Workers: 3-5 concurrent (configurable in broadcaster.py)
- Rate limit: 28 msg/sec (bot API), 20 msg/sec (userbot)
- Adjust in `config.py` via BROADCAST_BOT_RATE, BROADCAST_USERBOT_RATE

### Middleware
- Throttling: 1 message/sec per user
- Adjust in `bot/middlewares/throttling.py` if needed

## File Structure Reference

```
KINOBOT/
├── bot/              # Bot handlers and utilities
├── db/               # Database models and repositories
├── services/         # Business logic services
├── utils/            # Utilities (logging, texts, helpers)
├── tests/            # Unit tests
├── main.py           # Entry point
├── config.py         # Configuration
├── verify_deployment.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Support

For issues:
1. Check logs: `docker-compose logs <service>`
2. Review: README.md
3. Check: db/models.py (schema)
4. Review: services/ (business logic)

---

**Status**: ✅ Production Ready
**Last Updated**: 2026-04-25
