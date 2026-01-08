from aiogram.fsm.state import State, StatesGroup

class UserFSM(StatesGroup):
    waiting_for_file = State()
    