from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

m_broadcast_kb = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton("1"),
            KeyboardButton("2"),
            KeyboardButton("3"),
            KeyboardButton("4"),
            KeyboardButton("5"),
        ]
    ], resize_keyboard= True
)