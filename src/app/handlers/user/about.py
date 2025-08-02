from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

about_router = Router()

@about_router.message(Command("about"))
async def about_bot(message: Message):
    text = (
        "👋 <b>Biz haqimizda</b>\n\n"
        "Bizning kichik ammo qudratli botimiz — sizning oddiy videolaringizni "
        "<b>dumaloq, original va chiroyli ko‘rinishga</b> olib chiqish uchun yaratilgan.\n\n"
        "🎯 Maqsadimiz: oddiy videolaringizni <b>Telegramda dumaloq</b> "
        "video-xabarga aylantirish.\n\n"
        "📮 Taklif yoki savollaringiz bo‘lsa, biz doimo aloqadamiz:\n"
        "<a href='https://www.instagram.com/hikmatilloyev__/'>Instagram  hikmatilloyev__</a>\n"
        "<a href='https://t.me/hikmatilloyev_j'>Telegram  hikmatilloyev_j</a>"

    )

    await message.answer(text, parse_mode="HTML")