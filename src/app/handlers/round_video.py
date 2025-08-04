import asyncio
import os
import subprocess
import uuid

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from src.app.common.system_functions import upload_video_to_system, get_video_file_name, delete_video_for_system

round_video_router = Router()


# @round_video_router.message(F.video)
# async def take_square_video(message: Message, bot: Bot):
#
#     file = await bot.get_file(message.video.file_id)
#     print(file, "f")
#
#     file_data = await bot.download_file(file.file_path)
#     print(file_data, "fd")
#
#     file_name = message.video.file_name or f"{message.video.file_id}.mp4"
#     print(file_name, "fn")
#
#     saved_path = await upload_video_to_system(file_name, file_data)
#     print(saved_path, "sp")
#
#     video_note = await convert_square_to_round_video(saved_path)
#
#     await message.answer_video_note(FSInputFile(video_note))
#     await asyncio.create_task(os.remove(saved_path))
#     await asyncio.create_task(os.remove(video_note))


# @round_video_router.message(F.video)
# async def take_square_video(message: Message, bot: Bot):
#     size = 340
#     file = await bot.get_file(message.video.file_id)
#     file_data = await bot.download_file(file.file_path)
#
#     file_name = get_video_file_name()
#
#
#
#     saved_path = await upload_video_to_system(file_name, file_data)
#
#
#
#     output_filename = f"{uuid.uuid4().hex}_square_{size}x{size}.mp4"
#     output_path = os.path.join("./videos", output_filename)
#
#     command = [
#         "ffmpeg",
#         "-i", saved_path,
#         "-vf", f"scale={size}:{size}",
#         "-c:a", "copy",
#         output_path
#     ]
#
#     subprocess.run(command, check=True)
#     await message.answer_video_note(FSInputFile(output_path))
#     asyncio.create_task(os.remove(output_path))


@round_video_router.message(F.video)
async def answer_video_note(message: Message, bot: Bot):
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
        file_name = get_video_file_name()

        saved_path = await upload_video_to_system(file_name, file_data)
        video = await asyncio.to_thread(crop_center_square_video, saved_path, "./videos")
        await bot.send_chat_action(message.chat.id, 'record_video_note')
        await message.answer_video_note(FSInputFile(video))
        await load_msg.delete()
        await asyncio.to_thread(delete_video_for_system, saved_path, video)
    except Exception:
        await load_msg.delete()
        await message.reply(
            "❗ Vidoni qayta ishlashda xatolik yuz berdi hajmi\n"
            "💾 20MB dan pastroq video yuboring"
        )


def crop_center_square_video(input_path: str, output_dir: str = "./videos", size: int = 360) -> str:
    output_filename = f"{uuid.uuid4().hex}_note_{size}x{size}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    filter_str = f"crop='min(in_w\\,in_h)':'min(in_w\\,in_h)',scale={size}:{size}"

    command = [
        "ffmpeg",
        "-i", input_path,
        "-t", "60",
        "-vf", filter_str,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-y",
        output_path
    ]

    subprocess.run(command, check=True)
    return output_path

# def convert_to_rount(input_path: str, output_dir: str = "./videos", size: int = 340) -> str:
#     output_filename = f"{uuid.uuid4().hex}_square_{size}x{size}.mp4"
#     output_path = os.path.join(output_dir, output_filename)
#
#     command = [
#         "ffmpeg",
#         "-i", input_path,
#         "-vf", f"scale={size}:{size}",
#         "-c:v", "libx264",
#         "-crf", "28",
#         "-preset", "veryfast",
#         "-c:a", "copy",
#         output_path
#     ]
#
#     subprocess.run(command, check=True)
#     return output_path
