from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from TG_user.filters import is_admin

from TG_admin.menu.handlers import router as menu_router


router = Router()
router.message.filter(is_admin())
router.callback_query.filter(is_admin())

router.include_router(menu_router)


