@dp.message_handler(commands=['На_Заказе'])
async def process_on_order_command(message: types.Message):
    argument = message.get_args()
    amoconfigpl = AmoConfigPipelines.config.first()
    fl_ok = False
    orderbot = OrderBot.objects.filter(name=argument).first()
    if orderbot:
        # user = TGUserAmo.objects.filter(tg_id=message.from_user.id).first()
        user = orderbot.user.first()
        if user.tg_id == message.from_user.id:
            orderbot.status = 'on_order'
            orderbot.save()
            lead = amoapi.get_lead_from_id(None, id=orderbot.amo_leads_id)
            # val = len(lead['custom_fields'])
            lead['status_id'] = amoconfigpl.pipelines_status_on_order.amo_id
            amoapi.post_leads(lead)
            # lead['']
            await message.reply('Спасибо', parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)
            pass
            fl_ok = True

    if not fl_ok:
        await message.reply('Заказ не найден', parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)


@dp.message_handler(commands=['Продолжение'])
async def process_continuation_command(message: types.Message):
    argument = message.get_args()
    amoconfigpl = AmoConfigPipelines.config.first()
    bt_3t = KeyboardButton('/Меню')
    kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_3t.add(bt_3t)
    fl_ok = False
    orderbot = OrderBot.objects.filter(name=argument).first()
    if orderbot:
        # user = TGUserAmo.objects.filter(tg_id=message.from_user.id).first()
        user = orderbot.user.first()
        if user.tg_id == message.from_user.id:
            orderbot.status = 'continuation'
            orderbot.save()
            lead = amoapi.get_lead_from_id(None, id=orderbot.amo_leads_id)
            # val = len(lead['custom_fields'])
            lead['status_id'] = amoconfigpl.pipelines_status_continuation.amo_id
            amoapi.post_leads(lead)
            # lead['']
            await message.reply('Спасибо', parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)
            pass
            fl_ok = True

    if not fl_ok:
        await message.reply('Заказ не найден', parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)


@dp.message_handler(commands=['Диагностика'])
async def process_diagnostics_command(message: types.Message):
    argument = message.get_args()
    amoconfigpl = AmoConfigPipelines.config.first()
    bt_3t = KeyboardButton('/Меню')
    kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_3t.add(bt_3t)
    fl_ok = False
    orderbot = OrderBot.objects.filter(name=argument).first()
    if orderbot:
        # user = TGUserAmo.objects.filter(tg_id=message.from_user.id).first()
        user = orderbot.user.first()
        if user.tg_id == message.from_user.id:
            orderbot.status = 'diagnostics'
            orderbot.save()
            lead = amoapi.get_lead_from_id(None, id=orderbot.amo_leads_id)
            # val = len(lead['custom_fields'])
            lead['status_id'] = amoconfigpl.pipelines_status_diagnostics.amo_id
            amoapi.post_leads(lead)
            # lead['']
            user.completed_block = True
            user.status_block = 'diagnostics'
            user.save()
            hide_markup = types.ReplyKeyboardRemove()
            await message.reply('Введите сумму диагностики в рублях, без копеек', parse_mode=ParseMode.MARKDOWN,
                                reply_markup=hide_markup)
            pass
            fl_ok = True

    if not fl_ok:
        await message.reply('Заказ не найден', parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)


@dp.message_handler(commands=['Выполнен_Ремонт'])
async def process_completed_command(message: types.Message):
    argument = message.get_args()
    amoconfigpl = AmoConfigPipelines.config.first()
    bt_3t = KeyboardButton('/Меню')
    kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_3t.add(bt_3t)
    fl_ok = False
    orderbot = OrderBot.objects.filter(name=argument).first()
    if orderbot:
        # user = TGUserAmo.objects.filter(tg_id=message.from_user.id).first()
        user = orderbot.user.first()
        if user.tg_id == message.from_user.id:
            orderbot.status = 'completed'
            orderbot.save()
            user.completed_block = True
            lead = amoapi.get_lead_from_id(None, id=orderbot.amo_leads_id)
            # val = len(lead['custom_fields'])
            lead['status_id'] = amoconfigpl.pipelines_status_completed.amo_id
            amoapi.post_leads(lead)
            # lead['']
            user.completed_block = True
            user.status_block = 'amount_repair'
            user.save()
            hide_markup = types.ReplyKeyboardRemove()
            await message.reply('Введите сумму которую взяли с клиента в рублях, без копеек',
                                parse_mode=ParseMode.MARKDOWN, reply_markup=hide_markup)
            pass
            fl_ok = True

    if not fl_ok:
        await message.reply('Заказ не найден', parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)


@dp.message_handler(commands=['Перенести'])
async def process_change_time_command(message: types.Message):
    argument = message.get_args()
    amoconfigpl = AmoConfigPipelines.config.first()
    orderbot = OrderBot.objects.filter(name=argument).first()
    user = TGUserAmo.objects.filter(tg_id=message.from_user.id).first()
    if orderbot and user:
        user.active_orderbot = orderbot
        user.change_time = True
        user.save()

    # bt_3t = KeyboardButton('/Меню')
    # kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
    # kb_3t.add(bt_3t)
    hide_markup = types.ReplyKeyboardRemove()

    await message.reply(
        ('На какое время Вы хотите перенести заказ \n\n '),
        parse_mode=ParseMode.MARKDOWN, reply_markup=hide_markup)


@dp.message_handler(commands=['Заказ'])
async def active_order(message: types.Message):
    argument = message.get_args()
    tguser = TGUserAmo.objects.filter(tg_id=message.from_user.id).first()
    ordersbot = tguser.orderbot.all()
    orderbot = OrderBot.objects.filter(name=argument).first()
    bt_on_order = KeyboardButton('/На_Заказе {}'.format(orderbot.name))
    bt_continuation = KeyboardButton('/Продолжение {}'.format(orderbot.name))
    bt_diagnostics = KeyboardButton('/Диагностика {}'.format(orderbot.name))
    bt_completed = KeyboardButton('/Выполнен_Ремонт {}'.format(orderbot.name))
    bt_3t = KeyboardButton('/Меню')
    kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_3t.add(bt_on_order)
    kb_3t.add(bt_continuation)
    kb_3t.add(bt_diagnostics)
    kb_3t.add(bt_completed)
    kb_3t.add(bt_3t)
    if orderbot in ordersbot:
        tguser.active_orderbot = orderbot
        tguser.save()
        msg = amoapi.get_message(orderbot)
        await message.reply((' активный заказ \n\n {0}').format(msg),
                            parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)
    else:
        await message.reply(' нет такого заказа -- {}'.format(argument), parse_mode=ParseMode.MARKDOWN,
                            reply_markup=kb_3t)


@dp.message_handler()
async def echo(message: types.Message):
    bt_3t = KeyboardButton('/Меню')
    kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_3t.add(bt_3t)

    hide_markup = types.ReplyKeyboardRemove()

    if not TGUserAmo.objects.filter(tg_id=message.from_user.id).count():
        if TGUserAmo.objects.filter(phone=message.text).count():
            tguseramo = TGUserAmo.objects.get(phone=message.text)
            tguseramo.tg_id = message.from_user.id
            tguseramo.save()
            await message.reply('номер принят, вы подключены к системе. \n'
                                'Скоро поступят первые заявки', reply=False)
        if not TGUserAmo.objects.filter(tg_id=message.from_user.id).count():
            await message.reply('Введите свой номер телефона в формате +79998887766, '
                                'если не удается ввести номер, то свяжитесь с менеджером '
                                'для оперативного решения задачи')
    else:
        # print(message.text)
        tguser = TGUserAmo.objects.filter(tg_id=message.from_user.id).first()
        # order = tguser.active_order
        if tguser.completed_block:
            if tguser.status_block == 'diagnostics':
                if message.text.isdigit():
                    tguser.active_order.amount_diagnostics = int(message.text)
                    proceeds = (tguser.active_orderbot.amount_diagnostics * tguser.percent) // 100
                    tguser.active_orderbot.proceeds = proceeds
                    tguser.active_orderbot.save()

                    amoapi.update_proceeds(tguser.active_orderbot)

                    tguser.completed_block = False
                    tguser.orderbot.remove(tguser.active_orderbot)
                    tguser.active_orderbot = None
                    tguser.save()

                    await message.reply(('диагностика принята \n К переводу {0} руб').format(proceeds), reply=False,
                                        reply_markup=kb_3t)
                else:
                    await message.reply('Ошибка. Введите цену диагностики в рублях без копеек))', reply=False)

            elif tguser.status_block == 'amount_repair':
                if message.text.isdigit():
                    tguser.active_orderbot.amount_repair = int(message.text)
                    tguser.active_orderbot.save()
                    # tguser.completed_block = False
                    # tguser.order.remove(tguser.active_order)
                    # tguser.active_order = None
                    tguser.status_block = 'amount_consumables'
                    tguser.save()

                    await message.reply('Сумма ремонта принята \n Введите сумму запчастей', reply=False,
                                        reply_markup=hide_markup)
                else:
                    await message.reply('Ошибка. Введите сумму ремонта в рублях без копеек)', reply=False,
                                        reply_markup=hide_markup)

            elif tguser.status_block == 'amount_consumables':
                if message.text.isdigit():
                    tguser.active_orderbot.amount_consumables = int(message.text)
                    tguser.active_orderbot.save()
                    # tguser.completed_block = False
                    # tguser.order.remove(tguser.active_order)
                    # tguser.active_order = None
                    tguser.status_block = 'consumables'
                    tguser.save()
                    hide_markup = types.ReplyKeyboardRemove()
                    await message.reply('Сумма ремонта запчастей принята \n Введите использованные расходнки',
                                        reply=False, reply_markup=hide_markup)
                else:
                    await message.reply('Ошибка. Введите сумму запчастей в рублях без копеек)', reply=False)

            elif tguser.status_block == 'consumables':
                tguser.active_orderbot.consumables = message.text
                proceeds = ((
                                        tguser.active_orderbot.amount_repair - tguser.active_orderbot.amount_consumables) * tguser.percent) // 100
                tguser.active_orderbot.proceeds = proceeds
                tguser.active_orderbot.save()
                amoapi.update_proceeds(tguser.active_orderbot)
                tguser.completed_block = False
                tguser.orderbot.remove(tguser.active_orderbot)
                tguser.active_orderbot = None
                tguser.status_block = 'consumables'
                tguser.save()
                await message.reply(('Список запчастей записан \n Спасибо \n К переводу {0} руб').format(proceeds),
                                    reply=False, reply_markup=kb_3t)

        # if not tguser.active_order:
        #     bt_3t = KeyboardButton('/Меню')
        #     kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
        #     kb_3t.add(bt_3t)
        #     await message.reply('выберите заказ', parse_mode=ParseMode.MARKDOWN, reply_markup=kb_3t)

        if tguser.active_orderbot and tguser.change_time:
            logist = TGLogist.objects.first()
            bt_3t = KeyboardButton('/Меню')
            kb_3t = ReplyKeyboardMarkup(resize_keyboard=True)
            kb_3t.add(bt_3t)
            order_name = tguser.active_orderbot.name
            tguser.active_orderbot = None
            tguser.change_time = False
            tguser.choice = False
            tguser.save()
            await bot.send_message(logist.tg_id,
                                   'Мастер {0} просит перенос заказа {1} на {2}'.format(tguser.name,
                                                                                        order_name,
                                                                                        message.text),
                                   reply_markup=kb_3t)

            pass
            # tgamochat = TGAmoChat(amo_leads_id=tguser.active_order.amo_leads_id, text=message.text, amo2tg=False)
            # tgamochat.save()
            # print(text)