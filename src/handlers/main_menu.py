from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command,CommandStart,StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from src.keyboards.reply import button


menu_router = Router()


@menu_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот, который регистрирует людей в системе\n'
             'Чтобы перейти к заполнению анкеты - '
             'Нажмите на кнопку "Зарегистрироваться на мероприятие"\n\n'
             'Для просмотра списка зарегистрированных - введите команду /showdata\n\n'
             'Для отмены регистрации - введите команду /cancel',
        reply_markup=button
    )

@menu_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из процесса регистрации\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'нажмите на кнопку "Зарегистрироваться на мероприятие"'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

@menu_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'нажмите на кнопку "Зарегистрироваться на мероприятие"'
    )
