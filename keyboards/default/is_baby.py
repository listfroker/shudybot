from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

is_baby = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Пропустити")
        ]
    ], resize_keyboard=True
)