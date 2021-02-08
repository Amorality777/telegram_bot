from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import emoji

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


def get_kb_order_in_progress(order_id, completed: bool = False):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Диагностика", callback_data=f"diagnostic:{order_id}"))
    keyboard.add(InlineKeyboardButton(text="Ремонт", callback_data=f"repair:{order_id}"))
    keyboard.add(InlineKeyboardButton(text="Расходники", callback_data=f"consumable:{order_id}"))
    if completed:
        keyboard.add(InlineKeyboardButton(text="Завершить заказ", callback_data=f"order_completed:{order_id}"))
    return keyboard


def get_kb_confirm_cost(order_id, state):
    keyboard = InlineKeyboardMarkup()
    keyboard.insert(InlineKeyboardButton(text="Да", callback_data=f"order_in_progress:{order_id}"))
    keyboard.insert(InlineKeyboardButton(text="Нет, ввести заного", callback_data=f"{state}:{order_id}"))
    return keyboard
