from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.from_db import get_personal_orders

orders = {
    '1': {
        'address': 'SPb',
        'date': '11.11.2021'
    },
    '2': {
        'address': 'SPb',
        'date': '11.11.2021'
    },
    '3': {
        'address': 'SPb',
        'date': '11.11.2021'
    },
    '4': {
        'address': 'SPb',
        'date': '11.11.2021'
    },
    '5': {
        'address': 'SPb',
        'date': '11.11.2021'
    },
    '6': {
        'address': 'SPb',
        'date': '11.11.2021'
    },
    '7': {
        'address': 'SPb',
        'date': '11.11.2021'
    },
    '8': {
        'address': 'SPb',
        'date': '11.11.2021'
    }
}
menu_cb = CallbackData('my_menu', "handler", "order_id")

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Мои заказы", callback_data='my_orders')
    ],
    [
        InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")
    ]
])


def get_kb_order_list(user_id):
    order_list_kb = InlineKeyboardMarkup(row_width=4)
    order_list = get_personal_orders(user_id)
    if orders:
        for order_id in orders:  # TODO заменить orders на order_list
            order_list_kb.insert(InlineKeyboardButton(text=f"Заказ {order_id}",
                                                      callback_data=f'my_menu:order_detail:{order_id}'))
    else:
        order_list_kb.insert(InlineKeyboardButton(text=f"У вас нет активных заказов", callback_data='pass'))
        order_list_kb.insert(InlineKeyboardButton(text="Назад ↩️", callback_data="start"))
    return order_list_kb


def get_kb_order_detail(order_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать выполнение заказа", callback_data=f"order_in_progress:{order_id}")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="my_orders"),
            InlineKeyboardButton(text="На главную", callback_data="start")
        ]
    ])
    return keyboard


def get_kb_order_in_progress(order_id, d=True, completed: bool = False):
    keyboard = InlineKeyboardMarkup()
    # TODO либо не добавлять заполненые значения, либо изменять текст
    keyboard.add(
        InlineKeyboardButton(text='Диагностика ✅' if d else 'Диагностика', callback_data=f"diagnostic:{order_id}"))
    keyboard.add(InlineKeyboardButton(text="Ремонт", callback_data=f"repair:{order_id}"))
    keyboard.add(InlineKeyboardButton(text="Расходники", callback_data=f"consumable:{order_id}"))
    if completed:
        keyboard.add(InlineKeyboardButton(text="🏁 Завершить заказ 🎯", callback_data=f"order_completed:{order_id}"))
    return keyboard


def get_kb_confirm_cost(order_id, state):
    keyboard = InlineKeyboardMarkup()
    keyboard.insert(InlineKeyboardButton(text="Да", callback_data=f"order_in_progress:{order_id}"))
    keyboard.insert(InlineKeyboardButton(text="Нет, ввести заного", callback_data=f"{state}:{order_id}"))
    return keyboard


def get_kb_calk():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data='calk:1'),
            InlineKeyboardButton(text='2', callback_data='calk:2'),
            InlineKeyboardButton(text='3', callback_data='calk:3')
        ],
        [
            InlineKeyboardButton(text='4', callback_data='calk:4'),
            InlineKeyboardButton(text='5', callback_data='calk:5'),
            InlineKeyboardButton(text='6', callback_data='calk:6')
        ],
        [
            InlineKeyboardButton(text='7', callback_data='calk:7'),
            InlineKeyboardButton(text='8', callback_data='calk:8'),
            InlineKeyboardButton(text='9', callback_data='calk:9')
        ],
        [
            InlineKeyboardButton(text='Enter', callback_data='save'),
            InlineKeyboardButton(text='0', callback_data='calk:0'),
            InlineKeyboardButton(text='удалить', callback_data='delete'),
        ],
    ])
    return keyboard
