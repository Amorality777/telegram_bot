from typing import Union

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from misc import dp
from keyboards.inlines.menu import menu_kb, get_kb_order_list, orders, get_kb_order_detail


@dp.callback_query_handler(text='start')
@dp.message_handler(Command("start"))
async def show_items(message: Union[CallbackQuery, Message]):
    if isinstance(message, Message):
        await message.answer(text='Выберите пункт меню', reply_markup=menu_kb)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(text='Выберите пункт меню', reply_markup=menu_kb)


@dp.callback_query_handler(text='my_orders')
async def show_items(callback: CallbackQuery):
    await callback.message.edit_text(text='Ваши заказы', reply_markup=get_kb_order_list(orders))


def get_order_detail(order_id):
    message = 'Информация о заказе\n'
    for name, info in orders[order_id].items():
        message += f"{name}: {info}\n"
    return message


@dp.callback_query_handler(lambda call: call.data.startswith('order_detail:'))
async def show_items(callback: CallbackQuery, ):
    order_id = callback.data.strip('order_detail:')
    await callback.message.edit_text(text=get_order_detail(order_id), reply_markup=get_kb_order_detail())
