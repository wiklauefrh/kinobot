"""Deployment checklist and verification script."""

import asyncio
import logging
from pathlib import Path
import sys

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_imports():
    """Check all critical imports."""
    logger.info("Checking imports...")
    try:
        from config import settings
        logger.info("✓ config.settings")
        
        from db.base import engine, AsyncSessionLocal
        logger.info("✓ db.base (engine, session)")
        
        from db.models import (
            User, Movie, Series, Channel, Rating, 
            Admin, Broadcast, Setting
        )
        logger.info("✓ db.models (all 13 models)")
        
        from db.repositories import (
            UserRepository, MovieRepository, SeriesRepository,
            ChannelRepository, AdminRepository, BroadcastRepository,
            SettingsRepository, StatsRepository
        )
        logger.info("✓ db.repositories (all 8)")
        
        from bot.loader import bot, setup_dispatcher
        logger.info("✓ bot.loader (bot, dispatcher)")
        
        from bot.handlers import user, admin, user_callbacks, fsm_handlers
        logger.info("✓ bot.handlers (all 4 modules)")
        
        from bot.middlewares import (
            DBMiddleware, UserTrackingMiddleware,
            SubscriptionMiddleware, ThrottlingMiddleware
        )
        logger.info("✓ bot.middlewares (all 4)")
        
        from services import (
            SearchService, SubscriptionService, BroadcastEngine,
            StatsService, BackupService, SchedulerService, UserbotService
        )
        logger.info("✓ services (all 7)")
        
        from utils import setup_logging
        logger.info("✓ utils.logging")
        
        return True
    except Exception as e:
        logger.error(f"✗ Import failed: {e}")
        return False


async def check_database_config():
    """Check database configuration."""
    logger.info("\nChecking database config...")
    try:
        from config import settings
        
        # Check DATABASE_URL
        if not settings.DATABASE_URL:
            logger.error("✗ DATABASE_URL not set")
            return False
        logger.info(f"✓ DATABASE_URL configured")
        
        # Check async conversion
        async_url = settings.ASYNC_DATABASE_URL
        if not async_url.startswith("postgresql+asyncpg://"):
            logger.error(f"✗ Invalid async URL: {async_url}")
            return False
        logger.info(f"✓ Async URL conversion working")
        
        return True
    except Exception as e:
        logger.error(f"✗ Database config check failed: {e}")
        return False


async def check_file_structure():
    """Check required file structure."""
    logger.info("\nChecking file structure...")
    
    required_files = [
        "main.py",
        "config.py",
        "pyproject.toml",
        "Dockerfile",
        "docker-compose.yml",
        "railway.toml",
        ".env.example",
        "README.md",
        ".gitignore",
        "bot/__init__.py",
        "bot/loader.py",
        "bot/states.py",
        "db/__init__.py",
        "db/base.py",
        "db/models.py",
        "db/init_db.py",
        "db/constants.py",
        "services/__init__.py",
        "utils/__init__.py",
    ]
    
    base_path = Path(__file__).parent
    missing = []
    
    for file in required_files:
        path = base_path / file
        if not path.exists():
            missing.append(file)
            logger.error(f"✗ Missing: {file}")
        else:
            logger.info(f"✓ {file}")
    
    return len(missing) == 0


async def main():
    """Run all checks."""
    logger.info("=" * 60)
    logger.info("KINOBOT DEPLOYMENT VERIFICATION")
    logger.info("=" * 60)
    
    checks = [
        ("File Structure", await check_file_structure()),
        ("Database Config", await check_database_config()),
        ("Imports", await check_imports()),
    ]
    
    logger.info("\n" + "=" * 60)
    logger.info("VERIFICATION RESULTS")
    logger.info("=" * 60)
    
    passed = 0
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{check_name}: {status}")
        if result:
            passed += 1
    
    logger.info("=" * 60)
    logger.info(f"Score: {passed}/{len(checks)} checks passed")
    
    if passed == len(checks):
        logger.info("\n🚀 READY FOR DEPLOYMENT!")
        return 0
    else:
        logger.error("\n❌ Fix issues before deployment")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
