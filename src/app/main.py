import asyncio
import logging
import os

import asyncpg
from aiogram import Dispatcher, Bot

from logs.file.logger_conf import setup_logging
from src.app.common.bot_commands import bot_commands
from src.app.common.get_db_url import construct_postgresql_url
from src.app.core.config import Settings
from src.app.database.tables import create_database_tables
from src.app.handlers import registrar_routers
from src.app.middleware import register_middlewares

logger = logging.getLogger(__name__)



async def main():
    settings = Settings()

    dsn = construct_postgresql_url(settings)

    pool = await asyncpg.create_pool(
        dsn,
    )

    async with pool.acquire() as conn:
        await create_database_tables(conn)

    dp = Dispatcher()
    register_middlewares(dp, settings, pool)
    registrar_routers(dp, settings.admins_ids)



    bot = Bot(token=settings.bot_token)

    await bot_commands(bot, settings)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        setup_logging("logs/logger.yml")
        os.makedirs("videos", exist_ok=True)
        asyncio.run(main())
    except Exception as e:
        logger.exception(e)
