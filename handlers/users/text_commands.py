from aiogram import types
import keyboards as kb
from loader import dp
from config import ADMINS
from utils.manage_users import get_users

# Обработчик текстовых команд
@dp.message_handler(content_types=['text'])
async def text(message: types.message):
    command = message.text.strip()

    if command == 'Пользователи':
        if message.from_user.id in ADMINS:
            await message.answer('<b>Выберите:</b>', reply_markup=kb.users)
        else:
            await message.answer('Вы не Администратор!', reply_markup=kb.menu)

        await message.delete()

    elif command == 'Другое':
        if message.from_user.id in ADMINS or message.from_user.id in get_users():
            await message.answer('Вы пользователь!')
        else:
            await message.answer('Вы не пользователь!')

    else:
        await message.answer('Неизвестная команда!')
