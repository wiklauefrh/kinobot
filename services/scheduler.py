"""Scheduler service for background jobs."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from db.base import AsyncSessionLocal
from services.backup import BackupService
from services.stats import StatsService
from aiogram import Bot
import logging

logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for scheduling background jobs."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """Start the scheduler."""
        # Daily backup at 3 AM UTC+5 (10 PM UTC)
        self.scheduler.add_job(
            self._backup_job,
            CronTrigger(hour=22, minute=0, timezone="UTC"),
            id="daily_backup",
            name="Daily backup",
        )

        self.scheduler.start()
        logger.info("✓ Scheduler started")

    async def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

    async def _backup_job(self):
        """Backup job."""
        try:
            async with AsyncSessionLocal() as session:
                backup_service = BackupService(session)
                await backup_service.backup_now()
        except Exception as e:
            logger.error(f"Backup job failed: {e}")

    async def _refresh_channels_job(self):
        """Refresh channel member counts."""
        # To be implemented
        pass
