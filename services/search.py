"""Search service."""

from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.movie_repo import MovieRepository
from db.repositories.series_repo import SeriesRepository
from db.repositories.stats_repo import StatsRepository
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """Service for searching movies and series."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.movie_repo = MovieRepository(session)
        self.series_repo = SeriesRepository(session)
        self.stats_repo = StatsRepository(session)

    async def full(self, query: str, user_id: int, limit: int = 10) -> Tuple[List, List]:
        """Full search for movies and series."""
        movies = await self.movie_repo.search(query, limit=limit)
        series = await self.series_repo.search(query, limit=limit)

        # Log search query
        results_count = len(movies) + len(series)
        await self.stats_repo.log_search_query(user_id, query, results_count)
        await self.session.commit()

        return movies, series

    async def by_code(self, code: str):
        """Search by code."""
        movie = await self.movie_repo.get_by_code(code)
        if movie:
            return movie, None
        series = await self.series_repo.get_by_code(code)
        return None, series

    async def by_genre(self, genre: str, limit: int = 10) -> Tuple[List, List]:
        """Search by genre."""
        movies = await self.movie_repo.search_by_genre(genre, limit=limit)
        series = await self.series_repo.search_by_genre(genre, limit=limit)
        return movies, series

    async def random(self, limit: int = 5) -> Tuple[List, List]:
        """Get random content."""
        movies = await self.movie_repo.get_random(limit=limit)
        series = await self.series_repo.get_random(limit=limit)
        return movies, series

    async def top(self, limit: int = 10) -> Tuple[List, List]:
        """Get top content."""
        movies = await self.movie_repo.get_top_movies(limit=limit)
        series = await self.series_repo.get_top_series(limit=limit)
        return movies, series
