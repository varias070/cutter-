import uuid
import asyncio
import os

from aiohttp import web
from aiofile import async_open
from dotenv import load_dotenv

load_dotenv()

class Controller:

    def __init__(self, db, cutter):
        self.db = db
        self.cutter = cutter
        self.chunk_size = int(os.getenv("CHUNK_SIZE"))

    async def save_image(self, request):
        if request.method == "POST":
            data = request.body
            filename = uuid.uuid4()
            async with async_open(f'media/{filename}.jpg', 'bw') as file:
                async for data in request.content.iter_any():
                    await file.write(data)
                await asyncio.sleep(2)
                await self.db.create_image(filename)
                self.cutter.run(file, data.width, data.height)
                await self.db.add_carved_content(f'carved-{filename}')
                return web.Response(text=f'new file name carved-{filename}')
        else:
            return web.Response(text=f"request method must be POST, and you have {request.method}")

    async def get_image(self, request):
        if request.method == "GET":
            image = await self.db.get_image(request.query.file_name)
            response = web.StreamResponse(
                status=200,
                reason='OK',
                headers={
                    'Content-Type': 'multipart/x-mixed-replace',
                    'CONTENT-DISPOSITION': f'attachment;filename={image.name}'
                }
            )
            await response.prepare(request)
            try:
                async with async_open(f'media/{image.name}.jpg', 'rb') as f:
                    chunk = await f.read(self.chunk_size)

                    while chunk:
                        await response.write(chunk)
                        chunk = await f.read(self.chunk_size)

            except asyncio.CancelledError:
                raise Exception("Download chunk for response error")

            return response
        else:
            return web.Response(text=f"request method must be GET, and you have {request.method}")
