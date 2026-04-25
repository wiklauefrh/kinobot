import asyncio
import logging
from config import settings
from utils.logging import setup_logging
from db.init_db import setup_database
from bot.loader import setup_dispatcher, bot, router
from bot.middlewares.db import DBMiddleware
from bot.middlewares.user import UserTrackingMiddleware
from bot.middlewares.subscription import SubscriptionMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware

from bot.handlers import user as user_handlers
from bot.handlers import admin as admin_handlers
from bot.handlers import user_callbacks
from bot.handlers import fsm_handlers

logger = setup_logging()


async def main():
    logger.info("Starting KINOBOT")

    # Init DB
    await setup_database()

    # Setup dispatcher
    dp = await setup_dispatcher()

    # Register middlewares
    dp.update.middleware(DBMiddleware())
    dp.update.middleware(UserTrackingMiddleware())
    dp.update.middleware(SubscriptionMiddleware())
    dp.update.middleware(ThrottlingMiddleware())

    # Include routers
    dp.include_router(user_handlers.router)
    dp.include_router(user_callbacks.router)
    dp.include_router(fsm_handlers.router)
    dp.include_router(admin_handlers.router)

    # Start polling
    try:
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
