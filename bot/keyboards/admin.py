from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def broadcast_controls(broadcast_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Boshlash", callback_data=f"bc_start:{broadcast_id}"))
    kb.add(InlineKeyboardButton(text="To'xtatish", callback_data=f"bc_pause:{broadcast_id}"))
    kb.add(InlineKeyboardButton(text="Davom ettirish", callback_data=f"bc_resume:{broadcast_id}"))
    kb.add(InlineKeyboardButton(text="Bekor qilish", callback_data=f"bc_cancel:{broadcast_id}"))
    return kb


def admin_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Kontent qo'shish", callback_data="admin_add_content"))
    kb.add(InlineKeyboardButton(text="Broadcast yaratish", callback_data="admin_create_broadcast"))
    kb.add(InlineKeyboardButton(text="Statistika", callback_data="admin_stats"))
    return kb
