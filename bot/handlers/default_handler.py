from aiogram import types
from aiogram.types import ContentType, ParseMode

from misc import dp


@dp.message_handler()
async def all_other_messages(msg: types.Message):
    await msg.reply(msg.text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    await msg.reply(msg.text, parse_mode=ParseMode.MARKDOWN)
