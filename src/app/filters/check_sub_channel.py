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
        op_channels = []
        for channel in channels:
            if channel[3] == "majburiy obuna":
                op_channels.append(channel)

        member = []

        for op_channel in op_channels:
            user_status = await bot.get_chat_member(op_channel[0], message.from_user.id)
            print(user_status.status)
            if user_status.status == "left":
                member.append("False")
            else:
                member.append("True")

        print(member)
        if "False" in member:
            return True
        else:
            return False
