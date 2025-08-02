from aiogram.fsm.state import StatesGroup, State


class AddReferralSG(StatesGroup):
    get_referral_name = State()