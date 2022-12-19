from aiogram import Router, F
from aiogram.types import Message

from aiogram.filters.text import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

import config
from . import keyboard, states

import parsers

timetable = Router()

available_type = ['Учителя', 'Группы', 'Кабинеты']
text_to_item_id = {"Учителя": "teacher", "Группы": "group", "Кабинеты": "cab"}


@timetable.message(Command(commands="start"))
async def start(message: Message):
    
    await message.answer(
        "Тут будет типо текст приветсвенный",
        reply_markup=keyboard.menu()
    )

@timetable.message(Text(text="назад", ignore_case=True))
async def start(message: Message, state: FSMContext):
    
    await message.answer(
        "Вовзращаем",
        reply_markup=keyboard.type_timetable()
    )
    
    state.set_state(states.GetGroup.type)

@timetable.message(Command(commands="menu"))
@timetable.message(Text(text="меню", ignore_case=True))
async def main(message: Message):
    
    await message.answer(
        "Главное меню",
        reply_markup=keyboard.menu()
    )

@timetable.message(Text(text="расписание", ignore_case=True))
async def timetable_cmd(message: Message, state: FSMContext):
    
    await message.answer(
        "Выберите то, на что хотите получить расписание",
        reply_markup=keyboard.type_timetable()
    )

    await state.set_state(states.GetGroup.type)

@timetable.message(states.GetGroup.type, F.text.in_(available_type))
async def timetable_get_group(message: Message, state: FSMContext):
    
    await state.update_data(type=message.text.lower())

    table = parsers.pars.StudyPars(0, 0, text_to_item_id[message.text])

    await message.answer(
        text=f"Выберите {message.text.lower()}: ",
        reply_markup=await keyboard.item_info(await table.get_all_item())
    )

    await state.set_state(states.GetGroup.group)

@timetable.message(states.GetGroup.type)
async def timetable_get_group_incorrect(message: Message, state: FSMContext):

    await message.answer(
        text="Неверный тип. Выберите только кабинет/группы или учителя"
    )

    state.set_state(states.GetGroup.type)

@timetable.message(states.GetGroup.group)
async def timetable_get_times(message: Message, state: FSMContext):
    
    await state.update_data(group=message.text)
    
