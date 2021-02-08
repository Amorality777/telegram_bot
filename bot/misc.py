import logging
from aiogram import Bot, Dispatcher

from settings import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
