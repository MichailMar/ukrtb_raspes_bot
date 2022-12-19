from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from datetime import datetime, timedelta

def menu():
    kb = [
        [KeyboardButton(text="Расписание")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт из меню"
    )

    return keyboard

def type_timetable():
    kb = [
        [KeyboardButton(text="Учителя"),KeyboardButton(text="Группы")],
        [KeyboardButton(text="Кабинеты"), KeyboardButton(text="Меню")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт из меню"
    )

    return keyboard

async def item_info(items: dict[str, str]):
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(KeyboardButton(text="Назад"))

    for k, _ in items.items():
        keyboard.add(KeyboardButton(text=k))

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)

async def date_keyboard():
    
    today = datetime.now()

    