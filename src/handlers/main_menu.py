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
        text='Этот бот, который регистрирует людей в системе ИЦТМС\n'
             'Чтобы перейти к заполнению данных о себе - '
             'Нажмите на кнопку "Зарегистрироваться в системе\n\n'
             'Для добавления мероприятия в список мероприятий - нажмите на кнопку "Добавить мероприятие"\n\n'
             'Для отмены действия- введите команду /cancel',
        reply_markup=button
    )

@menu_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из процесса регистрации\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'нажмите на кнопку "Зарегистрироваться в системе"'
             'Чтобы снова добавить мероприятие -'
             'нажмите на кнопку "Добавить мероприятие"'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

@menu_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне процесса регистрации\n\n'

    )
