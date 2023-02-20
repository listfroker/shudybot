from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Залишити відгук📢"),
            KeyboardButton("Змінити данні🔄")
        ],
        [
            KeyboardButton("Про студію✨")
        ],

    ], resize_keyboard= True
)

kb_main_menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Залишити відгук📢"),
            KeyboardButton("Змінити данні🔄")
        ],
        [
            KeyboardButton("Про студію✨"),
            KeyboardButton("Адмін панель")
        ]
    ], resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Назад")
        ]
    ], resize_keyboard=True
)