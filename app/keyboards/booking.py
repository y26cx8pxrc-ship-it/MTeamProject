from datetime import datetime, timedelta

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def get_date_keyboard():
    keyboard = []

    for i in range(3):
        date = datetime.now() + timedelta(days=i)

        date_text = date.strftime("%d.%m.%Y")

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=date_text,
                    callback_data=f"date_{date_text}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


from app.database.database import count_bookings
from app.config import SLOT_LIMIT


from app.database.database import count_bookings
from app.config import SLOT_LIMIT


async def get_time_keyboard(date: str):
    times = [
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00"
    ]

    keyboard = []

    for time in times:
        count = await count_bookings(date, time)

        text = f"{time} ({count}/{SLOT_LIMIT})"

        if count >= SLOT_LIMIT:
            callback = "full"
        else:
            callback = f"time_{time}"

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def get_confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить бронирование ✅",
                    callback_data="confirm_booking"
                )
            ]
        ]
    )


def get_cancel_keyboard(bookings):
    keyboard = []

    for booking_id, date, time in bookings:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{date} {time} ❌",
                    callback_data=f"cancel_{booking_id}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

def get_admin_cancel_keyboard(bookings):
    keyboard = []

    for booking_id, user, date, time in bookings:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{user} | {date} {time} ❌",
                    callback_data=f"admin_cancel_{booking_id}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )