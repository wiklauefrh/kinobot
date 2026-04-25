from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime
from db import models
from typing import Optional, List


class ChannelRepository:
    """Repository for Channel operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tg_chat_id: int, title: str, channel_type: str = "public",
                     invite_link: Optional[str] = None, is_required: bool = False) -> models.Channel:
        """Create a new channel."""
        channel = models.Channel(
            tg_chat_id=tg_chat_id,
            title=title,
            type=channel_type,
            invite_link=invite_link,
            is_required=is_required
        )
        self.session.add(channel)
        await self.session.flush()
        return channel

    async def get_by_id(self, channel_id: int) -> Optional[models.Channel]:
        """Get channel by ID."""
        stmt = select(models.Channel).where(models.Channel.id == channel_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_tg_chat_id(self, tg_chat_id: int) -> Optional[models.Channel]:
        """Get channel by Telegram chat ID."""
        stmt = select(models.Channel).where(models.Channel.tg_chat_id == tg_chat_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_required_channels(self) -> List[models.Channel]:
        """Get all required subscription channels."""
        stmt = select(models.Channel).where(models.Channel.is_required == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all(self) -> List[models.Channel]:
        """Get all channels."""
        stmt = select(models.Channel).order_by(models.Channel.created_at)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_members_count(self, channel_id: int, count: int) -> Optional[models.Channel]:
        """Update channel members count."""
        channel = await self.get_by_id(channel_id)
        if channel:
            channel.members_count = count
            channel.updated_at = datetime.utcnow()
            await self.session.flush()
        return channel

    async def add_join_request(self, user_id: int, channel_id: int) -> models.ChannelJoinRequest:
        """Add a join request."""
        req = models.ChannelJoinRequest(user_id=user_id, channel_id=channel_id)
        self.session.add(req)
        await self.session.flush()
        return req

    async def approve_join_request(self, user_id: int, channel_id: int) -> Optional[models.ChannelJoinRequest]:
        """Approve a join request."""
        stmt = select(models.ChannelJoinRequest).where(
            models.ChannelJoinRequest.user_id == user_id,
            models.ChannelJoinRequest.channel_id == channel_id
        )
        result = await self.session.execute(stmt)
        req = result.scalars().first()
        if req:
            req.approved = True
            await self.session.flush()
        return req

    async def get_join_request(self, user_id: int, channel_id: int) -> Optional[models.ChannelJoinRequest]:
        """Get join request."""
        stmt = select(models.ChannelJoinRequest).where(
            models.ChannelJoinRequest.user_id == user_id,
            models.ChannelJoinRequest.channel_id == channel_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def is_join_request_approved(self, user_id: int, channel_id: int) -> bool:
        """Check if join request is approved."""
        req = await self.get_join_request(user_id, channel_id)
        return req.approved if req else False

    async def add_referral(self, user_id: int, channel_id: int) -> models.ChannelReferral:
        """Add channel referral."""
        referral = models.ChannelReferral(user_id=user_id, channel_id=channel_id)
        self.session.add(referral)
        await self.session.flush()
        return referral

    async def get_channel_referrals(self, channel_id: int, limit: int = 100) -> List[models.ChannelReferral]:
        """Get recent referrals for a channel."""
        stmt = select(models.ChannelReferral).where(
            models.ChannelReferral.channel_id == channel_id
        ).order_by(desc(models.ChannelReferral.joined_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_referral_count(self, channel_id: int) -> int:
        """Get referral count for a channel."""
        stmt = select(func.count(models.ChannelReferral.id)).where(
            models.ChannelReferral.channel_id == channel_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def delete(self, channel_id: int) -> bool:
        """Delete channel."""
        channel = await self.get_by_id(channel_id)
        if channel:
            await self.session.delete(channel)
            await self.session.flush()
            return True
        return False

    async def update(self, channel_id: int, **kwargs) -> Optional[models.Channel]:
        """Update channel."""
        channel = await self.get_by_id(channel_id)
        if channel:
            for key, value in kwargs.items():
                if hasattr(channel, key):
                    setattr(channel, key, value)
            channel.updated_at = datetime.utcnow()
            await self.session.flush()
        return channel
