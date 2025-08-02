from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asyncpg import Connection

from src.app.common.channel_and_bot_info_txt import user_status_text
from src.app.database.queries.users import UserActions
from src.app.keyboards.inline.callback_data import UserStatusCD
from src.app.keyboards.inline.inline_keyboards import user_status_actions, back_to_admin_menu_keyboards
from src.app.states.admin.user_status import UserStatus

block_un_block_router = Router()


@block_un_block_router.callback_query(F.data == "blocked_unblocked")
async def blovk_and_un_block_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(UserStatus.get_user_id)
    await call.message.edit_text("Foydalanuvchini ID sini yuboring")


@block_un_block_router.message(UserStatus.get_user_id)
async def block_and_un_block_user(message: Message, state: FSMContext, conn: Connection):
    if message.text.isdigit():
        user_actions = UserActions(conn)
        usera_data = await user_actions.get_user(int(message.text))
        if usera_data:
            text = user_status_text(usera_data[0], usera_data[1], usera_data[2])
            await message.answer(
                text,
                reply_markup=user_status_actions(usera_data[2], usera_data[0]), parse_mode="HTML"
            )
            await state.clear()
            return True
    elif not message.text.isdigit():
        await message.answer("raqamli ID yuboring", reply_markup=back_to_admin_menu_keyboards)
        await state.clear()
        return False

    if not usera_data:
        await message.answer(
            "bunaqa foydalanuvchi mavjud emas qaytatdan urinib ko'ring",
            reply_markup=back_to_admin_menu_keyboards
        )
        await state.clear()

        return False


@block_un_block_router.callback_query(UserStatusCD.filter())
async def user_status_actons(call: CallbackQuery, conn: Connection, callback_data: UserStatusCD):
    user_actions = UserActions(conn)

    if callback_data.action == "blocked_user":
        await user_actions.update_user_status("blocked", callback_data.user_id)
        usera_data = await user_actions.get_user(callback_data.user_id)
        text = user_status_text(usera_data[0], usera_data[1], usera_data[2])
        await call.message.edit_text(
            text, reply_markup=user_status_actions(usera_data[2], usera_data[0]), parse_mode="HTML"
        )
    elif callback_data.action == "unblocked_user":
        await user_actions.update_user_status("unblocked", callback_data.user_id)
        usera_data = await user_actions.get_user(callback_data.user_id)
        text = user_status_text(usera_data[0], usera_data[1], usera_data[2])
        await call.message.edit_text(
            text, reply_markup=user_status_actions(usera_data[2], usera_data[0]),
            parse_mode="HTML"
        )
