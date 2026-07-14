from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.config import ADMINS

from app.keyboards.booking import (
    get_date_keyboard,
    get_cancel_keyboard
)

from app.database.users import get_user_id
from app.database.database import get_user_bookings

from app.handlers.booking import BookingState


router = Router()


@router.message(F.text == "Забронировать место 📚")
async def booking(message: Message, state: FSMContext):
    await state.set_state(BookingState.choosing_date)

    await message.answer(
        "Выбери дату:",
        reply_markup=get_date_keyboard()
    )


@router.message(F.text == "Мои бронирования 📖")
async def my_bookings(message: Message):
    user_id = await get_user_id(message.from_user.id)

    if user_id is None:
        await message.answer("Ошибка пользователя.")
        return

    bookings = await get_user_bookings(user_id)

    if not bookings:
        await message.answer("У вас нет бронирований.")
        return

    text = "Ваши бронирования:\n\n"

    for _, date, time in bookings:
        text += f"📅 {date} ⏰ {time}\n"

    await message.answer(
        text,
        reply_markup=get_cancel_keyboard(bookings)
    )


@router.message(F.text == "Помощь ℹ️")
async def help_command(message: Message):
    await message.answer(
        "Если возникли вопросы, обратись к администратору."
    )

@router.message(F.text == "Админка ⚙️")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return

    await message.answer(
        "Админ-панель:\n\n"
        "1. /all_bookings\n"
        "2. /today_bookings"
    )