from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions


async def get_unsubscribed_required_channels(
    bot: Bot, user_id: int, conn: Connection
) -> list[dict]:
    channel_actions = ChannelActions(conn)
    channels = await channel_actions.get_all_channels()
    required_channels = [ch for ch in channels if ch[-2] == "yes"]
    unsubscribed_channels = []
    for ch in required_channels:
        try:
            member = await bot.get_chat_member(chat_id=ch[1], user_id=user_id)
            if member.status in ("left", "kicked"):
                unsubscribed_channels.append(ch)
        except TelegramAPIError:
            unsubscribed_channels.append(ch)

    return unsubscribed_channels