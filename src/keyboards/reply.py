from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton)




button_sign = KeyboardButton(text = "Вход в систему")

button = ReplyKeyboardMarkup(
    keyboard = [[button_sign]],
    resize_keyboard = True,
    one_time_keyboard = True)


button_1 = InlineKeyboardButton(text='Да', callback_data='yes_button_pressed')
keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[[button_1]])


button_event_not_expire = KeyboardButton(text = "Список текущих мероприятий")
registered_events = KeyboardButton(text="Мои мероприятия")
add_event = KeyboardButton(text = "Добавить мероприятие")
show_the_registered = KeyboardButton(text = "Списки зарегистрировавшихся")
show_the_info = KeyboardButton(text = "Посмотреть информацию о мероприятии" )
button_variety = ReplyKeyboardMarkup(
keyboard = [[button_event_not_expire],
                      [registered_events],
                      [show_the_registered],
                      [add_event],
                      [show_the_info]] ,resize_keyboard = True, one_time_keyboard = True)


button_variety_simple = ReplyKeyboardMarkup(
    keyboard = [[button_event_not_expire],
                [registered_events],
                [show_the_info]],         
    resize_keyboard = True,
    one_time_keyboard = True)



