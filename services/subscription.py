"""Subscription service."""

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from db.repositories.channel_repo import ChannelRepository
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Service for checking user subscriptions."""

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.channel_repo = ChannelRepository(session)

    async def is_user_subscribed(self, user_id: int, channel_id: int) -> bool:
        """Check if user is subscribed to a channel."""
        channel = await self.channel_repo.get_by_id(channel_id)
        if not channel:
            return False

        try:
            member = await self.bot.get_chat_member(channel.tg_chat_id, user_id)

            # Check membership status
            ok_statuses = ["member", "administrator", "creator", "owner"]
            if member.status not in ok_statuses:
                return False

            # For request_join channels, verify join request is approved
            if channel.type == "request_join":
                is_approved = await self.channel_repo.is_join_request_approved(user_id, channel_id)
                return is_approved

            return True

        except TelegramAPIError as e:
            logger.warning(f"Error checking subscription for user {user_id}: {e}")
            # On error, deny access (safe fallback)
            return False

    async def check_all_required(self, user_id: int) -> bool:
        """Check if user subscribed to all required channels."""
        required = await self.channel_repo.get_required_channels()
        for channel in required:
            if not await self.is_user_subscribed(user_id, channel.id):
                return False
        return True

    async def get_required_channels(self):
        """Get all required subscription channels."""
        return await self.channel_repo.get_required_channels()
