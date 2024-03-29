from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.keyboards.reply import button


menu_router = Router()


@menu_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Это бот, предназаченный для работы c системой учёта достижений и активности студентов ИЦТМС на мероприятиях \n'
             'Нажмите на кнопку "Вход в систему" для запуска бота\n\n',
        reply_markup=button
    )

'''@menu_router.message(Command(commands='cancel'), ~StateFilter(default_state))
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

    )'''
