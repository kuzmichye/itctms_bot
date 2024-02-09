from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)




button_sign = KeyboardButton(text = "Зарегистрироваться на мероприятие")

button = ReplyKeyboardMarkup(
    keyboard = [[button_sign]],
    resize_keyboard = True,
    one_time_keyboard = True)
