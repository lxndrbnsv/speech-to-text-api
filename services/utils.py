import os
import uuid

import aiohttp
import aiofiles

from config import Config as cfg


def unique_name() -> str:
    return str(uuid.uuid4())


async def delete_file(filepath: str) -> None:
    os.remove(filepath)


async def download_file(url, save_path: str) -> None:
    save_dir = save_path.rsplit("/", 1)[0]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            status_code = response.status
            if status_code == 200:
                file = await aiofiles.open(save_path, mode="wb")
                await file.write(await response.read())
                await file.close()
            else:
                raise ConnectionError(f"STATUS CODE: {status_code}")
