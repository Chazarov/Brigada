import asyncio

from aiogram import F, types, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from TG.filters import user_is_not_registered

from Database.Orm_query import orm_query

from TG.user.registration.kbds import finish_registration_buttons




class UserRegistration(StatesGroup):
    Start_registration = State()
    Get_name = State()
    Get_phone_number = State()
    Get_group = State()
    Get_experiense = State()
    Finish_registretion = State()


router = Router()
router.message.filter(user_is_not_registered())
router.callback_query.filter(user_is_not_registered())


# Функция для очистки чата
# удаляет все сообщения , чьи id записаны в state_data.sent_messages 
# сохраняет отправленные ботом сообщения в stste_data.sent_messages, чтобы удалить их при следующем вызове
# удаляет отправленное пользователем сообщение, если флаг delete_message стоит в состоянии true
async def clean_chat(state:FSMContext, message:types.Message, sent_messages:list[types.Message] = None, delete_message:bool = True):

    data = await state.get_data()

    if "sent_messages" in data.keys():
        messages = data["sent_messages"]
        if(messages != None):
            for m in messages:
                await message.bot.delete_message(chat_id = message.from_user.id, message_id = m.message_id)
            await state.update_data(sent_messages = None)

    if(sent_messages != None):
        await state.update_data(sent_messages = sent_messages)

    if(delete_message):
        await message.delete()




async def start_registration(message:types.Message, state:FSMContext):
    sm1 = await message.answer("Здравствуйте!✋\n" +
                        "Для использования этого бота сначала \n" +
                        "необходимо пройти регистрацию✒️")
    sm2 = await message.answer("Укажите, как к вам можно обращаться:")

    await state.set_state(UserRegistration.Get_name)


    await clean_chat(state, message, [sm1, sm2]) # очистка чата
    
@router.message(UserRegistration.Get_name)
async def get_name(message:types.Message, state:FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    name = data["name"]

    sm = await message.answer(f"Отлично, {name}.\n" +
                            "Теперь укажите ваш номер телефона для связи.📞")
    await state.set_state(UserRegistration.Get_phone_number)


    await clean_chat(state, message, [sm]) # очистка чата
    
# Добавить выбор из существующих групп!!!!!!!!!!!!!!
@router.message(UserRegistration.Get_phone_number)
async def get_phone_number(message:types.Message, state:FSMContext):
    await state.update_data(phone_number = message.text)
    await state.set_state(UserRegistration.Get_group)
    sm = await message.answer("Напишите, кем бы вы хотели работать.\n Или выберите из списка ниже")
    
    await clean_chat(state, message, [sm]) # очистка чата


#Добавить кнопку - пропустить
@router.message(UserRegistration.Get_group)
async def get_group(message:types.Message, state:FSMContext):
    await state.update_data(group = message.text)
    await state.set_state(UserRegistration.Get_experiense)
    sm = await message.answer("Кратко опишите, какой опыт у вас имеется:")

    await clean_chat(state, message, [sm]) # очистка чата



@router.message(UserRegistration.Get_experiense)
async def get_experience(message:types.Message, state:FSMContext, session = AsyncSession):
    await state.update_data(experience = message.text)
    data = await state.get_data()
    admins = await orm_query.get_all_admins(session = session)

    #temp function:
    for admin in admins:
        await message.bot.send_message(chat_id = admin.id)

    name = data["name"]
    phone_num = data["phone_number"]
    group = data["group"]
    exp = data["experience"]
    sm = await message.answer("Регистрация завершена, вот ваши данные:" +
                        f"  Имя: {name}\n" +
                        f"  Телефон: {phone_num}\n" +
                        f"  Спецификация: {group}\n" +
                        f"  Опыт работы: {exp}", reply_markup = finish_registration_buttons())
    await state.set_state(UserRegistration.Finish_registretion)
    
    await clean_chat(state, message, [sm]) # очистка чата

@router.callback_query(StateFilter(UserRegistration.Finish_registretion), F.data == "finish_registration")
async def finish_registration(callback:types.CallbackQuery, state:FSMContext, session:FSMContext):
    data = await state.get_data()
    await orm_query.add_user(session = session, user_id = callback.from_user.id, name = data["name"], phone_number = data["phone_number"], start_group_id = None)
    await callback.answer("Регистрация завершена успешно✅")
    await state.clear()

    await clean_chat(state, callback.message) # очистка чата

@router.callback_query(F.data == "again")
async def registration_again(callback:types.CallbackQuery, state:FSMContext):
    await state.clear()
    await state.set_state(UserRegistration.Get_name)
    await start_registration(message = callback.message, state = state)

    clean_chat(state, callback.message) # очистка чата


router.message.register(start_registration, StateFilter(None))