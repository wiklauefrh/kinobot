import asyncio
import logging
from db.base import engine, Base, AsyncSessionLocal
from db import models

logger = logging.getLogger(__name__)


async def init_db():
    """Initialize database schema."""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✓ Database schema created/verified")


async def create_default_settings():
    """Create default settings if they don't exist."""
    async with AsyncSessionLocal() as session:
        default_settings = {
            "force_subscription": "true",
            "maintenance_mode": "false",
            "allow_paid_broadcast": "false",
            "broadcast_bot_rate": "28",
            "broadcast_userbot_rate": "20",
        }
        
        for key, value in default_settings.items():
            # Check if setting exists
            from sqlalchemy import select
            stmt = select(models.Setting).where(models.Setting.key == key)
            result = await session.execute(stmt)
            existing = result.scalars().first()
            
            if not existing:
                setting = models.Setting(key=key, value=value)
                session.add(setting)
        
        await session.commit()
        logger.info("✓ Default settings created")


async def setup_database():
    """Full database setup."""
    try:
        await init_db()
        await create_default_settings()
        logger.info("✓ Database initialized successfully")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        raise
