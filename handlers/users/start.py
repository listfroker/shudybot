import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from data.config import admins
from keyboards.default.is_baby import is_baby
from keyboards.default.to_menu import to_menu
from loader import dp, db, bot

from states.reg import Registration


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    user = db.select_user(id=message.from_user.id)

    await bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEH0ntj8zhu-BhYd9AmTDBUzODCDwthYAAC_CsAAomCmEs3tSBs_jhz8S4E")
    await message.answer('Добрий день, мене звати Shudy!\nЯ бот-помічник студії танцю VDC😊\nТут Ви можете залишати відгуки про досвід занять в нашій студії!\nІноді я робитиму оголошення та проводитиму опитування📢\nОбіцяю не докучати😉')
    if user == None:
        try:
            db.add_user(id=message.from_user.id, Name= name, nickname=message.from_user.username)
        except sqlite3.IntegrityError as err:
            print(err)
        await message.answer("Давайте познайомимось🙂\nБудь ласка, напишіть Ваше ім'я")
        await Registration.Q1.set()
    else:
        print(user)
        await message.answer("Я пам'ятаю Вас👍, заходьте в головне меню", reply_markup=to_menu)
        await state.finish()



@dp.message_handler(state=Registration.Q1)
async def first_quest(message: types.Message):
    answer = message.text
    db.update_user_name(answer, message.from_user.id)
    await message.answer(
        "\n".join(["Приємно познайомитися!",
                   "Якщо в нас займається Ваша дитина, напишіть, також, її ім'я",
                   "Або натисніть кнопку нижче"]
                  ), reply_markup=is_baby
    )
    await Registration.Q2.set()

@dp.message_handler(state=Registration.Q2)
async def second_quest(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Пропустити":
        await message.answer("Дякую за реєстрацію💞 \nТепер Вам буде доступно меню боту✅\nЯкщо ви неправильно вказали дані під час реєстрації - їх можна легко змінити, натиснувши, на відповідну кнопку в меню!", reply_markup=to_menu)
        await state.finish()
        print(db.select_all_users())
        for admin in admins:
            bot.send_message(admin, "Зареєструвався новий користувач!\nДля перевірки зайдіть в Адмін панель -> Усі юзери")
    else:
        db.update_baby_name(answer, message.from_user.id)
        await message.answer("Дякую за реєстрацію💞 \nТепер Вам буде доступно меню боту✅\nЯкщо ви неправильно вказали дані під час реєстрації - їх можна легко змінити, натиснувши, на відповідну кнопку в меню!", reply_markup=to_menu)
        await state.reset_state()
        print(db.select_all_users())
        for admin in admins:
            bot.send_message(admin, "Зареєструвався новий користувач!\nДля перевірки зайдіть в Адмін панель -> Усі юзери")
