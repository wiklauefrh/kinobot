"""FSM handlers for stateful conversations."""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.movie_repo import MovieRepository
from db.repositories.admin_repo import AdminRepository
from db.constants import AdminRole
from bot.states import AddMovieSG
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "Kino qo'shish")
async def start_add_movie(message: Message, state: FSMContext, session: AsyncSession | None = None):
    """Start adding a movie."""
    if session is None:
        await message.reply("Xatolik: sessiya topilmadi")
        return

    # Check permissions
    admin_repo = AdminRepository(session)
    is_content_mgr = await admin_repo.has_permission(message.from_user.id, "manage_content")
    
    if not is_content_mgr:
        await message.reply("Sizda bu amalni bajarish ruxsati yo'q.")
        return

    await message.reply("Kino nomini kiriting:")
    await state.set_state(AddMovieSG.title)


@router.message(AddMovieSG.title)
async def process_title(message: Message, state: FSMContext):
    """Process movie title."""
    await state.update_data(title=message.text)
    await message.reply("Kino kodini kiriting (masalan: avatar2):")
    await state.set_state(AddMovieSG.code)


@router.message(AddMovieSG.code)
async def process_code(message: Message, state: FSMContext, session: AsyncSession | None = None):
    """Process movie code."""
    code = message.text.lower().strip()
    
    if session:
        movie_repo = MovieRepository(session)
        existing = await movie_repo.get_by_code(code)
        if existing:
            await message.reply(f"Kod '{code}' allaqachon mavjud. Boshqa kod kiriting:")
            return

    await state.update_data(code=code)
    await message.reply("Janrlarni kiriting (vergul bilan ajratib):")
    await state.set_state(AddMovieSG.genres)


@router.message(AddMovieSG.genres)
async def process_genres(message: Message, state: FSMContext):
    """Process genres."""
    genres = [g.strip() for g in message.text.split(",")]
    await state.update_data(genres=genres)
    await message.reply("Yilni kiriting:")
    await state.set_state(AddMovieSG.year)


@router.message(AddMovieSG.year)
async def process_year(message: Message, state: FSMContext):
    """Process year."""
    try:
        year = int(message.text)
        await state.update_data(year=year)
        await message.reply("Videofileni yuklang:")
        await state.set_state(AddMovieSG.video)
    except ValueError:
        await message.reply("Yil raqam bo'lishi kerak:")


@router.message(AddMovieSG.video)
async def process_video(message: Message, state: FSMContext, session: AsyncSession | None = None):
    """Process video."""
    if not message.video:
        await message.reply("Video fayl yuklang:")
        return

    data = await state.get_data()
    
    if session:
        movie_repo = MovieRepository(session)
        movie = await movie_repo.create(
            code=data["code"],
            title=data["title"],
            video_file_id=message.video.file_id,
            genres=data.get("genres"),
            year=data.get("year"),
        )
        await session.commit()
        
        await message.reply(
            f"✓ Kino qo'shildi!\n\n"
            f"Nomi: {movie.title}\n"
            f"Kodi: {movie.code}\n"
            f"Yili: {movie.year}"
        )
    
    await state.clear()
