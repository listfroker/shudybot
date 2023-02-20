from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

month_broadcast_kb = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text = "1", callback_data="one"),
            InlineKeyboardButton(text = "2", callback_data = "two"),
            InlineKeyboardButton(text = "3", callback_data= "three"),
            InlineKeyboardButton(text = "4", callback_data= "four"),
            InlineKeyboardButton(text = "5", callback_data="five"),
        ]
    ]
)