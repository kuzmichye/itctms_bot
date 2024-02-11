from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)




button_sign = KeyboardButton(text = "Зарегистрироваться в системе")

button_sign_2 = KeyboardButton(text = "Добавить мероприятие")
button = ReplyKeyboardMarkup(
    keyboard = [[button_sign,button_sign_2]],
    resize_keyboard = True,
    one_time_keyboard = True)

