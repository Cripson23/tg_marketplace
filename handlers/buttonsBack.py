from telegram.ext import ConversationHandler

from res.const import PAGE_MAX_INDEX
from res.func import clear_user_data, check_shop_banned, show_dashboard_menu
from res.menu import user_select_shop_menu
from .buttons import *


# КНОПКИ НАЗАД
def buttons_back(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if query.data == 'back_to_dashboard_menu':
        show_dashboard_menu(chat_id, update)
        return ConversationHandler.END
    # Назад из показа списка
    if query.data == 'back_show_list':
        if DATA not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        if context.user_data[DATA] == 'requests' or context.user_data[DATA] == 'shops':
            update.callback_query.edit_message_text(f'{e_policeman}   <b>Раздел модератора</b>',
                                                    reply_markup=InlineKeyboardMarkup(shop_moder_menu,
                                                                                      resize_keyboard=True),
                                                    parse_mode='HTML')
        if context.user_data[DATA] == 'requisites':
            update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\nВыберите действие",
                                                    reply_markup=InlineKeyboardMarkup(my_shop_finance_requisites,
                                                                                      resize_keyboard=True),
                                                    parse_mode='HTML')
        clear_user_data(context)
    if query.data == 'back_shop_moder_requests_approved_menu':
        update.callback_query.edit_message_text(
            f"   <b>Заявки на открытие</b>\n\nСписок заявок на открытие магазина",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "requests"),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_moder_menu':
        update.callback_query.edit_message_text(f'{e_policeman}   <b>Раздел модератора</b>',
                                                reply_markup=InlineKeyboardMarkup(moderator_menu, resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_moder_select_shop':
        update.callback_query.edit_message_text(
            f"   <b>Список магазинов</b>\n",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "shops"),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_moder_select_shop_menu':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        owner_id = context.user_data[SELECT_ID]
        text = get_shop_info_text(chat_id, owner_id)
        update.callback_query.edit_message_text(text,
                                                reply_markup=InlineKeyboardMarkup(get_moder_select_shop_menu(owner_id),
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_user_select_shop_menu':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        owner_id = context.user_data[SELECT_ID]
        text = get_shop_info_text(chat_id, owner_id)
        update.callback_query.edit_message_text(text,
                                                reply_markup=InlineKeyboardMarkup(user_select_shop_menu,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_comments_select_section':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        button_select_shop_comments(update, context)

    if query.data == 'back_moder_search_shop':
        update.callback_query.edit_message_text(
            f"   <b>Магазины</b>\n\nРаздел модерации Магазинов",
            reply_markup=InlineKeyboardMarkup(shop_moder_menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END
    if query.data == 'back_moder_search_user':
        update.callback_query.edit_message_text(
            f'{e_policeman}   <b>Раздел модератора</b>',
            reply_markup=InlineKeyboardMarkup(moderator_menu, resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END
    if query.data == 'back_moder_select_user_menu':
        chat_id = query.message.chat.id
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        select_user_id = context.user_data[SELECT_ID]
        text = get_user_info_text(chat_id, select_user_id)
        update.callback_query.edit_message_text(text,
                                                reply_markup=InlineKeyboardMarkup(moder_select_user_menu,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_moder_shop_sales_select_section':
        if SELECT_ID not in context.user_data or SELECT_SALE_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        query = update.callback_query
        query.answer()
        shop_id = context.user_data[SELECT_ID]
        count_dispute = get_shop_dispute_deals_count(shop_id)
        count_open = get_shop_open_deals_count(shop_id)
        count_close = get_shop_close_deals_count(shop_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_shop_sales")
        update.callback_query.edit_message_text(
            f"<b>Сделки магазина {get_shop_id(shop_id)} (товары)</b>\n\n<b>❓ Выберите раздел</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    if query.data == 'back_moder_shop_services_sales_select_section':
        if SELECT_ID not in context.user_data or SELECT_SALE_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        query = update.callback_query
        query.answer()
        shop_id = context.user_data[SELECT_ID]
        count_dispute = get_shop_dispute_orders_count(shop_id)
        count_open = get_shop_open_orders_count(shop_id)
        count_close = get_shop_close_orders_count(shop_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_shop_service_sales")
        update.callback_query.edit_message_text(
            f"<b>Заказы магазина {get_shop_id(shop_id)} (услуги)</b>\n\n<b>❓ Выберите раздел</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    if query.data == 'back_moder_user_buys_select_section':
        query = update.callback_query
        query.answer()
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        user_id = context.user_data[SELECT_ID]
        count_dispute = get_user_dispute_deals_count(user_id)
        count_open = get_user_open_deals_count(user_id)
        count_close = get_user_close_deals_count(user_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_user_buys")
        update.callback_query.edit_message_text(
            f"<b>Сделки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)</b>\n\n<b>❓ Выберите раздел товара</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_moder_user_orders_select_section':
        query = update.callback_query
        query.answer()
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        user_id = context.user_data[SELECT_ID]
        count_dispute = get_user_dispute_orders_count(user_id)
        count_open = get_user_open_orders_count(user_id)
        count_close = get_user_close_orders_count(user_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_user_orders")
        update.callback_query.edit_message_text(
            f"<b>Заказы пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (услуги)</b>\n\n<b>❓ Выберите раздел заказа</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
    # =============== Мой магазин ===================
    if query.data == 'back_to_my_shop_menu':
        query = update.callback_query
        query.answer()
        if check_shop_banned(chat_id):
            return
        chat_id = query.message.chat.id
        text = get_shop_info_text(chat_id, chat_id)
        update.callback_query.edit_message_text(text,
                                                reply_markup=InlineKeyboardMarkup(my_shop_menu,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    # -------------- Мой магазин -> Финансы -------------
    if query.data == 'back_to_my_shop_finance_menu':
        text = get_myshop_finance_text(chat_id)
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(my_shop_submenu_finance, resize_keyboard=True),
            parse_mode='HTML')
        clear_user_data(context)
    if query.data == 'back_to_finance_guarantee':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(f"{e_handshake}   <b>Гарант</b>\n\n"
                                                f"<b>Гарант является уровнем доверия к магазину, вносится по желанию.</b>\n\n"
                                                f"<b>Магазины с  гарантом будут показываться выше в списке товаров.</b>\n\n"
                                                f"<b>При наличии гаранта , вы сможете принимать платежи на личный реквизит.</b>\n\n"
                                                f"⚠  Минимальный размер гаранта = {min_guarantee} LTC\n\n"
                                                f"❓ Хотите внести или вывести гарант?",
                                                reply_markup=InlineKeyboardMarkup(my_shop_finance_guarantee,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')

    if query.data == 'back_to_my_shop_finance_withdrawal':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(
            f"{e_dollar_banknote}   <b>Вывод</b>\n\n❓ Куда желаете вывести LITECOIN?",
            reply_markup=InlineKeyboardMarkup(my_shop_finance_withdrawal,
                                              resize_keyboard=True),
            parse_mode='HTML')

    # --------------- Мой магазин -> Настройки --------------
    if query.data == 'back_to_my_shop_submenu_settings':
        query = update.callback_query
        query.answer()
        owner_id = query.message.chat.id
        shop = get_shop_obj(owner_id)
        if shop.terms_trade is None:
            terms_text = "Не указаны"
        else:
            terms_text = shop.terms_trade
        update.callback_query.edit_message_text(f'{e_wrench}   <b>Настройки</b>\n\n'
                                                f'⏱  <b>Время проверка товара:</b> {shop.check_buyer_time // 60}\n'
                                                f'📑  <b>Условия торговли:</b> {terms_text}',
                                                reply_markup=InlineKeyboardMarkup(
                                                    get_my_shop_submenu_settings(shop),
                                                    resize_keyboard=True),
                                                parse_mode='HTML')

    # ----------- Назад в меню "Мои реквизиты" -------------------
    if query.data == 'back_to_my_shop_finance_requisites':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\nВыберите действие",
                                                reply_markup=InlineKeyboardMarkup(my_shop_finance_requisites,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_my_shop_finance_requisites_select_menu':
        query = update.callback_query
        query.answer()
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        select_id = context.user_data[SELECT_ID]
        requisite_info = get_requisite_info(chat_id, select_id)
        update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                                f"{requisite_info}",
                                                reply_markup=InlineKeyboardMarkup(
                                                    my_shop_finance_requisites_select_menu,
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    # ------------------- Мои товары ----------------------
    if query.data == 'back_to_my_shop_submenu_products':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(
            f"   <b>📦  Мои товары</b>\n\nВ данном разделе вы можете <b>добавить</b> новый товар, либо <b>редактировать</b> уже ранее добавленный товар.\n\n"
            f"<b>Предложить категорию</b> - Если вы вдруг не нашли нужную вам категорию, вы можете предложить её к добавлению.\n\n"
            f"После модерации она появится в нашем сервисе.\n\n"
            f"<b>❓ Изменить товар, добавить новый товар или предложить категорию?</b>",
            reply_markup=InlineKeyboardMarkup(my_shop_submenu_products,
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_prev_cat_menu':
        if CATEGORY_INFO not in context.user_data or DATA not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        query = update.callback_query
        chat_id = query.message.chat.id
        query.answer()
        cat = ProductCategory.objects(id=context.user_data[CATEGORY_INFO]['cat_id']).first()
        head = ""
        input_info = ''
        cat_path_text = ""

        if cat.sub_id is None and SELECT_PROD_ID not in context.user_data:
            context.user_data[CATEGORY_INFO]['cat_path'] = ""
            cat_path_text = ""
        elif SELECT_PROD_ID not in context.user_data:
            cat_path = context.user_data[CATEGORY_INFO]['cat_path']
            index = context.user_data[CATEGORY_INFO]['cat_path'].rfind("\t\t\t\t ->")
            context.user_data[CATEGORY_INFO]['cat_path'] = cat_path[:index]
            cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']
        elif SELECT_PROD_ID in context.user_data:
            cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']

        if context.user_data[DATA] == 'add':
            head = "<b>➕  Добавление товара</b>"
            if cat_path_text == "":
                input_info = "\n\n❓ <b>Выберите категорию товара:</b>"
            else:
                input_info = "\n❓ <b>Выберите категорию товара:</b>"
        elif context.user_data[DATA] == 'my_list':
            head = f"<b>{e_page}  Изменить товар</b>"
            if cat_path_text == "":
                input_info = "\n\n❓ <b>Выберите категорию товара:</b>"
            else:
                input_info = "\n❓ <b>Выберите категорию товара:</b>"
        elif context.user_data[DATA] == 'for_user':
            head = f"<b>📦 Товары</b>\n\n" \
                   "📂 Вы видите все представленные категории товаров которые существуют на рынке.\n\n" \
                   "⚠️ Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила ведет к потере денежных средств без разбирательств."
            if cat_path_text == "":
                input_info = "\n\n❓ <b>Выберите категорию товаров:</b>"
            else:
                input_info = "\n❓ <b>Выберите категорию товаров:</b>"

        elif context.user_data[DATA] == 'select_shop_prods':
            head = f"<b>📦 Товары магазина</b>\n\n" \
                   "📂 Вы видите категории товаров которые есть у выбранного магазина.\n\n" \
                   "⚠️ Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила ведет к потере денежных средств без разбирательств."
            if cat_path_text == "":
                input_info = "\n\n❓ <b>Выберите категорию товаров:</b>"
            else:
                input_info = "\n❓ <b>Выберите категорию товаров:</b>"

        if SELECT_PROD_ID in context.user_data and context.user_data[DATA] == 'my_list':
            input_info = "\n❓ <b>Выберите товар:</b>"
            update.callback_query.edit_message_text(f"{head}{cat_path_text}{input_info}",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        get_subcat_btnlist_by_catid(context,
                                                                                    context.user_data[CATEGORY_INFO][
                                                                                        'cat_id'],
                                                                                    context.user_data[DATA], chat_id),
                                                        resize_keyboard=True),
                                                    parse_mode='HTML')
            context.user_data.pop(SELECT_PROD_ID)
        elif SELECT_PROD_ID in context.user_data and context.user_data[DATA] == 'select_shop_prods':
            if SELECT_ID not in context.user_data:
                return update.callback_query.edit_message_text("Не актуально")
            head = f"<b>📦 Товары магазина</b>\n\n" \
                   "📂 Вы видите товары которые есть у магазина в выбранной категории."
            input_info = "\n❓ <b>Выберите товар:</b>"
            update.callback_query.edit_message_text(f"{head}{cat_path_text}{input_info}",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        get_subcat_btnlist_by_catid(context, cat.id,
                                                                                    context.user_data[DATA], chat_id),
                                                        resize_keyboard=True),
                                                    parse_mode='HTML')
            context.user_data.pop(SELECT_PROD_ID)

        elif SELECT_PROD_ID in context.user_data and context.user_data[DATA] == 'for_user':
            if SELECT_ID not in context.user_data:
                return update.callback_query.edit_message_text("Не актуально")
            catid = context.user_data[CATEGORY_INFO]['cat_id']
            owner_id = context.user_data[SELECT_ID]
            products = Product.objects(category_id=catid, owner_id=owner_id)
            menu = []
            for prod in products:
                if prod.count > 0:
                    menu.append([InlineKeyboardButton(f"{prod.name}  |  {prod.price} ₽  [{prod.count} шт.]",
                                                      callback_data=f"select_product_{prod.id}")])
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_select_shop_by_prods"),
                 InlineKeyboardButton(f"{back_for_button}  Выбор раздела",
                                      callback_data='back_to_select_market_section')])
            context.user_data.pop(SELECT_PROD_ID)
            shop = get_shop_obj(owner_id)
            rating = get_sum_shop_deal_rating(owner_id)
            likes = get_count_likes_deal(owner_id)
            dislikes = get_count_dislikes_deal(owner_id)
            last_comments = get_shop_two_comments(shop.owner_id)
            last_active = shop.last_active
            now = datetime.now()
            if last_active is None:
                active_info = "Нет данных"
            else:
                diff = now - last_active
                minutes = divmod(diff, timedelta(seconds=60))[0]
                if minutes < 1:
                    active_info = f"1 минуту назад"
                elif minutes > 60:
                    active_info = "больше часа назад"
                else:
                    active_info = f"{minutes} минут назад"
            if shop.terms_trade is None:
                terms_trade = "Нет данных"
            else:
                terms_trade = shop.terms_trade
            if int_r(rating / 20) == 0:
                rating_info = "Нет рейтинга"
            else:
                rating_info = e_star * (int_r(rating / 20))
            update.callback_query.edit_message_text(
                f"<b>📈 Покупка</b>\n\n"
                f"<b>Магазин:</b>  {shop.shop_name}  ({shop.shop_id})\n"
                f"<b>Рейтинг:</b>  {rating_info}\n"
                f"<b>Отзывы:</b>  ({likes}) {e_like}   ({dislikes}) {e_dislike}\n"
                f"<b>Был в сети:</b>  {active_info}\n"
                f"<b>Успешных сделок:</b>  {get_shop_successful_deals(owner_id)}\n"
                f"<b>Поражений в диспутах:</b>  {get_shop_defeat_dispute(owner_id)}\n\n"
                f"<b>⚠ Условия торговли:</b>  {terms_trade}\n\n"
                f"{last_comments}<b>❓ Выберите товар:</b>",
                reply_markup=InlineKeyboardMarkup(menu,
                                                  resize_keyboard=True),
                parse_mode='HTML')
        else:
            update.callback_query.edit_message_text(f"{head}{cat_path_text}{input_info}",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        get_subcat_btnlist_by_catid(context, cat.sub_id,
                                                                                    context.user_data[DATA], chat_id),
                                                        resize_keyboard=True),
                                                    parse_mode='HTML')
    if query.data == 'back_to_prev_serv_cat_menu':
        if CATEGORY_INFO not in context.user_data or DATA not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        query = update.callback_query
        chat_id = query.message.chat.id
        query.answer()
        cat = ServiceCategory.objects(id=context.user_data[CATEGORY_INFO]['cat_id']).first()
        head = ""
        chapter = ""
        cat_path_text = ""

        if cat.sub_id is None and SELECT_SERV_ID not in context.user_data:
            context.user_data[CATEGORY_INFO]['cat_path'] = ""
            cat_path_text = ""

        elif SELECT_SERV_ID in context.user_data:
            cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']

        elif SELECT_SERV_ID not in context.user_data:
            cat_path = context.user_data[CATEGORY_INFO]['cat_path']
            index = context.user_data[CATEGORY_INFO]['cat_path'].rfind("\t\t\t\t ->")
            context.user_data[CATEGORY_INFO]['cat_path'] = cat_path[:index]
            cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']

        if context.user_data[DATA] == 'add_service':
            head = "➕  <b>Добавление услуги</b>"
            if cat_path_text == "":
                chapter = "\n\n❓ <b>Выберите категорию услуги:</b>"
            else:
                chapter = "\n❓ <b>Выберите категорию услуги:</b>"

        elif context.user_data[DATA] == 'my_list_services':
            head = f"<b>{e_page}  Изменить услугу</b>"
            if cat_path_text == "":
                chapter = "\n\n❓ <b>Выберите категорию услуги:</b>"
            else:
                chapter = "\n❓ <b>Выберите категорию услуги:</b>"

        elif context.user_data[DATA] == 'for_user_services':
            head = f"🤝  <b>Услуги</b>\n\n" \
                   f"⚠  Фрилансеры оформляют свои услуги в виде обьявлений, которые можно купить в один клик. То есть работа исполнителей продается как товар, а это экономит массу времени, денег и нервов. Идеально подходит для типовых задач: логотипы, баннеры, SEO и др."
            if cat_path_text == "":
                chapter = f"\n\n<b>Какой раздел вас интересует❓</b>"
            else:
                chapter = f"\n<b>Какой раздел вас интересует❓</b>"

        elif context.user_data[DATA] == 'select_shop_services':
            head = "🤝  <b>Услуги магазина</b>\n\n" \
                   "📂 Вы видите категории услуг, которые предоставляет выбранный магазин."
            if cat_path_text == "":
                chapter = f"\n\n<b>Какой раздел вас интересует❓</b>"
            else:
                chapter = f"\n<b>Какой раздел вас интересует❓</b>"

        if context.user_data[DATA] == 'my_list_services' and SELECT_SERV_ID in context.user_data:
            chapter = "\n❓ <b>Выберите услугу:</b>"
            update.callback_query.edit_message_text(f"{head}{cat_path_text}{chapter}",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        get_subcat_service_btnlist_by_catid(context,
                                                                                            context.user_data[
                                                                                                CATEGORY_INFO][
                                                                                                'cat_id'],
                                                                                            context.user_data[DATA],
                                                                                            chat_id),
                                                        resize_keyboard=True),
                                                    parse_mode='HTML')
            context.user_data.pop(SELECT_SERV_ID)
        elif context.user_data[DATA] == 'select_shop_services' and SELECT_SERV_ID in context.user_data:
            head = "🤝  <b>Услуги магазина</b>\n\n" \
                   "📂 Вы видите услуги, которые предоставляет магазин в выбранной категории."
            chapter = f"\n<b>❓ Выберите услугу</b>"
            update.callback_query.edit_message_text(f"{head}{cat_path_text}{chapter}",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        get_subcat_service_btnlist_by_catid(context,
                                                                                            context.user_data[
                                                                                                CATEGORY_INFO][
                                                                                                'cat_id'],
                                                                                            context.user_data[DATA],
                                                                                            chat_id),
                                                        resize_keyboard=True),
                                                    parse_mode='HTML')
            context.user_data.pop(SELECT_SERV_ID)

        elif context.user_data[DATA] == 'for_user_services' and SELECT_SERV_ID in context.user_data:
            head = "\n<b>Категория</b>\n\n👤 Это список из фрилансеров, выберите подходящего и сделайте заказ.\n\n" \
                   "⚠  Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила может привести к потере денежных средств без разбирательств."
            chapter = f"\n✅  <b>Выберите фрилансера:</b>"
            update.callback_query.edit_message_text(
                f"{head}{cat_path_text}{chapter}",
                reply_markup=InlineKeyboardMarkup(
                    get_subcat_service_btnlist_by_catid(context,
                                                        context.user_data[CATEGORY_INFO]['cat_id'],
                                                        context.user_data[DATA],
                                                        chat_id),
                    resize_keyboard=True),
                parse_mode='HTML')
            context.user_data.pop(SELECT_SERV_ID)

        else:
            update.callback_query.edit_message_text(f"{head}{cat_path_text}{chapter}",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        get_subcat_service_btnlist_by_catid(context, cat.sub_id,
                                                                                            context.user_data[DATA],
                                                                                            chat_id),
                                                        resize_keyboard=True),
                                                    parse_mode='HTML')

    if query.data == 'back_to_prod_menu':
        query = update.callback_query
        query.answer()
        owner_id = query.message.chat.id
        if SELECT_PROD_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        product_id = context.user_data[SELECT_PROD_ID]
        product_info = get_product_info(owner_id, context, product_id)
        update.callback_query.edit_message_text(f"   <b>Управление товаром</b>{product_info}",
                                                reply_markup=InlineKeyboardMarkup(
                                                    my_shop_submenu_products_prod_menu,
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_products_prod_edit':
        query = update.callback_query
        query.answer()
        owner_id = query.message.chat.id
        if SELECT_PROD_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        product_id = context.user_data[SELECT_PROD_ID]
        product_info = get_product_info(owner_id, context, product_id)
        update.callback_query.edit_message_text(f"   <b>Редактирование товара</b>{product_info}",
                                                reply_markup=InlineKeyboardMarkup(my_shop_product_edit_menu,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_select_shop_by_prods':
        query = update.callback_query
        query.answer()
        context.user_data[DATA] = 'for_user'
        cat_path_text = ""
        if CATEGORY_INFO not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        if 'cat_path' in context.user_data[CATEGORY_INFO]:
            cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']
        update.callback_query.edit_message_text("🏪<b>Магазины</b>\n\n"
                                                "🛍 Ниже представлены все магазины которые продают данный товар.\n\n"
                                                "⚠ <u>Будьте внимательны</u>, проверяйте отзывы о магазинах и рейтинг магазина."
                                                f"Каждый продавец вправе выставить любую цену за товар.{cat_path_text}\n✅ <b>Выберите магазин:</b>",
                                                reply_markup=InlineKeyboardMarkup(
                                                    get_subcat_btnlist_by_catid(context,
                                                                                context.user_data[CATEGORY_INFO][
                                                                                    'cat_id'], context.user_data[DATA],
                                                                                chat_id),
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_select_market_section':
        update.callback_query.edit_message_text(f"<b>🛒  Рынок</b>\n\n"
                                                f"<i>📦  Товары</i> -  данный раздел покажет вам магазины с товарами для вашей онлайн деятельности, либо просто какими-то цифровыми товарами.\n\n"
                                                f"<i>🤝  Услуги</i> - данный раздел является своего рода фриланс биржей, где вы сможете найти любого исполнителя на ваш вкус.\n\n"
                                                f"⚠  Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения"
                                                f"этого правила ведет к потере денежных средств без разбирательств.\n\n"
                                                f"❓  Какой раздел вас интересует?\n\n"
                                                f"📦  Товары или  🤝  Услуги?",
                                                reply_markup=InlineKeyboardMarkup(select_market_section,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_select_payment_method':
        if SELECT_PROD_ID not in context.user_data or PRODUCT_COUNT not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        product_id = context.user_data[SELECT_PROD_ID]
        product = get_product_by_id(product_id)
        ltc_price = round(get_ltc_by_rub(product.price), 5)
        count = context.user_data[PRODUCT_COUNT]
        update.callback_query.edit_message_text(f"   <b>Покупка товара</b>\n\n"
                                                f"Категория:  <b>{context.user_data[CATEGORY_INFO]['cat_path']}</b>\n"
                                                f"Название:  <b>{product.name}</b>\n"
                                                f"Стоимость (1 шт.):  <b>{product.price} ₽  ({ltc_price} LTC)</b>\n"
                                                f"Выбранное количество товара:  <b>{count} шт.</b>\n"
                                                f"Итоговая стоимость:  <b>{context.user_data[PRODUCT_SUM_PRICE]}  ₽ ({context.user_data[PRODUCT_LTC_SUM_PRICE]} LTC)</b>\n\n"
                                                f"<b>❓ Выберите способ оплаты</b>",
                                                reply_markup=InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("Счет LITECOIN",
                                                                           callback_data=f"payment_for_litecoin"),
                                                      InlineKeyboardButton("Реквизиты магазина",
                                                                           callback_data=f"payment_shop_requisites_list")],
                                                     [InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                           callback_data='back_to_select_product')]],
                                                    resize_keyboard=True), parse_mode="HTML")
    if query.data == 'back_to_select_product':
        if SELECT_PROD_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        product_id = context.user_data[SELECT_PROD_ID]
        button_select_product(update, context, product_id)
    if query.data == 'back_to_my_buys_list':
        if DEAL_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        buys_section = context.user_data[SELECT_BUYS_SECTION]
        section_text = ""
        if buys_section == 'dispute':
            section_text = "Диспуты"
        elif buys_section == 'open':
            section_text = "Незавершенные"
        elif buys_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} сделки (товары)</b>\n\n❓ Выберите сделку",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys"),
                                              resize_keyboard=True), parse_mode='HTML')
    # В список заказов в выбранной секции
    if query.data == 'back_to_my_orders_list':
        if ORDER_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        buys_section = context.user_data[SELECT_BUYS_SECTION]
        section_text = ""
        if buys_section == 'dispute':
            section_text = "Диспуты"
        elif buys_section == 'open':
            section_text = "Незавершенные"
        elif buys_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} заказы (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys_service"),
                                              resize_keyboard=True), parse_mode='HTML')
    if query.data == 'back_to_my_sales_list':
        if DEAL_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_SALE_SECTION]
        section_text = ""
        if sale_section == 'dispute':
            section_text = "Диспуты"
        elif sale_section == 'open':
            section_text = "Незавершенные"
        elif sale_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} сделки (товары)</b>\n\n❓ Выберите сделку",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_sales"),
                                              resize_keyboard=True), parse_mode='HTML')
    if query.data == 'back_to_my_service_sales_list':
        if ORDER_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_SALE_SECTION]
        section_text = ""
        if sale_section == 'dispute':
            section_text = "Диспуты"
        elif sale_section == 'open':
            section_text = "Незавершенные"
        elif sale_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} заказы (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_service_sales"),
                                              resize_keyboard=True), parse_mode='HTML')
    if query.data == 'back_to_shop_sales_list':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_SALE_SECTION]
        section_text = ""
        if sale_section == 'dispute':
            section_text = "Диспуты"
        elif sale_section == 'open':
            section_text = "Незавершенные"
        elif sale_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} сделки магазина (товары)</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_sales"),
                                              resize_keyboard=True), parse_mode='HTML')
    if query.data == 'back_to_shop_service_sales_list':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_SALE_SECTION]
        section_text = ""
        if sale_section == 'dispute':
            section_text = "Диспуты"
        elif sale_section == 'open':
            section_text = "Незавершенные"
        elif sale_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} заказы магазина (услуги)</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_service_sales"),
                                              resize_keyboard=True), parse_mode='HTML')

    if query.data == 'back_to_user_buys_list':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        user_id = context.user_data[SELECT_ID]
        buy_section = context.user_data[SELECT_BUYS_SECTION]
        section_text = ""
        if buy_section == 'dispute':
            section_text = "Диспуты"
        elif buy_section == 'open':
            section_text = "Незавершенные"
        elif buy_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} сделки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_buys"),
                                              resize_keyboard=True), parse_mode='HTML')

    if query.data == 'back_to_user_orders_list':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        user_id = context.user_data[SELECT_ID]
        buy_section = context.user_data[SELECT_BUYS_SECTION]
        section_text = ""
        if buy_section == 'dispute':
            section_text = "Диспуты"
        elif buy_section == 'open':
            section_text = "Незавершенные"
        elif buy_section == 'close':
            section_text = "Завершенные"
        update.callback_query.edit_message_text(
            f"<b>{section_text} заказы пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (услуги)</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_orders"),
                                              resize_keyboard=True), parse_mode='HTML')

    if query.data == 'back_to_my_sales_select_section':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        count_dispute = get_shop_dispute_deals_count(chat_id)
        count_open = get_shop_open_deals_count(chat_id)
        count_close = get_shop_close_deals_count(chat_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "my_sales")
        update.callback_query.edit_message_text(
            "<b>📦  Продажи (товары)</b>\n\n<u>Завершенные</u> - абсолютно все продажи которые были завершены в вашем магазине.\n\n"
            "<u>Незавершенные</u> -  продажи которые на текущий момент являются незавершенными, обычно это проверка "
            "товара, либо ожидания оплаты.\n\n"
            "<u>Диспуты</u> - продажи в которых у клиента возникли проблемы с вашим товаром.\n\n"
            "<b>❓ Какой раздел вас интересует?</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_my_service_sales_select_section':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        count_dispute = get_shop_dispute_orders_count(chat_id)
        count_open = get_shop_open_orders_count(chat_id)
        count_close = get_shop_close_orders_count(chat_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "my_sales_service")
        update.callback_query.edit_message_text(
            "<b>🤝 Заказы (Услуги)</b>\n\n<u>Завершенные</u> -  абсолютно все заказы, которые были завершены в вашем магазине.\n\n"
            "<u>Незавершенные</u> -  заказы, которые на текущий момент являются незавершенными, обычно это проверка работ, "
            "либо ожидание оплаты.\n\n"
            "<u>Диспуты</u> - продажи, в которых у клиента возникли проблемы с вашей услугой.\n\n"
            "<b>❓ Какой раздел вас интересует?</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    if query.data == 'back_to_my_buys_select_section':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        count_dispute = get_user_dispute_deals_count(chat_id)
        count_open = get_user_open_deals_count(chat_id)
        count_close = get_user_close_deals_count(chat_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "my_buys")
        update.callback_query.edit_message_text(
            "📦  <b>Мои покупки (товары)</b>\n\n<u>Завершенные</u> - абсолютно все покупки которые были завершены.\n\n"
            "<u>Незавершенные</u> -  покупки, которые на текущий момент являются незавершенными, обычно это проверка "
            "товара, либо ожидание оплаты.\n\n"
            "<u>Диспуты</u> - покупки, в которых у вас возникли проблемы с товаром.\n\n"
            "<b>❓ Какой раздел вас интересует?</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_my_service_buys_select_section':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        count_dispute = get_user_dispute_orders_count(chat_id)
        count_open = get_user_open_orders_count(chat_id)
        count_close = get_user_close_orders_count(chat_id)
        menu = get_submenu_trades(count_dispute, count_open, count_close, "my_buys_service")
        update.callback_query.edit_message_text(
            "<b>🤝  Мои заказы (Услуги)</b>\n\n<u>Завершенные</u> -  абсолютно все заказы, которые были завершены.\n\n"
            "<u>Незавершенные</u> -  заказы, которые на текущий момент являются незавершенными, обычно это выполнение и проверка работ, "
            "либо ожидание оплаты.\n\n"
            "<u>Диспуты</u> - покупки, в которых у вас возникли проблемы с заказом.\n\n"
            "<b>❓ Какой раздел вас интересует?</b>",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    if query.data == 'back_to_buyer_deal_menu':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        if DEAL_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        deal_id = context.user_data[DEAL_ID]
        deal = get_deal_by_id(deal_id)
        if not deal:
            return update.callback_query.edit_message_text("Не актуально")
        deal_info = get_deal_info(deal_id)
        menu = get_buyer_deal_menu(deal, deal.status, context)
        update.callback_query.edit_message_text(
            deal_info,
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)
    if query.data == 'back_to_shop_deal_menu':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        if DEAL_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        deal_id = context.user_data[DEAL_ID]
        deal = get_deal_by_id(deal_id)
        if not deal:
            return update.callback_query.edit_message_text("Не актуально")
        deal_info = get_deal_info(deal_id)
        update.callback_query.edit_message_text(
            deal_info,
            reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(deal.status, deal, context),
                                              resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)
    if query.data == 'back_to_moder_call_list_deals':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(
            f"   <b>Список вызовов (сделки)</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "deal_moder_call"),
                                              resize_keyboard=True),
            parse_mode='HTML')

    if query.data == 'back_to_moder_call_list_orders':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(
            f"   <b>Список вызовов (заказы)</b>",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "order_moder_call"),
                                              resize_keyboard=True),
            parse_mode='HTML')

    if query.data == 'back_to_select_deal_call_menu':
        if DEAL_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        deal_id = context.user_data[DEAL_ID]
        deal_info = get_deal_info(deal_id)
        update.callback_query.edit_message_text(
            deal_info,
            reply_markup=InlineKeyboardMarkup(moder_select_call_menu,
                                              resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)
    if query.data == 'back_to_select_order_call_menu':
        if ORDER_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        order_id = context.user_data[ORDER_ID]
        order = get_order_by_id(order_id)
        if order is None:
            return update.callback_query.edit_message_text(f"   <b>Список вызовов (Заказы)</b>\n\nЗаказ не найден!")
        context.user_data[ORDER_ID] = order_id
        update.callback_query.edit_message_text(get_order_info(order_id),
                                                reply_markup=InlineKeyboardMarkup(
                                                    moder_select_call_order_menu,

                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_call_menu_messages':
        deal_id = context.user_data[DEAL_ID]
        deal = get_deal_by_id(deal_id)
        messages_text = get_deal_messages(deal)
        update.callback_query.edit_message_text(
            f"   <b>Сообщения в диспуте</b>\n\n"
            f"Покупатель:  <b>{get_user_tg_id(deal.buyer_id)}</b>\n"
            f"Владелец магазина:  <b>{get_user_tg_id(deal.shop_id)}</b>\n\n"
            f"{messages_text}",
            reply_markup=InlineKeyboardMarkup(moder_select_call_menu_messages,
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_call_order_menu_messages':
        button_moder_select_call_order_menu_messages(update, context)
    if query.data == 'back_my_buys_select_type':
        update.callback_query.edit_message_text("<b>Мои покупки</b>\n\n❓ Выберите тип покупки",
                                                reply_markup=InlineKeyboardMarkup([
                                                    [InlineKeyboardButton(f"📦  Товары",
                                                                          callback_data='my_buys_type_products'),
                                                     InlineKeyboardButton(f"🤝  Услуги",
                                                                          callback_data='my_buys_type_services')],
                                                    [InlineKeyboardButton(
                                                        f'{back_for_button}  Назад',
                                                        callback_data='back_to_dashboard_menu')]
                                                ],
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_my_sales_select_type':
        open_deals = count_open_deals(chat_id)
        open_orders = count_open_sh_orders(chat_id)
        update.callback_query.edit_message_text(f"{e_shopping_bags}  <b>Продажи</b>\n\n"
                                                "Незавершенных продаж:\n"
                                                f"\t\tТовары - <b>{open_deals}</b>\n"
                                                f"\t\tУслуги - <b>{open_orders}</b>\n\n"
                                                f"❓ <b>Выберите тип продаж:</b>",
                                                reply_markup=InlineKeyboardMarkup([
                                                    [InlineKeyboardButton(f"📦  Товары",
                                                                          callback_data='my_sales_type_products'),
                                                     InlineKeyboardButton(f"🤝  Услуги",
                                                                          callback_data='my_sales_type_services')],
                                                    [InlineKeyboardButton(
                                                        f'{back_for_button}  Назад',
                                                        callback_data='back_to_my_shop_menu')]
                                                ],
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_moder_shop_sales_type':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        query = update.callback_query
        query.answer()
        shop_id = context.user_data[SELECT_ID]
        open_deals = count_open_deals(shop_id)
        open_orders = count_open_sh_orders(shop_id)
        update.callback_query.edit_message_text(
            f"{e_shopping_bags}  <b>Продажи магазина {get_shop_name(shop_id)}  ({get_shop_id(shop_id)})</b>\n\n"
            f"Незавершенных продаж:\n"
            f"\t\tТовары - <b>{open_deals}</b>\n"
            f"\t\tУслуги - <b>{open_orders}</b>\n\n❓ Выберите тип продаж",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"📦  Товары",
                                      callback_data='moder_shop_sales_type_products'),
                 InlineKeyboardButton(f"🤝  Услуги",
                                      callback_data='moder_shop_sales_type_services')],
                [InlineKeyboardButton(
                    f'{back_for_button}  Назад',
                    callback_data='back_moder_select_shop_menu')]
            ],
                resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_my_shop_submenu_services':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(
            f"🤝  <b>Мои услуги</b>\n\nВ данном разделе вы можете <b>добавить</b> новую услугу, либо <b>редактировать</b> уже ранее добавленную услугу.\n\n"
            f"<b>Предложить категорию</b> - Если вы вдруг не нашли нужную вам категорию, вы можете предложить её к добавлению.\n\n"
            f"После модерации она появится в нашем сервисе.\n\n"
            f"<b>❓ Изменить услугу или добавить новую услугу?</b>",
            reply_markup=InlineKeyboardMarkup(my_shop_submenu_services,
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_my_service_packets_menu':
        if SELECT_SERV_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        update.callback_query.edit_message_text(f"   <b>Добавление пакетов</b>\n\n"
                                                f"Также вы можете добавить пакеты к своей услуги (Эконом, Стандарт, Бизнес)\n\n"
                                                f"При добавлении пакета вы должны указать:\n"
                                                f"1) Что входит в выбранный пакет\n"
                                                f"2) Стоимость выбранного пакета\n\n",
                                                reply_markup=InlineKeyboardMarkup(
                                                    get_my_service_packets_menu(update, context, chat_id,
                                                                                "my_service"),
                                                    resize_keyboard=True),
                                                parse_mode='HTML')

    if query.data == 'back_to_my_shop_select_service_menu':
        if SELECT_SERV_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        query = update.callback_query
        query.answer()
        owner_id = query.message.chat.id
        service_id = context.user_data[SELECT_SERV_ID]
        serv_info = get_service_info(owner_id, context, service_id)
        picture_id = get_service_picture_id(service_id)
        context.bot.sendPhoto(owner_id, picture_id)
        context.bot.sendMessage(owner_id, f"   <b>Управление услугой</b>{serv_info}",
                                reply_markup=InlineKeyboardMarkup(my_shop_select_service_menu,
                                                                  resize_keyboard=True),
                                parse_mode='HTML')

    if query.data == 'back_to_service_edit_packet_eco':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        if SELECT_SERV_ID not in context.user_data:
            return context.bot.sendMessage(chat_id, "Не актуально")
        context.user_data[DATA] = "edit_eco"
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        update.callback_query.edit_message_text(f'<b>Редактирование пакета "Эконом"</b>\n\n'
                                                f'<b>Стоимость:</b>  {service.eco_price} ₽\n\n'
                                                f'<b>Описание:</b>  {service.eco_description}',
                                                reply_markup=InlineKeyboardMarkup(my_shop_service_edit_packet,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_service_edit_packet_standart':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        if SELECT_SERV_ID not in context.user_data:
            return context.bot.sendMessage(chat_id, "Не актуально")
        context.user_data[DATA] = "edit_standart"
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        update.callback_query.edit_message_text(f'<b>Редактирование пакета "Стандарт"</b>\n\n'
                                                f'<b>Стоимость:</b>  {service.standart_price} ₽\n\n'
                                                f'<b>Описание:</b>  {service.standart_description}',
                                                reply_markup=InlineKeyboardMarkup(my_shop_service_edit_packet,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_service_edit_packet_biz':
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        if SELECT_SERV_ID not in context.user_data:
            return context.bot.sendMessage(chat_id, "Не актуально")
        context.user_data[DATA] = "edit_biz"
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        update.callback_query.edit_message_text(f'<b>Редактирование пакета "Бизнес"</b>\n\n'
                                                f'<b>Стоимость:</b>  {service.biz_price} ₽\n\n'
                                                f'<b>Описание:</b>  {service.biz_description}',
                                                reply_markup=InlineKeyboardMarkup(my_shop_service_edit_packet,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_select_service_menu_edit':
        query = update.callback_query
        query.answer()
        owner_id = query.message.chat.id
        if SELECT_SERV_ID not in context.user_data:
            return context.bot.sendMessage(owner_id, "Не актуально")
        service_id = context.user_data[SELECT_SERV_ID]
        serv_info = get_service_info(owner_id, context, service_id)
        update.callback_query.edit_message_text(f"   <b>Редактирование услуги</b>{serv_info}",
                                                reply_markup=InlineKeyboardMarkup(my_shop_select_service_menu_edit,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_market_select_service_menu':
        query = update.callback_query
        query.answer()
        owner_id = context.user_data[SELECT_ID]
        if SELECT_SERV_ID not in context.user_data or SELECT_ID not in context.user_data:
            return context.bot.sendMessage(owner_id, "Не актуально")
        service_id = context.user_data[SELECT_SERV_ID]
        serv = get_service_by_id(service_id)
        shop = get_shop_obj(owner_id)
        context.user_data[DATA] = 'for_user_services'
        update.callback_query.edit_message_text(f"<b>Исполнитель:</b>  {shop.shop_name}  ({shop.shop_id})\n\n"
                                                f"<b>Название услуги:</b>  {serv.name}\n\n"
                                                f"<b>Минимальная стоимость:</b>  {serv.min_price} ₽\n\n"
                                                f"<b>Описание услуги:</b>  {serv.description}",
                                                reply_markup=InlineKeyboardMarkup(
                                                    market_select_service_menu,
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    if query.data == 'back_to_market_select_service_menu_portfolio':
        query = update.callback_query
        query.answer()
        owner_id = context.user_data[SELECT_ID]
        if SELECT_SERV_ID not in context.user_data or SELECT_ID not in context.user_data:
            return context.bot.sendMessage(owner_id, "Не актуально")
        service_id = context.user_data[SELECT_SERV_ID]
        serv = get_service_by_id(service_id)
        shop = get_shop_obj(owner_id)
        context.bot.sendMessage(chat_id, f"<b>Исполнитель:</b>  {shop.shop_name}  ({shop.shop_id})\n\n"
                                         f"<b>Название услуги:</b>  {serv.name}\n\n"
                                         f"<b>Минимальная стоимость:</b>  {serv.min_price} ₽\n\n"
                                         f"<b>Описание услуги:</b>  {serv.description}",
                                reply_markup=InlineKeyboardMarkup(
                                    market_select_service_menu,
                                    resize_keyboard=True),
                                parse_mode='HTML')

    if query.data == 'back_to_market_select_service_order':
        button_market_select_service_order(update, context)

    if query.data == 'back_to_client_order_menu':
        if ORDER_ID not in context.user_data:
            return context.bot.sendMessage(chat_id, "Не актуально")
        order_id = context.user_data[ORDER_ID]
        order = get_order_by_id(order_id)
        if order is None:
            return context.bot.sendMessage(chat_id,
                                           f"   <b>Информация о заказе</b>\n\n"
                                           f"Заказ не найден",
                                           parse_mode='HTML')
        menu = get_client_order_menu(order.id, order.status, context)
        context.bot.sendMessage(chat_id,
                                f"{get_order_info(order.id)}",
                                reply_markup=InlineKeyboardMarkup(menu,
                                                                  resize_keyboard=True),
                                parse_mode='HTML')
    if query.data == 'back_to_my_orders_select_section':
        return button_my_buys_type_services(update, context)

    if query.data == 'back_to_shop_order_menu':
        if ORDER_ID not in context.user_data:
            return context.bot.sendMessage(chat_id, "Не актуально")
        order_id = context.user_data[ORDER_ID]
        order = get_order_by_id(order_id)
        if order is None:
            return context.bot.sendMessage(chat_id,
                                           f"   <b>Информация о заказе</b>\n\n"
                                           f"Заказ не найден",
                                           parse_mode='HTML')
        context.bot.sendMessage(chat_id,
                                f"{get_order_info(order.id)}",
                                reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                                                  resize_keyboard=True),
                                parse_mode='HTML')

    if query.data == 'back_to_select_section_calls':
        query = update.callback_query
        query.answer()
        update.callback_query.edit_message_text(
            f"   <b>Список вызовов</b>\n\n<b>❓ Выберите раздел</b>",
            reply_markup=InlineKeyboardMarkup(select_section_calls,
                                              resize_keyboard=True),
            parse_mode='HTML')
    if query.data == 'back_to_moder_select_sale':
        query = update.callback_query
        query.answer()
        if DEAL_ID not in context.user_data or SELECT_SALE_SECTION not in context.user_data:
            return update.callback_query.edit_message_text('Не актуально')
        deal_id = context.user_data[DEAL_ID]
        button_moder_shop_sales(update, context, deal_id)
    if query.data == 'back_to_moder_select_service_sale':
        query = update.callback_query
        query.answer()
        if ORDER_ID not in context.user_data or SELECT_SALE_SECTION not in context.user_data:
            return update.callback_query.edit_message_text('Не актуально')
        order_id = context.user_data[ORDER_ID]
        button_moder_shop_service_sales(update, context, order_id)
    if query.data == 'back_to_moder_user_select_buy':
        query = update.callback_query
        query.answer()
        if DEAL_ID not in context.user_data or SELECT_BUYS_SECTION not in context.user_data:
            return update.callback_query.edit_message_text('Не актуально')
        deal_id = context.user_data[DEAL_ID]
        button_moder_user_buys(update, context, deal_id)
    if query.data == 'back_to_moder_user_select_orders':
        query = update.callback_query
        query.answer()
        if ORDER_ID not in context.user_data or SELECT_BUYS_SECTION not in context.user_data:
            return update.callback_query.edit_message_text('Не актуально')
        order_id = context.user_data[ORDER_ID]
        button_moder_user_orders(update, context, order_id)
    if query.data == 'back_to_change_terms_trade':
        button_my_shop_settings_terms(update, context)
    if query.data == 'back_to_submenu_up_balance':
        chat_id = query.message.chat.id
        user = get_user_obj(chat_id)
        update.callback_query.edit_message_text(f'   *Внести LITECOIN*\n\n'
                                                f'Для пополнения счёта создан Ваш персональный LITECOIN адрес.\n\n'
                                                f'Чтобы пополнить счет выполните перевод по адресу в сообщении ниже\n\n'
                                                f'После выполнения перевода нажмите кнопку\n*\'Найти перевод\'*\n\n'
                                                f'Ваш баланс автоматически пополнится на отправленную сумму! {e_smiling}',
                                                reply_markup=InlineKeyboardMarkup(up_balance_menu,
                                                                                  resize_keyboard=True),
                                                parse_mode=telegram.ParseMode.MARKDOWN)
    if query.data == 'back_to_submenu_balance_menu':
        button_submenu_balance_menu(update, context)

    # Удаление данных
    if PAGE_INDEX in context.user_data:
        context.user_data.pop(PAGE_INDEX)
    if PAGE_MAX_INDEX in context.user_data:
        context.user_data.pop(PAGE_MAX_INDEX)
    return ConversationHandler.END
