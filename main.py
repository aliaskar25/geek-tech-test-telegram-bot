import logging

from aiogram import executor

from db import sqlite_db
from bot import dp, bot
from handlers.client import info
from handlers.admin import student as admin_student
from heroku_settings import (
    HEROKU_APP_NAME, WEBHOOK_HOST,
    WEBHOOK_PATH, WEBHOOK_URL,
    WEBAPP_HOST, WEBAPP_PORT,
)


async def on_startup(_):
    print('Bot has started')
    sqlite_db.sql_start()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp): # dispatcher
    await bot.delete_webhook()


info.register_client_handler(dp)
admin_student.register_student_handler(dp)


if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
