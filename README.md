# KINOBOT 🎬

Telegram bot for streaming movies and TV series with admin panel, advanced broadcasting, and analytics.

## Features

- 🎥 **Content Management**: Add movies, series, seasons, and episodes
- 📤 **Smart Broadcasting**: Rate-limited multi-worker broadcast engine with segment targeting
- 🔍 **Full-Text Search**: Search by title, code, genre, year
- ⭐ **Rating System**: 1-5 star ratings with discussion threads
- 📊 **Analytics Dashboard**: DAU, WAU, MAU, trending content, search analytics
- 👥 **Admin Panel**: Role-based access (owner, admin, content_mgr, broadcaster)
- 📥 **Subscription Management**: Force-required channels, join request handling
- 💾 **Backup/Restore**: Daily automatic backups + manual restore
- 🔐 **Referral System**: Track user invitations and channel joins

## Tech Stack

- **Framework**: aiogram 3 (Telegram bot)
- **Userbot**: Pyrogram 2 (optional, for enhanced delivery)
- **Database**: PostgreSQL + asyncpg + SQLAlchemy (async)
- **Cache**: Redis (FSM storage, rate limiting signals)
- **Scheduler**: APScheduler (cron jobs)
- **Logging**: structlog (JSON structured logs)
- **Deployment**: Docker + Railway.io

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))

### Local Development

1. **Clone and setup**
```bash
cd KINOBOT
cp .env.example .env
# Edit .env with your BOT_TOKEN, etc.
```

2. **Start services (Docker)**
```bash
docker-compose up -d
```

3. **Run bot**
```bash
docker-compose up bot
# Or locally:
python -m pip install -e .
python main.py
```

4. **Database**
Tables are auto-created on first run. To initialize:
```bash
python -c "import asyncio; from db.init_db import setup_database; asyncio.run(setup_database())"
```

## Configuration

Create `.env` file from `.env.example`:

```env
# Bot
BOT_TOKEN=your_token_here
BOT_USERNAME=your_bot_name
SUPER_ADMIN_IDS=123456789,987654321

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/kinobot_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Userbot (optional)
API_ID=123456
API_HASH=abc123...
USERBOT_SESSION_STRING=...

# Channels
BASE_CHANNEL_ID=-1001234567890
LOG_CHANNEL_ID=-1001234567890
COMMENT_GROUP_ID=-1001234567890

# Features
FORCE_SUBSCRIPTION=true
MAINTENANCE_MODE=false
```

## Deployment to Railway

1. Push code to GitHub
2. Create Railway project, connect GitHub repo
3. Add services:
   - PostgreSQL (Railway marketplace)
   - Redis (Railway marketplace)
4. Set environment variables in Railway dashboard
5. Deploy!

## Admin Commands

- `/start` - Start bot (user)
- `/admin` - Admin panel entry (admin only)

## User Commands

- Send text to search movies/series
- `/code_XXX` - Show movie by code

## Database Schema

**13 Tables**:
- User, Admin, Channel, ChannelJoinRequest, ChannelReferral
- Movie, MovieView, Series, Season, Episode
- Rating, SearchQuery, Broadcast, Setting

## Performance Tuning

- Connection pool: 20 base + 30 overflow
- Broadcast workers: 3-5 concurrent (configurable)
- Rate limiting: 28 msg/sec (bot API), 20 msg/sec (userbot)
- Database indices on: broadcast(status, updated_at), user(banned, blocked, active_at), movie_view(user_id, viewed_at)

## File Structure

```
├── bot/
│   ├── handlers/       # Message/callback handlers
│   ├── keyboards/      # Inline keyboards
│   ├── middlewares/    # DB, user tracking, subscription, throttling
│   ├── states.py       # FSM state groups
│   └── loader.py       # Bot initialization
├── db/
│   ├── models.py       # SQLAlchemy models (13 tables)
│   ├── repositories/   # Data access layer (8 repos)
│   └── constants.py    # Enums (SettingKey, AdminRole, etc.)
├── services/
│   ├── broadcaster.py  # Rate-limited broadcast engine
│   ├── search.py       # Full-text search
│   ├── subscription.py # Subscription checking
│   ├── stats.py        # Analytics
│   ├── backup.py       # Backup/restore
│   ├── scheduler.py    # APScheduler jobs
│   └── userbot.py      # Pyrogram wrapper
├── utils/
│   ├── logging.py      # Structured logging (structlog)
│   ├── texts.py        # Uzbek UI messages
│   └── helpers.py      # Utility functions
├── main.py             # Bot entrypoint
└── config.py           # Pydantic settings
```

## Development

### Adding a Movie

```python
movie = await movie_repo.create(
    code="avatar2",
    title="Avatar: The Way of Water",
    video_file_id="AgACAgI...",
    year=2022,
    genres=["sci-fi", "adventure"]
)
```

### Broadcasting to Users

```python
broadcast = await broadcast_repo.create(admin_id=123, mode="custom")
broadcast.text = "Yangi film: Avatar 2"
broadcast.segment = {"lang": "uz", "active_days": 30}
await session.commit()

engine = BroadcastEngine(session, bot)
await engine.start(broadcast.id, admin_chat_id=123)
```

### Checking Subscriptions

```python
sub_service = SubscriptionService(session, bot)
is_sub = await sub_service.is_user_subscribed(user_id, channel_id)
```

## Troubleshooting

**Bot not responding?**
- Check `BOT_TOKEN` is correct
- Verify PostgreSQL and Redis are running
- Check logs: `docker-compose logs bot`

**Broadcast stuck?**
- Check connection pool: may need to increase `max_overflow`
- Verify broadcaster workers are running
- Check user IDs are valid

**Userbot not working?**
- Ensure `API_ID`, `API_HASH`, and `USERBOT_SESSION_STRING` are set
- Pyrogram requires valid Telegram account session

## License

MIT
