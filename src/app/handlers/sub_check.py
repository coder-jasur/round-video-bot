import asyncpg
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.filters.check_sub_channel import CheckSubChannel
from src.app.keyboards.inline.subscription import else_create_channels_keyboard, create_channels_keyboard
from src.app.services.subscription import get_unsubscribed_required_channels


check_sub_channel_router = Router()
check_sub_channel_router.message.filter(CheckSubChannel())
check_sub_channel_router.callback_query.filter(CheckSubChannel())


@check_sub_channel_router.message(F.text)
async def handle_user_message(message: Message, bot: Bot, conn: Connection):
    unsubscribed = await get_unsubscribed_required_channels(
        bot, message.from_user.id, conn
    )

    if unsubscribed:
        keyboard = await create_channels_keyboard(unsubscribed, conn)
        await message.answer(
            "Bot butunlay bepul. Undan foydalanish uchun ushbu kanallarga obuna bo'ling", reply_markup=keyboard
        )
    else:
        await message.edit_text("✅ Siz barcha kanallarga obuna bo'ldingiz. Rahmat!")


@check_sub_channel_router.callback_query(F.data == "check_subs")
async def check_subs_callback(call: CallbackQuery, bot: Bot, conn: Connection):
    unsubscribed = await get_unsubscribed_required_channels(
        bot, call.from_user.id, conn
    )
    print(unsubscribed)
    if not unsubscribed:
        await call.message.edit_text("✅ Siz barcha kanallarga obuna bo'ldingiz. Rahmat!")
    else:
        keyboard = await else_create_channels_keyboard(unsubscribed)
        await call.message.edit_text(
            "Bot butunlay bepul. Undan foydalanish uchun ushbu kanallarga obuna bo'ling", reply_markup=keyboard
        )


@check_sub_channel_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_subscribed_to_channel(chat_member: ChatMemberUpdated, bot: Bot, pool: asyncpg.Pool):
    user_id = chat_member.from_user.id
    channel_id = chat_member.chat.id
    async with pool.acquire() as conn_:
        conn = conn_
        channel_actions = ChannelActions(conn)
        channel_message = await channel_actions.get_channel(channel_id)
        channel_message = channel_message[4]

        unsubscribed = await get_unsubscribed_required_channels(
            bot, chat_member.from_user.id, conn
        )
    if not unsubscribed:
        text = (
            str(channel_message)
            if channel_message
            else "✅ Siz barcha kanallarga obuna bo‘ldingiz. Endi botdan foydalanishingiz mumkin."
        )
        await bot.edit_message_text(chat_id=user_id, text=text)