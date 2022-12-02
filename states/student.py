from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class StudentFSMAdmin(StatesGroup):
    name = State()
    photo = State()
    course = State()
