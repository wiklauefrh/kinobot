from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import models
from typing import Optional


class SettingsRepository:
    """Repository for Settings operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, key: str) -> Optional[str]:
        """Get a setting value."""
        stmt = select(models.Setting).where(models.Setting.key == key)
        result = await self.session.execute(stmt)
        setting = result.scalars().first()
        return setting.value if setting else None

    async def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a setting value as boolean."""
        value = await self.get(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    async def get_int(self, key: str, default: int = 0) -> int:
        """Get a setting value as integer."""
        value = await self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    async def get_float(self, key: str, default: float = 0.0) -> float:
        """Get a setting value as float."""
        value = await self.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    async def set(self, key: str, value: str) -> models.Setting:
        """Set a setting value."""
        stmt = select(models.Setting).where(models.Setting.key == key)
        result = await self.session.execute(stmt)
        setting = result.scalars().first()
        
        if setting:
            setting.value = str(value)
        else:
            setting = models.Setting(key=key, value=str(value))
            self.session.add(setting)
        
        await self.session.flush()
        return setting

    async def get_all(self) -> dict:
        """Get all settings as dict."""
        stmt = select(models.Setting)
        result = await self.session.execute(stmt)
        settings = result.scalars().all()
        return {s.key: s.value for s in settings}

    async def delete(self, key: str) -> bool:
        """Delete a setting."""
        stmt = select(models.Setting).where(models.Setting.key == key)
        result = await self.session.execute(stmt)
        setting = result.scalars().first()
        
        if setting:
            await self.session.delete(setting)
            await self.session.flush()
            return True
        return False
