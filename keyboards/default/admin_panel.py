from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Розсилка повідомлень"),
            KeyboardButton("Подивитися відгуки")
        ],
        [
            KeyboardButton("Усі юзери"),
            KeyboardButton("Щомісячні відгуки")
        ],
        [
            KeyboardButton("Назад")
        ]
    ], resize_keyboard=True
)