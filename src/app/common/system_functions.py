import logging
import time
from io import BytesIO
from typing import BinaryIO

import aiofiles
import aiogram
import aiohttp
import os

from aiogram import Bot
from aiogram.types import Message

logger = logging.getLogger(__name__)


def delete_video_for_system(path_1: str, path_2: str, path_3: str):
    try:
        for p in [path_1, path_2, path_3]:
            if p:
                os.remove(p)

    except Exception as e:
        logger.exception("Can not remove video %s", e)


def get_video_file_name() -> str:
    return f"{time.time_ns()}.mp4"


async def upload_video_to_system(file_name: str, file_data: BinaryIO) -> str:
    save_path = f"./videos/{file_name}"

    file_data.seek(0)

    async with aiofiles.open(save_path, "wb") as f:
        await f.write(file_data.read())

    return save_path
