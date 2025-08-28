import asyncio
import os
import uuid

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from src.app.common.system_functions import upload_video_to_system, get_video_file_name, delete_video_for_system

round_video_router = Router()



@round_video_router.message(F.video)
async def answer_video_note(message: Message, bot: Bot):
    saved_path = None
    video = None
    load_msg = None

    try:
        video_size = message.video.file_size
        size_kb = video_size / 1024
        size_mb = size_kb / 1024
        if size_mb > 20:
            await message.reply("❗ siz yuborgan yuborgan video 20MB dan oshmasligi kerak")
            return False

        load_msg = await message.reply("⏳")
        file = await bot.get_file(message.video.file_id)
        file_data = await bot.download_file(file.file_path)
        print(file_data)
        file_name = get_video_file_name()

        saved_path = await upload_video_to_system(file_name, file_data)
        await bot.send_chat_action(message.chat.id, 'record_video_note')
        video = await crop_center_square_video(saved_path, "./videos")
        await message.answer_video_note(FSInputFile(video))
        await load_msg.delete()
    except Exception as e :
        print("Error",e)
        await load_msg.delete()
        await message.reply(
            "❗ Vidoni qayta ishlashda xatolik yuz berdi\n"
            "💾 hajmi 20MB dan pastroq video yuboring"
        )
    finally:
        await asyncio.to_thread(delete_video_for_system, saved_path, video)



async def crop_center_square_video(input_path: str, output_dir: str = "./videos", size: int = 570) -> str:
    output_filename = f"{uuid.uuid4().hex}_note_{size}x{size}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    filter_str = f"crop='min(in_w\\,in_h)':'min(in_w\\,in_h)',scale={size}:{size}"

    command = [
        "ffmpeg",
        "-i", input_path,
        "-t", "60",
        "-vf", filter_str,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "21",
        "-y",
        output_path
    ]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise Exception(f"FFmpeg error: {stderr.decode()}")

    return output_path

