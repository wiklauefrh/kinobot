"""Quick start guide for KINOBOT."""

# KINOBOT - QUICK START

## 🚀 One-Liner Start (Docker)

```bash
cp .env.example .env
# Edit .env with your BOT_TOKEN
docker-compose up
```

Done! Bot is running.

## 📖 First Steps

### 1. Add Admin Content

Go to Telegram bot and:
```
/admin
```

### 2. Add a Movie

1. Click "Kino qo'shish" (Add Movie)
2. Enter title: "Avatar 2"
3. Enter code: "avatar2"
4. Enter genres: "sci-fi, adventure"
5. Enter year: "2022"
6. Send video file
7. Confirm

### 3. Search Movies

Send to bot:
```
Avatar
```

Bot responds with search results.

### 4. Rate Movie

Click star buttons under movie → Select rating

### 5. Create Broadcast

```
/admin
→ Create Broadcast
→ Enter message text
→ Select media (optional)
→ Select target users (optional filter)
→ Send broadcast
```

### 6. View Statistics

```
/admin
→ Statistics
```

Shows: DAU, WAU, MAU, top movies, etc.

## 🔧 Configuration

Edit `.env` file:

| Variable | Example | Required |
|----------|---------|----------|
| `BOT_TOKEN` | `123:ABC...` | ✅ |
| `BOT_USERNAME` | `@mybot` | ✅ |
| `SUPER_ADMIN_IDS` | `123456789` | ✅ |
| `DATABASE_URL` | `postgresql://...` | ✅ (auto Railway) |
| `REDIS_URL` | `redis://localhost` | ✅ (auto Railway) |
| `BASE_CHANNEL_ID` | `-1001234567890` | ✅ |
| `API_ID` | (from my.telegram.org) | ❌ Pyrogram |
| `API_HASH` | (from my.telegram.org) | ❌ Pyrogram |
| `USERBOT_SESSION_STRING` | (from pyrogram) | ❌ Pyrogram |
| `FORCE_SUBSCRIPTION` | `true` | ✅ |

## 📦 Services

All running in docker-compose:

- **PostgreSQL** (Port 5432) - Database
- **Redis** (Port 6379) - Cache & FSM
- **Bot** - Telegram bot (polling)

## 🧪 Test Bot Commands

```
/start              # Welcome message
/admin              # Admin panel
search query        # Search movies
/code_avatar2       # Get specific movie
/stats              # Statistics
```

## ❌ Common Issues

**Bot not responding?**
- Check BOT_TOKEN: `https://api.telegram.org/bot<TOKEN>/getMe`
- Check logs: `docker-compose logs bot`

**Cannot connect to database?**
- Verify PostgreSQL is running: `docker-compose ps`
- Check DATABASE_URL in .env

**Redis error?**
- Check Redis is running: `docker-compose ps`
- Verify REDIS_URL in .env

## 📊 Monitoring

### Logs
```bash
docker-compose logs bot          # Bot logs
docker-compose logs postgres     # Database logs
docker-compose logs redis        # Redis logs
```

### Database
```bash
docker-compose exec postgres psql -U kinobot_user -d kinobot_db
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM movies;
```

## 🌐 Deployment

### To Railway.io

1. Push to GitHub
2. Go to railway.app
3. Create project from GitHub repo
4. Add PostgreSQL & Redis from marketplace
5. Set environment variables
6. Deploy!

See `DEPLOYMENT.md` for details.

## 📚 Full Docs

- `README.md` - Features & architecture
- `DEPLOYMENT.md` - Production deployment
- `db/models.py` - Database schema
- `services/` - Business logic
- `bot/handlers/` - Message handlers

## 💡 Pro Tips

- Admin panel: `/admin`
- Add to channel: `/admin → Channels`
- Set subscription required: `/admin → Settings`
- Schedule broadcasts: Use APScheduler
- Backup data: Runs daily at 3 AM (configurable)

---

**Ready?** Start with: `docker-compose up`
