from typing import AsyncGenerator

from bootstrap.db import async_session
from service.user import UserService


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_user_crud() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield UserService(session)
