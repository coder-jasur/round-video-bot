from aiogram.fsm.state import StatesGroup, State


class Channel(StatesGroup):
    get_channel_id = State()

class AddChannelMessage(StatesGroup):
    get_chanel_message = State()
