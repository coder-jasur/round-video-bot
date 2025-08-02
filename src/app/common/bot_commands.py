from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeChat, BotCommandScopeChatAdministrators

from src.app.core.config import Settings


async def bot_commands(bot: Bot, settings: Settings):
    await bot.set_my_commands(
        commands=[
            BotCommand(command="/start", description="botni ishga tushirish"),
            BotCommand(command="/help", description="yordam"),
            BotCommand(command="/about", description="biz haqimizda")
        ],

    )
    for admin_id in settings.admins_ids:
        scoupe = BotCommandScopeChat(chat_id=int(admin_id))

        await bot.set_my_commands(
            commands=[
                BotCommand(command="/start", description="botni ishga tushirish"),
                BotCommand(command="/help", description="yordam"),
                BotCommand(command="/about", description="biz haqimizda"),
                BotCommand(command="/admin_menu", description="admin menyu")
            ],
            scope=scoupe
        )
