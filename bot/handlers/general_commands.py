from typing import Union

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from misc import dp, bot
from keyboards.inlines.menu import menu_kb, get_kb_order_list, orders, get_kb_order_detail, get_kb_order_in_progress, \
    get_kb_confirm_cost, get_kb_calk, menu_cb


@dp.callback_query_handler(text='start')
@dp.message_handler(Command("start"))
async def show_items(message: Union[CallbackQuery, Message]):
    if isinstance(message, Message):
        await message.answer(text=f'{message.from_user.first_name}, Выберите пункт меню', reply_markup=menu_kb)
    elif isinstance(message, CallbackQuery):
        await message.answer(cache_time=1)
        await message.message.edit_text(text=f'{message.from_user.first_name}, Выберите пункт меню',
                                        reply_markup=menu_kb)


@dp.callback_query_handler(text='my_orders')
async def show_orders(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    user_id = callback.message.from_user.id
    await callback.message.edit_text(text='Ваши заказы', reply_markup=get_kb_order_list(user_id=user_id))


# @dp.callback_query_handler(lambda call: True)
# async def query_handler(call):
#     if call.data == 'cancel':
#         await bot.answer_callback_query(callback_query_id=call.id, text='Данная кнопка никуда не ведет!', show_alert=True)


def get_order_detail(order_id):
    message = 'Информация о заказе\n'
    for name, info in orders[order_id].items():
        message += f"{name}: {info}\n"
    return message


@dp.callback_query_handler(menu_cb.filter(handler="order_detail"))
async def show_items(callback: CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=1)
    order_id = callback_data.get('order_id')
    await callback.message.edit_text(text=get_order_detail(order_id), reply_markup=get_kb_order_detail(order_id))


@dp.callback_query_handler(menu_cb.filter(handler="order_in_progress"))
async def enter_order_info(callback: CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=1)
    order_id = callback_data.get('order_id')
    message_text = 'Заполните всю информацию по ремонту'
    if 1 > 0:  # TODO Проверять заполнены ли все поля, если нет, то кнопка завершить заказ не появляется
        await callback.message.edit_text(text=message_text, reply_markup=get_kb_order_in_progress(order_id))
    else:
        await callback.message.edit_text(text=message_text,
                                         reply_markup=get_kb_order_in_progress(order_id, completed=True))


@dp.callback_query_handler(menu_cb.filter(handler="diagnostic"))
async def enter_order_info(callback: CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=1)
    order_id = callback_data.get('order_id')
    # TODO Фиксируем состояние пользователя на данном заказе в фазе диагностика
    message_text = 'Какую сумму вы взяли за диагностику?'
    # await callback.message.edit_text(text=message_text)
    message_text = 'Введите сумму диагностики➾ '
    await callback.message.edit_text(text=message_text, reply_markup=get_kb_calk())


@dp.message_handler(regexp='[0-9]+')
async def get_cost(message: Message):
    message_text = f'Введенная сумма = {message.text}'
    order_id = '2'  # TODO Получаем из состояния
    state = 'diagnostic'  # TODO Получаем из состояния
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()
    await message.answer(message_text, reply_markup=get_kb_confirm_cost(order_id, state))


@dp.callback_query_handler(lambda call: call.data.startswith('calk:'))
async def show_items(callback: CallbackQuery, ):
    await callback.answer(cache_time=1)
    num = callback.data.strip('calk:')
    message_text = callback.message.text + num
    await callback.message.edit_text(text=message_text, reply_markup=get_kb_calk())
