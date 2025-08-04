from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from asyncpg import Connection

from src.app.database.queries.bots import BotActions
from src.app.database.queries.channels import ChannelActions



async def get_unsubscribed_required_channels(bot: Bot, user_id: int , conn: Connection) -> list[dict]:
    channel_actions = ChannelActions(conn)
    channels = await channel_actions.get_all_channels()

    bot_actions = BotActions(conn)
    bots = await bot_actions.get_all_bots()
    unsubscribed_channels = []
    check = []

    for bot_ in bots:
        if bot_[2] == "majburiy obuna":
            check.append("bot")
            unsubscribed_channels.append(bot_)


    for channel in channels:
        member = await bot.get_chat_member(chat_id=channel[0], user_id=user_id)
        if channel[3] == "majburiy obuna":
            if member.status in ("left", "kicked"):
                check.append("channel")
                unsubscribed_channels.append(channel)
    if "bot" in check and "channel" in check or "channel" in check:
        return unsubscribed_channels

