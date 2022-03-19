from handlers.buttons import button_about_handler, \
    button_section_moderator_handler, button_my_shop_handler, button_dashboard_handler, \
    button_user_agree, button_submenu_up_balance, button_check_up_balance, button_open_shop_handler, \
    button_submenu_moder_shops, button_shop_moder_requests, button_req_open_shop, \
    button_shop_moder_requests_approved_yes, button_shop_moder_requests_approved_no, \
    button_switcher_list_page, button_moder_select_shop, button_shop_moder_list, button_moder_select_shop_ban, \
    button_moder_select_user_ban, button_moder_select_user_payments, button_up_balance_history, \
    button_moder_select_shop_operations, \
    button_settings_handler, button_submenu_balance_menu, button_submenu_moder_users, button_shop_moder_search, \
    button_my_shop_settings_stop, button_my_shop_settings_stop_confirmed, button_my_shop_finance_operations, \
    button_my_shop_submenu_finance, button_my_shop_finance_guarantee, button_my_shop_finance_withdrawal, \
    button_my_shop_submenu_settings, button_my_shop_finance_guarantee_up, button_my_shop_finance_requisites, \
    button_my_shop_finance_requisites_all, button_my_shop_finance_requisites_select, \
    button_my_shop_finance_requisites_select_edit, button_my_shop_finance_requisites_select_del, \
    button_my_shop_submenu_products, button_my_shop_products_add, button_select_product_cat, \
    button_my_shop_products_list, button_select_my_product, button_my_shop_products_prod_edit, \
    button_my_shop_products_prod_del, button_my_shop_products_prod_del_accept, \
    button_select_product, button_select_shop_products, button_select_shop_prods_bycat, button_market_handler, \
    button_select_market_section_products, button_payment_shop_requisites_list, button_payment_for_litecoin, \
    button_deal_buyer_close, button_deal_buyer_dispute, button_deal_buyer_get_product, button_requisite_payment_select, \
    button_deal_buyer_cancel, button_deal_buyer_confirm_payment, button_deal_shop_confirm_payment, \
    button_my_shop_settings_pause_trade, button_submenu_my_buys, button_select_my_buy, button_my_shop_submenu_trades, \
    button_select_my_sale, button_moder_select_shop_sales, button_moder_shop_sales, button_moder_select_user_buys, \
    button_moder_user_buys, button_select_shop_comments, \
    button_my_sales_select_section_close, button_my_sales_select_section_open, button_my_sales_select_section_dispute, \
    button_my_buys_select_section_dispute, button_my_buys_select_section_open, button_my_buys_select_section_close, \
    button_moder_select_section_dispute, button_moder_select_section_open, button_moder_select_section_close, \
    button_moder_select_user_buys_section_dispute, button_moder_select_user_buys_section_open, \
    button_moder_select_user_buys_section_close, button_deal_buyer_moder_call, \
    button_deal_moder_call, button_moder_select_call_menu_close_deal, button_moder_select_call_menu_content, \
    button_moder_select_call_menu_messages, \
    button_my_buys_type_products, button_my_buys_type_services, button_my_sales_type_products, \
    button_my_sales_type_services, button_moder_shop_sales_type_products, button_moder_shop_sales_type_services, \
    button_moder_user_buys_type_products, button_moder_user_buys_type_services, button_my_shop_submenu_services, \
    button_my_shop_services_add, button_select_serv_cat, button_my_shop_services_list, button_select_my_service, \
    button_my_shop_service_menu_edit, button_my_shop_service_menu_packets, button_my_shop_service_menu_portfolio, \
    button_service_edit_packet_eco, button_service_edit_packet_standart, button_service_edit_packet_biz, \
    button_my_shop_service_edit_packet_del, button_select_shop_services, \
    button_select_comments_section_products, button_select_comments_section_services, \
    button_select_market_section_services, button_market_select_service_comments, \
    button_market_select_service_portfolio, button_market_select_service_order, button_my_shop_service_menu_delete, \
    button_my_shop_service_menu_del_accept, button_select_service, button_market_select_service_packet_eco, \
    button_market_select_service_packet_standart, button_market_select_service_packet_biz, \
    button_market_select_service_packet_unique, button_order_client_cancel, button_order_shop_tz, \
    button_order_shop_cancel, button_order_shop_accept, button_order_client_confirm, button_order_client_close, \
    button_order_client_get_service, button_order_client_dispute, button_order_client_moder_call, \
    button_submenu_moder_calls, button_submenu_moder_calls_deals, button_submenu_moder_calls_orders, \
    button_select_order_moder_call, button_moder_select_call_order_menu_tz, button_moder_select_call_order_menu_content, \
    button_moder_select_call_order_menu_messages, button_moder_select_call_order_menu_close, \
    button_my_orders_service_select_section_dispute, button_my_orders_service_select_section_open, \
    button_my_orders_service_select_section_close, button_select_my_order, \
    button_my_service_sales_select_section_dispute, button_my_service_sales_select_section_open, \
    button_my_service_sales_select_section_close, button_select_my_service_sale, \
    button_moder_select_service_section_dispute, button_moder_select_service_section_open, \
    button_moder_select_service_section_close, button_moder_shop_service_sales, \
    button_moder_select_user_orders_section_dispute, button_moder_select_user_orders_section_open, \
    button_moder_select_user_orders_section_close, button_moder_user_orders, \
    button_moder_select_call_menu_close_deal_shop, button_moder_select_call_menu_close_deal_buyer, \
    button_moder_select_call_order_menu_close_shop, button_moder_select_call_order_menu_close_client, \
    button_my_shop_settings_terms, button_restore_shop, button_deal_buyer_like, button_deal_buyer_dislike, \
    button_order_buyer_like, button_order_buyer_dislike, button_order_client_tz, \
    button_moder_select_call_order_menu_work, button_submenu_moder_bookkeeping
from handlers.buttonsBack import buttons_back, SELECT_ID
from handlers.commands import user_command_handler, shop_command_handler, deal_command_handler, order_command_handler, \
    not_reg_start
from res.func import check_user_banned, check_shop_owner, check_moderator, check_shop_banned, get_username, \
    update_username, clear_user_data, update_last_active, get_user_obj
from res.menu import button_market, button_dashboard, button_settings, button_about, button_section_moderator, \
    button_my_shop
from res.moderCategory import ModerCategory
from res.suggestCategory import SuggestCategory, ModerSuggestCategory


def echo_handler(update, context):
    if update.message is None:
        return
    chat_id = update.message.chat_id

    user = get_user_obj(chat_id)
    if not user:
        return not_reg_start(chat_id, context)

    if check_shop_owner(chat_id):
        update_last_active(chat_id)
    username = update.message.chat.username
    clear_user_data(context)
    if username != get_username(chat_id):
        update_username(chat_id, username)
    if check_user_banned(chat_id):
        return
    text = update.message.text
    if text == button_market:
        return button_market_handler(update, context)
    elif text == button_dashboard:
        return button_dashboard_handler(update, context)
    elif text == button_settings:
        return button_settings_handler(update, context)
    elif text == button_about:
        return button_about_handler(update, context)
    elif text == button_section_moderator:
        if check_moderator(chat_id):
            return button_section_moderator_handler(update, context)
    elif text == button_my_shop:
        if check_shop_owner(chat_id):
            if not check_shop_banned(chat_id):
                return button_my_shop_handler(update, context)
            else:
                context.bot.sendMessage(chat_id, "<b>Ваш магазин заблокирован!</b> Обратитесь в тех. поддержку",
                                        parse_mode='HTML')
    elif text[:2] == '/u':
        user_command_handler(update, context)
    elif text[:2] == '/s':
        shop_command_handler(update, context)
    elif text[:2] == '/d':
        deal_command_handler(update, context)
    elif text[:2] == '/o':
        order_command_handler(update, context)
    else:
        context.bot.sendMessage(chat_id, "Неизвестная команда!",
                                parse_mode='HTML')


def photo_handler(update, context):
    chat_id = update.message.chat_id
    user = get_user_obj(chat_id)
    if not user:
        return not_reg_start(chat_id, context)
    context.bot.sendMessage(chat_id, "Неизвестная команда!",
                            parse_mode='HTML')


def document_handler(update, context):
    if update.message is None:
        return
    chat_id = update.message.chat_id
    user = get_user_obj(chat_id)
    if not user:
        return not_reg_start(chat_id, context)
    context.bot.sendMessage(chat_id, "Неизвестная команда!",
                            parse_mode='HTML')


def query_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    user = get_user_obj(chat_id)

    if check_user_banned(chat_id):
        return

    if query.data == 'user_agree':
        return button_user_agree(update, context)

    if not user:
        return not_reg_start(chat_id, context)

    if check_shop_owner(chat_id):
        update_last_active(chat_id)

    username = query.message.chat.username
    if username != get_username(chat_id):
        update_username(chat_id, username)
    if query.data[:4] == 'back':
        return buttons_back(update, context)
    elif query.data == 'balance_menu':
        return button_submenu_balance_menu(update, context)
    elif query.data == 'submenu_up_balance':
        return button_submenu_up_balance(update, context)
    elif query.data == 'check_up_balance':
        return button_check_up_balance(update, context)
    elif query.data == 'submenu_open_shop':
        return button_open_shop_handler(update, context)

    # ------------ Свитчер страниц
    elif query.data[:25] == 'button_switcher_list_page':
        return button_switcher_list_page(update, context)

    # ================ РЫНОК ====================
    # ========== ТОВАРЫ ========
    elif query.data == 'select_market_section_products':
        return button_select_market_section_products(update, context)

    # --------- Обработка выбора категории товара
    elif query.data[:11] == 'select_cat_':
        cat_id = query.data[11:]
        return button_select_product_cat(update, context, cat_id)

    # --------- Обработка выбора категории услуги
    elif query.data[:16] == 'select_serv_cat_':
        cat_id = query.data[16:]
        return button_select_serv_cat(update, context, cat_id)

    # --------- Просмотр товаров магазина ------------
    elif query.data == 'select_shop_products':
        return button_select_shop_products(update, context)

    # --------- Выбор товаров магазина в опр. категории ------------
    elif query.data[:24] == 'select_shop_prods_bycat_':
        owner_id = query.data[24:]
        return button_select_shop_prods_bycat(update, context, owner_id)

    # --------- Выбор товара
    elif query.data[:15] == 'select_product_':
        product_id = query.data[15:]
        return button_select_product(update, context, product_id)

    # ------- Вывод списка реквизитов магазина ----------
    elif query.data == 'payment_shop_requisites_list':
        return button_payment_shop_requisites_list(update, context)

    # ------- Покупка товара ---------
    elif query.data == 'payment_for_litecoin':
        return button_payment_for_litecoin(update, context)

    # ------- Закрытие сделки покупателем ---------
    elif query.data[:17] == 'deal_buyer_close_':
        deal_id = query.data[17:]
        return button_deal_buyer_close(update, context, deal_id)

    # ------- Спор ---------
    elif query.data[:19] == 'deal_buyer_dispute_':
        deal_id = query.data[19:]
        return button_deal_buyer_dispute(update, context, deal_id)

    # -------- Получение товара --------
    elif query.data == 'deal_buyer_get_product':
        return button_deal_buyer_get_product(update, context)

    # ------- Выбор реквизита Магазина для оплаты --------
    elif query.data[:25] == 'requisite_payment_select_':
        return button_requisite_payment_select(update, context)

    # ------- Отмена сделки -----------
    elif query.data[:18] == 'deal_buyer_cancel_':
        deal_id = query.data[18:]
        return button_deal_buyer_cancel(update, context, deal_id)

    # ------ Подтверждение оплаты -------
    elif query.data[:27] == 'deal_buyer_confirm_payment_':
        deal_id = query.data[27:]
        return button_deal_buyer_confirm_payment(update, context, deal_id)

    # ------ Подтверждение получения оплаты -------
    elif query.data[:26] == 'deal_shop_confirm_payment_':
        deal_id = query.data[26:]
        return button_deal_shop_confirm_payment(update, context, deal_id)

    # -------- Вызов модератора -----------
    elif query.data[:22] == 'deal_buyer_moder_call_':
        deal_id = query.data[22:]
        return button_deal_buyer_moder_call(update, context, deal_id)

    # -------- Отзывы ------------
    elif query.data[:23] == 'button_deal_buyer_like_':
        deal_id = query.data[23:]
        return button_deal_buyer_like(update, context, deal_id)
    elif query.data[:26] == 'button_deal_buyer_dislike_':
        deal_id = query.data[26:]
        return button_deal_buyer_dislike(update, context, deal_id)
    # ======= Услуги =======
    elif query.data == 'select_market_section_services':
        return button_select_market_section_services(update, context)
    elif query.data == 'select_shop_services':
        return button_select_shop_services(update, context)
    elif query.data[:15] == 'select_service_':
        service_id = query.data[15:]
        return button_select_service(update, context, service_id)
    elif query.data == 'market_select_service_portfolio':
        return button_market_select_service_portfolio(update, context)
    elif query.data == 'market_select_service_order':
        return button_market_select_service_order(update, context)
    elif query.data == 'market_select_service_packet_eco':
        return button_market_select_service_packet_eco(update, context)
    elif query.data == 'market_select_service_packet_standart':
        return button_market_select_service_packet_standart(update, context)
    elif query.data == 'market_select_service_packet_biz':
        return button_market_select_service_packet_biz(update, context)
    elif query.data == 'market_select_service_packet_unique':
        return button_market_select_service_packet_unique(update, context)
    # ------- Отказ от заказа заказчиком --------
    elif query.data[:20] == 'order_client_cancel_':
        order_id = query.data[20:]
        return button_order_client_cancel(update, context, order_id)
    # ------- Просмотр тех. задания для исполнителя -----------
    elif query.data[:14] == 'order_shop_tz_':
        order_id = query.data[14:]
        return button_order_shop_tz(update, context, order_id)
    # ------- Отказ от заказа Исполнителем --------------
    elif query.data[:18] == 'order_shop_cancel_':
        order_id = query.data[18:]
        return button_order_shop_cancel(update, context, order_id)
    # ------- Взятие заказа Исполнителем ------
    elif query.data[:18] == 'order_shop_accept_':
        order_id = query.data[18:]
        return button_order_shop_accept(update, context, order_id)
    # ------- Подтверждение заказа Заказчиком ------------
    elif query.data[:21] == 'order_client_confirm_':
        order_id = query.data[21:]
        return button_order_client_confirm(update, context, order_id)
    # ------------ Просмотр тех. задания заказчиком ----------
    elif query.data[:16] == 'order_client_tz_':
        order_id = query.data[16:]
        return button_order_client_tz(update, context, order_id)
    # ------- Завершение заказа Заказчиком -------------
    elif query.data[:19] == 'order_client_close_':
        order_id = query.data[19:]
        return button_order_client_close(update, context, order_id)
    # -------- Посмотреть выполненный заказ -----------
    elif query.data[:25] == 'order_client_get_service_':
        order_id = query.data[25:]
        return button_order_client_get_service(update, context, order_id)
    # ------- Открыть спор ----------
    elif query.data[:21] == 'order_client_dispute_':
        order_id = query.data[21:]
        return button_order_client_dispute(update, context, order_id)
    # ------- Вызвать модератора ----------
    elif query.data[:24] == 'order_client_moder_call_':
        order_id = query.data[24:]
        return button_order_client_moder_call(update, context, order_id)
    # -------- Отзывы -----------
    elif query.data[:24] == 'button_order_buyer_like_':
        order_id = query.data[24:]
        return button_order_buyer_like(update, context, order_id)
    elif query.data[:27] == 'button_order_buyer_dislike_':
        order_id = query.data[27:]
        return button_order_buyer_dislike(update, context, order_id)
    # =================== Личный кабинет ====================
    elif query.data == 'submenu_up_balance_history':
        return button_up_balance_history(update, context)
    elif query.data == 'restore_shop':
        return button_restore_shop(update, context)
    # ----------------- Мои покупки --------------------
    elif query.data == 'submenu_my_buys':
        return button_submenu_my_buys(update, context)
    elif query.data == 'my_buys_type_products':
        return button_my_buys_type_products(update, context)
    elif query.data == 'my_buys_type_services':
        return button_my_buys_type_services(update, context)
    # ------------------- Покупки ---------------------
    elif query.data == 'my_buys_select_section_dispute':
        return button_my_buys_select_section_dispute(update, context)
    elif query.data == 'my_buys_select_section_open':
        return button_my_buys_select_section_open(update, context)
    elif query.data == 'my_buys_select_section_close':
        return button_my_buys_select_section_close(update, context)
    elif query.data[:8] == 'my_buys_':
        deal_id = query.data[8:]
        return button_select_my_buy(update, context, deal_id)
    # ------------------ Заказы --------------------
    elif query.data == 'my_orders_service_select_section_dispute':
        return button_my_orders_service_select_section_dispute(update, context)
    elif query.data == 'my_orders_service_select_section_open':
        return button_my_orders_service_select_section_open(update, context)
    elif query.data == 'my_orders_service_select_section_close':
        return button_my_orders_service_select_section_close(update, context)
    elif query.data[:10] == 'my_orders_':
        order_id = query.data[10:]
        return button_select_my_order(update, context, order_id)
    # ======================== МОДЕРАТОР ========================
    # Вывод списка магазинов для модератора
    elif query.data == 'shop_moder_list':
        return button_shop_moder_list(update, context)
    elif query.data == 'shop_moder_search':
        return button_shop_moder_search(update, context)
    elif query.data == 'submenu_moder_users':
        return button_submenu_moder_users(update, context)
    elif query.data == 'moder_select_shop_ban':
        return button_moder_select_shop_ban(update, context)
    elif query.data == 'moder_select_user_ban':
        return button_moder_select_user_ban(update, context)
    elif query.data == 'moder_select_user_payments':
        return button_moder_select_user_payments(update, context)
    elif query.data == 'submenu_moder_shops':
        return button_submenu_moder_shops(update, context)
    elif query.data == 'shop_moder_requests':
        return button_shop_moder_requests(update, context)
        # Выбор конкрентной заявки / магазина
    elif query.data[:20] == 'req_open_shop_select':
        creator_id = query.data[21:]
        return button_req_open_shop(update, context, creator_id)
    elif query.data == 'moder_select_shop_operations':
        return button_moder_select_shop_operations(update, context)
        # --- Одобрение или отказ заявки на создание магаза
    elif query.data[:33] == 'shop_moder_requests_approved_yes_':
        return button_shop_moder_requests_approved_yes(update, context)
    elif query.data[:32] == 'shop_moder_requests_approved_no_':
        return button_shop_moder_requests_approved_no(update, context)
    # ==================== Выбор продаж магазина
    elif query.data == 'moder_select_shop_sales':
        return button_moder_select_shop_sales(update, context)
    # --------- Выбор раздела
    elif query.data == 'moder_shop_sales_type_products':
        return button_moder_shop_sales_type_products(update, context)
    elif query.data == 'moder_shop_sales_type_services':
        return button_moder_shop_sales_type_services(update, context)
    # ============== Товары
    elif query.data == 'moder_select_section_dispute':
        return button_moder_select_section_dispute(update, context)
    elif query.data == 'moder_select_section_open':
        return button_moder_select_section_open(update, context)
    elif query.data == 'moder_select_section_close':
        return button_moder_select_section_close(update, context)
    # --------- Выбор магазина
    elif query.data[:17] == 'moder_select_shop':
        owner_id = query.data[18:]
        return button_moder_select_shop(update, context, owner_id)
    # -------- Выбор конкретной продажи
    elif query.data[:17] == 'moder_shop_sales_':
        deal_id = query.data[17:]
        return button_moder_shop_sales(update, context, deal_id)
    # ============== Услуги -------------
    elif query.data == 'moder_select_service_section_dispute':
        return button_moder_select_service_section_dispute(update, context)
    elif query.data == 'moder_select_service_section_open':
        return button_moder_select_service_section_open(update, context)
    elif query.data == 'moder_select_service_section_close':
        return button_moder_select_service_section_close(update, context)
    elif query.data[:25] == 'moder_shop_service_sales_':
        order_id = query.data[25:]
        return button_moder_shop_service_sales(update, context, order_id)
    # =============== Выбор покупки пользователя
    elif query.data == 'moder_select_user_buys':
        return button_moder_select_user_buys(update, context)
    # ------------- Выбор раздела
    elif query.data == 'moder_user_buys_type_products':
        return button_moder_user_buys_type_products(update, context)
    elif query.data == 'moder_user_buys_type_services':
        return button_moder_user_buys_type_services(update, context)
    # ------------- Товары
    elif query.data == 'moder_select_user_buys_section_dispute':
        return button_moder_select_user_buys_section_dispute(update, context)
    elif query.data == 'moder_select_user_buys_section_open':
        return button_moder_select_user_buys_section_open(update, context)
    elif query.data == 'moder_select_user_buys_section_close':
        return button_moder_select_user_buys_section_close(update, context)
    elif query.data[:16] == 'moder_user_buys_':
        deal_id = query.data[16:]
        return button_moder_user_buys(update, context, deal_id)
    # ------------- Услуги
    elif query.data == 'moder_select_user_orders_section_dispute':
        return button_moder_select_user_orders_section_dispute(update, context)
    elif query.data == 'moder_select_user_orders_section_open':
        return button_moder_select_user_orders_section_open(update, context)
    elif query.data == 'moder_select_user_orders_section_close':
        return button_moder_select_user_orders_section_close(update, context)
    elif query.data[:18] == 'moder_user_orders_':
        order_id = query.data[18:]
        return button_moder_user_orders(update, context, order_id)
    # ----------- Список вызовов ----------
    elif query.data == 'submenu_moder_calls':
        return button_submenu_moder_calls(update, context)
    # ------ Сделки ------
    elif query.data == 'submenu_moder_calls_deals':
        return button_submenu_moder_calls_deals(update, context)
    elif query.data == 'submenu_moder_calls_orders':
        return button_submenu_moder_calls_orders(update, context)
    elif query.data[:16] == 'deal_moder_call_':
        deal_id = query.data[16:]
        return button_deal_moder_call(update, context, deal_id)
    elif query.data == 'moder_select_call_menu_close_deal':
        return button_moder_select_call_menu_close_deal(update, context)
    elif query.data == 'moder_select_call_menu_close_deal_shop':
        return button_moder_select_call_menu_close_deal_shop(update, context)
    elif query.data == 'moder_select_call_menu_close_deal_buyer':
        return button_moder_select_call_menu_close_deal_buyer(update, context)
    elif query.data == 'moder_select_call_menu_content':
        return button_moder_select_call_menu_content(update, context)
    elif query.data == 'moder_select_call_menu_messages':
        return button_moder_select_call_menu_messages(update, context)
    elif query.data == 'moder_select_call_order_menu_work':
        return button_moder_select_call_order_menu_work(update, context)
    # ------ Заказы -------
    elif query.data[:17] == 'order_moder_call_':
        order_id = query.data[17:]
        return button_select_order_moder_call(update, context, order_id)
    elif query.data == 'moder_select_call_order_menu_tz':
        return button_moder_select_call_order_menu_tz(update, context)
    elif query.data == 'moder_select_call_order_menu_content':
        return button_moder_select_call_order_menu_content(update, context)
    elif query.data == 'moder_select_call_order_menu_messages':
        return button_moder_select_call_order_menu_messages(update, context)
    elif query.data == 'moder_select_call_order_menu_close':
        return button_moder_select_call_order_menu_close(update, context)
    elif query.data == 'moder_select_call_order_menu_close_shop':
        return button_moder_select_call_order_menu_close_shop(update, context)
    elif query.data == 'moder_select_call_order_menu_close_client':
        return button_moder_select_call_order_menu_close_client(update, context)
    # --------- Категории ----------
    elif query.data[:14] == 'moder_category':
        return ModerCategory(update, context, query.data[15:])
    # -------- Заявки на добавление категории
    elif query.data[:27] == 'shop_moder_category_suggest':
        return ModerSuggestCategory(update, context, query.data[28:])
    # -------- Бухгалтерия
    elif query.data == 'submenu_moder_bookkeeping':
        return button_submenu_moder_bookkeeping(update, context)
    # ============================ МОЙ МАГАЗИН ===============================
    if check_shop_owner(chat_id) and not check_shop_banned(chat_id):
        # ---------- Мои продажи
        if query.data == 'my_shop_submenu_trades':
            return button_my_shop_submenu_trades(update, context)
        # ---------- Выбор типа -------------
        elif query.data == 'my_sales_type_products':
            return button_my_sales_type_products(update, context)
        elif query.data == 'my_sales_type_services':
            return button_my_sales_type_services(update, context)
        # ---------- Товары -------------
        elif query.data == 'my_sales_select_section_dispute':
            return button_my_sales_select_section_dispute(update, context)
        elif query.data == 'my_sales_select_section_open':
            return button_my_sales_select_section_open(update, context)
        elif query.data == 'my_sales_select_section_close':
            return button_my_sales_select_section_close(update, context)
        elif query.data[:9] == 'my_sales_':
            deal_id = query.data[9:]
            return button_select_my_sale(update, context, deal_id)
        # --------- Услуги --------------
        elif query.data == 'my_service_sales_select_section_dispute':
            return button_my_service_sales_select_section_dispute(update, context)
        elif query.data == 'my_service_sales_select_section_open':
            return button_my_service_sales_select_section_open(update, context)
        elif query.data == 'my_service_sales_select_section_close':
            return button_my_service_sales_select_section_close(update, context)
        elif query.data[:17] == 'my_service_sales_':
            order_id = query.data[17:]
            return button_select_my_service_sale(update, context, order_id)
    # --------------- Финансы ----------------
        elif query.data == 'my_shop_submenu_finance':
            return button_my_shop_submenu_finance(update, context)
        elif query.data == 'my_shop_finance_withdrawal':
            return button_my_shop_finance_withdrawal(update, context)
        elif query.data == 'my_shop_finance_guarantee':
            return button_my_shop_finance_guarantee(update, context)
        elif query.data == 'my_shop_finance_guarantee_up':
            return button_my_shop_finance_guarantee_up(update, context)
        elif query.data == 'my_shop_finance_operations':
            return button_my_shop_finance_operations(update, context)
        elif query.data == 'my_shop_finance_requisites':
            return button_my_shop_finance_requisites(update, context)
        elif query.data == 'my_shop_finance_requisites_all':
            return button_my_shop_finance_requisites_all(update, context)
        elif query.data == 'my_shop_finance_requisites_select_edit':
            return button_my_shop_finance_requisites_select_edit(update, context)
        elif query.data == 'my_shop_finance_requisites_select_del':
            return button_my_shop_finance_requisites_select_del(update, context)
        elif query.data[:30] == 'my_shop_finance_requisites_id_':
            select_id = query.data[30:]
            return button_my_shop_finance_requisites_select(update, context, select_id)
    # -------------- Мои товары -------------------
        elif query.data == 'my_shop_submenu_products':
            return button_my_shop_submenu_products(update, context)
        elif query.data == 'my_shop_products_add':
            return button_my_shop_products_add(update, context)
        elif query.data == 'my_shop_products_list':
            return button_my_shop_products_list(update, context)
        elif query.data[:18] == 'select_my_product_':
            product_id = query.data[18:]
            return button_select_my_product(update, context, product_id)
        elif query.data == 'my_shop_products_prod_edit':
            return button_my_shop_products_prod_edit(update, context)
        elif query.data == 'my_shop_products_prod_del':
            return button_my_shop_products_prod_del(update, context)
        elif query.data == 'my_shop_products_prod_del_accept':
            return button_my_shop_products_prod_del_accept(update, context)
    # ------------ Мои услуги -------------------------
        elif query.data == 'my_shop_submenu_services':
            return button_my_shop_submenu_services(update, context)
        elif query.data == 'my_shop_services_add':
            return button_my_shop_services_add(update, context)
        elif query.data == 'my_shop_services_list':
            return button_my_shop_services_list(update, context)
        elif query.data[:18] == 'select_my_service_':
            service_id = query.data[18:]
            return button_select_my_service(update, context, service_id)
        elif query.data == 'my_shop_service_menu_edit':
            return button_my_shop_service_menu_edit(update, context)
        elif query.data == 'my_shop_service_menu_packets':
            return button_my_shop_service_menu_packets(update, context)
        elif query.data == 'my_shop_service_menu_portfolio':
            return button_my_shop_service_menu_portfolio(update, context)
        elif query.data == 'service_edit_packet_eco':
            return button_service_edit_packet_eco(update, context)
        elif query.data == 'service_edit_packet_standart':
            return button_service_edit_packet_standart(update, context)
        elif query.data == 'service_edit_packet_biz':
            return button_service_edit_packet_biz(update, context)
        elif query.data == 'my_shop_service_edit_packet_del':
            return button_my_shop_service_edit_packet_del(update, context)
        elif query.data == 'my_shop_service_menu_delete':
            return button_my_shop_service_menu_delete(update, context)
        elif query.data[:33] == 'my_shop_products_prod_del_accept_':
            service_id = query.data[33:]
            return button_my_shop_service_menu_del_accept(update, context, service_id)
    # ----------------------------
        elif query.data[:24] == 'my_shop_suggest_category':
            return SuggestCategory(update, context, query.data[25:])
        # ====================== Настройки ============================
    if query.data == 'my_shop_submenu_settings':
        if not check_shop_banned(chat_id):
            return button_my_shop_submenu_settings(update, context)
    elif query.data == 'my_shop_settings_stop':
        if not check_shop_banned(chat_id):
            return button_my_shop_settings_stop(update, context)
    elif query.data == 'my_shop_settings_stop_confirmed':
        if not check_shop_banned(chat_id):
            return button_my_shop_settings_stop_confirmed(update, context)
    elif query.data == 'my_shop_settings_pause_trade':
        if not check_shop_banned(chat_id):
            return button_my_shop_settings_pause_trade(update, context)
    elif query.data == 'my_shop_settings_terms':
        if not check_shop_banned(chat_id):
            return button_my_shop_settings_terms(update, context)
    # ================ Отзывы ==============
    elif query.data == 'select_shop_comments':
        return button_select_shop_comments(update, context)
    elif query.data == 'select_comments_section_products':
        return button_select_comments_section_products(update, context)
    elif query.data == 'select_comments_section_services':
        return button_select_comments_section_services(update, context)
    elif query.data == 'market_select_service_comments':
        return button_market_select_service_comments(update, context)
    elif query.data == 'my_shop_comments':
        context.user_data[SELECT_ID] = chat_id
        return button_select_shop_comments(update, context)
