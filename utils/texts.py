"""Uzbek UI texts and templates."""

TEXTS = {
    "start": "Salom! Kinobotga xush kelibsiz 🎬\n\nFilmlar va seriallarni qidirish uchun nom yoki kod yuboring.",
    "not_found": "Hech narsa topilmadi 😕",
    "no_results": "Hech qanday natija topilmadi.",
    "error_db": "Xatolik: ma'lumotlar bazasi aloqasi mavjud emas.",
    "error_general": "Kechirasiz, xatolik yuz berdi.",
    "error_send_video": "Kechirasiz, videoni yuborishda xato yuz berdi.",
    "error_sub_required": "Videoni ko'rish uchun avval kanalga obuna bo'ling:",
    "rating_thanks": "Rahmat! Siz bu filmga {value} yulduz berdingiz. 👍",
    "broadcast_draft_created": "Broadcast qoralashtirindi ✓",
    "broadcast_started": "Broadcast boshlandi! 📤",
    "broadcast_paused": "Broadcast to'xtatildi ⏸",
    "broadcast_resumed": "Broadcast davom ettirildi ▶",
    "broadcast_completed": "Broadcast tugallandi ✓\n\nJami yuborilgan: {sent}\nXatolik: {failed}\nBlokirkkan: {blocked}",
    "admin_panel": "Admin paneli",
    "admin_add_content": "Kontent qo'shish",
    "admin_broadcast": "Broadcast yaratish",
    "admin_stats": "Statistika",
    "admin_channels": "Kanallarni boshqarish",
    "admin_backup": "Backup/Restore",
    "admin_settings": "Sozlamalar",
}

TEMPLATES = {
    "movie_card": "<b>{title}</b> ({year})\n\n{description}\n\n<i>Janrlar:</i> {genres}\n<i>Ko'rishlar:</i> {views}\n<i>Reyting:</i> {rating_avg:.1f}/5.0 ({rating_count} sharhlar)",
    "series_card": "<b>{title}</b> ({year})\n\n{description}\n\n<i>Janrlar:</i> {genres}\n<i>Sezonlar:</i> {season_count}",
    "stats_header": "📊 <b>Statistika</b>\n\nJami foydalanuvchilar: {total_users}\nBugun faol: {active_today}\n7 kun faol: {active_week}\n30 kun faol: {active_month}",
    "stats_content": "\n<i>Kino:</i> {movie_count}\n<i>Serial:</i> {series_count}\n<i>Ban qilingan:</i> {banned_count}\n<i>Bloklab qo'ygan:</i> {blocked_count}",
    "broadcast_preview": "<b>Broadcast ko'rikni</b>\n\n{text}\n\nJamiyatga: {target_count} foydalanuvchi",
}


def get_text(key: str, **kwargs) -> str:
    """Get text by key with optional formatting."""
    text = TEXTS.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text


def get_template(key: str, **kwargs) -> str:
    """Get template by key with formatting."""
    template = TEMPLATES.get(key, key)
    return template.format(**kwargs)
