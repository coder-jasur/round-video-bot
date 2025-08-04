from aiogram import Bot
from aiogram.filters import (
    Filter,
)
from aiogram.types import (
    Message,
)
from asyncpg import Connection

from src.app.services.subscription import get_unsubscribed_required_channels


class CheckSubChannel(Filter):
    async def __call__(self, message: Message, bot: Bot, conn: Connection):
        unsubscribed_channels = await get_unsubscribed_required_channels(
            bot, message.from_user.id, conn
        )

        return bool(unsubscribed_channels)
