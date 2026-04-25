from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from db.repositories.user_repo import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.movie_repo import MovieRepository
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession | None = None):
    """Handle /start command."""
    if session is None:
        await message.answer("Xatolik: ma'lumotlar bazasi aloqasi mavjud emas.")
        return

    user_repo = UserRepository(session)
    # Create or update user
    db_user = await user_repo.get_or_create(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        lang=message.from_user.language_code or "uz"
    )
    await session.commit()

    text = (
        "Salom! Kinobotga xush kelibsiz.\n"
        "Filmlar va seriallarni qidirish uchun nom yoki kod yuboring."
    )
    await message.answer(text)


@router.message()
async def handle_text(message: Message, session: AsyncSession | None = None):
    """Handle plain text as search query."""
    if not message.text:
        return
    query = message.text.strip()

    movie_repo = MovieRepository(session)
    results = await movie_repo.search(query, limit=8)

    if not results:
        await message.reply("Hech narsa topilmadi 😕")
        return

    # Send simple list of titles
    text_lines = [f"{m.title} ({m.year}) — /code_{m.code}" for m in results]
    await message.answer("\n".join(text_lines))


@router.message(F.text.startswith("/code_"))
async def handle_code_command(message: Message, session: AsyncSession | None = None):
    code = message.text.replace("/code_", "", 1)
    movie_repo = MovieRepository(session)
    movie = await movie_repo.get_by_code(code)
    if not movie:
        await message.reply("Kod topilmadi")
        return

    caption = f"<b>{movie.title}</b> ({movie.year})\n\n{movie.description or ''}\n\nReyting: {movie.rating_avg or 0} ({movie.rating_count})"
    # Try to send via file_id
    try:
        await message.answer_video(video=movie.video_file_id, caption=caption)
    except Exception as e:
        logger.error(f"Error sending video for movie {movie.id}: {e}")
        await message.reply("Kechirasiz, videoni yuborishda xato yuz berdi.")
