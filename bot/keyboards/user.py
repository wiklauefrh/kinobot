from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def rating_keyboard(movie_id: int) -> InlineKeyboardMarkup:
    """Return inline keyboard for rating 1-5."""
    kb = InlineKeyboardMarkup(row_width=5)
    buttons = [InlineKeyboardButton(text=str(i), callback_data=f"rate:{movie_id}:{i}") for i in range(1, 6)]
    kb.add(*buttons)
    return kb


def simple_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Top kinolar", callback_data="top_movies"))
    kb.add(InlineKeyboardButton(text="Tasodifiy", callback_data="random"))
    return kb
