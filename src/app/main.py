import asyncio
import logging
import os

import asyncpg
from aiogram import Dispatcher, Bot


from common.bot_commands import bot_commands_c
from common.get_db_url import construct_postgresql_url
from core.config import Settings
from database.tables import create_database_tables
from handlers import registrar_routers
from middleware import register_middlewares

logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")



async def main():
    settings = Settings()

    dsn = construct_postgresql_url(settings)

    pool = await asyncpg.create_pool(
        dsn,
    )

    async with pool.acquire() as conn:
        await create_database_tables(conn)


    bot = Bot(token=settings.bot_token)
    await bot_commands_c(bot, settings)

    dp = Dispatcher()
    register_middlewares(dp, settings, pool)
    registrar_routers(dp, settings.admins_ids)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        os.makedirs("videos", exist_ok=True)
        asyncio.run(main())
    except Exception as e:
        logger.exception(e)
