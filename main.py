import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from Database.engine import as_create_db, session_maker
from Database.middleweares import DataBaseSession
from Database.Orm_query import setup_base

from TG.admin.handlers import router as admin_router
from TG.user.handlers import router as users_router 
from TG.temp_app.handlers import router as temp_router




bot = Bot(token = os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(users_router)
dp.include_router(admin_router)
dp.include_router(temp_router)



async def on_startup(bot):
    await as_create_db()


    #Создание базовых моделей в базе данных (подробнее о таких смотреть в Database/Readme.txt) 
    async with session_maker() as session:
        await setup_base.create_base_group(session)


async def on_shutdown(bot):
    print("бот лег")


user_commands = [
    BotCommand(command='start', description='начать работу с ботом'),
    BotCommand(command='help', description='инструкция по работе с ботом'),
    BotCommand(command='profile', description='мой профиль'),
    
]

async def main()->None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool = session_maker))


    await bot.delete_webhook(drop_pending_updates = True)
    await bot.set_my_description("/start - начать работу")
    await bot.set_my_commands(commands = user_commands,scope = types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())