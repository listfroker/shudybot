from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from data.config import admins
from handlers.admins.menu import admin_main_menu
from keyboards.default.main_menu import kb_main_menu, back
from keyboards.inline.callback_datas import util_callback
from keyboards.inline.change_menu import choice, choice1
from loader import dp, db, bot
from states.menu import Menu
from states.reg import ChangeData


@dp.message_handler(text = "Перейти в головне меню")
async def main_menu(message: types.Message):
    await message.answer("Оберіть потрібний розділ, натиснувши кнопку нижче👇", reply_markup=kb_main_menu)


#Review Menu  и выход из него + реакция на оставленный отзыв
@dp.message_handler(text = "Залишити відгук📢")
async def review_menu(message: types.Message):
    await message.answer("Напишіть ваш відгук:",reply_markup=back)
    await Menu.Review_Menu.set()

@dp.message_handler(text = "Назад", state=Menu.Review_Menu)
async def back_to_menu(message: types.Message, state: FSMContext):
    if message.from_user.id in admins:
        await state.finish()
        await admin_main_menu(message)
    else:
        await state.finish()
        await main_menu(message)

@dp.message_handler(state=Menu.Review_Menu)
async def enter_review(message:types.Message, state: FSMContext):
    answer = message.text
    user = db.select_user(id = message.from_user.id)
    print(user)
    db.add_review(user_id = message.from_user.id, Name=user[2], nickname = message.from_user.username, baby_name=user[3], review=answer)
    await message.answer("Дякую!")
    await bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEH0n9j8zk1bM8IzhETea9TRZ1OfawFFQACEioAAhjSmUsleKP1kMbq7i4E")
    for admin in admins:
        await bot.send_message(admin, "Надійшов новий відгук! \nПеревірте відповідну вкладку на панелі адміна")
    if message.from_user.id in admins:
        await state.finish()
        await admin_main_menu(message)
    else:
        await state.finish()
        await main_menu(message)




#Изменение данных пользователя
#Реакция на использование кнопки из меню
@dp.message_handler(text = "Змінити данні🔄")
async def change_settings(message: types.Message):
    user = db.select_user(id = message.from_user.id)
    if user[3] == None:
        text = [
            "Це налаштування вашого профілю:",
            f"Ваше ім'я: {user[2]}",
            "В нас займаєтесь Ви",
            "<b>Щоб змінити ваші данні - використовуйте кнопки нижче</b>"
        ]
        await message.answer("\n".join(text), reply_markup=choice1, parse_mode="HTML")
    else:
        text = [
            "Це налаштування вашого профілю:",
            f"Ваше ім'я: {user[2]}",
            f"В нас займається Ваша дитина - {user[3]}",
            "<b>Щоб змінити ваші данні - використовуйте кнопки нижче</b>"
        ]
        await message.answer("\n".join(text), reply_markup=choice, parse_mode="HTML")





@dp.message_handler(state=ChangeData.Q1)
async def entername_menu(message: types.Message, state: FSMContext):
    answer = message.text
    db.update_user_name(name=answer, id=message.from_user.id)
    user = db.select_user(id = message.from_user.id)
    print(user)
    await message.answer(f"Ім'я змінено успішно на {answer}!✅")

    if message.from_user.id in admins:
        await state.finish()
        await admin_main_menu(message)
    else:
        await state.finish()
        await main_menu(message)

@dp.message_handler(state=ChangeData.Q2)
async def enterbabyname_menu(message: types.Message, state: FSMContext):
    answer = message.text
    db.update_baby_name(baby_name=answer, id=message.from_user.id)
    user = db.select_user(id = message.from_user.id)
    print(user)
    await message.answer(f"Ім'я дитини змінено успішно на {answer}!✅")
    if message.from_user.id in admins:
        await state.finish()
        await admin_main_menu(message)
    else:
        await state.finish()
        await main_menu(message)

#About studio

@dp.message_handler(text = "Про студію✨")
async def about_studio(message: types.Message):
    text = "🌟Вас вітає танцювальна студія Victory Dance Company🌟 \n\n" \
           "Ми раді, що ви завітали до нашого помічника, тут викладена основна інформація про студію:  \n\n" \
           "Наші соціальні мережі😊: \n<a href = 'https://www.facebook.com/victory.dance.companyy/'>FACEBOOK</a> \n" \
           "<a href = 'https://instagram.com/victory.dance.comp?igshid=YmMyMTA2M2Y='>INSTAGRAM</a> \n\n" \
           "Адреса нашого залу🗺️: <a href = 'https://goo.gl/maps/huAgHwRnyfLC4PpN7'>вулиця Марсельська 42, Одеса</a>\n\n" \
           "Номер телефону нашого тренера та телеграм📱: \n097 410 32 81\n<a href = 't.me/vicktooria_shu'>Вікторія Шувалова</a>\n"
    await message.answer(text, parse_mode="HTML")


#Реакция на кнопки
#Потом перенести в отдельный файл!!!!!!
@dp.callback_query_handler()
async def change_callback(call: CallbackQuery):
    if call.data == "user_name":
        await call.answer(cache_time=60)
        await call.message.answer("Будь ласка, введіть нове ім'я користувача:", reply_markup=ReplyKeyboardRemove())
        await ChangeData.Q1.set()
    elif call.data == "baby_name":
        await call.answer(cache_time=60)
        await call.message.answer("Будь ласка, введіть нове ім'я дитини:", reply_markup=ReplyKeyboardRemove())
        await ChangeData.Q2.set()
    elif call.data == "one":
        await call.message.answer("За бажанням, Ви можете конкретно описати, що Вам не сподобалося")
        db.update_month_mark(user_id=call.from_user.id, mark="1")
        await Menu.BadMark_Menu.set()
    elif call.data == "two":
        await call.message.answer("За бажанням, Ви можете конкретно описати, що Вам не сподобалося")
        db.update_month_mark(user_id=call.from_user.id, mark="2")
        await Menu.BadMark_Menu.set()
    elif call.data == "three":
        await call.message.answer("За бажанням, Ви можете конкретно описати, що Вам не сподобалося")
        db.update_month_mark(user_id=call.from_user.id, mark="3")
        await Menu.BadMark_Menu.set()
    elif call.data == "four":
        await call.message.answer("За бажанням, Ви можете написати, щоб ви ще хотіли бачити на заняттях")
        db.update_month_mark(user_id=call.from_user.id, mark="4")
        await Menu.GoodMark_Menu.set()
    elif call.data == "five":
        await call.message.answer("За бажанням, Ви можете написати, щоб ви ще хотіли бачити на заняттях")
        db.update_month_mark(user_id=call.from_user.id, mark="5")
        await Menu.GoodMark_Menu.set()


@dp.message_handler(state = Menu.BadMark_Menu)
async def badmark_explanation(message: types.Message, state: FSMContext):
    answer = message.text
    user = db.select_user(id=message.from_user.id)
    db.add_month_review(Name = user[2], nickname=user[4], baby_name=user[3], month_review=answer, user_id=user[0])
    await message.answer("Дякую за ваш відгук!❤️\nМи намагатимемося зробити ваш майбутній досвід тренувань у нашій студії краще\nБажаю гарного дня😊")
    if message.from_user.id in admins:
        await state.finish()
        await admin_main_menu(message)
    else:
        await state.finish()
        await main_menu(message)

@dp.message_handler(state=Menu.GoodMark_Menu)
async def goodmark_explanation(message:types.Message, state: FSMContext):
    answer = message.text
    user = db.select_user(id=message.from_user.id)
    db.add_month_review(Name=user[2], nickname=user[4], baby_name=user[3], month_review=answer, user_id=user[0])
    await message.answer("Дякую за ваш відгук!❤️\nМи дуже раді, що вам сподобалися тренування у нас☺️\nБажаю гарного дня😊")
    if message.from_user.id in admins:
        await state.finish()
        await admin_main_menu(message)
    else:
        await state.finish()
        await main_menu(message)











