from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Store last message time per user
_user_last_action = {}


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware that limits user action rate."""

    # Throttle delay in seconds (1 message per 1 second)
    delay = 1.0

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        """Check throttle limit."""
        user = None
        if event.message:
            user = event.message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
        
        if not user:
            return await handler(event, data)
        
        user_id = user.id
        now = datetime.now()
        
        if user_id in _user_last_action:
            last_action = _user_last_action[user_id]
            if now - last_action < timedelta(seconds=self.delay):
                logger.debug(f"Throttling user {user_id}")
                # Don't process the event
                return
        
        _user_last_action[user_id] = now
        return await handler(event, data)
