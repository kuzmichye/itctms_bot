from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.main_menu import *
from handlers.registration import registration_router
from handlers.main_menu import menu_router
from database.add_student import db
import os
import asyncio
import logging
import sys


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)




async def on_startup(_):
    await db.db_start()


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot, on_startup=on_startup)


dp.include_router(registration_router)
dp.include_router(menu_router)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




