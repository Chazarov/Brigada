from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from TG.filters import user_is_not_registered

from TG.user.menu.handlers import router as menu_router
from TG.user.registration.handlers import router as registration_router



router = Router()
router.include_router(registration_router)
router.include_router(menu_router)