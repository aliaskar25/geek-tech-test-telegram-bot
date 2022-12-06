from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)

from db.sqlite_db import get_all_courses


client_address_btn = KeyboardButton('/address') # student_button
client_courses_btn = KeyboardButton('/courses_list')


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
client_keyboard.row(client_address_btn, client_courses_btn)


async def start_command(message: Message):
    await message.answer('Choose your next option', reply_markup=client_keyboard)


async def get_address(message: Message):
    await message.answer('Ибраимова 103')


def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(get_address, commands=['address'])
