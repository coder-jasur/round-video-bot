from aiogram import F, Router

from src.app.handlers.admin.block_un_block import block_un_block_router
from src.app.handlers.admin.broadcast import broadcater_router
from src.app.handlers.admin.channels_and_bots.bot import bot_router
from src.app.handlers.admin.channels_and_bots.channel import channel_router
from src.app.handlers.admin.admin_commands import admin_commands_router
from src.app.handlers.admin.referals import referrals_router


def registrar_admin_routers(router: Router, admins: list):
    admins_id = []
    for admin in admins:
        admins_id.append(int(admin))
    admin_router = Router()
    admin_router.message.filter(F.from_user.id.in_(admins_id))
    admin_router.callback_query.filter(F.from_user.id.in_(admins_id))

    admin_router.include_router(admin_commands_router)
    admin_router.include_router(referrals_router)
    admin_router.include_router(block_un_block_router)
    admin_router.include_router(broadcater_router)
    admin_router.include_router(bot_router)
    admin_router.include_router(channel_router)
    router.include_router(admin_router)
