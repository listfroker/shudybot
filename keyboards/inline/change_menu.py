from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import util_callback

choice = InlineKeyboardMarkup(row_width=3,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text="Змінити ім'я",
                                          callback_data = "user_name")
                                  ],
                                  [
                                      InlineKeyboardButton(
                                          text="Змінити ім'я дитини",
                                          callback_data = "baby_name")
                                  ]
                              ])

choice1 = InlineKeyboardMarkup(row_width=3,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text="Змінити ім'я",
                                          callback_data = "user_name")
                                  ]
                              ])