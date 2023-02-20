import json

from handlers.admins.broadcast import broadcast
from keyboards.default.broadcast import m_broadcast_kb
from keyboards.inline.inline_broadcast import month_broadcast_kb
from loader import Bot, db
from states.menu import Menu
from data import config


async def month_broadcast(bot: Bot, config: config):
    users = db.select_all_users_id()
    users_massive = [row[0] for row in users]
    text = "Привіт, настав час щомісячного опитування!\n Я хотів би дізнатися, чи сподобалися тобі тренування в нашій студії. Будь ласка, оціни тренування у нашій школі від 1 до 5: \n"

    await broadcast(bot=bot, users=users_massive, text=text, reply_markup=month_broadcast_kb)



