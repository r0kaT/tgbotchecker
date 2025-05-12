from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    waiting_for_addresses_jup = State()
    waiting_for_addresses_kiloex = State()
    waiting_for_addresses_hyperlane = State()
