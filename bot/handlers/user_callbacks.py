from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.movie_repo import MovieRepository
from db.repositories.stats_repo import StatsRepository
from db import models
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data.startswith("rate:"))
async def handle_rate(call: CallbackQuery, session: AsyncSession | None = None, user: models.User | None = None):
    data = call.data  # rate:{movie_id}:{value}
    try:
        _, movie_id_str, value_str = data.split(":")
        movie_id = int(movie_id_str)
        value = int(value_str)
    except Exception:
        await call.answer("Noma'lum format", show_alert=True)
        return

    if session is None or user is None:
        await call.answer("Xatolik: sessiya yoki foydalanuvchi topilmadi", show_alert=True)
        return

    movie_repo = MovieRepository(session)

    # Check existing rating
    from sqlalchemy import select
    stmt = select(models.Rating).where(models.Rating.user_id == user.id, models.Rating.movie_id == movie_id)
    result = await session.execute(stmt)
    existing = result.scalars().first()

    if existing:
        existing.value = value
    else:
        rating = models.Rating(user_id=user.id, movie_id=movie_id, value=value)
        session.add(rating)

    # Update aggregate
    await movie_repo.update_rating(movie_id)
    await session.commit()

    await call.answer(f"Rahmat! Siz bu filmga {value} yulduz berdingiz.")


@router.callback_query(F.data == "top_movies")
async def handle_top_movies(call: CallbackQuery, session: AsyncSession | None = None):
    if session is None:
        await call.answer("Xatolik: sessiya topilmadi", show_alert=True)
        return
    stats = StatsRepository(session)
    top = await stats.get_top_movies(limit=10)
    if not top:
        await call.answer("Top kinolar topilmadi", show_alert=True)
        return
    lines = [f"{i+1}. {t[0]} — {t[1]} ko'rish — Reyting: {t[2] or 0:.1f}" for i, t in enumerate(top)]
    await call.message.answer("\n".join(lines))
    await call.answer()


@router.callback_query(F.data == "random")
async def handle_random(call: CallbackQuery, session: AsyncSession | None = None):
    if session is None:
        await call.answer("Xatolik: sessiya topilmadi", show_alert=True)
        return
    movie_repo = MovieRepository(session)
    objs = await movie_repo.get_random(limit=3)
    if not objs:
        await call.answer("Hech narsa topilmadi", show_alert=True)
        return
    lines = [f"{m.title} ({m.year}) — /code_{m.code}" for m in objs]
    await call.message.answer("\n".join(lines))
    await call.answer()
