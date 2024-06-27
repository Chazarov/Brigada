from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from Database.Orm_query import orm_query as orm

class user_is_not_registered(Filter):
    def __init__(self) -> None:
        return

    async def __call__(self, message:Message, session:AsyncSession) -> bool:
        user = await orm.get_user_by_id(session = session, user_id = message.from_user.id)
        return user == None
    
class is_admin(Filter):
    def __init__(self) -> None:
        return

    async def __call__(self, message:Message, session:AsyncSession) -> bool:
        admin = await orm.get_user_by_id(session = session, user_id = message.from_user.id)
        return admin != None