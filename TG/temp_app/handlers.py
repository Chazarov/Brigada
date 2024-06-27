from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from Database.Orm_query import orm_query


router = Router()

@router.message(Command("add_admin"))
async def add_admin(message: types.Message, session:AsyncSession):
    await orm_query.add_admin(session = session, admin_id = message.from_user.id, name = message.from_user.first_name)
    await message.answer("Админ добавлен")


