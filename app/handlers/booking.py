from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from datetime import datetime

from app.database.database import (
    create_booking,
    cancel_booking,
    get_all_bookings,
    get_today_bookings
)

from app.database.users import get_user_id

from app.database.database import count_bookings

from app.config import SLOT_LIMIT

from app.keyboards.booking import (
    get_time_keyboard,
    get_confirm_keyboard,
    get_admin_cancel_keyboard
)

from app.config import ADMINS


router = Router()


class BookingState(StatesGroup):
    choosing_date = State()
    choosing_time = State()


# ======================
# USER BOOKING FLOW
# ======================

@router.callback_query(F.data.startswith("date_"))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    date = callback.data.replace("date_", "")

    await state.update_data(date=date)
    await state.set_state(BookingState.choosing_time)

    await callback.message.edit_text(
        "Выберите время:",
        reply_markup=await get_time_keyboard(date)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("time_"))
async def choose_time(callback: CallbackQuery, state: FSMContext):
    time = callback.data.replace("time_", "")

    await state.update_data(time=time)
    data = await state.get_data()

    await callback.message.edit_text(
        f"Дата: {data['date']}\n"
        f"Время: {time}\n\n"
        "Подтвердите бронирование:",
        reply_markup=get_confirm_keyboard()
    )

    await callback.answer()

@router.callback_query(F.data == "full")
async def slot_full(callback: CallbackQuery):
    await callback.answer("❌ Все места заняты", show_alert=True)

@router.callback_query(F.data == "confirm_booking")
async def confirm_booking(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = await get_user_id(callback.from_user.id)

    if user_id is None:
        await callback.message.answer("Ошибка пользователя.")
        await state.clear()
        return

    count = await count_bookings(data["date"], data["time"])

    if count >= SLOT_LIMIT:
        await callback.message.edit_text(
        "❌ Все места на это время уже заняты."
    )
        await state.clear()
        await callback.answer()
        return

    result = await create_booking(
        user_id=user_id,
        date=data["date"],
        time=data["time"]
    )

    if result:
        await callback.message.edit_text(
            "✅ Бронирование успешно создано!"
        )
    else:
        await callback.message.edit_text(
            "❌ Это время уже занято."
        )

    await state.clear()
    await callback.answer()


# ======================
# USER CANCEL
# ======================

@router.callback_query(F.data.startswith("cancel_"))
async def cancel_user_booking(callback: CallbackQuery):
    booking_id = int(callback.data.replace("cancel_", ""))

    user_id = await get_user_id(callback.from_user.id)

    if user_id is None:
        await callback.message.answer("Ошибка пользователя.")
        return

    await cancel_booking(booking_id, user_id)

    await callback.message.edit_text(
        "✅ Бронирование отменено."
    )

    await callback.answer()


# ======================
# ADMIN COMMANDS
# ======================

@router.message(F.text == "/all_bookings")
async def all_bookings(message: Message):
    if message.from_user.id not in ADMINS:
        return

    bookings = await get_all_bookings()

    if not bookings:
        await message.answer("Нет бронирований.")
        return

    text = "Все бронирования:\n\n"

    for _, user, date, time in bookings:
        text += f"{user} | {date} {time}\n"

    await message.answer(
        text,
        reply_markup=get_admin_cancel_keyboard(bookings)
    )


@router.message(F.text == "/today_bookings")
async def today_bookings(message: Message):
    if message.from_user.id not in ADMINS:
        return

    today = datetime.now().strftime("%d.%m.%Y")

    bookings = await get_today_bookings(today)

    if not bookings:
        await message.answer("Сегодня бронирований нет.")
        return

    text = "Бронирования на сегодня:\n\n"

    for _, user, date, time in bookings:
        text += f"{user} | {time}\n"

    await message.answer(
        text,
        reply_markup=get_admin_cancel_keyboard(bookings)
    )


# ======================
# ADMIN CANCEL
# ======================

@router.callback_query(F.data.startswith("admin_cancel_"))
async def admin_cancel_booking(callback: CallbackQuery):
    if callback.from_user.id not in ADMINS:
        return

    booking_id = int(callback.data.replace("admin_cancel_", ""))

    await cancel_booking(booking_id, user_id=None)

    await callback.message.edit_text(
        "❌ Бронирование удалено администратором."
    )

    await callback.answer()