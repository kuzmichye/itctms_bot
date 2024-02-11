from aiogram.filters import StateFilter,Command
from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from src.states.fsm_states import FSMFillForm
from src.database.add import insert_student
import sqlite3


registration_router = Router()

#Ввод ВК    
@registration_router.message(F.text == "Зарегистрироваться в системе",StateFilter(default_state))
async def call_data(message:Message,state:FSMContext):
    await message.answer(text='Введите вашу фамилию')
    await state.set_state(FSMFillForm.fill_surname)
    

#ввод фамилии
@registration_router.message(StateFilter(FSMFillForm.fill_surname), F.text.isalpha())
async def process_surname_sent(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer(text='Введите ваше имя:')
    await state.set_state(FSMFillForm.fill_name)


#неправильный ввод фамилии
@registration_router.message(StateFilter(FSMFillForm.fill_surname))
async def warning_not_surname(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на фамилию\n\n'
             'Пожалуйста, введите вашу фамилию\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


#ввод имени
@registration_router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Введите ваше отчество:')
    await state.set_state(FSMFillForm.fill_mid_name)


#неправильный ввод фамилии
@registration_router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )
    
    
#ввод отчества
@registration_router.message(StateFilter(FSMFillForm.fill_mid_name), F.text.isalpha())
async def process_mid_name_sent(message: Message, state: FSMContext):
    await state.update_data(mid_name=message.text)
    await message.answer(text='Введите ваш курс:')
    await state.set_state(FSMFillForm.fill_grade)
    
#неправильный ввод отчества
@registration_router.message(StateFilter(FSMFillForm.fill_mid_name))
async def warning_not_mid_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на отчество\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


#ввод курса
@registration_router.message(StateFilter(FSMFillForm.fill_grade),
            lambda x: x.text.isdigit() and 1 <= int(x.text) <= 4)
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer(text='Введите вашу группу:')
    await state.set_state(FSMFillForm.fill_group)


#неправильный ввод курса
@registration_router.message(StateFilter(FSMFillForm.fill_grade))
async def warning_not_age(message: Message):
    await message.answer(
        text='Курс должен быть целым числом от 1 до 4\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


#ввод группы
@registration_router.message(StateFilter(FSMFillForm.fill_group),lambda x: x.text.isdigit())
async def process_group_sent(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    data = await state.get_data()
    student_tg_username = message.from_user.username
    student_tg_id = message.from_user.id
    name = data.get("name")
    surname = data.get("surname")
    mid_name = data.get("mid_name")
    grade = data.get("grade")
    student_group = data.get("group")
    conn = sqlite3.connect("src/itctms_system.db")
    cursor = conn.cursor()
    # Проверяем, есть ли пользователь в таблице
    cursor.execute("SELECT * FROM students WHERE telegram_id=?", (student_tg_id,))
    existing_user = cursor.fetchone()
    
    
    if existing_user:
        await message.answer("Вы уже зарегистрированы!")
        await state.clear()
    else:
        # Вызов функции для добавления данных в базу данных
        await insert_student(student_tg_id,student_tg_username, name, surname, mid_name, grade, student_group)
        await state.clear()
        await message.answer(
        text='Спасибо! Ваши данные сохранены!\n\n'
             'Вы вышли из процесса регистрации'
    )


@registration_router.message(Command(commands='showdata'), StateFilter(default_state))
async def show_data(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"Фамилия: {data.get('surname')}\n"
        f"Имя: {data.get('name')}\n"
        f"Отчество: {data.get('mid_name')}\n"
        f"Курс: {data.get('grade')}\n"
        f"Группа: {data.get('group')}"
    )
   

    
    
