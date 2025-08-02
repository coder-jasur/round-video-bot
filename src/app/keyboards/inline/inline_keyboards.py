from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asyncpg import Connection

from src.app.database.queries.referals import RefferralActions
from src.app.keyboards.inline.callback_data import ChannelCD, BotCD, ReferralCD, UserStatusCD

admin_menu_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔗 Obuna bog‘lamasi", callback_data="channel_and_bot_settings")
        ],
        [
            InlineKeyboardButton(text="👥 Referallar", callback_data="referasls")
        ],
        [
            InlineKeyboardButton(text="📊 Foydalanuvchilar soni", callback_data="memebers_count")
        ],
        [
            InlineKeyboardButton(text="📢 E’lon tarqatish", callback_data="distribute_advertising")
        ],
        [
            InlineKeyboardButton(text="🚫 Bloklash / ✅ Blokdan chiqarish", callback_data="blocked_unblocked")
        ],
        [
            InlineKeyboardButton(text="🔙admin menyusidan chiqish", callback_data="quit")
        ]

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def channels_and_bots_keyboards(channels_list: list, bots_list: list) -> InlineKeyboardMarkup:
    keyboards = InlineKeyboardBuilder()
    if channels_list:

        keyboards.row(
            InlineKeyboardButton(
                text="📂 -----kanallar-----",
                callback_data="some_data"
            )
        )

    for channel in channels_list:
        keyboards.row(
            InlineKeyboardButton(
                text=channel[1],
                callback_data=ChannelCD(
                    id=channel[0],
                    action="channel_modified"
                ).pack()
            )
        )
    if bots_list:
        keyboards.row(
            InlineKeyboardButton(
                text="📂 -----botlar-----",
                callback_data="some_data"
            )
        )

    for bot in bots_list:

        keyboards.row(
            InlineKeyboardButton(
                text=bot[0],
                callback_data=BotCD(
                    username=bot[1],
                    action="bot_modified"
                ).pack()
            )
        )
    keyboards.row(
        InlineKeyboardButton(
            text="➕ bot qo'shish",
            callback_data="add_bot"

        ),
        InlineKeyboardButton(
            text="📢 kanal qo'shish",
            callback_data="add_channel"
        )
    )
    keyboards.row(
        InlineKeyboardButton(
            text="◀️ orqaga",
            callback_data="back_to_admin_menu"
        )
    )

    return keyboards.as_markup()


def channel_menu(
    channel_id: int,
    channel_sattus: str
) -> InlineKeyboardMarkup:
    keyboards = InlineKeyboardBuilder()

    if channel_sattus == "majburiy obuna":
        keyboards.row(
            InlineKeyboardButton(
                text="❌ majburiy obunani bekor qilish",
                callback_data=ChannelCD(
                    id=channel_id,
                    action="forced_cancellation_of_subscription"
                ).pack()
            )
        )
    elif channel_sattus == "majburiy obuna siz":
        keyboards.row(
            InlineKeyboardButton(
                text="✅ majburiy obunaga qo'shish",
                callback_data=ChannelCD(
                    id=channel_id,
                    action="add_to_mandatory_subscription"
                ).pack()
            )
        )

    keyboards.row(
        InlineKeyboardButton(
            text="🗑️ kanalni o'chirish",
            callback_data=ChannelCD(id=channel_id, action="delete_channel").pack()
        ),
        InlineKeyboardButton(
            text="📄 kanalga xabar qo'shish",
            callback_data=ChannelCD(id=channel_id, action="add_channel_message").pack()
        )
    )
    keyboards.row(
        InlineKeyboardButton(
            text="◀️ orqaga",
            callback_data="back_to_channels_menu"
        )
    )

    return keyboards.as_markup()


def bot_menu(
    bot_username: str,
    bot_sattus: str
) -> InlineKeyboardMarkup:
    keyboards = InlineKeyboardBuilder()

    if bot_sattus == "majburiy obuna":
        keyboards.row(
            InlineKeyboardButton(
                text="❌majburiy obunani bekor qilish",
                callback_data=BotCD(
                    username=bot_username,
                    action="forced_cancellation_of_subscription"
                ).pack()
            )
        )
    elif bot_sattus == "majburiy obuna siz":
        keyboards.row(
            InlineKeyboardButton(
                text="✅ majburiy obunaga qo'shish",
                callback_data=BotCD(
                    username=bot_username,
                    action="add_to_mandatory_subscription"
                ).pack()
            )
        )

    keyboards.row(
        InlineKeyboardButton(
            text="🗑️ botni o'chirish",
            callback_data=BotCD(
                username=bot_username,
                action="delete_bot"
            ).pack()
        ),
        InlineKeyboardButton(
            text="◀️ orqaga",
            callback_data="back_to_channels_menu"
        )
    )
    return keyboards.as_markup()


add_channel_and_bot_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ bot qo'shish", callback_data="add_bot"),
            InlineKeyboardButton(text="📢 kanal qo'shish", callback_data="add_channel")

        ],
        [
            InlineKeyboardButton(text="◀️ orqaga", callback_data="back_to_admin_menu")
        ]
    ]
)


def delite_bot_menu(bot_username: str) -> InlineKeyboardMarkup:
    keybards = InlineKeyboardBuilder()

    keybards.row(
        InlineKeyboardButton(text="✅ ha", callback_data=BotCD(username=bot_username, action="sure").pack()),
        InlineKeyboardButton(text="❌ yo'q", callback_data=BotCD(username=bot_username, action="not_sure").pack())
    )
    return keybards.as_markup()


def delite_channel_menu(channel_id: int) -> InlineKeyboardMarkup:
    keybards = InlineKeyboardBuilder()

    keybards.row(
        InlineKeyboardButton(text="✅ ha", callback_data=ChannelCD(id=channel_id, action="sure").pack()),
        InlineKeyboardButton(text="❌ yo'q", callback_data=ChannelCD(id=channel_id, action="not_sure").pack())
    )
    return keybards.as_markup()


back_to_admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ orqaga", callback_data="back_to_channels_menu")
        ]
    ]
)


def back_to_channel_menu(channel_id: int):
    keyboards = InlineKeyboardBuilder()
    keyboards.row(
        InlineKeyboardButton(text="◀️ orqaga", callback_data=ChannelCD(id=channel_id, action="channel_modified").pack())
    )

    return keyboards.as_markup()


async def create_referrals_keyboard(conn: Connection) -> InlineKeyboardMarkup:
    referrlas_actions = RefferralActions(conn)
    referrals = await referrlas_actions.get_all_referrals()

    buttons = InlineKeyboardBuilder()

    if referrals:
        for referral in referrals:
            buttons.row(

                InlineKeyboardButton(
                    text=referral[1] + " - " + str(referral[2]),
                    callback_data=ReferralCD(
                        referral_id=referral[0], action="get_data"
                    ).pack(),
                )

            )

    buttons.row(InlineKeyboardButton(text="➕ referal qo'shish", callback_data="add_referal"))
    buttons.row(InlineKeyboardButton(text="◀️ orqaga", callback_data="back_to_admin_menu"))

    return buttons.as_markup()


def refrral_menu(
    referral_id: str,
) -> InlineKeyboardMarkup:
    keyboards = InlineKeyboardBuilder()

    keyboards.row(
        InlineKeyboardButton(
            text="🗑️ referalni o'chirish",
            callback_data=ReferralCD(
                referral_id=referral_id,
                action="delete_referral"
            ).pack()
        ),
        InlineKeyboardButton(
            text="◀️ orqaga",
            callback_data="back_to_referral_menu"
        )
    )
    return keyboards.as_markup()


def delite_referral_menu(referral_id: str) -> InlineKeyboardMarkup:
    keybards = InlineKeyboardBuilder()

    keybards.row(
        InlineKeyboardButton(text="✅ ha", callback_data=ReferralCD(referral_id=referral_id, action="sure").pack()),
        InlineKeyboardButton(text="❌ yo'q", callback_data=ReferralCD(referral_id=referral_id, action="not_sure").pack())
    )
    return keybards.as_markup()


back_to_referrals_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ orqaga", callback_data="back_to_referral_menu")
        ]
    ]
)

back_to_admin_menu_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ orqaga", callback_data="back_to_admin_menu")
        ]
    ]
)


def user_status_actions(status: str, user_id: int):
    keyboards = InlineKeyboardBuilder()
    print(status)

    if status == "unblocked":
        keyboards.row(
            InlineKeyboardButton(
                text="🚫 Bloklash", callback_data=UserStatusCD(
                    user_id=user_id,
                    action="blocked_user"
                ).pack()
            )
        )

    elif status == "blocked":
        keyboards.row(
            InlineKeyboardButton(
                text="✅ Blokdan chiqarish", callback_data=UserStatusCD(
                    user_id=user_id,
                    action="unblocked_user"
                ).pack()
            )
        )

    keyboards.row(InlineKeyboardButton(text="◀️ orqaga", callback_data="back_to_admin_menu"))

    return keyboards.as_markup()
