from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

from bot import dp, bot

from states.student import StudentFSMAdmin
from states.course import CourseFSMAdmin

from db import sqlite_db

from keyboards.admin.student import (
    student_keyboard, courses_keyboard
)


ID = None


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id, "choose action: ", reply_markup=student_keyboard
    )
    await message.delete()


async def create_student(message: types.Message):
    if message.from_user.id == ID:
        await StudentFSMAdmin.name.set()
        await message.answer('Send your name')
        return
    await message.answer('You are not an admin')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if message.from_user.id == ID:
        if current_state is None:
            return
        await state.finish()
        await message.answer("canceled")


async def set_student_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await StudentFSMAdmin.next()
        await message.answer('Send your photo')


async def set_student_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await StudentFSMAdmin.next()
        await bot.send_message(
            message.from_user.id, 'Выберите курс (Python, JavaScript)', reply_markup=courses_keyboard
        )
        # await message.answer('Выберите курс (Python, JavaScript)', reply_markup=student_keyboard)


async def set_student_course(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['course'] = message.text[1:].capitalize()

        await sqlite_db.sql_add_command(state, table='student')
        await state.finish()
        await bot.send_message(
            message.from_user.id, 'Готово', reply_markup=student_keyboard
        )


async def get_students_list(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(
            message.from_user.id, "students by courses: ", reply_markup=courses_keyboard
        )
    await bot.send_message('you are not an admin')
    # for obj in sqlite_db.cursor.execute('SELECT * FROM student').fetchall():
    #     await bot.send_photo(ID, obj[1], f"name: {obj[0]}\n course: {obj[2]}")


async def create_course(message: types.Message):
    if message.from_user.id == ID:
        await CourseFSMAdmin.name.set()
        await message.answer('Type course: ')


async def set_course_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text.capitalize()
        
        await sqlite_db.sql_add_command(state, table='course')
        await state.finish()
        await message.answer('course created!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete_'))
async def delete_course(callback: types.CallbackQuery):
    course_id = callback.data.replace('delete_', '')
    await sqlite_db.sql_delete_course(course_id)
    await callback.answer(text=f"Курс под ID {course_id} был удален", show_alert=True)


async def get_courses_list(message: types.Message):
    for obj in sqlite_db.cursor.execute('SELECT * FROM course').fetchall():
        await bot.send_message(
            message.from_user.id, 
            text=f'ID курса: {obj[0]}\nНазвание курса: {obj[1]}\n',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Удалить', callback_data=f"delete_{obj[0]}")
            )
        )

async def get_students_by_course(message: types.Message):
    if message.text in ['/python', '/javascript']:
        query = f"SELECT * FROM student WHERE course = '{message.text[1:].capitalize()}'"
    else:
        await message.answer('wrong data')
        return

    for obj in sqlite_db.cursor.execute(query).fetchall():
        await bot.send_photo(ID, obj[2], f"name: {obj[1]}\ncourse: {obj[3]}")
    await bot.send_message(
        message.from_user.id, "choose action: ", reply_markup=student_keyboard
    )


async def delete_student(message: types.Message):
    if message.from_user.id == ID:
        students = sqlite_db.cursor.execute(f"SELECT * FROM student").fetchall()
        for student in students:
            await bot.send_photo(
                message.from_user.id, student[2], 
                f"name: {student[1]}\ncourse: {student[3]}"
            )
            await bot.send_message(
                message.from_user.id, 
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(f"Delete {student[1]}", callback_data=f"delete_{student[1]}")
                )
            )


def register_student_handler(dp: Dispatcher):
    dp.register_message_handler(create_student, commands=['create_student'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(set_student_name, state=StudentFSMAdmin.name)
    dp.register_message_handler(set_student_photo, content_types=['photo'], state=StudentFSMAdmin.photo)
    dp.register_message_handler(set_student_course, state=StudentFSMAdmin.course)
    dp.register_message_handler(get_students_list, commands=['students_list'])
    dp.register_message_handler(make_changes_command, commands=['admin'])
    dp.register_message_handler(create_course, commands=['add_course'])
    dp.register_message_handler(set_course_name, state=CourseFSMAdmin.name)
    dp.register_message_handler(get_courses_list, commands=['courses_list'])
    dp.register_message_handler(get_students_by_course, commands=['python', 'javascript'])
    dp.register_message_handler(delete_student, commands=['delete_student'])
