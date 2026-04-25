"""Test fixtures and utilities for KINOBOT testing."""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from db.base import Base
from config import settings
from aiogram import Bot
from aiogram.types import User as TgUser, Chat, Message as TgMessage
from datetime import datetime


# Test database
@pytest.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        yield session
    
    await engine.dispose()


# Mock Telegram user
@pytest.fixture
def mock_tg_user():
    """Create mock Telegram user."""
    return TgUser(
        id=123456789,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser",
        language_code="uz",
    )


# Mock Telegram message
@pytest.fixture
def mock_tg_message(mock_tg_user):
    """Create mock Telegram message."""
    chat = Chat(id=123456789, type="private")
    message = TgMessage(
        message_id=1,
        date=datetime.utcnow(),
        chat=chat,
        from_user=mock_tg_user,
        text="test message",
    )
    return message


# Pytest async mode
pytest_plugins = ('pytest_asyncio',)
