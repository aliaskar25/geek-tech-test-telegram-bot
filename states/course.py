from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class CourseFSMAdmin(StatesGroup):
    name = State()
