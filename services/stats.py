"""Stats/Analytics service."""

from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.stats_repo import StatsRepository
import logging

logger = logging.getLogger(__name__)


class StatsService:
    """Service for analytics and statistics."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.stats = StatsRepository(session)

    async def get_dashboard_stats(self) -> dict:
        """Get dashboard statistics."""
        return {
            "total_users": await self.stats.get_total_users(),
            "active_today": await self.stats.get_active_users_today(),
            "active_week": await self.stats.get_active_users_week(),
            "active_month": await self.stats.get_active_users_month(),
            "new_today": await self.stats.get_new_users_today(),
            "new_week": await self.stats.get_new_users_week(),
            "new_month": await self.stats.get_new_users_month(),
            "banned": await self.stats.get_banned_users_count(),
            "blocked": await self.stats.get_blocked_users_count(),
            "premium": await self.stats.get_premium_users_count(),
            "movies": await self.stats.get_movies_count(),
            "series": await self.stats.get_series_count(),
        }

    async def get_top_content(self, limit: int = 10) -> dict:
        """Get top movies and series."""
        return {
            "top_movies": await self.stats.get_top_movies(limit=limit),
            "top_series": await self.stats.get_top_series(limit=limit),
            "top_queries": await self.stats.get_top_search_queries(limit=limit),
        }

    async def get_growth_data(self, days: int = 30) -> dict:
        """Get user growth data."""
        return {
            "new_users_by_day": await self.stats.get_new_users_by_day(days=days),
            "active_users_by_day": await self.stats.get_active_users_by_day(days=days),
        }

    async def get_referral_stats(self) -> dict:
        """Get referral statistics."""
        return await self.stats.get_referral_stats()

    async def get_broadcast_stats(self) -> dict:
        """Get broadcast statistics."""
        return await self.stats.get_broadcast_stats()
