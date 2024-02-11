from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.main_menu import *
from handlers.registration import registration_router
from handlers.main_menu import menu_router
from handlers.event import event_router
from database.add import db_start
import os
import asyncio
import logging
import sys


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)




async def on_startup(_):
    await db_start()


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp.include_router(menu_router)
    dp.include_router(registration_router)
    dp.include_router(event_router)
    await db_start()
    await dp.start_polling(bot, on_startup=on_startup)
    




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




