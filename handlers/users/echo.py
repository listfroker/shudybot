from aiogram import types
from loader import dp


@dp.message_handler()
async def bot_err(message: types.Message):
    await message.answer("Вибачте, але я Вас не розумію😢")
