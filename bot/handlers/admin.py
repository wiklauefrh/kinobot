from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.admin_repo import AdminRepository
from db.repositories.stats_repo import StatsRepository
from services.stats import StatsService
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("admin"))
async def cmd_admin(message: Message, session: AsyncSession | None = None):
    """Admin menu entry point."""
    if session is None:
        await message.reply("Xatolik: sessiya topilmadi")
        return

    admin_repo = AdminRepository(session)
    is_admin = await admin_repo.is_admin(message.from_user.id)

    if not is_admin:
        await message.reply("Siz admin emassiz.")
        return

    role = await admin_repo.get_role(message.from_user.id)
    
    text = (
        "👨‍💼 Admin paneli\n\n"
        f"Rolingiz: {role}\n\n"
        "Mavjud amallar:\n"
        "- Kino qo'shish\n"
        "- Broadcast yaratish\n"
        "- Statistika ko'rish"
    )
    await message.reply(text)


@router.message(F.text == "Statistika")
async def handle_stats(message: Message, session: AsyncSession | None = None):
    """Show statistics."""
    if session is None:
        await message.reply("Xatolik: sessiya topilmadi")
        return

    admin_repo = AdminRepository(session)
    is_admin = await admin_repo.is_admin(message.from_user.id)
    
    if not is_admin:
        await message.reply("Ruxsati yo'q")
        return

    try:
        stats_service = StatsService(session)
        dashboard = await stats_service.get_dashboard_stats()

        text = (
            "📊 <b>Statistika</b>\n\n"
            f"Jami foydalanuvchilar: {dashboard['total_users']}\n"
            f"Bugun faol: {dashboard['active_today']}\n"
            f"7-kunlik faol: {dashboard['active_week']}\n"
            f"30-kunlik faol: {dashboard['active_month']}\n\n"
            f"Kinolar: {dashboard['movies']}\n"
            f"Seriallar: {dashboard['series']}\n\n"
            f"Ban qilingan: {dashboard['banned']}\n"
            f"Bloklab qo'ygan: {dashboard['blocked']}\n"
            f"Premium: {dashboard['premium']}"
        )
        
        await message.reply(text)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await message.reply("Xatolik: statistika olishda muammo")
