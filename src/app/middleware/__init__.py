from aiogram import Dispatcher
from asyncpg import Pool

from src.app.core.config import Settings
from src.app.middleware.conn import ConnectionMiddleware
from src.app.middleware.settings import SettingsMiddleware


def register_middlewares(dp: Dispatcher, _settings: Settings, pool: Pool) -> None:
    settings_ = SettingsMiddleware(_settings)
    dp.message.outer_middleware(settings_)
    dp.callback_query.outer_middleware(settings_)

    connection = ConnectionMiddleware(pool)
    dp.message.outer_middleware(connection)
    dp.callback_query.outer_middleware(connection)
