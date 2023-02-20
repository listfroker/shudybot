import os
import sqlite3
from datetime import datetime, date

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from prettytable import PrettyTable

from data.config import admins
from handlers.admins.broadcast import broadcast
from keyboards.default.admin_panel import admin_panel_kb
from keyboards.default.main_menu import kb_main_menu_admin, back
from loader import dp, db, bot
from states.menu import Menu


@dp.message_handler(text = "Перейти в головне меню", user_id = admins)
async def admin_main_menu(message: types.Message):
    await message.answer("Оберіть потрібний розділ, натиснувши кнопку нижче👇", reply_markup=kb_main_menu_admin)


#Admin panel

@dp.message_handler(text = "Адмін панель", user_id = admins)
async def admin_panel(message: types.Message):
    await message.answer("Ви в адмін панелі:", reply_markup=admin_panel_kb)


@dp.message_handler(text = "Назад")
async def cancel(message: types.Message):
    await admin_main_menu(message)

#Message broadcast
@dp.message_handler(text = "Розсилка повідомлень")
async def message_broadcasting(message: types.Message):
    await message.answer("Введіть повідомлення, яке бажаєте надіслати користувачам бота:", reply_markup=back)
    await Menu.Broadcast_Menu.set()


@dp.message_handler(state=Menu.Broadcast_Menu)
async def broadcast_proceeding(message: types.Message, state: FSMContext):
    text = message.text
    if text == "Назад":
        await state.finish()
        await admin_panel(message)
    else:
        users = db.select_all_users_id()
        users_massive = [row[0] for row in users]
        await broadcast(bot=bot, users=users_massive, text=text, reply_markup=None)
        await message.answer("Розсилка успішна!")
        await state.finish()
        await admin_panel(message)


@dp.message_handler(text = "Подивитися відгуки")
async def show_reviews(message : types.Message):
    # reviews = db.select_all_reviews()
    # table = PrettyTable()
    # table.field_names = ["id", "added_at", "user_id", "Name", "baby_name", "review"]
    # for row in reviews:
    #     table.add_row(row)
    # await message.answer(table.get_string())
    timestamp = date.today()
    conn = sqlite3.connect('data/main.db')
    df = pd.read_sql_query("SELECT * FROM Reviews", conn)
    df.to_excel(f'Reviews_{timestamp}.xlsx', index=False)
    with open(f'Reviews_{timestamp}.xlsx', 'rb') as file:
        await bot.send_document(message.from_user.id, file)
    os.remove(f"Reviews_{timestamp}.xlsx")


@dp.message_handler(text="Усі юзери")
async def all_users(message: types.Message):
    timestamp = date.today()
    conn = sqlite3.connect('data/main.db')
    df = pd.read_sql_query("SELECT * FROM Users", conn)
    df.to_excel(f'Users_{timestamp}.xlsx', index=True)
    with open(f'Users_{timestamp}.xlsx', 'rb') as file:
        await bot.send_document(message.from_user.id, file)
    os.remove(f"Users_{timestamp}.xlsx")


@dp.message_handler(text="Щомісячні відгуки")
async def all_users_month_review(message: types.Message):
    timestamp = date.today()
    conn = sqlite3.connect('data/main.db')
    df = pd.read_sql_query("SELECT * FROM Month_Reviews", conn)
    df.to_excel(f'Month_Reviews_{timestamp}.xlsx', index = True)
    with open(f'Month_Reviews_{timestamp}.xlsx', 'rb') as file:
        await bot.send_document(message.from_user.id, file)
    os.remove(f"Month_Reviews_{timestamp}.xlsx")








