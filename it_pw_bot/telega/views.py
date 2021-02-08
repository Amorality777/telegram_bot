from django.http import HttpResponse
from django.views.generic import View
from .models import TGConfig, TGAmoChat, TGLogist

import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .models import TGUserAmo
from amo import amoapi
from amo.models import AmoConfigPipelines, OrderBot
import handlers

logging.basicConfig(level=logging.INFO, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')

__author__ = '@itpw'


class StartBot(View):
    def get(self, request, *args, **kwargs):
        tgconfig = TGConfig.config.all()[0]
        bot = Bot(token=tgconfig.token)
        dp = Dispatcher(bot)





        async def get_access_token():
            amoapi.get_access_token()
            await asyncio.sleep(0)


        async def get_leads_tg():
            amoapi.get_leads_tg()
            await asyncio.sleep(0)


        async def tg_amo_chat():
            tgamochats = TGAmoChat.objects.filter(issend=False, amo2tg=True, iserror=False)
            for amochat in tgamochats:
                orderbot = OrderBot.objects.filter(amo_leads_id=amochat.amo_leads_id).first()
                if not orderbot:
                    amochat.iserror = True
                    amochat.save()
                    continue
                # orders = Order.objects.all()
                # order = orders[0]
                user = orderbot.user.first()
                if user:
                    bt_3t = KeyboardButton('/Меню')
                    kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
                    kb_3t.add(bt_3t)
                    amochat.issend = True
                    amochat.save()
                    await bot.send_message(user.tg_id, amochat.text, reply_markup=kb_3t)
                else:
                    amochat.iserror = True
                    amochat.save()
                # print(user)
                pass
                # await bot.send_message(order., send_msg[chat_id][1], reply_markup=greet_kb)

        async def get_orderbot():
            amoapi.get_orderbot()
            await asyncio.sleep(0)


        async def get_orderbot_change():
            amoapi.get_orderbot_change()
            await asyncio.sleep(0)


        async def get_orderbot_canceled():
            amoapi.get_orderbot_canceled()
            await asyncio.sleep(0)


        async def add_notes():
            amoapi.add_notes()
            await asyncio.sleep(0)

        async def send_master():
            send_msg = amoapi.send_master()

            for chat_id in send_msg:
                bt_accept = KeyboardButton('/Принять {}'.format(send_msg[chat_id][0]))
                bt_cancel = KeyboardButton('/Отказаться {}'.format(send_msg[chat_id][0]))
                bt_transfer = KeyboardButton('/Перенести {}'.format(send_msg[chat_id][0]))
                bt_3t = KeyboardButton('/Меню')
                greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
                greet_kb.add(bt_accept)
                greet_kb.add(bt_cancel)
                greet_kb.add(bt_transfer)
                # greet_kb.add(bt_3t)
                await bot.send_message(chat_id, send_msg[chat_id][1], reply_markup=greet_kb)
                pass


        async def send_reminder():
            send_msg = amoapi.send_reminder()

            for chat_id in send_msg:
                # bt_accept = KeyboardButton('/Принять {}'.format(send_msg[chat_id][0]))
                # bt_cancel = KeyboardButton('/Отказаться {}'.format(send_msg[chat_id][0]))
                # bt_transfer = KeyboardButton('/Перенести {}'.format(send_msg[chat_id][0]))
                bt_3t = KeyboardButton('/Меню')
                greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
                # greet_kb.add(bt_accept)
                # greet_kb.add(bt_cancel)
                # greet_kb.add(bt_transfer)
                greet_kb.add(bt_3t)
                await bot.send_message(chat_id, send_msg[chat_id], reply_markup=greet_kb)
                pass

        async def send_change_orderbot():
            send_msg = amoapi.send_change_orderbot()

            for chat_id in send_msg:
                # bt_accept = KeyboardButton('/Принять {}'.format(send_msg[chat_id][0]))
                # bt_cancel = KeyboardButton('/Отказаться {}'.format(send_msg[chat_id][0]))
                # bt_transfer = KeyboardButton('/Перенести {}'.format(send_msg[chat_id][0]))
                bt_3t = KeyboardButton('/Меню')
                greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
                # greet_kb.add(bt_accept)
                # greet_kb.add(bt_cancel)
                # greet_kb.add(bt_transfer)
                greet_kb.add(bt_3t)
                await bot.send_message(chat_id, send_msg[chat_id], reply_markup=greet_kb)
                pass


        async def send_canceled_orderbot():
            send_msg = amoapi.send_canceled_orderbot()

            for chat_id in send_msg:
                # bt_accept = KeyboardButton('/Принять {}'.format(send_msg[chat_id][0]))
                # bt_cancel = KeyboardButton('/Отказаться {}'.format(send_msg[chat_id][0]))
                # bt_transfer = KeyboardButton('/Перенести {}'.format(send_msg[chat_id][0]))
                bt_3t = KeyboardButton('/Меню')
                greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
                # greet_kb.add(bt_accept)
                # greet_kb.add(bt_cancel)
                # greet_kb.add(bt_transfer)
                greet_kb.add(bt_3t)
                await bot.send_message(chat_id, send_msg[chat_id], reply_markup=greet_kb)
                pass


        # async def testprint():
        #     for i in range(0, 10):
        #         print(i)
        #         await asyncio.sleep(20)
        #
        #
        # async def testprint2():
        #     print('QQQQQQQ11111')
        #     await asyncio.sleep(10)
        #     print('QQQQQQQ22222')

        def repeat(coro, loop, delay):
            loop.create_task(coro())
            # asyncio.ensure_future(coro(), loop=loop)
            loop.call_later(delay, repeat, coro, loop, delay)

        # logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')
        print("Start TG Bot")
        # loop = asyncio.get_event_loop()

        loop = asyncio.new_event_loop()  # itpw
        asyncio.set_event_loop(loop)  # itpw

        loop.call_later(10, repeat, get_access_token, loop, 60*60*10) #получаем ключ каждые 10 часов
        loop.call_later(11, repeat, get_orderbot, loop, 30) #получаем список новых заказов каждые 30 секунд
        loop.call_later(17, repeat, get_orderbot_change, loop, 30)  # получаем список измененных заказов каждые 30 секунд
        loop.call_later(18, repeat, get_orderbot_canceled, loop, 30)  # получаем список отмененных заказов каждые 30 секунд
        loop.call_later(15, repeat, get_leads_tg, loop, 30)  # получаем список новых мастеров каждые 30 секунд
        # loop.call_later(12, repeat, tg_amo_chat, loop, 2)  # чат из амо в тг
        # loop.call_later(13, repeat, add_notes, loop, 2)  # чат из тг в амо
        # loop.call_later(20, repeat, send_master, loop, 30) #отправляем сообщения мастерам каждые 30 секунд там где надо
        # loop.call_later(25, repeat, send_reminder, loop, 300)  # напоминание о заказе
        loop.call_later(27, repeat, send_change_orderbot, loop, 30)  # сообщение об изменении заказа
        loop.call_later(28, repeat, send_canceled_orderbot, loop, 30)  # сообщение об отмене заказа

        # loop.call_later(2, repeat, testprint2, loop, 20)
        # loop.create_task(testprint())
        # loop.call_later(2, testprint2)

        print("dalsche")
        executor.start_polling(dp, skip_updates=True, loop=loop)

        return HttpResponse(("Бот работает."))
