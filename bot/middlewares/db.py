from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import AsyncSessionLocal


class DBMiddleware(BaseMiddleware):
    """Middleware that injects AsyncSession into handler context."""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        """Add database session to context."""
        async with AsyncSessionLocal() as session:
            data["session"] = session
            return await handler(event, data)
