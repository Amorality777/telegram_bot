from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from misc import dp
from keyboards.inlines.menu import menu_kb


@dp.message_handler(Command("start"))
async def show_items(message: Message):
    await message.answer(text='Выберите пункт меню',
                         reply_markup=menu_kb)
