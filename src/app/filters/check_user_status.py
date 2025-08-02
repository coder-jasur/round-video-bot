from aiogram import Bot
from aiogram.filters import (
    Filter,
)
from aiogram.types import (
    Message, CallbackQuery,
)
from asyncpg import Connection

from src.app.database.queries.users import UserActions


class CheckUserStatus(Filter):
    async def __call__(self, message: Message, bot: Bot, conn: Connection):
        user_actions = UserActions(conn)
        user = await user_actions.get_user(message.from_user.id)

        if user and user[2] == "blocked":
            await message.answer(
                "🚫 siz adminlar tomonidan bloklangan siz\n\n"
                "📮 Taklif yoki savollaringiz bo‘lsa, biz doimo aloqadamiz:\n"
                "<a href='https://www.instagram.com/hikmatilloyev__/'>Instagram  hikmatilloyev__</a>\n"
                "<a href='https://t.me/hikmatilloyev_j'>Telegram  hikmatilloyev_j</a>",
                parse_mode="HTML"

            )
            return False

        return True


class CheckUserStatusCallback(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot, conn: Connection):
        user_actions = UserActions(conn)
        user = await user_actions.get_user(call.from_user.id)
        if user and user[2] == "blocked":
            await call.message.answer(
                "🚫 siz adminlar tomonidan bloklangan siz\n\n"
                "📮 Taklif yoki savollaringiz bo‘lsa, biz doimo aloqadamiz:\n"
                "<a href='https://www.instagram.com/hikmatilloyev__/'>Instagram  hikmatilloyev__</a>\n"
                "<a href='https://t.me/hikmatilloyev_j'>Telegram  hikmatilloyev_j</a>",
                parse_mode="HTML"

            )
            return False

        return True




