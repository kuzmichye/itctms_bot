from aiogram.filters import StateFilter
from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from src.states.fsm_states import FSMFillevent
from database.add import insert_event
from dotenv import load_dotenv
import os
import sqlite3


event_router = Router()

load_dotenv()
admin_id_1 = int(os.getenv("ADMIN_ID_1"))
admin_id_2 = int(os.getenv("ADMIN_ID_2"))

@event_router.message(F.text == "Добавить мероприятие",StateFilter(default_state))
async def call_data(message:Message,state:FSMContext):
    if not message.from_user.id in [admin_id_1,admin_id_2]:
        await message.answer(text='У вас нет доступа к этой функции')
        await state.clear()
    else:
        await message.answer(text='Пожалуйста, введите название мероприятия:')
        await state.set_state(FSMFillevent.fill_name_event)
    

#ввод названия о мероприятии
@event_router.message(StateFilter(FSMFillevent.fill_name_event))
async def process_name_event_sent(message: Message, state: FSMContext):
    await state.update_data(name_event=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите дату мероприятия в формате ДД.ММ.ГГ(Например, 12.01.2004):')
    await state.set_state(FSMFillevent.fill_date_event)






@event_router.message(StateFilter(FSMFillevent.fill_date_event))
async def process_date_event_sent(message: Message, state: FSMContext):
    await state.update_data(date_event=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите место мероприятия:')
    await state.set_state(FSMFillevent.fill_place_event)


@event_router.message(StateFilter(FSMFillevent.fill_place_event))
async def process_date_event_sent(message: Message, state: FSMContext):
    await state.update_data(place_event=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите квоту мероприятия:')
    await state.set_state(FSMFillevent.fill_kvota)

    
    
#ввод квоты
@event_router.message(StateFilter(FSMFillevent.fill_kvota),lambda x: x.text.isdigit())
async def process_mid_name_sent(message: Message, state: FSMContext):
    await state.update_data(kvota=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите информацию о мероприятии:')
    await state.set_state(FSMFillevent.fill_info_event)
    
#неправильный ввод квоты
@event_router.message(StateFilter(FSMFillevent.fill_kvota))
async def warning_not_kvota_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на квоту мероприятия\n\n'
             'Пожалуйста, введите число, которое будет обозначать квоту на мероприятие\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


#ввод информации
@event_router.message(StateFilter(FSMFillevent.fill_info_event))
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите детали участия в мероприятии(постоять у стендах, просто сфотографироваться):')
    await state.set_state(FSMFillevent.fill_details_event)


#ввод деталей
@event_router.message(StateFilter(FSMFillevent.fill_details_event))
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(details=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите дату истечения регистрации в формате (время и дата, например 23:59 09.02.2024):')
    await state.set_state(FSMFillevent.fill_registration_expire_date)
    

@event_router.message(StateFilter(FSMFillevent.fill_registration_expire_date))
async def process_mid_name_sent(message: Message, state: FSMContext):
    await state.update_data(expire_data=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите количество очков за участие в мероприятии:')
    await state.set_state(FSMFillevent.fill_points)

    

#ввод группы
@event_router.message(StateFilter(FSMFillevent.fill_points),lambda x: x.text.isdigit())
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
    
    conn = sqlite3.connect("src/itctms_system.db")
    cursor = conn.cursor()
   
    cursor.execute("SELECT * FROM students WHERE name=?", (name_event,))
    existing_event = cursor.fetchone()
    
    
    if existing_event:
        await message.answer("Мероприятие уже добавлено!")
        await state.clear()
    else:
        # Вызов функции для добавления данных в базу данных
        await insert_event(name_event,date_event,place_event,kvota,info,details,expire_data,points)
        await state.clear()
        await message.answer(
        text='Спасибо! Ваши данные сохранены!\n\n'
             'Вы вышли из процесса добавления'
        )
    
#неправильный ввод количества очков
@event_router.message(StateFilter(FSMFillevent.fill_points))
async def warning_not_mid_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на количество очков за мероприятии\n\n'
             'Пожалуйста, введите число, которое будет обозначать количество очков за участие в мероприятии\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )

