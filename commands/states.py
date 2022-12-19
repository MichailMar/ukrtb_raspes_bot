from aiogram.fsm.state import StatesGroup, State

class GetGroup(StatesGroup):

    type = State()
    group = State()
    time = State()