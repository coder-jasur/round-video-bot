from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from asyncpg import Connection

from src.app.database.queries.users import UserActions
from src.app.handlers.admin.channels_and_bots.channel import get_channels_menu
from src.app.keyboards.inline.inline_keyboards import (
    admin_menu_keyboards, back_to_admin_menu_keyboards
)

admin_commands_router = Router()


@admin_commands_router.message(Command("admin_menu"))
async def get_admin_menu(message: Message):
    await message.answer(
        "📋 <b>Admin menyu:</b>\n\n"
        "Pastdagilardan kerakli bo‘limni tanlang.",
        reply_markup=admin_menu_keyboards,
        parse_mode="HTML"
    )


@admin_commands_router.callback_query(F.data == "back_to_channels_menu")
async def back_to_admin_menu(call: CallbackQuery, conn: Connection):
    await get_channels_menu(call, conn)


@admin_commands_router.callback_query(F.data == "back_to_admin_menu")
async def back_to_admin_menu(call: CallbackQuery):
    await call.message.edit_text(
        "📋 <b>Admin menyu:</b>\n\n"
        "Pastdagilardan kerakli bo‘limni tanlang.",
        reply_markup=admin_menu_keyboards,
        parse_mode="HTML"
    )


@admin_commands_router.callback_query(F.data == "memebers_count")
async def get_users_count(call: CallbackQuery, conn: Connection):
    user_actions = UserActions(conn)
    users = await user_actions.get_all_user()
    await call.message.edit_text(
        f"👥 <b>foydalanuvchilar soni</b>: {len(users)}",
        reply_markup=back_to_admin_menu_keyboards,
        parse_mode="HTML"
    )


@admin_commands_router.callback_query(F.data == "quit")
async def quit_for_admin_menu(call: CallbackQuery):
    await call.message.delete()
