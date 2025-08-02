from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery


class ChannelCD(CallbackData, prefix="channel"):
    id: int
    action: str

class BotCD(CallbackData, prefix="bot"):
    username: str
    action: str

class ReferralCD(CallbackData, prefix="referral"):
    referral_id: str
    action: str

class UserStatusCD(CallbackData, prefix="user_status"):
    user_id: int
    action: str

