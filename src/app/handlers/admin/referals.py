from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asyncpg import Connection

from src.app.common.channel_and_bot_info_txt import referral_text
from src.app.common.generate_referral_id import generate_referal_id
from src.app.database.queries.referals import RefferralActions
from src.app.keyboards.inline.callback_data import ReferralCD
from src.app.keyboards.inline.inline_keyboards import (
    create_referrals_keyboard, refrral_menu, delite_referral_menu,
    back_to_referrals_menu
)
from src.app.states.admin.referral import AddReferralSG

referrals_router = Router()


@referrals_router.callback_query(F.data.in_(["referasls", "back_to_referral_menu"]))
async def referrals_list(call: CallbackQuery, conn: Connection):
    referral_action = RefferralActions(conn)
    referral_data = await referral_action.get_all_referrals()

    if not referral_data:
        await call.message.edit_text(
            "📥 Siz hali referal qo'shmagansiz",
            reply_markup=await create_referrals_keyboard(conn)
        )
        return

    await call.message.edit_text(
        "👥 <b>Referallar:</b>\n\n"
        "Pastdagilardan birni tanlang.", reply_markup=await create_referrals_keyboard(conn),
        parse_mode="HTML"
    )


@referrals_router.callback_query(ReferralCD.filter())
async def referrals_action(call: CallbackQuery, callback_data: ReferralCD, conn: Connection):
    referrals_actions = RefferralActions(conn)
    referal_data = await referrals_actions.get_referral(callback_data.referral_id)
    text = referral_text(callback_data.referral_id, referal_data[1], referal_data[2])

    if callback_data.action == "get_data":
        await call.message.edit_text(text, reply_markup=refrral_menu(callback_data.referral_id), parse_mode="HTML")
    elif callback_data.action == "delete_referral":
        await call.message.edit_text(
            f"🤔 Siz {referal_data[1]} referalini ochirishga amin misiz",
            reply_markup=delite_referral_menu(callback_data.referral_id)
        )

    elif callback_data.action == "not_sure":
        await call.message.edit_text(text, reply_markup=refrral_menu(callback_data.referral_id), parse_mode="HTML")

    elif callback_data.action == "sure":
        try:
            await referrals_actions.delite_referral(callback_data.referral_id)
            await call.message.edit_text("✅ referal muvafaqiyatli ochirildi", reply_markup=back_to_referrals_menu)
        except Exception as e:
            await call.message.edit_text("❗ referalni o'chirishda xatolik yuzberdi",
                reply_markup=back_to_referrals_menu)


@referrals_router.callback_query(F.data == "add_referal")
async def get_referral_name(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddReferralSG.get_referral_name)
    await call.message.edit_text("📥 referalni nomini yuboring")


@referrals_router.message(AddReferralSG.get_referral_name)
async def add_referral_for_db(message: Message,conn: Connection, state: FSMContext):
    try:
        referal_actions = RefferralActions(conn)
        referal_id = await generate_referal_id(conn)
        print(referal_id)
        await referal_actions.add_referral(str(referal_id.lower()), message.text)
        await message.answer("✅ referal muvafaqiyatli qo'shildi", reply_markup=back_to_referrals_menu)

    except Exception as e:
        print(e)
        await message.answer(
            text="❗ referal qo'shishda xatolik yuz berdi qaytatdan urinib ko'ring",
            reply_markup=back_to_referrals_menu
        )
    finally:
        await state.clear()
