import asyncio

import os
import time

from aiofiles import os as aos
from aiofiles.ospath import isdir
from shutil import copy2

PATH = '/mnt/HDD/Tests/Роддом/2022-06-09'
DEST = '/mnt/HDD/_Dest/2022-06-09'


async def __generator():
    orders = await aos.listdir(PATH)
    for order in orders:
        op = f'{PATH}/{order}'
        is_dir = await isdir(op)
        if not is_dir:
            continue
        img_formats = await aos.listdir(op)
        for img_format in img_formats:
            if img_format in ('9x15', '15x21', '21x30'):
                photos = await aos.listdir(f'{PATH}/{order}/{img_format}')
                yield order, img_format, photos

async def copy_file(rel_path, files):
    for file in files:
        copy2(f'{PATH}/{rel_path}/{file}', f'{DEST}/{rel_path}/{file}')


async def main():
    start = time.time()
    async for order, imgf, photos in __generator():
        path = f'{DEST}/{order}/{imgf}'
        os.makedirs(path)
        await copy_file(f'{order}/{imgf}', photos)
    print('end ' + str(time.time() - start))

asyncio.run(main())