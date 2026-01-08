from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.lexicon import Buttons


def start_keyboard() -> ReplyKeyboardMarkup:
    start_button = KeyboardButton(text=Buttons.start)

    return ReplyKeyboardMarkup(
        keyboard=[
            [start_button],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )