import sqlite3


from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.config import admins
from keyboards.default.to_menu import to_menu
from loader import dp, db, bot
from states.reg import Registration


@dp.message_handler(CommandStart(), user_id = admins)
async def bot_start(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    user = db.select_user(id=message.from_user.id)

    await bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEH0ntj8zhu-BhYd9AmTDBUzODCDwthYAAC_CsAAomCmEs3tSBs_jhz8S4E")
    await message.answer(f"Добрий день, мене звати Shudy!\nЯ бот-помічник студії танцю VDC😊\nТут Ви можете залишати відгуки про досвід занять в нашій студії!\nІноді я робитиму оголошення та проводитиму опитування📢\nОбіцяю не докучати😉")
    if user == None:
        try:
            db.add_user(id=message.from_user.id, nickname=message.from_user.username, Name= name)
        except sqlite3.IntegrityError as err:
            print(err)
        await message.answer("Давайте познайомимось🙂\nБудь ласка, напишіть Ваше ім'я")
        await Registration.Q1.set()
    else:
        print(user)
        await message.answer("Я вас пам'ятаю, Ви є адміністратором цього боту. В головному меню ви знайдете додаткову кнопку для управління ботом", reply_markup=to_menu)
        await state.finish()

@dp.message_handler(state=Registration.Q1, user_id = admins)
async def first_quest(message: types.Message, state: FSMContext):
    answer = message.text
    db.update_user_name(answer, message.from_user.id)
    await message.answer(
        "\n".join(["Приємно познайомитися!",
                   "Ви є адміністратором боту",
                   "У вас буде додаткова кнопка для управління ботом"]
                  ), reply_markup=to_menu
    )
    await state.finish()