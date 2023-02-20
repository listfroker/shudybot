import telebot
from telebot import types

import time


TOKEN = "5308655718:AAGUt0xaSAZTiMFEPHUFHxUkbqYcluKoDKg"
ADMIN_ID = '739690267'
FULLADMINID = "546049755"
# токен для бота

bot = telebot.TeleBot(TOKEN, parse_mode=None)

name = ""
childName = ""
complaint = ""
user_mailing = True
in_comp_menu = False
in_feedback_menu = False
in_feedback_menu1 = False
month_feedback = None
chat_id = 0
ids = open('ids.txt', 'r')
userIds = set ()
for line in ids:
    userIds.add(line.strip())
ids.close()




@bot.message_handler(commands=['start'])
# приветствие + начало регистрации
def welcome(message):
    ids = open('ids.txt', 'r')
    userIds = set()
    for line in ids:
        userIds.add(line.strip())
    ids.close()
    if not str(message.from_user.id) in userIds:
        ids = open('ids.txt', 'a')
        ids.write(str(message.from_user.id) + "\n")
        userIds.add(message.from_user.id)
    global chat_id
    chat_id = message.from_user.id
    bot.reply_to(message, f"Добрий день, {message.from_user.first_name}, мене звати Shudy!\nЯ бот-помічник студії танцю VDC😊", parse_mode='html')
    time.sleep(1)
    inMarkup = types.InlineKeyboardMarkup()
    inMarkup.add(types.InlineKeyboardButton('Перейти в головне меню😉', callback_data='choice1'))
    bot.send_message(message.from_user.id,"Щомісяця я списуватимусь з вами для того, щоб запитати у вас про тренування у VDC та покращити якість занять у нашій студії 🙂 ",reply_markup=inMarkup)
    bot.send_message(FULLADMINID, f"Был зарегистрирован новый пользователь!\n Имя/Фамилия в телеграм: {message.from_user.first_name} {message.from_user.last_name}\n "
                               f"Никнейм: @{message.from_user.username}\n ")
    bot.send_message(ADMIN_ID,
                     f"Был зарегистрирован новый пользователь!\n Имя/Фамилия в телеграм: {message.from_user.first_name} {message.from_user.last_name}\n "
                     f"Никнейм: @{message.from_user.username}\n ")


@bot.message_handler(commands=['secret'])
def ponos(message):
    if message.from_user.id == 546049755 or message.from_user.id == 739690267:
        for user in userIds:
            bot.send_message(user, message.text[message.text.find(' '):])
    else:
        bot.send_message(message.from_user.id, "Нажаль, цю команду можуть використовувати лише адміністратори боту😥")


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    try:
        if callback.message:
            if callback.data == "choice1":
                menu1(callback)
                bot.answer_callback_query(callback_query_id=callback.id, text = 'Велике прохання🥺\n \nБудь ласка, підійдіть до опросів серйозно, бо від цього залежить якість тренувань у нашій студії!', show_alert=True)
                # callback.answer(text = 'Велике прохання🥺\n \n Будь ласка, підійдіть до опросів серйозно, бо від цього залежить якість тренувань у нашій студії!', show_alert = True)
    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=['text'])
def menu(message):
    global in_comp_menu
    global user_mailing
    global in_feedback_menu
    global in_feedback_menu1
    global month_feedback
    global mark
    # Завершение рассылки, замена переменной
    # if (message.text == "Завершити розсилку⛔"):
    #     bot.send_message(message.from_user.id, "Ви зупинили розсилку⛔, але все ще можете відправляти відгуки за кнопкою")
    #     user_mailing = False
    #     menu2(message)
    # elif (message.text == "Відновити розсилку✅"):
    #     bot.send_message(message.from_user.id, "Ви відновили розсилку✅")
    #     user_mailing = True
    #     menu1(message)
    if (message.text == "Скарги/Пропозиції👂"):
        in_comp_menu = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Назад🔙")
        markup.add(but1)
        bot.send_message(message.from_user.id, "Докладно опишіть вашу пропозицію/скаргу, по бажанню можете вказати ім'я дитини, яка тренується в нас", reply_markup=markup)
    elif (message.text == "Назад🔙"):
        in_comp_menu = False
        if (user_mailing == True):
            menu1(message)
        elif (user_mailing == False):
            menu2(message)
    elif (message.text == 'test'):
        feedback(message)
    elif (in_comp_menu == True):
        comp = message.text
        print(message.from_user.username + " написал отзыв: " + comp)
        bot.send_message(FULLADMINID, f"Оставлен новый отзыв!\nИмя/Фамилия: "
                                      f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                      f"Никнейм: @{message.from_user.username}\nТекст отзыва: {comp}")
        bot.send_message(ADMIN_ID, f"Оставлен новый отзыв!\nИмя/Фамилия: "
                                      f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                      f"Никнейм: @{message.from_user.username}\nТекст отзыва: {comp}")

        bot.reply_to(message, "Дякую за ваш відгук!")
        in_comp_menu = False
        if (user_mailing == True):
            menu1(message)
        elif (user_mailing == False):
            menu2(message)

    elif (message.text == "Про студію✨"):
        text = "🌟Вас вітає танцювальна студія Victory Dance Company🌟 \n\nМи раді, що ви завітали до нашого помічника, тут викладена основна інформація про студію:  \n\nНаші соціальні мережі😊: \n[FACEBOOK](https://www.facebook.com/victory.dance.companyy/) \n[INSTAGRAM](https://instagram.com/victory.dance.comp?igshid=YmMyMTA2M2Y=) \n\n" \
               "Адреса нашого залу🗺️: [вулиця Марсельська 42, Одеса](https://goo.gl/maps/huAgHwRnyfLC4PpN7)\n\nНомер телефону нашого тренера та телеграм📱: \n097 410 32 81\n[Вікторія Шувалова](t.me/vicktooria_shu)\n"


        bot.send_message(message.from_user.id, text, parse_mode='MarkdownV2', disable_web_page_preview = True)
    else:
        if ( in_feedback_menu == True):

            if message.text == "1" or message.text == "2" or message.text == "3":
                mark = message.text
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                but1 = types.KeyboardButton("Пропустити")
                markup.add(but1)
                bot.send_message(message.from_user.id, "Уточніть, будь ласка, що Вам не сподобалося:", reply_markup=markup)
                in_feedback_menu1 = True

            elif message.text == "Пропустити":
                print(f'{message.from_user.username} ответил на рассылку поставив : {mark}')
                bot.send_message(message.from_user.id, "Дякую за ваш відгук!")
                in_feedback_menu1 = False
                in_feedback_menu = False
                bot.send_message(FULLADMINID, f"Оставлен ответ на ежемесячную рассылку!\nИмя/Фамилия: "
                                              f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                              f"Никнейм: @{message.from_user.username}\nОценка за предыдущий месяц: {mark}")
                bot.send_message(ADMIN_ID, f"Оставлен ответ на ежемесячную рассылку!\nИмя/Фамилия: "
                                              f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                              f"Никнейм: @{message.from_user.username}\nОценка за предыдущий месяц: {mark}")

                menu1(message)

            elif in_feedback_menu1 == True:
                month_feedback = message.text
                print(f'{message.from_user.username} ответил на рассылку поставив : {mark} и написав комментарий: {month_feedback}')
                bot.send_message(message.from_user.id, "Дякую за ваш відгук! Постараємося наступного місяця зробити ваші тренування ще краще!")
                in_feedback_menu1 = False
                in_feedback_menu = False
                bot.send_message(FULLADMINID, f"Оставлен новый ответ на ежемясячную рассылку!\nИмя/Фамилия: "
                                              f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                              f"Никнейм: @{message.from_user.username}\nОценка за предыдущий месяц: {mark}\nТекст ответа: {month_feedback}")
                bot.send_message(ADMIN_ID, f"Оставлен новый ответ на ежемясячную рассылку!\nИмя/Фамилия: "
                                              f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                              f"Никнейм: @{message.from_user.username}\nОценка за предыдущий месяц: {mark}\nТекст ответа: {month_feedback}")

                menu1(message)

            elif message.text == "4" or message.text == "5":
                mark = message.text
                print(f'{message.from_user.username} ответил на рассылку и поставил оценку: {mark}')

                bot.send_message(message.from_user.id, "Ми раді, що вам сподобалися тренування! Гарного дня!")
                in_feedback_menu1 = False
                in_feedback_menu = False

                bot.send_message(FULLADMINID, f"Оставлен новый ответ на ежемесячную рассылку!\nИмя/Фамилия: "
                                              f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                              f"Никнейм: @{message.from_user.username}\nОценка за предыдущий месяц: {mark}")
                bot.send_message(ADMIN_ID, f"Оставлен новый ответ на ежемесячную рассылку!\nИмя/Фамилия: "
                                              f" {message.from_user.first_name} {message.from_user.last_name}\n"
                                              f"Никнейм: @{message.from_user.username}\nОценка за предыдущий месяц: {mark}")

                menu1(message)

        else:
            bot.reply_to(message, "Нажаль я не розумію вас. Будь ласка, використовуйте кнопки, які розміщенні трохи нижче")

def feedback(message):
    global user_mailing
    global in_feedback_menu
    in_feedback_menu = True
    ids = open('ids.txt', 'r')
    userIds = set()
    for line in ids:
        userIds.add(line.strip())
    ids.close()
    if not str(message.from_user.id) in userIds:
        ids = open('ids.txt', 'a')
        ids.write(str(message.from_user.id) + "\n")
        userIds.add(message.from_user.id)
    if user_mailing == True:
        for user in userIds:
            bot.send_message(user, "Добрий день! Настав час щомісячного опитування🤗\nБудь ласка, перейдіть за посиланням та дайте відповідь буквально на пару запитань - https://forms.gle/PUNH7a9vD7YrXAnX7\nБудемо дуже вдячні!")





def menu1(message):
    global user
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but2 = types.KeyboardButton("Скарги/Пропозиції👂")
    but3 = types.KeyboardButton("Про студію✨")
    markup.add(but2, but3)
    bot.send_message(message.from_user.id, 'Ви в головному меню', reply_markup=markup)

def menu2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but2 = types.KeyboardButton("Скарги/Пропозиції👂")
    but3 = types.KeyboardButton("Про студію✨")
    markup.add(but2, but3)
    bot.send_message(message.from_user.id, 'Ви в головному меню', reply_markup=markup)

def menu11():
    global user
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but2 = types.KeyboardButton("Скарги/Пропозиції👂")
    but3 = types.KeyboardButton("Про студію✨")
    markup.add(but2, but3)
    bot.send_message(user, 'Ви в головному меню', reply_markup=markup)




bot.infinity_polling()
