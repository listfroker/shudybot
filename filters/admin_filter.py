from aiogram import types
from loader import dp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters.builtin import BaseFilter
from data.config import admins

class IsAdmin(BaseFilter):
    def check(self, message: types.Message):
        return message.from_user.id in admins

dp.filters_factory.bind(IsAdmin())

@dp.message_handler(IsAdmin())
async def process_message(message: types.Message):
    await message.answer("This message was sent by an admin")

