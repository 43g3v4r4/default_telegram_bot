from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пользователи"),
            KeyboardButton(text="Другое"),
        ],
    ],
    resize_keyboard=True
)


users = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить пользователя',
                callback_data='add_user',
            )
        ],
        [
            InlineKeyboardButton(
                text='Удалить пользователя',
                callback_data='delete_user',
            )
        ],
    ]
)


back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='back',
            )
        ],
    ]
)
