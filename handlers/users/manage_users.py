from aiogram import types
from sqlalchemy import text

from db.database import sqlite_engine
from loader import dp
import keyboards as kb
from aiogram.dispatcher import FSMContext
from states.manage_users import Add_User, Delete_User


# Обработка inline кнопки "Добавить админа"
@dp.callback_query_handler(lambda c: c.data == 'add_user')
async def callback_button_add_user(callback_query: types.CallbackQuery, state: FSMContext):
    message = await dp.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Введите ID пользователя.\n'
             'Для получения id пришлите сообщение '
             'пользователя боту - @getmyid_bot',
        reply_markup=kb.back,
    )

    await state.update_data(message_id=message.message_id)
    await Add_User.Q1.set()


# Запрос на Add_User "Введите id пользователя"
@dp.message_handler(content_types=['text'], state=Add_User.Q1)
async def add_user(message: types.message, state: FSMContext):
    answer = message.text.strip()

    if answer.isdigit():
        with sqlite_engine.connect() as conn:
            res = conn.execute(text(f'SELECT * FROM users WHERE telegram_id = {answer}'))
            user = res.all()

        if user:
            await message.answer('У пользователя уже есть права!')
        else:
            with sqlite_engine.connect() as conn:
                conn.execute(text(f'INSERT INTO users (telegram_id) VALUES ({answer})'))
                conn.commit()
            await message.answer(f'Пользователю <b>{answer}</b> выданы права!')

        message_id_dict = await state.get_data()
        message_id = message_id_dict['message_id']

        await dp.bot.edit_message_reply_markup(
            chat_id=message.from_user.id,
            message_id=message_id,
            reply_markup=None
        )

        await state.finish()

    else:
        await message.answer('ID состоит только из цифр.\n'
                             'Введите ID пользователя ')


# Обработка inline кнопки "Удалить админа"
@dp.callback_query_handler(lambda c: c.data == 'delete_user')
async def callback_button_delete_user(callback_query: types.CallbackQuery, state: FSMContext):
    message = await dp.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Введите ID пользователя, чтобы удалить.\n'
             'Для получения id пришлите сообщение пользователя боту - '
             '@getmyid_bot',
        reply_markup=kb.back,
    )

    await state.update_data(message_id=message.message_id)
    await Delete_User.Q1.set()


# Запрос на Delete_User "Введите id пользователя"
@dp.message_handler(content_types=['text'], state=Delete_User.Q1)
async def delete_user(message: types.message, state: FSMContext):
    answer = message.text.strip()

    if answer.isdigit():
        with sqlite_engine.connect() as conn:
            conn.execute(text(f'DELETE FROM users WHERE telegram_id = {answer}'))
            conn.commit()

        await message.answer(f'Пользователь <b>{answer}</b> удалён!')

        message_id_dict = await state.get_data()
        message_id = message_id_dict['message_id']

        await dp.bot.edit_message_reply_markup(
            chat_id=message.from_user.id,
            message_id=message_id,
            reply_markup=None
        )

        await state.finish()

    else:
        await message.answer('ID состоит только из цифр.\nВведите ID пользователя ')
