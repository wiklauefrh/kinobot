"""Integration test for KINOBOT services."""

import pytest
from db.repositories.user_repo import UserRepository
from db.repositories.movie_repo import MovieRepository
from db.models import User, Movie
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_user_creation(test_db: AsyncSession):
    """Test user creation."""
    repo = UserRepository(test_db)
    
    user = await repo.create(
        user_id=123456789,
        username="testuser",
        first_name="Test",
        lang="uz"
    )
    await test_db.commit()
    
    assert user.id == 123456789
    assert user.username == "testuser"
    assert user.lang == "uz"
    
    # Verify retrieval
    fetched = await repo.get_by_id(123456789)
    assert fetched is not None
    assert fetched.username == "testuser"


@pytest.mark.asyncio
async def test_user_get_or_create(test_db: AsyncSession):
    """Test user get_or_create."""
    repo = UserRepository(test_db)
    
    # Create new
    user1 = await repo.get_or_create(123, username="user1")
    await test_db.commit()
    assert user1.id == 123
    
    # Get existing
    user2 = await repo.get_or_create(123, username="user2")
    await test_db.commit()
    assert user2.id == 123
    assert user2.username == "user1"  # Should keep original username


@pytest.mark.asyncio
async def test_movie_creation(test_db: AsyncSession):
    """Test movie creation."""
    repo = MovieRepository(test_db)
    
    movie = await repo.create(
        code="avatar2",
        title="Avatar: The Way of Water",
        video_file_id="AgACAgI...",
        year=2022,
        genres=["sci-fi", "adventure"]
    )
    await test_db.commit()
    
    assert movie.code == "avatar2"
    assert movie.title == "Avatar: The Way of Water"
    assert movie.year == 2022
    assert "sci-fi" in movie.genres


@pytest.mark.asyncio
async def test_movie_search(test_db: AsyncSession):
    """Test movie search."""
    repo = MovieRepository(test_db)
    
    # Create test movies
    await repo.create(
        code="avatar1",
        title="Avatar",
        video_file_id="file1",
        year=2009,
        genres=["sci-fi"]
    )
    await repo.create(
        code="avatar2",
        title="Avatar 2",
        video_file_id="file2",
        year=2022,
        genres=["sci-fi"]
    )
    await test_db.commit()
    
    # Search
    results = await repo.search("Avatar")
    assert len(results) >= 2


@pytest.mark.asyncio
async def test_movie_by_code(test_db: AsyncSession):
    """Test get movie by code."""
    repo = MovieRepository(test_db)
    
    await repo.create(
        code="test123",
        title="Test Movie",
        video_file_id="file_id",
        year=2023
    )
    await test_db.commit()
    
    movie = await repo.get_by_code("test123")
    assert movie is not None
    assert movie.title == "Test Movie"
    
    not_found = await repo.get_by_code("nonexistent")
    assert not_found is None
