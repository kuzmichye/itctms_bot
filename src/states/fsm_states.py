from aiogram.fsm.state import  State, StatesGroup

class FSMFillForm(StatesGroup):
    fill_surname = State()
    fill_name = State()
    fill_mid_name = State()
    fill_grade = State()
    fill_group = State()
