from aiogram.dispatcher.filters.state import StatesGroup, State

class Registration(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()

class ChangeData(StatesGroup):
    Q1 = State()
    Q2 = State()
