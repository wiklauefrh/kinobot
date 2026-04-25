"""Userbot service using Pyrogram."""

from config import settings
import logging

logger = logging.getLogger(__name__)


class UserbotService:
    """Pyrogram userbot wrapper for enhanced delivery."""

    def __init__(self):
        self.client = None
        self.has_session = False

    async def initialize(self):
        """Initialize userbot connection."""
        if not settings.has_userbot():
            logger.warning("Userbot credentials not configured - will use bot API only")
            return False

        try:
            from pyrogram import Client
            
            self.client = Client(
                name="kinobot_userbot",
                api_id=settings.API_ID,
                api_hash=settings.API_HASH,
                session_string=settings.USERBOT_SESSION_STRING,
                no_updates=True,
            )
            
            await self.client.connect()
            self.has_session = True
            logger.info("✓ Userbot connected")
            return True
        
        except Exception as e:
            logger.warning(f"Userbot connection failed: {e}")
            return False

    async def send_video(self, chat_id: int, file_id: str, caption: str = None):
        """Send video via userbot."""
        if not self.has_session or not self.client:
            raise RuntimeError("Userbot not available")
        
        try:
            await self.client.send_video(chat_id, file_id, caption=caption)
        except Exception as e:
            logger.error(f"Error sending video via userbot: {e}")
            raise

    async def copy_message(self, chat_id: int, from_chat_id: int, message_id: int):
        """Copy message via userbot."""
        if not self.has_session or not self.client:
            raise RuntimeError("Userbot not available")
        
        try:
            await self.client.copy_message(chat_id, from_chat_id, message_id)
        except Exception as e:
            logger.error(f"Error copying message via userbot: {e}")
            raise

    async def close(self):
        """Close userbot connection."""
        if self.client:
            try:
                await self.client.disconnect()
                logger.info("Userbot disconnected")
            except Exception as e:
                logger.error(f"Error closing userbot: {e}")
