from aiogram.fsm.state import StatesGroup, State


class AddBotSG(StatesGroup):
    get_bot_name = State()
    get_bot_nickname = State()


class DeleteBot(StatesGroup):
    delite_bot = State()