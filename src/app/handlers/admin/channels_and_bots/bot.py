from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asyncpg import Connection

from src.app.common.channel_and_bot_info_txt import bot_text
from src.app.database.queries.bots import BotActions
from src.app.keyboards.inline.callback_data import BotCD
from src.app.keyboards.inline.inline_keyboards import bot_menu, delite_bot_menu, back_to_admin_menu
from src.app.states.admin.bot import AddBotSG

bot_router = Router()


@bot_router.callback_query(F.data == "add_bot")
async def add_bots(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddBotSG.get_bot_name)
    await call.message.edit_text("botni nomini yuboring")


@bot_router.message(AddBotSG.get_bot_name)
async def add_bot_for_db(message: Message, state: FSMContext):
    await state.update_data({"bot_name": message.text})
    await state.set_state(AddBotSG.get_bot_nickname)
    await message.answer("botni usernamini yuboring")


@bot_router.message(AddBotSG.get_bot_nickname)
async def get_username_bot(message: Message, conn: Connection, state: FSMContext):
    bot_action = BotActions(conn)
    data = await state.get_data()
    try:
        await bot_action.add_bot(data["bot_name"], message.text)
        await message.answer("✅ bot muvafaqiyatli qo'shildi", reply_markup=back_to_admin_menu)
    except Exception as e:
        print(e)
        await message.answer("❗ xatolik yuz berdi qaytatdan urinib ko'ring", reply_markup=back_to_admin_menu)
    finally:
        await state.clear()


@bot_router.callback_query(BotCD.filter())
async def bot_actions(call: CallbackQuery, callback_data: BotCD, conn: Connection, state: FSMContext):
    bot_action = BotActions(conn)
    bot = await bot_action.get_bot(callback_data.username)
    if callback_data.action == "bot_modified":
        await call.message.edit_text(
            text=bot_text(bot[0], callback_data.username, bot[2]),
            parse_mode="HTML",
            reply_markup=bot_menu(callback_data.username, bot[2])
        )
    elif callback_data.action == "forced_cancellation_of_subscription":
        await bot_action.update_bot_status("majburiy obuna siz", callback_data.username)
        bot = await bot_action.get_bot(callback_data.username)
        await call.message.edit_text(
            text=bot_text(bot[0], callback_data.username, bot[2]),
            parse_mode="HTML",
            reply_markup=bot_menu(callback_data.username, bot[2])
        )
    elif callback_data.action == "add_to_mandatory_subscription":
        await bot_action.update_bot_status("majburiy obuna", callback_data.username)
        bot = await bot_action.get_bot(callback_data.username)
        await call.message.edit_text(
            text=bot_text(bot[0], callback_data.username, bot[2]),
            parse_mode="HTML",
            reply_markup=bot_menu(callback_data.username, bot[2])
        )

    elif callback_data.action == "delete_bot":
        await call.message.edit_text(
            f"🤔 Siz {callback_data.username} botini ochirishga amin misiz",
            reply_markup=delite_bot_menu(callback_data.username)
        )


    elif callback_data.action == "not_sure":
        bot = await bot_action.get_bot(callback_data.username)
        await call.message.edit_text(
            text=bot_text(bot[0], callback_data.username, bot[2]),
            parse_mode="HTML",
            reply_markup=bot_menu(callback_data.username, bot[2])
        )
    elif callback_data.action == "sure":
        try:
            await bot_action.delete_bot(callback_data.username)
            await call.message.edit_text("✅ bot muvfaqiyatli o'chirildi", reply_markup=back_to_admin_menu)
            await state.clear()
        except Exception as e:
            await call.message.edit_text(
                f"❗ xatolik yuzberdi qaytadan urinib ko'ring {e}",
                reply_markup=back_to_admin_menu
            )
