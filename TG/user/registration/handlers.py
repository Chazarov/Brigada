from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from TG.filters import user_is_not_registered




class UserRegistration(StatesGroup):
    Start_registration = State()
    Get_name = State()
    Get_phone_number = State()
    Get_group = State()
    Get_expirense = State()


router = Router()
router.message.filter(user_is_not_registered())
router.callback_query.filter(user_is_not_registered())



@router.message(StateFilter(None))
async def start_registration(message:types.Message, state:FSMContext):
    await message.answer("Здравствуйте!✋\n\
                          Для использования этого бота сначала \n\
                         необходимо пройти регистрацию✒️")
    await message.answer("Укажите, как к вам можно обращаться:")
    await state.set_state(UserRegistration.Get_name)
    
@router.message(UserRegistration.Get_name)
async def get_name(message:types.Message, state:FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(UserRegistration.Get_phone_number)

    name = data["name"]

    data = await state.get_data()
    await message.answer(f"Отлично, {name}.\n\
                            Теперь укажите ваш номер телефона для связи.📞")
    
# Добавить выбор из существующих групп!!!!!!!!!!!!!!
@router.message(UserRegistration.Get_phone_number)
async def get_phone_number(message:types.Message, state:FSMContext):
    await state.update_data(phone_number = message.text)
    await state.set_state(UserRegistration.Get_group)
    await message.answer("Напишите, кем бы выхотели работать.\n Или выберите из списка ниже")

#Добавить кнопку - пропустить
@router.message(UserRegistration.Get_group)
async def get_group(message:types.Message, state:FSMContext):
    await state.update_data(group = message.text)
    await state.set_state(UserRegistration.Get_expirense)
    await message.answer("Кратко опишите, какой опыт работы по этой специальности у вас имеется:")

@router.message(UserRegistration.Get_expirense)
async def get_expirence(message:types.Message, state:FSMContext):
    await state.update_data(expirence = message.text)
    await message.answer("Регистрация завершена успешно✅")
