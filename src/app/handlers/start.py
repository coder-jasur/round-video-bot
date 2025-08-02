from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from asyncpg import Connection

from src.app.database.queries.referals import RefferralActions
from src.app.database.queries.users import UserActions

start_router = Router()


@start_router.message(CommandStart(magic=F.args.regexp(r"^[a-z0-9]{10}$")))
async def on_message_with_args(
    message: Message, command: CommandObject, conn: Connection, state: FSMContext
) -> None:
    await state.clear()
    user_actions = UserActions(conn)
    referrals_actions = RefferralActions(conn)
    user = await user_actions.get_user(message.from_user.id)
    print(user)

    if not user:
        await user_actions.add_user(
            message.from_user.id,
            message.from_user.username
        )
        await referrals_actions.increment_referal_members_count(
            referral_id=command.args
        )

    await message.answer(
        f"🤓 salom {message.from_user.first_name}. Men dumaloq man!\n\n"
        f"- Men sizga oddiy 🟦 TO'RTBUCHAK videoni 🔵 DUMALOQ video xabarga aylantiriberaman.\n\n"
        f"🫡 Menga shunchaki kerakli videoni yuborsangiz kifoya."
    )


@start_router.message(CommandStart())
async def command_start(message: Message, conn: Connection):
    user_action = UserActions(conn)
    user = await user_action.get_user(message.from_user.id)
    if not user:
        if message.from_user.username:
            await user_action.add_user(message.from_user.id, message.from_user.username)
        else:
            await user_action.add_user(message.from_user.id, message.from_user.first_name)

    await message.answer(
        f"🤓 salom {message.from_user.first_name}. Men dumaloq man!\n\n"
        f"- Men sizga oddiy 🟦 TO'RTBUCHAK videoni 🔵 DUMALOQ video xabarga aylantiriberaman.\n\n"
        f"🫡 Menga shunchaki kerakli videoni yuborsangiz kifoya."
    )
