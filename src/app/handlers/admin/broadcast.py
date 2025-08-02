import logging
from typing import Any

from aiogram import Router, F, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from asyncpg import Connection

from src.app.keyboards.inline.inline_keyboards import back_to_admin_menu_keyboards
from src.app.services.broadcaster import Broadcaster
from src.app.states.admin.broadcast import BroadcastingManagerSG

logger = logging.getLogger(__name__)

broadcater_router = Router()

@broadcater_router.callback_query(F.data == "distribute_advertising")
async def start_broadcasting_manager(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "E'lon uchun <b>xabar</b> yuboring.",
        parse_mode="HTML"
    )
    await state.set_state(BroadcastingManagerSG.get_message)


@broadcater_router.message(BroadcastingManagerSG.get_message)
async def get_broadcasting_message(message: Message, state: FSMContext, **kwargs):
    if message.poll:
        await message.delete()
        return await message.answer(
            "❌ noto'g'ri farmat!"
        )

    album = kwargs.get("album")
    if album:
        await state.update_data(album=album)
    else:
        await state.update_data(message=message)

    await state.set_state(BroadcastingManagerSG.confirm_broadcasting)
    await message.answer(
        "Siz e'linni boshlashga aminmisiz",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="❌ bekor qilish", callback_data="broadcast:cancel"),
                    InlineKeyboardButton(text="✅ tasdiqlash", callback_data="broadcast:confirm"),
                ]
            ]
        )
    )


@broadcater_router.callback_query(BroadcastingManagerSG.confirm_broadcasting, F.data == "broadcast:cancel")
async def on_cancel_broadcast(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("E'lon bekor qiindi", reply_markup=back_to_admin_menu_keyboards)


@broadcater_router.callback_query(BroadcastingManagerSG.confirm_broadcasting, F.data == "broadcast:confirm")
async def on_confirm_broadcast(call: CallbackQuery, state: FSMContext, conn: Connection, bot: Bot) -> Any:
    try:
        data = await state.get_data()
        print(data)
        message = data.get("message")
        album = data.get("album")

        if not album and not message:
            raise ValueError("Broadcasting message not present!")

        await call.message.edit_text("E'lon foydalnuvchirlarga tarqatiliyapti...")
        broadcaster = Broadcaster(
            bot=bot,
            conn=conn,
            admin_id=call.from_user.id,
            broadcasting_message=message,
            album=album,
            batch_size=5000  # Устанавливаем размер пачки
        )

        # Запуск рассылки
        count_blocked, count_deleted, count_limited, count_deactivated = await broadcaster.broadcast()

        # Вывод результатов рассылки
        result_message = "E'lon tarqatish tugadi."

        if count_blocked:
            result_message += (
                f"\nTopildi {count_blocked} botni blok qilganlar."
            )

        if count_deleted:
            result_message += (
                f"\nTopildi {count_deleted} akuntlar, o'chirlib ketgan."
            )

        if count_limited:
            result_message += (
                f"\nTopildi {count_limited} akauntlar, telegram tomondan cheklangan."
            )

        if count_deactivated:
            result_message += (
                f"\nTopildi {count_deleted} akauntlar, ochiriligan."
            )

        if not count_blocked and not count_deleted and not count_limited and not count_deactivated:
            result_message += "\nHamma xabarlar muvafaqiyatli yetkazildi."

        await call.message.edit_text(result_message)

    except ValueError as e:
        # Обработка ошибок валидации в Broadcaster
        return await call.message.answer(f"E'lon tarqatishda xatolik kuzatildi: {e}")

    except Exception as e:
        logger.error(f"E'lon tarqatishda xatolik kuzatildi: {e}")
        return await call.message.answer(f"E'lon tarqatishda xatolik kuzatildi: {e}")
