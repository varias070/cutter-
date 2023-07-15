from sqlalchemy import update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from model import Image


class Db:

    def __init__(self, database_url):
        self.base = declarative_base()
        self.engine = create_async_engine(database_url)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self):
        async with self.async_session() as session:
            yield session

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)

    async def create_image(self, filename):
        try:
            session = await self.get_session().__anext__()
            image = Image(name=filename,
                          content=open(f'{filename}.jpg'))
            session.add(image)
        except Exception as ex:
            print(ex)

    async def add_carved_content(self, filename):
        try:
            session = await self.get_session().__anext__()
            q = update(Image).where(name=filename).values({"carved_content": f'carved-{filename}'})
            await session.execute(q)
            return f'carved-{filename}'
        except Exception as ex:
            print(ex)

    async def get_image(self, image_name):
        try:
            session = await self.get_session().__anext__()
            q = select(Image).where(name=image_name)
            result = session.execute(q)
            return result
        except Exception as ex:
            print(ex)
