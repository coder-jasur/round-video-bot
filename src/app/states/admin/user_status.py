from aiogram.fsm.state import StatesGroup, State


class UserStatus(StatesGroup):
    get_user_id = State()