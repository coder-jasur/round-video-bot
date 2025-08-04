from aiogram import Bot
from aiogram.filters import (
    Filter,
)
from aiogram.types import (
    Message,
)
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions


class CheckSubChannel(Filter):
    async def __call__(self, message: Message, bot: Bot, conn: Connection):
        channel_actions = ChannelActions(conn)
        channels = await channel_actions.get_all_channels()
        for channel in channels:
            if channel[3] == "majburiy obuna":
                user_status = await bot.get_chat_member(channel[0], message.from_user.id)
                if user_status.status in ["member", "administrator", "creator"]:
                    return False
            else:
                return True
