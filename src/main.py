from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from src.handlers.main_menu import *
from src.handlers.registration import registration_router
from src.handlers.main_menu import menu_router
from src.database.work_students import db_start
import os
import asyncio
import logging
import sys


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

redis = Redis(host='127.0.0.1',port = 6379)
storage = RedisStorage(redis=redis)


dp = Dispatcher(storage=storage)




async def on_startup(_):
    await db_start()


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp.include_router(menu_router)
    dp.include_router(registration_router)
    await db_start()
    await dp.start_polling(bot,on_startup = on_startup)
    




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




