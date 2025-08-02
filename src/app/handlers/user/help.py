from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()


@help_router.message(Command("help"))
async def help_user(message: Message):
    text = (
        "🎬 <b>Videongizni aylanaga aylantiring!</b>\n\n"
        "Siz menga <b>kvadrat yoki to‘g‘ri to‘rtburchak video</b> yuborasiz — "
        "men esa uni <b>dumaloq Telegram video-xabarga</b> aylantirib, sizga qaytaraman. \n"
        "Shu tariqa, xabarlaringizni <b>yanada samimiy va chiroyli</b> yetkaza olasiz! 💫\n\n"
        "📌 <b>Qanday foydalaniladi?</b>\n"
        "1️⃣ Videongizni shunchaki menga yuboring.\n"
        "2️⃣ Men uni qisqa vaqt ichida dumaloq formatga aylantiraman.\n"
        "3️⃣ <b>Eslatma:</b> video <b>60 soniyadan oshmasligi</b> kerak. Aks holda avtomatik qisqartiriladi. ⏱️\n\n"
        "✉️ Savollar bo‘lsa, bemalol murojaat qiling:\n"
        "<a href='https://t.me/hikmatilloyev_j'>@hikmatilloyev_j</a>"
    )

    await message.answer(text, parse_mode="HTML")
