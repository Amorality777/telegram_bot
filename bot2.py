class StartBot2(View):
    tgconfig = TGConfig.config.first()
    bot = Bot(token=tgconfig.token)
    dp = Dispatcher(bot)

    async def delete_message(self, chat_id, message_id):
        try:
            await self.bot.delete_message(chat_id, message_id)
        except Exception:
            pass

    def menu_handlers(self):

        @self.dp.message_handler(content_types=['contact'])
        async def get_contact(message: Message):
            if message.contact is not None:
                phone = message.contact.phone_number
                if TGUserAmo.objects.filter(phone=phone).count():
                    user_id = message.from_user.id
                    save_phone(phone, user_id)
                    message_text = 'Вы успешно авторизовались'
                    await message.answer(text=message_text, reply_markup=ReplyKeyboardRemove())
                    await self.bot.send_message(text=message_text, chat_id=message.chat.id,
                                                reply_markup=auth_success_kb)
                else:
                    message_text = 'Данного номера нет в списке авторизованных, обратитесь за помощью к менеджеру'
                    await message.answer(text=message_text, reply_markup=auth_kb)
            else:
                message_text = 'Не удалось получить данные, пожалуйста, введите телефон в формате +79998887766'
                await message.answer(text=message_text)
            chat_id = message.chat.id
            message_id = message.message_id - 1
            await self.delete_message(chat_id, message_id)
            await message.delete()

        @self.dp.message_handler(regexp='[+]{1}[0-9]{10}')
        async def get_contact_manually(message: Message):
            phone = message.text
            if TGUserAmo.objects.filter(phone=phone).count():
                user_id = message.from_user.id
                save_phone(phone, user_id)
                message_text = 'Вы успешно авторизовались в системе'
                await self.bot.send_message(text=message_text, chat_id=message.chat.id,
                                            reply_markup=auth_success_kb)
            else:
                message_text = 'Данного номера нет в списке авторизованных, обратитесь за помощью к менеджеру'
                await message.answer(text=message_text, reply_markup=auth_kb)
            chat_id = message.chat.id
            message_id = message.message_id - 1
            await self.delete_message(chat_id, message_id)
            await message.delete()

        @self.dp.callback_query_handler(text='my_orders')
        async def show_orders(callback: CallbackQuery):
            await callback.answer(cache_time=1)
            user_id = callback.from_user.id
            await callback.message.edit_text(text='Ваши заказы', reply_markup=get_kb_order_list(user_id=user_id))

        @self.dp.callback_query_handler(menu_cb.filter(handler="order_detail"))
        async def order_detail(callback: CallbackQuery, callback_data: dict):
            await callback.answer(cache_time=1)
            order_id = callback_data.get('order_id')
            order = OrderBot.objects.get(amo_leads_id=order_id)
            message_text = amoapi.get_message(order)
            tguser = TGUserAmo.objects.get(tg_id=callback.from_user.id)
            if tguser.active_orderbot:
                await callback.message.edit_text(text=message_text,
                                                 reply_markup=get_continue_kb(order_id))
            else:
                await callback.message.edit_text(text=message_text,
                                                 reply_markup=get_kb_order_detail(order_id))

    def order_in_progress_scenario(self):
        @self.dp.callback_query_handler(menu_cb.filter(handler="order_in_progress"))
        async def enter_order_info(callback: CallbackQuery, callback_data: dict):
            await callback.answer(cache_time=1)
            order_id = callback_data.get('order_id')
            user_id = callback.from_user.id
            tguser = TGUserAmo.objects.get(tg_id=user_id)
            tguser.status_block = False
            if not tguser.active_orderbot:
                tguser.active_orderbot = OrderBot.objects.get(amo_leads_id=order_id)
            tguser.save()

            amount_diagnostics = tguser.active_orderbot.amount_diagnostics
            amount_repair = tguser.active_orderbot.amount_repair
            amount_consumables = tguser.active_orderbot.amount_consumables
            consumables = tguser.active_orderbot.consumables

            message_text = 'Заполните всю информацию по ремонту'
            if not all((amount_diagnostics, amount_repair, amount_consumables, consumables)):
                await callback.message.edit_text(
                    text=message_text,
                    reply_markup=get_kb_order_in_progress(
                        order_id=order_id,
                        diagnostics=amount_diagnostics,
                        amount_repair=amount_repair,
                        amount_consumables=amount_consumables,
                        consumables=consumables,
                    ))
            else:
                await callback.message.edit_text(text=message_text,
                                                 reply_markup=get_kb_order_in_progress(
                                                     order_id=order_id,
                                                     diagnostics=amount_diagnostics,
                                                     amount_repair=amount_repair,
                                                     amount_consumables=amount_consumables,
                                                     consumables=consumables,
                                                     completed=True))

        @self.dp.callback_query_handler(menu_cb.filter(
            handler=['diagnostics', 'amount_repair', 'amount_consumables', 'consumables']))
        async def enter_order_info(callback: CallbackQuery, callback_data: dict):
            await callback.answer(cache_time=1)
            process = callback_data.get('handler')
            tguser = TGUserAmo.objects.get(tg_id=callback.from_user.id)
            tguser.status_block = process
            tguser.save()
            if process == 'diagnostics':
                message_text = 'Какую сумму вы взяли за диагностику?'
            elif process == 'amount_repair':
                message_text = 'Какую сумму вы взяли за ремонт?'
            elif process == 'amount_consumables':
                message_text = 'Какую сумму вы взяли за расходники?'
            else:
                message_text = 'Какие расходники были использованны?'
            await callback.message.edit_text(text=message_text)

        @self.dp.callback_query_handler(menu_cb.filter(handler='completed'))
        async def completed(callback: CallbackQuery, callback_data: dict):
            await callback.answer(cache_time=1)
            tguser = TGUserAmo.objects.get(tg_id=callback.from_user.id)
            proceeds = (tguser.active_orderbot.amount_diagnostics * tguser.percent) // 100
            tguser.active_orderbot.proceeds = proceeds
            tguser.active_orderbot.save()

            amoapi.update_proceeds(tguser.active_orderbot)

            tguser.completed_block = False
            tguser.orderbot.remove(tguser.active_orderbot)
            tguser.active_orderbot = None
            tguser.save()
            message_text = 'Заказ переведен в статус выполнен!'
            await callback.message.edit_text(text=message_text, reply_markup=menu_kb)
            await callback.message.delete()

        @self.dp.message_handler(regexp='[0-9]+')
        async def get_cost(message: Message):
            tguser = TGUserAmo.objects.get(tg_id=message.from_user.id)
            order_id = tguser.active_orderbot.amo_leads_id
            process = tguser.status_block
            cost = message.text
            detect_process_and_save_cost(cost, order_id, process)
            if process == 'consumables':
                message_text = f'Введенные расходники = {message.text}'
            else:
                message_text = f'Введенная сумма = {message.text}'
            await message.answer(message_text, reply_markup=get_kb_confirm_cost(order_id, process))
            chat_id = message.chat.id
            message_id = message.message_id - 1
            await self.delete_message(chat_id, message_id)
            await message.delete()

        @self.dp.callback_query_handler(text='start')
        @self.dp.message_handler()
        async def all_other_messages(message: Union[CallbackQuery, Message]):
            if isinstance(message, Message):
                if not TGUserAmo.objects.filter(tg_id=message.from_user.id).count():
                    """Начинает логика обработки первого сообщения"""
                    message_text = 'Для начала необходимо авторизироватсья'
                    await message.answer(text=message_text, reply_markup=auth_kb)

                elif TGUserAmo.objects.get(tg_id=message.from_user.id):
                    tguser = TGUserAmo.objects.get(tg_id=message.from_user.id)
                    process = tguser.status_block
                    if process == 'consumables':
                        order_id = tguser.active_orderbot.amo_leads_id
                        consumables = message.text
                        detect_process_and_save_cost(consumables, order_id, process)
                        message_text = f'Введенные расходники = {message.text}'
                        await message.answer(message_text, reply_markup=get_kb_confirm_cost(order_id, process))


                else:
                    tguser = TGUserAmo.objects.get(tg_id=message.from_user.id)
                    if tguser.active_orderbot:
                        order_id = tguser.active_orderbot.amo_leads_id
                        message_text = 'У вас есть незавершенный зазак'
                        await message.answer(text=message_text, reply_markup=get_continue_kb(order_id=order_id))
                    else:
                        message_text = f'{message.from_user.first_name}, Выберите пункт меню'
                        await message.answer(text=message_text, reply_markup=menu_kb)
                chat_id = message.chat.id
                message_id = message.message_id - 1
                await self.delete_message(chat_id, message_id)
                await message.delete()

            elif isinstance(message, CallbackQuery):
                await message.answer(cache_time=1)
                await message.message.edit_text(text=f'{message.from_user.first_name}, Выберите пункт меню',
                                                reply_markup=menu_kb)

        @self.dp.callback_query_handler(lambda call: True)
        async def query_handler(call):
            if call.data == 'cancel':
                await self.bot.answer_callback_query(callback_query_id=call.id,
                                                     text='Данная кнопка никуда не ведет!',
                                                     show_alert=True)
            elif call.data == 'completed':
                await self.bot.answer_callback_query(callback_query_id=call.id,
                                                     text='Данные уже введены вами ранее')

    def get(self, request, *args, **kwargs):

        self.menu_handlers()
        self.order_in_progress_scenario()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        executor.start_polling(self.dp, skip_updates=True, loop=loop)

        return HttpResponse("Бот работает.")