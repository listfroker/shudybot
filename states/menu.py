from aiogram.dispatcher.filters.state import StatesGroup, State


class Menu(StatesGroup):
    To_Main_Menu = State()
    Main_Menu = State()
    Review_Menu = State()
    Broadcast_Menu = State()
    BadMark_Menu = State()
    GoodMark_Menu = State()
