from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asyncpg import Connection

from src.app.common.channel_and_bot_info_txt import channel_text
from src.app.database.queries.bots import BotActions
from src.app.database.queries.channels import ChannelActions
from src.app.keyboards.inline.callback_data import ChannelCD
from src.app.keyboards.inline.inline_keyboards import (
    channels_and_bots_keyboards, admin_menu_keyboards,
    channel_menu, add_channel_and_bot_keyboards, delite_channel_menu, back_to_admin_menu, back_to_channel_menu
)
from src.app.states.admin.channel import Channel, AddChannelMessage

channel_router = Router()


@channel_router.callback_query(F.data == "channel_and_bot_settings")
async def get_channels_menu(call: CallbackQuery, conn: Connection):
    channel_data = ChannelActions(conn)
    bot_data = BotActions(conn)
    bot_list = await bot_data.get_all_bots()
    channel_list = await channel_data.get_all_channels()
    if not channel_list and not bot_list:
        await call.message.edit_text(
            text="📥 Siz hali bot yoki kanal qo'shmagansiz",
            reply_markup=add_channel_and_bot_keyboards
        )
        return
    await call.message.edit_text(
        "🔗 <b>Obuna bog‘lamasi:</b>\n\n"
        "Pastdagilardan kerakli bo‘limni tanlang.",
        parse_mode="HTML",
        reply_markup=channels_and_bots_keyboards(channel_list, bot_list)
    )



@channel_router.callback_query(F.data == "add_channel")
async def get_channel_id(call: CallbackQuery, state: FSMContext):
    await state.set_state(Channel.get_channel_id)
    await call.message.edit_text("📃 kanal qo'shish uchun kanaldan bironta postni yuboring")



@channel_router.message(Channel.get_channel_id)
async def add_channel(message: Message, state: FSMContext, conn: Connection):
    try:
        channel_data = ChannelActions(conn)
        if message.forward_origin.chat.id:
            await channel_data.add_channel(
                message.forward_origin.chat.id,
                message.forward_origin.chat.full_name,
                message.forward_origin.chat.username
            )
            await message.answer("✅ kanal muvafaqiyatli qo'shildi", reply_markup=back_to_admin_menu)
    except Exception as e:
        await message.answer(
            f"❗ kanal qo'shishda xatolik yuz berdi qayta urinib ko'ring {e}", reply_markup=back_to_admin_menu)
    finally:
        await state.clear()


@channel_router.callback_query(ChannelCD.filter())
async def get_channel_info(call: CallbackQuery, callback_data: ChannelCD, conn: Connection, state: FSMContext):
    channel_action = ChannelActions(conn)
    channel = await channel_action.get_channel(callback_data.id)

    if callback_data.action == "channel_modified":
        await call.message.edit_text(
            text=channel_text(channel[0], channel[1], channel[2], channel[3]),
            parse_mode="HTML",
            reply_markup=channel_menu(channel[0], channel[3])
        )

    if callback_data.action == "forced_cancellation_of_subscription":

        await channel_action.update_channel_status("majburiy obuna siz", channel[0])
        channel = await channel_action.get_channel(callback_data.id)
        await call.message.edit_text(
            text=channel_text(channel[0], channel[1], channel[2], channel[3]),
            parse_mode="HTML",
            reply_markup=channel_menu(channel[0], channel[3])
        )
    elif callback_data.action == "add_to_mandatory_subscription":

        await channel_action.update_channel_status("majburiy obuna", channel[0])
        channel = await channel_action.get_channel(callback_data.id)
        await call.message.edit_text(
            text=channel_text(channel[0], channel[1], channel[2], channel[3]),
            parse_mode="HTML",
            reply_markup=channel_menu(channel[0], channel[3])
        )
    if callback_data.action == "delete_channel":
        await call.message.edit_text(
            f"🤔 Siz {channel[1]} kanalini o'chirishga aminmi siz",
            reply_markup=delite_channel_menu(callback_data.id)
        )

    elif callback_data.action == "not_sure":
        channel = await channel_action.get_channel(callback_data.id)
        await call.message.edit_text(
            text=channel_text(channel[0], channel[1], channel[2], channel[3]),
            reply_markup=channel_menu(channel[0], channel[3])
        )
    elif callback_data.action == "sure":
        try:
            await channel_action.delete_channel(callback_data.id)
            await call.message.edit_text("✅ kanal muvafaqiyatli ochirildi", reply_markup=back_to_admin_menu)
        except Exception as e:
            print("xatolik yuz berdi", e)


    elif callback_data.action == "add_channel_message":
        await state.set_state(AddChannelMessage.get_chanel_message)
        await state.update_data(
            {
                "channel_id": callback_data.id
            }
        )
        await call.message.edit_text("📥 kanal xabarni yuboring")


@channel_router.message(AddChannelMessage.get_chanel_message)
async def add_channel_message(message: Message, state: FSMContext, conn: Connection):
    channel_data = await state.get_data()
    try:
        channel_actions = ChannelActions(conn)
        await channel_actions.add_channel_message(channel_data["channel_id"], message.text)
        await message.answer(
            "✅ kanl xabari muvafaqiyatli qo'shildi",
            reply_markup=back_to_channel_menu(channel_data["channel_id"])
        )
    except Exception as e:
        await message.answer(f"❗ xatolik yuzberdi{e}", reply_markup=back_to_channel_menu(channel_data["channel_id"]))
    finally:
        await state.clear()
