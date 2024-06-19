from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from TG.filters import is_admin

from TG.admin.menu.handlers import router as menu_router



router = Router()
router.message.filter(is_admin)


