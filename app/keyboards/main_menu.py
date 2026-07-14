from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.config import ADMINS


def get_main_menu(user_id: int):
    keyboard = [
        [
            KeyboardButton(text="Забронировать место 📚")
        ],
        [
            KeyboardButton(text="Мои бронирования 📖")
        ],
        [
            KeyboardButton(text="Помощь ℹ️")
        ]
    ]

    if user_id in ADMINS:
        keyboard.append(
            [
                KeyboardButton(text="Админка ⚙️")
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Что будем делать?"
    )