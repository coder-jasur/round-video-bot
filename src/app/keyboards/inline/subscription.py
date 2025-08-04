from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asyncpg import Connection

from src.app.database.queries.bots import BotActions


async def else_create_channels_keyboard(channels) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ch in channels:
        if ch[3] == "majburiy obuna":
            builder.row(InlineKeyboardButton(text=ch[1], url=f"https://t.me/{ch[2]}"))

    chek_sub_button = InlineKeyboardButton(text="✅", callback_data="check_subs")

    builder.row(chek_sub_button)
    return builder.as_markup()


async def create_channels_keyboard(channels, conn: Connection) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    bot_actions = BotActions(conn)
    if channels:

        for ch in channels:
            if ch[3] == "majburiy obuna":
                builder.row(InlineKeyboardButton(text=ch[1], url=f"https://t.me/{ch[2]}"))

    bots = await bot_actions.get_all_bots()
    if bots:
        for bot in bots:
            if bot[-2] == "majburiy obuna":
                builder.row(InlineKeyboardButton(text=f"{bot[0]}", url=f"https://t.me/{bot[1][1:]}"))

    chek_sub_button = InlineKeyboardButton(text="✅", callback_data="check_subs")

    builder.row(chek_sub_button)

    return builder.as_markup()
