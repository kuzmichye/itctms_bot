from aiogram import F,Router
from aiogram.types import Message,CallbackQuery,ReplyKeyboardRemove
from aiogram.filters import StateFilter
from src.keyboards.reply import keyboard_inline, button_variety,button_variety_simple
from aiogram.fsm.context import FSMContext
from src.states.fsm_states import RegistrationState
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)
from datetime import datetime
from dotenv import load_dotenv
from aiogram.enums import ParseMode

import os
import sqlite3

conn = sqlite3.connect('src/itctms_system.db',isolation_level=None)
cursor = conn.cursor()
    
registration_router = Router()

load_dotenv()
  
@registration_router.message(F.text == 'Вход в систему')
async def start_command(message: Message, state: FSMContext):
    cursor.execute('SELECT tg_id FROM students WHERE tg_id=?', (message.from_user.id,))
    result = cursor.fetchone()
    if result is None:
        await message.answer("Введите ваш студенческий билет:")
        await state.set_state(RegistrationState.waiting_for_ticket)
    else:
        cursor.execute('SELECT surname, mid_name, name FROM students WHERE tg_id=?', (message.from_user.id,))
        result = cursor.fetchone()
        surname, mid_name, name = result
        welcome_message = f'Добро пожаловать, {surname} {name} {mid_name}!'
        admin_id_1 = int(os.getenv("ADMIN_ID_1"))
        admin_id_2 = int(os.getenv("ADMIN_ID_2"))
        if not message.from_user.id in [admin_id_1,admin_id_2]:
            await message.answer(text=welcome_message, reply_markup=button_variety_simple)
            await message.answer(text = 'Перед вами список кнопок:\n\n'
                                       ' 1. <b>Список текущих мероприятий</b>\n'
                                       "Просмотрите список текущих мероприятий, на которые вы можете зарегистрироваться. Выберите интересующее мероприятие и присоединитесь к нему!\n\n"
                                        '2. "<b>Мои мероприятия</b>":\n'
                                    "Узнайте, на какие мероприятия вы уже зарегистрировались. Просмотрите список ваших текущих мероприятий и будьте в курсе всех событий!", reply_markup=button_variety_simple,parse_mode=ParseMode.HTML)
            await state.set_state(RegistrationState.opening_menu)
        else:
            await message.answer(text=welcome_message, reply_markup=button_variety)
            await message.answer(text = 'Перед вами список кнопок:\n\n'
                                        '1. <b>Список текущих мероприятий</b>\n'
                                       "Просмотрите список текущих мероприятий, на которые вы можете зарегистрироваться. Выберите интересующее мероприятие,нажмите на него и присоединяйтесь к нему!\n\n"
                                        '2. <b>Мои мероприятия</b>\n'
                                    "Узнайте, на какие мероприятия вы уже зарегистрировались. Просмотрите список ваших текущих мероприятий и будьте в курсе всех событий!\n\n"
                                    '3. <b>Список зарегистрировавшихся</b>:\n'
                                    "Узнайте информацию о людях, которые зарегистрировались на мероприятие. Нажмите на кнопку с мероприятием, и список людей будет перед вами\n\n"
                                    '4. <b>Добавить мероприятие</b>\n'
                                    "Добавляет новое мероприятие в базу данных мероприятий",reply_markup=button_variety,parse_mode=ParseMode.HTML)
            await state.set_state(RegistrationState.opening_menu)


@registration_router.message(StateFilter(RegistrationState.waiting_for_ticket))
async def process_ticket(message: Message, state: FSMContext):
    ticket = message.text
    cursor.execute("SELECT surname, name, mid_name, institute, grade, number_group FROM students WHERE ticket = ?", (ticket,))
    result = cursor.fetchone()
    if result:
        surname, name, mid_name, institute, grade, number_group = result
        await message.answer(text=f'Добро пожаловать, {surname} {name} {mid_name} {institute} {grade}-{number_group}')
        await message.answer(text='Подтверждаете данные?', reply_markup=keyboard_inline)
        # Записываем tg_id в базу данных
        cursor.execute("UPDATE students SET tg_id = ? WHERE ticket = ?", (message.from_user.id, ticket))
        conn.commit()
        await state.set_state(RegistrationState.waiting_for_confirmation)
    else:
        await message.answer(text='Не удалось найти ваш студенческий билет')
    


@registration_router.callback_query(F.data == 'yes_button_pressed',StateFilter(RegistrationState.waiting_for_confirmation))
async def process_button_1_press(callback: CallbackQuery, state: FSMContext):
    admin_id_1 = int(os.getenv("ADMIN_ID_1"))
    admin_id_2 = int(os.getenv("ADMIN_ID_2"))
    if not callback.message.from_user.id in [admin_id_1,admin_id_2]:
        await callback.message.answer(text='Отлично!', reply_markup = button_variety_simple)
        await callback.message.answer('Перед вами список кнопок:\n\n'
                                       ' 1. <b>Список текущих мероприятий</b>\n'
                                       "Просмотрите список текущих мероприятий, на которые вы можете зарегистрироваться. Выберите интересующее мероприятие и присоединитесь к нему!\n\n"
                                        '2. "<b>Мои мероприятия</b>":\n'
                                    "Узнайте, на какие мероприятия вы уже зарегистрировались. Просмотрите список ваших текущих мероприятий и будьте в курсе всех событий!", reply_markup=button_variety_simple,parse_mode=ParseMode.HTML)
        await state.set_state(RegistrationState.opening_menu)
    else:
        await callback.message.answer(text='Отлично!', reply_markup = button_variety)
        await callback.message.answer(text = 'Перед вами список кнопок:\n\n'
                                        '1. <b>Список текущих мероприятий</b>\n'
                                       "Просмотрите список текущих мероприятий, на которые вы можете зарегистрироваться. Выберите интересующее мероприятие,нажмите на него и присоединяйтесь к нему!\n\n"
                                        '2. <b>Мои мероприятия</b>\n'
                                    "Узнайте, на какие мероприятия вы уже зарегистрировались. Просмотрите список ваших текущих мероприятий и будьте в курсе всех событий!\n\n"
                                    '3. <b>Список зарегистрировавшихся</b>:\n'
                                    "Узнайте информацию о людях, которые зарегистрировались на мероприятие. Нажмите на кнопку с мероприятием, и список людей будет перед вами\n\n"
                                    '4. <b> Добавить мероприятие</b>\n'
                                    "Добавляет новое мероприятие в базу данных мероприятий",reply_markup=button_variety,parse_mode=ParseMode.HTML)
        await state.set_state(RegistrationState.opening_menu)
        

#выводится список текущих мероприятий
@registration_router.message(F.text == 'Список текущих мероприятий', StateFilter(RegistrationState.opening_menu))
async def process_current_events(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.show_current_events)
    cursor.execute("SELECT name FROM events WHERE datetime(registration_expire_date) > datetime('now','+3 hours')")
    rows = cursor.fetchall()
    if len(rows) > 0:
        buttons = [KeyboardButton(text=row[0]) for row in rows]
        buttons_back = KeyboardButton(text="Назад в меню")
        buttons_сancel = KeyboardButton(text="Отмена регистрации")
        keyboard = ReplyKeyboardMarkup(keyboard=[[button] for button in buttons] 
                                                + [[buttons_back]] + 
                                                [[buttons_сancel]], resize_keyboard=True, one_time_keyboard=False)
        await message.answer("Выберите мероприятие:", reply_markup=keyboard)
    else:
        await message.answer("На данный момент нет текущих мероприятий")
        await state.set_state(RegistrationState.opening_menu)
    
    

# регистрация на Мероприятие по нажатию кнопки
@registration_router.message(F.text != "Назад в меню", F.text != "Отмена регистрации", StateFilter(RegistrationState.show_current_events))
async def process_registration(message: Message, state: FSMContext):
    event_name = message.text
    student_tg_id = message.from_user.id
    cursor.execute("SELECT event_id FROM events WHERE name = ?", (event_name,))
    event_row = cursor.fetchone()
    event_id = event_row[0]  # Получаем event_id из результата запроса
    cursor.execute("SELECT * FROM registrations WHERE tg_id = ? AND event_id = ?", (student_tg_id, event_id))
    existing_registration = cursor.fetchone()
    if existing_registration:
        await message.answer("Вы уже зарегистрированы на это мероприятие")
    else:
        registration_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registration_platform = "Telegram"
        cursor.execute("INSERT INTO registrations (tg_id, event_id, registration_time, registration_platform) VALUES (?, ?, ?, ?)",
                           (student_tg_id, event_id, registration_time, registration_platform))
        conn.commit()
        await message.answer("Вы успешно зарегистрированы на мероприятие!")

   

# кнопка Назад в меню после регистрации на мероприятие
@registration_router.message(F.text == "Назад в меню")
async def go_back_to_events_menu(message: Message, state: FSMContext):
    admin_id_1 = int(os.getenv("ADMIN_ID_1"))
    admin_id_2 = int(os.getenv("ADMIN_ID_2"))
    if not message.from_user.id in [admin_id_1,admin_id_2]:
        await state.set_state(RegistrationState.opening_menu)
        await message.answer(f"Вы вернулись в меню", reply_markup=button_variety_simple)
    else:
        await state.set_state(RegistrationState.opening_menu)
        await message.answer(f"Вы вернулись в меню", reply_markup=button_variety)


#отмена регистрации
@registration_router.message(F.text == "Отмена регистрации", StateFilter(RegistrationState.show_current_events))
async def cancel_registration_event(message:Message,state:FSMContext):
    await state.set_state(RegistrationState.show_cancel_events)
    student_tg_id = message.from_user.id
    cursor.execute("SELECT events.name FROM registrations JOIN events ON registrations.event_id = events.event_id WHERE registrations.tg_id = ? AND registrations.is_cancelled IS NULL", (student_tg_id,))
    event_names = cursor.fetchall()
    if len(event_names)>0:
        buttons = [KeyboardButton(text=row[0]) for row in event_names]
        buttons_back = KeyboardButton(text="Назад")
        keyboard = ReplyKeyboardMarkup(keyboard=[[button] for button in buttons] 
                                          + [[buttons_back]],resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Выберите мероприятие для отмена регистрации на него:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет зарегистрированных мероприятий,чтобы их отменить")
        await state.set_state(RegistrationState.show_current_events)
        
        
        

#добавляем отмену в  registrations
@registration_router.message((F.text != "Назад"),StateFilter(RegistrationState.show_cancel_events))
async def process_cancel_registration(message: Message, state: FSMContext):
    event_name = message.text
    cursor.execute("SELECT event_id FROM events WHERE name = ?", (event_name,))
    event_id = cursor.fetchone()[0]
    student_tg_id = message.from_user.id
    # Проверка, была ли регистрация на мероприятие уже отменена
    cursor.execute("UPDATE registrations SET is_cancelled = 'cancelled' WHERE tg_id = ? AND event_id = ?", (student_tg_id, event_id))
    conn.commit()
    buttons_back_2 = KeyboardButton(text="Назад")
    keyboard_new = ReplyKeyboardMarkup(keyboard=[[buttons_back_2]])
    await message.answer("Укажите причину отмены регистрации на мероприятие:",reply_markup = ReplyKeyboardRemove())
    await state.set_state(RegistrationState.enter_reason)


#назад при выборе мероприятий для отмены
@registration_router.message(F.text == "Назад", StateFilter(RegistrationState.show_cancel_events))
async def go_back_to_events_menu(message: Message, state: FSMContext):
    cursor.execute("SELECT name FROM events WHERE datetime(registration_expire_date) > datetime('now','+3 hours')")
    rows = cursor.fetchall()
    buttons = [KeyboardButton(text=row[0]) for row in rows]
    buttons_back = KeyboardButton(text="Назад в меню")
    cancel_button = KeyboardButton(text = "Отмена регистрации")
    keyboard_back = ReplyKeyboardMarkup(keyboard=[[button] for button in buttons] 
                                        + [[buttons_back] +
                                          [cancel_button]],resize_keyboard=True, one_time_keyboard=False)
    await message.answer("Выберите мероприятие:", reply_markup=keyboard_back)
    await state.set_state(RegistrationState.show_current_events)
    
    
    
#добавляем причину в registrations
@registration_router.message((F.text != "Назад"),StateFilter(RegistrationState.enter_reason))
async def process_cancel_reason(message: Message, state: FSMContext):
    reason = message.text
    student_tg_id = message.from_user.id
    cursor.execute("UPDATE registrations SET reason = ? WHERE tg_id = ?", (reason, student_tg_id))
    conn.commit()
    buttons_back_2 = KeyboardButton(text="Назад")
    keyboard_new = ReplyKeyboardMarkup(keyboard=[[buttons_back_2]],resize_keyboard=True)
    await message.answer("Регистрация на мероприятие успешно отменена. Спасибо за участие!",reply_markup = keyboard_new)
    
#кнопка назад после указания причины 
@registration_router.message(F.text == "Назад",StateFilter(RegistrationState.enter_reason))
async def сancel_back(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.show_current_events)
    cursor.execute("SELECT name FROM events WHERE datetime(registration_expire_date) > datetime('now','+3 hours')")
    rows = cursor.fetchall()
    if len(rows) > 0:
        buttons = [KeyboardButton(text=row[0]) for row in rows]
        buttons_back = KeyboardButton(text="Назад в меню")
        buttons_сancel = KeyboardButton(text="Отмена регистрации")
        keyboard = ReplyKeyboardMarkup(keyboard=[[button] for button in buttons] 
                                                + [[buttons_back]] + 
                                                [[buttons_сancel]], resize_keyboard=True, one_time_keyboard=False)
        await message.answer("Выберите мероприятие, нажмите на него, и вы будете зарегистрированы:\n\n"
                     "- Отменить регистрацию: Отменить вашу текущую регистрацию на мероприятие\n"
                     "- Назад в меню: Вернуться в главное меню", reply_markup=keyboard)

    else:
        await message.answer("На данный момент нет текущих мероприятий")
        await state.set_state(RegistrationState.opening_menu) 
    

#список мероприятий, на которые ты зарегистрирован
@registration_router.message(F.text == "Мои мероприятия",StateFilter(RegistrationState.opening_menu))
async def show_my_events(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.show_my_events)
    student_tg_id = message.from_user.id
    # Запрос на получение имен мероприятий, связанных с пользователем
    cursor.execute("SELECT events.name FROM registrations JOIN events ON registrations.event_id = events.event_id WHERE registrations.tg_id = ? AND registrations.is_cancelled IS NULL", (student_tg_id,))
    event_names = cursor.fetchall()
    if event_names:
        events_list = "\n".join([event[0] for event in event_names])
        await message.answer(f"Ваши мероприятия:\n{events_list}")
        await state.set_state(RegistrationState.opening_menu)
    else:
        await message.answer("У вас нет зарегистрированных мероприятий")
        await state.set_state(RegistrationState.opening_menu)

   
#вывод мероприятий для вывода списка зарегистрированных на них
@registration_router.message(F.text == 'Списки зарегистрировавшихся', StateFilter(RegistrationState.opening_menu))
async def process_current_events(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.select_event)
    cursor.execute("SELECT name FROM events WHERE datetime(registration_expire_date) > datetime('now','+3 hours')")
    rows = cursor.fetchall()
    if len(rows) > 0:
        buttons = [KeyboardButton(text=row[0]) for row in rows]
        buttons_back = KeyboardButton(text="Назад в меню")
        keyboard = ReplyKeyboardMarkup(keyboard=[[button] for button in buttons] 
                                                +[[buttons_back]],resize_keyboard=True, one_time_keyboard=False)
        await message.answer("Выберите мероприятие для просмотра списка зарегистрировавшихся:", reply_markup=keyboard)
    else:
        await message.answer("На данный момент нет текущих мероприятий")
        await state.set_state(RegistrationState.opening_menu)
    

#вывод для каждого мероприятий списков
@registration_router.message(F.text != "Назад в меню", StateFilter(RegistrationState.select_event))
async def process_registration(message: Message, state: FSMContext):
    event_name = message.text
    cursor.execute("SELECT event_id FROM events WHERE name = ?", (event_name,))
    event_id = cursor.fetchone()[0]
    cursor.execute("SELECT event_id FROM events WHERE name = ?", (event_name,))
    student_tg_id = message.from_user.id
    cursor.execute("""
    SELECT students.surname, students.name, students.mid_name, students.grade, students.number_group
    FROM registrations
    JOIN students ON registrations.tg_id = students.tg_id
    JOIN events ON registrations.event_id = events.event_id
    WHERE registrations.is_cancelled IS NULL and events.event_id = ?
    """,(event_id,))
    registered_users = cursor.fetchall()
    if len(registered_users) > 0:
        response_message = "<b>Список зарегистрированных пользователей на мероприятие</b>:\n"
        for idx, user in enumerate(registered_users, start=1):
            surname, name, mid_name, grade, number_group = user
            user_info = f"{surname} {name} {mid_name} ИЦТМС {grade}-{number_group}"
            response_message += f"{idx}. {user_info}\n"
        await message.answer(response_message)
    else:
        await message.answer("На данный момент на мероприятие нет зарегистрированных пользователей")



#обратно в меню после списка текущих мероприятий
@registration_router.message(F.text == "Назад в меню", StateFilter(RegistrationState.select_event))
async def go_back_to_events_menu(message: Message, state: FSMContext):
    admin_id_1 = int(os.getenv("ADMIN_ID_1"))
    admin_id_2 = int(os.getenv("ADMIN_ID_2"))
    if not message.from_user.id in [admin_id_1,admin_id_2]:
        await state.set_state(RegistrationState.opening_menu)
        await message.answer(f"Вы вернулись в меню", reply_markup=button_variety_simple)
    else:
        await state.set_state(RegistrationState.opening_menu)
        await message.answer(f"Вы вернулись в меню", reply_markup=button_variety)

@registration_router.message(F.text == 'Посмотреть информацию о мероприятии', StateFilter(RegistrationState.opening_menu))
async def process_current_events(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.show_information_events)
    cursor.execute("SELECT name FROM events WHERE datetime(registration_expire_date) > datetime('now','+3 hours')")
    rows = cursor.fetchall()
    if len(rows) > 0:
        buttons = [KeyboardButton(text=row[0]) for row in rows]
        buttons_back = KeyboardButton(text="Назад в меню")
        keyboard = ReplyKeyboardMarkup(keyboard=[[button] for button in buttons] 
                                                + [[buttons_back]], resize_keyboard=True, one_time_keyboard=False)
        await message.answer("Выберите мероприятие для просмотра информации о нём:", reply_markup=keyboard)
    else:
        await message.answer("На данный момент нет текущих мероприятий")
        await state.set_state(RegistrationState.opening_menu)


@registration_router.message(F.text != "Назад в меню", StateFilter(RegistrationState.show_information_events))
async def process_registration(message: Message, state: FSMContext):
    event_name = message.text
    cursor.execute("SELECT * from events where name = ?",(event_name,))
    event_info = cursor.fetchone()
    response_message = f"<b>Имя мероприятия:</b> {event_info[0]}\n" \
                           f"<b>Дата проведения:</b> {event_info[1]}\n" \
                           f"<b>Место проведения:</b> {event_info[2]}\n" \
                           f"<b>Квота:</b> {event_info[3]}\n" \
                           f"<b>Информация:</b> {event_info[4]}\n" \
                           f"<b>Детали участия в мероприятии:</b> {event_info[5]}\n" \
                           f"<b>Дата истечения регистрации:</b> {event_info[6]}\n" \
                           f"<b>Количество очков:</b> {event_info[7]}"
    await message.answer(response_message,parse_mode=ParseMode.HTML)
    
@registration_router.message(F.text == "Назад в меню", StateFilter(RegistrationState.show_information_events))
async def go_back_to_events_menu(message: Message, state: FSMContext):
    admin_id_1 = int(os.getenv("ADMIN_ID_1"))
    admin_id_2 = int(os.getenv("ADMIN_ID_2"))
    if not message.from_user.id in [admin_id_1,admin_id_2]:
        await state.set_state(RegistrationState.opening_menu)
        await message.answer(f"Вы вернулись в меню", reply_markup=button_variety_simple)
    else:
        await state.set_state(RegistrationState.opening_menu)
        await message.answer(f"Вы вернулись в меню", reply_markup=button_variety)



           
@registration_router.message(F.text == "Добавить мероприятие",StateFilter(RegistrationState.opening_menu))
async def call_data(message:Message,state:FSMContext):
    await state.set_state(RegistrationState.add_event)
    await message.answer(text='<b>Введите название мероприятия:</b>',reply_markup = ReplyKeyboardRemove(),parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_name_event) 
 
                

#ввод названия о мероприятии
@registration_router.message(StateFilter(RegistrationState.fill_name_event))
async def process_name_event_sent(message: Message, state: FSMContext):
    await state.update_data(name_event=message.text)
    await message.answer(text='<b>Введите дату мероприятия в формате ДД.ММ.ГГ (Например, 12.01.2004):</b>',parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_date_event)






@registration_router.message(StateFilter(RegistrationState.fill_date_event))
async def process_date_event_sent(message: Message, state: FSMContext):
    await state.update_data(date_event=message.text)
    await message.answer(text='<b>Введите место мероприятия:</b>',parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_place_event)


@registration_router.message(StateFilter(RegistrationState.fill_place_event))
async def process_date_event_sent(message: Message, state: FSMContext):
    await state.update_data(place_event=message.text)
    await message.answer(text='<b>Введите квоту мероприятия:</b>',parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_kvota)

    
    
#ввод квоты
@registration_router.message(StateFilter(RegistrationState.fill_kvota),lambda x: x.text.isdigit())
async def process_mid_name_sent(message: Message, state: FSMContext):
    await state.update_data(kvota=message.text)
    await message.answer(text='<b>Введите информацию о мероприятии:</b>',parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_info_event)
    
#неправильный ввод квоты
@registration_router.message(StateFilter(RegistrationState.fill_kvota))
async def warning_not_kvota_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на квоту мероприятия\n\n'
             'Пожалуйста, введите число, которое будет обозначать квоту на мероприятие\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


#ввод информации
@registration_router.message(StateFilter(RegistrationState.fill_info_event))
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await message.answer(text='<b>Введите детали участия в мероприятии (постоять у стендах, просто сфотографироваться):</b>',parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_details_event)


#ввод деталей
@registration_router.message(StateFilter(RegistrationState.fill_details_event))
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(details=message.text)
    await message.answer(text='<b>Введите дату истечения регистрации в формате год-месяц-число час:минута:секунда (например, 2024-02-20 16:00:00):</b>',parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_registration_expire_date)
    

@registration_router.message(StateFilter(RegistrationState.fill_registration_expire_date))
async def process_mid_name_sent(message: Message, state: FSMContext):
    await state.update_data(expire_data=message.text)
    await message.answer(text='<b>Введите количество очков за участие в мероприятии:</b>',parse_mode=ParseMode.HTML)
    await state.set_state(RegistrationState.fill_points)

    

#ввод группы
@registration_router.message(StateFilter(RegistrationState.fill_points), lambda x: x.text.isdigit())
async def process_group_sent(message: Message, state: FSMContext):
    await state.update_data(points=message.text)
    data = await state.get_data()
    name_event = data.get("name_event")
    date_event = data.get("date_event")
    place_event = data.get("place_event")
    kvota = data.get("kvota")
    info = data.get("info")
    details = data.get("details")
    expire_data = data.get("expire_data")
    points = data.get("points")
    cursor.execute("SELECT event_id FROM events WHERE name = ?", (name_event,))
    event_id = cursor.fetchone()
    message.answer(text = f"EVENT_ID:{event_id}")
    if event_id is None:
        # Вызов функции для добавления данных в базу данных
        cursor.execute('''
         INSERT INTO events (name, date, place, kvota, info, details, registration_expire_date, points)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
     ''', (name_event, date_event, place_event, kvota, info, details, expire_data, points))
        conn.commit()
        await state.set_state(RegistrationState.opening_menu)
        await message.answer(
            text='Ваше мероприятие сохранено!\n\n'
                 'Вы вышли из процесса добавления', reply_markup=button_variety
        )
    else:
        await state.set_state(RegistrationState.opening_menu)
        await message.answer("Такое меропрятие было уже добавлено.", reply_markup=button_variety)


    
#неправильный ввод количества очков
@registration_router.message(StateFilter(RegistrationState.fill_points))
async def warning_not_mid_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на количество очков за мероприятии\n\n'
             'Пожалуйста, введите число, которое будет обозначать количество очков за участие в мероприятии\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel')



#ввод фамилии
'''registration_router.message(StateFilter(FSMFillForm.fill_surname), F.text.isalpha())
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
   
'''
    
