from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


sb_1 = KeyboardButton('/create_student') # student_button
sb_2 = KeyboardButton('/students_list')
sb_3 = KeyboardButton('/add_course')
sb_4 = KeyboardButton('/courses_list')
sb_5 = KeyboardButton('/delete_student')


student_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
student_keyboard.add(sb_1).insert(sb_2)
student_keyboard.add(sb_3).insert(sb_4)



student_list_python = KeyboardButton('/python')
student_list_javascript = KeyboardButton('/javascript')

courses_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
courses_keyboard.add(student_list_python).insert(student_list_javascript)
