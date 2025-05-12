# keyboards.py
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="JUP checker")],
        [KeyboardButton(text="KiloEx checker")],
        [KeyboardButton(text="Hyperlane checker")],
    ],
    resize_keyboard=True
)
