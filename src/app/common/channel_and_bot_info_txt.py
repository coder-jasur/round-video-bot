def channel_text(channel_id: int, channel_name: str, channel_username: str, channel_status: str):
    text = (
        "📢 <b>Kanal haqida to‘liq ma’lumot</b>\n\n"
        f"🆔 <b>ID:</b> <code>{channel_id}</code>\n"
        f"📛 <b>Nomi:</b> {channel_name}\n"
        f"🔗 <b>Username:</b> @{channel_username}\n"
        f"📶 <b>Status:</b> <code>{channel_status}</code>\n"
        f"🚀 <b>Havola:</b> https://t.me/{channel_username}\n\n"
    )
    return text


def bot_text(bot_name: str, bot_username: str, bot_sattus: str):
    text = (
        "🤖 <b>Bot haqida qisqacha</b>\n\n"
        f"📛 <b>Nomi:</b> <code>{bot_name}</code>\n"
        f"🔗 <b>Username:</b> {bot_username}\n"
        f"📶 <b>Status:</b> <code>{bot_sattus}</code>\n"
        f"🚀 <b>Havola:</b> https://t.me/{bot_username[1:]}\n\n"
    )
    return text


def referral_text(referal_id: str,referam_name: str, referral_member_count: int):
    text = (
        "🤖 <b>referal haqida qisqacha</b>\n\n"
        f"📛 <b>Nomi:</b> <code>{referam_name}</code>\n"
        f"📶 <b>kelgan odamlar soni:</b> <code>{referral_member_count}</code>\n"
        f"🚀 <b>Havola:</b> https://t.me/DumaloqVideoUzBot?start={referal_id}\n\n"
    )
    return text


def user_status_text(user_id: int, username: str, status: str):
    text = (
        "👤 foydalanuvchi haqida:\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"🔗 username: <code>{username}</code>\n"
        f"📶 status: {status}"
    )

    return text
