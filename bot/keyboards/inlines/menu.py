from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

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


menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Выбрать новый заказ", callback_data='new_orders'),
        InlineKeyboardButton(text="Мои заказы", callback_data='my_orders')
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])


def get_kb_order_list(order_list):
    order_list_kb = InlineKeyboardMarkup(row_width=4)

    for order in order_list:
        order_list_kb.insert(InlineKeyboardButton(text=f"Заказ {order}", callback_data=f'order_detail:{order}'))
    order_list_kb.insert(InlineKeyboardButton(text="Назад", callback_data="start"))
    return order_list_kb


def get_kb_order_detail():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="my_orders"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="start"))
    return keyboard
