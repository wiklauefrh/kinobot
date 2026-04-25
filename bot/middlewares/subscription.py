from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, Update, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories import ChannelRepository, SettingsRepository
from db.constants import SettingKey
from config import settings as app_settings
import logging

logger = logging.getLogger(__name__)


class SubscriptionMiddleware(BaseMiddleware):
    """Middleware that checks force subscription."""

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        """Check if user is subscribed to required channels."""
        session: AsyncSession = data.get("session")
        
        # Get user from event
        user = None
        if event.message:
            user = event.message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
        
        if not user or not session:
            return await handler(event, data)
        
        try:
            # Check if force subscription is enabled
            settings_repo = SettingsRepository(session)
            force_sub = await settings_repo.get_bool(SettingKey.FORCE_SUBSCRIPTION.value, True)
            
            if not force_sub:
                return await handler(event, data)
            
            # Get required channels
            channel_repo = ChannelRepository(session)
            required_channels = await channel_repo.get_required_channels()
            
            if not required_channels:
                return await handler(event, data)
            
            # Check subscription for each channel
            from bot.loader import bot
            
            for channel in required_channels:
                try:
                    member = await bot.get_chat_member(channel.tg_chat_id, user.id)
                    
                    # Check membership status
                    ok_statuses = ["member", "administrator", "creator", "owner"]
                    if member.status not in ok_statuses:
                        # User not subscribed - send button to join
                        logger.info(f"User {user.id} not subscribed to {channel.title}")
                        
                        # TODO: Send subscription reminder with join button
                        # For now, just pass through (will be implemented in handlers)
                        return await handler(event, data)
                
                except Exception as e:
                    logger.warning(f"Error checking subscription for user {user.id}: {e}")
                    # On error, allow through (safe fallback)
                    continue
            
        except Exception as e:
            logger.error(f"Subscription middleware error: {e}")
            await session.rollback()
        
        return await handler(event, data)
