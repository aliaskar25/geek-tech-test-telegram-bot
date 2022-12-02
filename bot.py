from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()


bot = Bot(token=os.getenv("BOT_TOKEN", default="5663202583:AAE78paT0RNgDmNSxvw1zNfIYbzJ-w3yri0"))
dp = Dispatcher(bot, storage=storage)

