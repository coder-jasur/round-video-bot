from aiogram import Dispatcher, Router

from src.app.filters.check_user_status import CheckUserStatus, CheckUserStatusCallback
from src.app.handlers.admin import registrar_admin_routers
from src.app.handlers.round_video import round_video_router
from src.app.handlers.start import start_router
from src.app.handlers.sub_check import check_sub_channel_router
from src.app.handlers.user.about import about_router
from src.app.handlers.user.help import help_router


def registrar_routers(dp: Dispatcher, admins: list):
    registrar_all_routers = Router()

    registrar_all_routers.include_router(check_sub_channel_router)
    registrar_all_routers.message.filter(CheckUserStatus())
    registrar_all_routers.callback_query.filter(CheckUserStatusCallback())


    registrar_admin_routers(registrar_all_routers, admins)

    registrar_all_routers.include_router(start_router)
    registrar_all_routers.include_router(round_video_router)
    registrar_all_routers.include_router(help_router)
    registrar_all_routers.include_router(about_router)


    dp.include_router(registrar_all_routers)
