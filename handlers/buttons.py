from copy import deepcopy
from datetime import datetime, timedelta

import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from res.coinbase_func import create_coinbase_address, get_coinbase_address_id, get_coinbase_address, \
    get_transactions_list, get_coinbase_balance
from res.const import e_briefcase, e_money_bag, e_dollar_banknote, e_info, \
    e_policeman, e_smiling, PAGE_INDEX, \
    e_winking, back_for_button, SELECT_ID, url_support, min_guarantee, e_handshake, DATA, \
    e_wrench, e_stop_sign, e_credit_card, CATEGORY_INFO, CATEGORY_PRODS, SELECT_PROD_ID, PRODUCT_SUM_PRICE, \
    PRODUCT_LTC_SUM_PRICE, PRODUCT_COUNT, commission_per_deals, DEAL_ID, SELECT_REQUISITE_ID, SELECT_SALE_SECTION, \
    CATEGORY_SERVICES, SELECT_SERV_ID, SELECT_SERV_PACKET, CLIENT_SEND_TZ, ORDER_ID, e_like, e_dislike, \
    SELECT_BUYS_SECTION, e_star, e_page, e_cross_mark, e_pencil, e_shopping_bags
from res.func import get_user_obj, add_user, get_shop_request_obj, add_new_shop, delete_req_open_shop, \
    get_shop_info_text, get_shop_obj, shop_unban, shop_ban, user_unban, get_user_info_text, user_ban, \
    get_sum_new_transactions, add_user_balance, get_myshop_finance_text, \
    get_guarantee_shop, get_requisite_info, delete_shop_requisite, get_subcat_btnlist_by_catid, \
    get_cat_my_products_tree, \
    get_product_info, product_del, get_cat_products_shop_tree, get_cat_products_tree, \
    get_requisite_list, get_product_by_id, get_user_balance, add_deal, get_product_content_bytes, get_deal_info, \
    get_buyer_deal_menu, get_deal_by_id, add_shop_balance, get_shop_check_time, get_shop_deal_menu, \
    get_requisite_by_id, get_shop_two_comments, count_open_buys, \
    get_shop_dispute_deals_count, get_shop_open_deals_count, \
    get_shop_close_deals_count, get_user_dispute_deals_count, get_user_open_deals_count, get_user_close_deals_count, \
    get_user_id, moders_alert, get_deal_messages, get_user_tg_id, \
    get_subcat_service_btnlist_by_catid, get_cat_my_services_tree, get_service_info, get_service_picture_id, \
    get_my_service_packets_menu, get_service_by_id, get_cat_services_shop_tree, check_moderator, get_cat_services_tree, \
    get_ltc_by_rub, count_open_deals, get_order_info, get_order_by_id, get_client_order_menu, get_shop_order_menu, \
    count_open_cl_orders, get_shop_name, get_order_messages, get_shop_id, get_user_dispute_orders_count, \
    get_user_open_orders_count, get_user_close_orders_count, get_shop_dispute_orders_count, get_shop_open_orders_count, \
    get_shop_close_orders_count, get_user_name, get_moder_select_shop_menu, \
    get_sum_shop_deal_rating, get_count_likes_deal, get_count_dislikes_deal, int_r, get_shop_defeat_dispute, \
    get_shop_successful_deals, check_shop_owner, shop_stop, check_shop_stop, count_open_sh_orders, get_users_balance, \
    get_shops_balance, get_shops_guarantee, get_shops_freeze_guarantee, get_users_count
from res.func import get_money_balance, show_list_menu, update_main_menu, show_list_text
from res.menu import about_service_menu, my_shop_menu, moderator_menu, main_menu, \
    up_balance_menu, dashboard_menu, request_open_shop_menu, shop_moder_menu, \
    shop_moder_requests_approved_menu, \
    moder_select_user_menu, balance_menu, \
    moder_find_user_menu, shop_moder_find_menu, my_shop_setting_stop_confirmation, my_shop_finance_withdrawal, \
    my_shop_finance_guarantee, my_shop_submenu_finance, my_shop_finance_guarantee_up_menu, \
    my_shop_finance_requisites, my_shop_finance_requisites_select_menu, my_shop_finance_requisites_select_edit_menu, \
    my_shop_submenu_products, my_shop_submenu_products_prod_menu, my_shop_product_edit_menu, \
    my_shop_products_prod_del_accept, market_select_prod_menu, select_market_section, \
    get_submenu_trades, moder_select_call_menu, moder_select_call_menu_messages, my_shop_submenu_services, \
    my_shop_select_service_menu, my_shop_select_service_menu_edit, my_shop_service_edit_packet, select_comments_section, \
    market_select_service_menu, select_section_calls, moder_select_call_order_menu, \
    moder_select_call_order_menu_messages, get_my_shop_submenu_settings

# =================================================== РЕГИСТРАЦИЯ =====================================================
# Кнопка принятия пользовательского соглашения
from res.schemas import ProductCategory, Product, ServiceCategory, Service


def button_user_agree(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if get_user_obj(chat_id):
        return
    username = query.message.chat.username
    first_name = query.message.chat.first_name
    if username is None:
        return update.callback_query.edit_message_text(
            f'Добавьте username в настройках Telegram и введите "/start"! \n\n',
            parse_mode='HTML')
    add_user(chat_id, username, first_name)
    update.callback_query.edit_message_text(f'Поздравляем с успешной регистрацией в сервисе! {e_smiling}\n\n',
                                            parse_mode='HTML')
    context.bot.sendMessage(chat_id, f'Настоятельно рекомендуем изучить раздел <b>\'О сервисе\'</b>',
                            reply_markup=main_menu, parse_mode='HTML')


# =================================================== ГЛАВНОЕ МЕНЮ =====================================================
def button_market_handler(update, context):
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id, f"<b>🛒  Рынок</b>\n\n"
                                     f"<i>📦  Товары</i> -  данный раздел покажет вам магазины с товарами для вашей онлайн деятельности, либо просто какими-то электронными товарами.\n\n"
                                     f"<i>🤝  Услуги</i> - данный раздел является своего рода фриланс биржей, где вы сможете найти любого исполнителя на ваш вкус.\n\n"
                                     f"⚠  Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения "
                                     f"этого правила приведет к потере денежных средств без разбирательств.\n\n"
                                     f"<b>❓  Какой раздел вас интересует?</b>\n\n"
                                     f"📦  Товары или  🤝  Услуги?",
                            reply_markup=InlineKeyboardMarkup(select_market_section,
                                                              resize_keyboard=True),
                            parse_mode='HTML')


def button_select_market_section_products(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    context.user_data[CATEGORY_PRODS] = []
    context.user_data[CATEGORY_INFO] = {}
    get_cat_products_tree(context, update, chat_id)
    context.user_data[DATA] = 'for_user'
    update.callback_query.edit_message_text(f"<b>📦 Товары</b>\n\n"
                                            "📂 Вы видите все представленные категории товаров, которые существуют на рынке.\n\n"
                                            "⚠️ Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила ведет к потере денежных средств без разбирательств.\n\n"
                                            "❓ <b>Выберите категорию товаров:</b>",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_btnlist_by_catid(context, None, context.user_data[DATA],
                                                                            chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_dashboard_handler(update, context):
    chat_id = update.message.chat_id
    user = get_user_obj(chat_id)
    balance = user.balance
    if balance is None:
        return update.message.reply_text(f'Произошла ошибка! Код: notbalance')
    money_balance = get_money_balance(balance)
    update.message.reply_text(f'{e_briefcase}   <b>Личный кабинет</b>\n\n'
                              f'<b>Ваш ID:</b> {user.user_id}\n\n'
                              f'{e_money_bag}\t\t<b>Баланс</b>\n\t\t<i>{round(balance, 8)}</i>\t\tLITECOIN\n\n'
                              f'{e_dollar_banknote}\t\t<b>В валюте</b>\n'
                              f'\t\t<i>{round(money_balance[0], 2)}</i>\t\tUSD\n'
                              f'\t\t<i>{round(money_balance[1], 2)}</i>\t\tRUB'
                              f'\n\n<b>Незавершенных покупок:</b>\n'
                              f'\t\tСделки (товары) - <i>{count_open_buys(chat_id)}</i>\n'
                              f'\t\tЗаказы (услуги) - <i>{count_open_cl_orders(chat_id)}</i>',
                              reply_markup=InlineKeyboardMarkup(dashboard_menu, resize_keyboard=True),
                              parse_mode='HTML')


def button_settings_handler(update, context):
    update.message.reply_text(f'{e_wrench}   <b>Настройки</b>\n'
                              f'\nЗдесь будет раздел настроек', parse_mode='HTML')


def button_about_handler(update, context):
    update.message.reply_text(f'{e_info}   <b>О сервисе</b>\n\n'
                              f'В данном разделе Вы можете получить всю информацию о нашем сервисе',
                              reply_markup=InlineKeyboardMarkup(about_service_menu, resize_keyboard=True),
                              parse_mode='HTML')


# ========================================= РЫНОК ======================================================
# -------------------- ТОВАРЫ -----------------------------
def button_payment_shop_requisites_list(update, context):
    query = update.callback_query
    query.answer()
    product_id = context.user_data[SELECT_PROD_ID]
    product = get_product_by_id(product_id)
    owner_id = product.owner_id
    update.callback_query.edit_message_text(f"   <b>Покупка товара</b>\n\n"
                                            f"Выберите реквизит Магазина для оплаты покупки",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_requisite_list(update, context, owner_id),
                                                resize_keyboard=True), parse_mode="HTML")


def button_payment_for_litecoin(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if not SELECT_PROD_ID in context.user_data or PRODUCT_SUM_PRICE not in context.user_data or PRODUCT_LTC_SUM_PRICE not in context.user_data or PRODUCT_COUNT not in context.user_data or CATEGORY_INFO not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    user_balance = get_user_balance(chat_id)
    sum_ltc_price = context.user_data[PRODUCT_LTC_SUM_PRICE]
    if user_balance < sum_ltc_price:
        context.bot.sendMessage(chat_id, f"   <b>Покупка товара</b>\n\nНедостаточно LITECOIN на балансе\n"
                                         f"Пополните счет на <b> {sum_ltc_price - user_balance} LTC </b>",
                                parse_mode="HTML")
        return
    product_id = context.user_data[SELECT_PROD_ID]
    product = get_product_by_id(product_id)
    count = context.user_data[PRODUCT_COUNT]
    if product.count < count:
        context.bot.sendMessage(chat_id, f"   <b>Покупка товара</b>\n\nНедостаточно выбранного товара\n",
                                parse_mode="HTML")
        return
    owner_id = product.owner_id
    sum_price = context.user_data[PRODUCT_SUM_PRICE]
    category = context.user_data[CATEGORY_INFO]['cat_path']
    if product.count - count == 0:
        context.bot.sendMessage(product.owner_id, f"   <b>У вас закончился товар</b>\n\n"
                                                  f"Категория: {category}\n"
                                                  f"Название: {product.name}",
                                parse_mode="HTML")
    content_bytes = get_product_content_bytes(product_id, count)
    add_user_balance(chat_id, -sum_ltc_price)
    deal = add_deal(owner_id, chat_id, product_id, category, sum_price, "LITECOIN", sum_ltc_price, count, None, 1)
    check_time = get_shop_check_time(owner_id)
    deal_info = get_deal_info(
        deal.id) + f"\n‼  У вас *{int(check_time / 60)} минут* чтобы проверить товар, после чего сделка закроется автоматически\n\n" \
                   "‼  Если с товаром возникли проблемы - нажмите *открыть Диспут*\n\n" \
                   "🔔 Посмотреть историю покупок и продублировать товар можно в разделе:\n" \
                   "\t\t\t\t*'Личный кабинет -> Мои покупки -> Товары'*"
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                          resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)
    message = context.bot.sendDocument(chat_id, content_bytes, f"{deal.id}.{count}.txt",
                                       caption=f"Выдача товара [{count} шт.]")
    file_id = message.document.file_id
    deal.update(file_id=file_id)
    context.user_data[DEAL_ID] = deal.id
    job_context = f"{chat_id}|{deal.id}"
    new_job = context.job_queue.run_repeating(check_deal_status, check_time, context=job_context)
    context.chat_data['job'] = new_job


def check_deal_status(context):
    job = context.job
    job_context = job.context.split('|')
    chat_id = job_context[0]
    deal_id = job_context[1]
    deal = get_deal_by_id(deal_id)
    if deal.status == 1:
        deal.update(status=3, messages=None)
        deal_info = get_deal_info(
            deal_id) + "\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Покупка была автоматически завершена. Оставьте отзыв о Магазине*"
        menu = get_buyer_deal_menu(deal, 3, context)
        menu.pop(0)
        context.bot.sendMessage(chat_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(menu,
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
        if deal.payment_method == 'LITECOIN':
            add_shop_balance(deal.shop_id, deal.sum_price_ltc - (deal.sum_price_ltc * commission_per_deals))
            deal_info = get_deal_info(
                deal_id) + "\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Данная покупка была автоматически завершена, средства перечислены на LITECOIN счёт Магазина*"
        else:
            deal_info = get_deal_info(deal_id) + "\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Данная покупка была автоматически завершена*"
        context.bot.sendMessage(deal.shop_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(3, deal, context),
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
    job.schedule_removal()


def button_deal_buyer_close(update, context, deal_id):
    query = update.callback_query
    query.answer()
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.status == 1 or deal.status == 2:
        deal.update(status=3, messages=None)
        deal_info_get = get_deal_info(deal_id)
        deal_info = deal_info_get + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Вы завершили сделку, оставьте отзыв о Магазине {e_smiling}_"
        menu = get_buyer_deal_menu(deal, 3, context)
        menu.pop(0)
        update.callback_query.edit_message_text(
            deal_info,
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)
        if deal.payment_method == 'LITECOIN':
            add_shop_balance(deal.shop_id, deal.sum_price_ltc - (deal.sum_price_ltc * commission_per_deals))
            deal_info = deal_info_get + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Покупатель завершил данную сделку, средства перечислены на LITECOIN счёт Магазина_"
        else:
            deal_info = deal_info_get + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Покупатель завершил данную сделку, гарант возвращён_"
            shop = get_shop_obj(deal.shop_id)
            shop.update(freeze_guarantee=shop.freeze_guarantee - deal.sum_price_ltc,
                        guarantee=shop.guarantee + (deal.sum_price_ltc - (deal.sum_price_ltc * commission_per_deals)))
        context.bot.sendMessage(deal.shop_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(3, deal, context),
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        return update.callback_query.edit_message_text("🔔  Статус этой сделки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Товары'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')


def button_deal_buyer_dispute(update, context, deal_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.status == 1:
        deal.update(status=2)
        deal_info = get_deal_info(
            deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nВы открыли Диспут с _Магазином_. Решайте проблему через сообщения\n\n" \
                       f"Через *30 минут* вы сможете вызвать *модератора*, если проблема не будет решена\n\n" \
                       "🔔  Посмотреть историю покупок и продублировать товар можно в разделе:\n" \
                       "\t\t\t\t*'Личный кабинет -> Мои покупки -> Товары'*"
        update.callback_query.edit_message_text(
            deal_info,
            reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, 2, context),
                                              resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)
        deal_info = get_deal_info(
            deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nПокупатель открыл Диспут с Вашим магазином\n\nРешайте проблему через сообщения\n\n" \
                       f"Сделайте замену товара, если товар оказался *не валидным*!\n\n" \
                       f"Через *30 минут* Покупатель сможет вызвать *модератора*, если проблема не будет решена\n\n" \
                       "Управлять своими Продажами в любой момент можно в разделе:\n" \
                       "\t\t\t\t*'Мой магазин -> Продажи'*"
        context.bot.sendMessage(deal.shop_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(2, deal, context),
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
        job_context = f"{chat_id}|{deal.id}"
        new_job = context.job_queue.run_repeating(call_moder_add, 1800, context=job_context)
        context.chat_data['job'] = new_job
    else:
        return update.callback_query.edit_message_text("🔔  Статус этой покупки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Товары'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')


def call_moder_add(context):
    job = context.job
    job_context = job.context.split('|')
    chat_id = job_context[0]
    deal_id = job_context[1]
    deal = get_deal_by_id(deal_id)
    if deal.status == 2:
        deal_info = get_deal_info(deal_id) + "➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Теперь вы можете вызвать модератора для этой покупки*"
        deal.update(potential=True)
        deal = get_deal_by_id(deal_id)
        buyer_menu = get_buyer_deal_menu(deal, deal.status, context)
        context.bot.sendMessage(chat_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(buyer_menu,
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
    job.schedule_removal()


def button_deal_buyer_get_product(update, context):
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    context.bot.sendDocument(chat_id, deal.file_id, f"{deal.shop_id}.{deal.count} шт.txt",
                             caption=f"Выданный товар [{deal.count} шт.]")
    if deal.change_file_id is not None and deal.change_count is not None:
        context.bot.sendDocument(chat_id, deal.file_id, f"{deal.shop_id}.{deal.change_count} шт.txt",
                                 caption=f"Замена товара [{deal.change_count} шт.]")


def button_requisite_payment_select(update, context):
    query = update.callback_query
    query.answer()
    requisite_id = query.data[25:]
    chat_id = query.message.chat.id
    context.user_data[SELECT_REQUISITE_ID] = requisite_id
    if not SELECT_PROD_ID in context.user_data or PRODUCT_SUM_PRICE not in context.user_data or PRODUCT_LTC_SUM_PRICE not in context.user_data or PRODUCT_COUNT not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    product_id = context.user_data[SELECT_PROD_ID]
    product = get_product_by_id(product_id)
    owner_id = product.owner_id
    sum_price = context.user_data[PRODUCT_SUM_PRICE]
    sum_ltc_price = context.user_data[PRODUCT_LTC_SUM_PRICE]
    category = context.user_data[CATEGORY_INFO]['cat_path']
    count = context.user_data[PRODUCT_COUNT]
    requisite = get_requisite_by_id(requisite_id)
    requisite_text = requisite.payment_system + f"  ({requisite.account_number})"
    deal = add_deal(owner_id, chat_id, product_id, category, sum_price, requisite_text, sum_ltc_price, count, None, 0)
    deal_info = get_deal_info(
        deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nУ вас есть *15 минут* чтобы оплатить товар по выбранным реквизитам и подтвердить оплату\n\n" \
                   "Если подтверждения не последует, через 15 минут покупка *будет отменена*\n\n" \
                   "🔔Посмотреть историю покупок и продублировать товар можно в разделе:\n" \
                   "\t\t\t\t*'Личный кабинет -> Мои покупки -> Товары'*"
    shop = get_shop_obj(owner_id)
    shop.update(freeze_guarantee=shop.freeze_guarantee + deal.sum_price_ltc,
                guarantee=shop.guarantee - deal.sum_price_ltc)
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                          resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)
    context.user_data[DEAL_ID] = deal.id
    job_context = f"{chat_id}|{deal.id}"
    new_job = context.job_queue.run_repeating(check_proof_payment, 900, context=job_context)
    context.chat_data['job'] = new_job


def check_proof_payment(context):
    job = context.job
    job_context = job.context.split('|')
    chat_id = job_context[0]
    deal_id = job_context[1]
    deal = get_deal_by_id(deal_id)
    if not deal.proof_payment:
        deal_info = get_deal_info(deal_id) + \
                    "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Покупка была автоматически отменена, так как вы не подтвердили оплату*"
        shop = get_shop_obj(deal.shop_id)
        shop.update(freeze_guarantee=shop.freeze_guarantee - deal.sum_price_ltc,
                    guarantee=shop.guarantee + deal.sum_price_ltc)
        context.bot.sendMessage(chat_id,
                                deal_info,
                                parse_mode=telegram.ParseMode.MARKDOWN)
        deal.delete()
    job.schedule_removal()


def button_deal_buyer_cancel(update, context, deal_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.status != 0:
        return update.callback_query.edit_message_text("🔔  Статус этой покупки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Товары'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')
    deal_info = get_deal_info(deal_id) + \
                "\n*Вы отменили данную покупку*"
    context.bot.sendMessage(chat_id,
                            deal_info,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    shop = get_shop_obj(deal.shop_id)
    shop.update(freeze_guarantee=shop.freeze_guarantee - deal.sum_price_ltc,
                guarantee=shop.guarantee + deal.sum_price_ltc)

    deal.delete()
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()


def button_deal_buyer_confirm_payment(update, context, deal_id):
    query = update.callback_query
    query.answer()
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.status == 0:
        deal.update(proof_payment=True)
        deal_info = get_deal_info(
            deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Ожидайте пока Магазин подтвердит получение средств по выбранным Вами реквизитам_\n\n" \
                       "🔔 Посмотреть историю покупок и продублировать товар можно в разделе:\n" \
                       "\t\t\t\t*'Личный кабинет' -> 'Мои покупки'*"
        update.callback_query.edit_message_text(
            deal_info,
            parse_mode=telegram.ParseMode.MARKDOWN)
        deal_info = get_deal_info(
            deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nПокупатель подтвердил оплату по выбранным реквизитам\n\n" \
                       f"Проверьте оплату и *подтвердите* получение средств!"
        context.bot.sendMessage(deal.shop_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(0, deal, context),
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        return update.callback_query.edit_message_text("🔔  Статус этой покупки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Товары'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')


def button_deal_shop_confirm_payment(update, context, deal_id):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    deal = get_deal_by_id(deal_id)
    if deal is None:
        return update.callback_query.edit_message_text("<b>Сделка не найдена</b>\n",
                                                       parse_mode='HTML')
    buyer_id = deal.buyer_id
    product = get_product_by_id(deal.product_id)
    deal_info_get = get_deal_info(deal_id)
    if product.count < deal.count:
        deal_info = deal_info_get + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Недостаточно товара для выдачи! Срочно пополинте товар и подтвердите оплату ещё раз!*"
        update.callback_query.edit_message_text(
            deal_info, reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                                         resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)

        deal_info = deal_info_get + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*У магазина недостаточно товара для выдачи!*"
        context.bot.sendMessage(buyer_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
        return
    if deal.status != 0:
        return update.callback_query.edit_message_text("🔔  Статус этой покупки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Товары'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')
    if not deal.proof_payment:
        return update.callback_query.edit_message_text("<b>Покупатель ещё не подтвердил оплату</b>\n",
                                                       parse_mode='HTML')
    if product.count - deal.count == 0:
        context.bot.sendMessage(product.owner_id, f"   <b>У вас закончился товар</b>\n"
                                                  f"Название: {product.name}",
                                parse_mode="HTML")
    content_bytes = get_product_content_bytes(deal.product_id, deal.count)
    check_time = get_shop_check_time(owner_id)
    deal_info = deal_info_get + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nВы подтвердили получение средств. *Товар отправлен покупателю!*"
    update.callback_query.edit_message_text(
        deal_info,
        parse_mode=telegram.ParseMode.MARKDOWN)

    deal_info = deal_info_get + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\nУ вас есть *{int(check_time / 60)} минут* чтобы проверить товар, после чего покупка будет автоматически завершена\n\n" \
                                "‼  Если с товаром возникли проблемы - нажмите *открыть Диспут*\n\n" \
                                "🔔Посмотреть историю покупок и продублировать товар можно в разделе:\n" \
                                "\t\t\t\t*'Личный кабинет -> Мои покупки -> Товары'*"
    context.bot.sendMessage(buyer_id,
                            deal_info,
                            reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, 1, context),
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    message = context.bot.sendDocument(buyer_id, content_bytes, f"{deal.id}.{deal.count}.txt",
                                       caption=f"Выдача товара [{deal.count} шт.]")
    file_id = message.document.file_id
    deal.update(status=1, file_id=file_id)
    context.user_data[DEAL_ID] = deal.id
    job_context = f"{buyer_id}|{deal.id}"
    new_job = context.job_queue.run_repeating(check_deal_status, 60, context=job_context)
    context.chat_data['job'] = new_job


def button_select_shop_services(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[CATEGORY_SERVICES] = []
    context.user_data[CATEGORY_INFO] = {}
    get_cat_services_shop_tree(context, update)
    context.user_data[DATA] = 'select_shop_services'
    update.callback_query.edit_message_text(f"🤝  <b>Услуги магазина</b>\n\n"
                                            "📂 Вы видите категории услуг, которые предоставляет выбранный магазин."
                                            "\n\n<b>Какой раздел вас интересует❓</b>",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_service_btnlist_by_catid(context, None,
                                                                                    context.user_data[DATA],
                                                                                    chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_select_shop_prods_bycat(update, context, owner_id):
    query = update.callback_query
    query.answer()
    if CATEGORY_INFO not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    catid = context.user_data[CATEGORY_INFO]['cat_id']
    context.user_data[SELECT_ID] = owner_id
    products = Product.objects(category_id=catid, owner_id=owner_id)
    menu = []
    for prod in products:
        if prod.count > 0:
            menu.append([InlineKeyboardButton(f"{prod.name} |{prod.price} ₽|{prod.count}шт|",
                                              callback_data=f"select_product_{prod.id}")])
    menu.append(
        [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_select_shop_by_prods"),
         InlineKeyboardButton(f"{back_for_button}  Выбор раздела", callback_data='back_to_select_market_section')])
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
        terms_trade = "Не указаны"
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
        f"<b>Поражений в Диспутах:</b>  {get_shop_defeat_dispute(owner_id)}\n\n"
        f"<b>⚠ Условия торговли:</b>  {terms_trade}\n\n"
        f"{last_comments}<b>❓ Выберите товар:</b>",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_select_shop_products(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[CATEGORY_PRODS] = []
    context.user_data[CATEGORY_INFO] = {}
    get_cat_products_shop_tree(context, update)
    context.user_data[DATA] = 'select_shop_prods'
    update.callback_query.edit_message_text(f"<b>📦 Товары магазина</b>\n\n"
                                            "📂 Вы видите категории товаров которые есть у выбранного магазина.\n\n"
                                            "⚠️ Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила ведет к потере денежных средств без разбирательств.\n\n"
                                            "❓ <b>Выберите категорию товаров:</b>",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_btnlist_by_catid(context, None, context.user_data[DATA],
                                                                            chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_deal_buyer_moder_call(update, context, deal_id):
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.status == 2:
        deal.update(call_moderator=True)
        deal = get_deal_by_id(deal_id)
        deal_info = get_deal_info(
            deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Вы вызвали модератора, ожидайте...*\n\n"
        update.callback_query.edit_message_text(
            deal_info,
            reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                              resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)
        deal_info = get_deal_info(
            deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Покупатель вызвал модератора для данной сделки*\n\n"
        moders_alert(context, 'new_deal_moder_call')
        context.bot.sendMessage(deal.shop_id,
                                deal_info,
                                reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(2, deal, context),
                                                                  resize_keyboard=True),
                                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        return update.callback_query.edit_message_text("🔔  Статус этой покупки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Товары'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')


# ------------ Отзывы товары
def button_deal_buyer_like(update, context, deal_id):
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    deal.update(like=True)
    deal = get_deal_by_id(deal_id)
    deal_info = get_deal_info(deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Вы поставили Like Магазину*\n\n"
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                          resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)


def button_deal_buyer_dislike(update, context, deal_id):
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    deal.update(like=False)
    deal = get_deal_by_id(deal_id)
    deal_info = get_deal_info(deal.id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n*Вы поставили Dislike Магазину*\n\n"
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                          resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)


# -------------------- УСЛУГИ ----------------
def button_select_market_section_services(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    context.user_data[CATEGORY_SERVICES] = []
    context.user_data[CATEGORY_INFO] = {}
    get_cat_services_tree(context, update, chat_id)
    context.user_data[DATA] = 'for_user_services'
    update.callback_query.edit_message_text(f"🤝  <b>Услуги</b>\n\n"
                                            f"⚠  Фрилансеры оформляют свои услуги в виде обьявлений, которые можно купить в один клик. То есть работа исполнителей продается как товар, а это экономит массу времени, денег и нервов. Идеально подходит для типовых задач: логотипы, баннеры, SEO и др.\n\n"
                                            f"<b>Какой раздел вас интересует❓</b>\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_service_btnlist_by_catid(context, None,
                                                                                    context.user_data[DATA],
                                                                                    chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_select_service(update, context, service_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if CATEGORY_INFO not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    serv = Service.objects(id=service_id).first()
    context.user_data[SELECT_SERV_ID] = serv.id
    context.bot.sendPhoto(chat_id, serv.picture)
    shop = get_shop_obj(serv.owner_id)
    context.user_data[SELECT_ID] = shop.owner_id
    context.bot.sendMessage(chat_id, f"Категория:  {context.user_data[CATEGORY_INFO]['cat_path']}\n"
                                     f"<b>Исполнитель:</b>  {shop.shop_name}  ({shop.shop_id})\n\n"
                                     f"<b>Название услуги:</b>  {serv.name}\n\n"
                                     f"<b>Минимальная стоимость:</b>  {serv.min_price} ₽\n\n"
                                     f"<b>Описание услуги:</b>  {serv.description}",
                            reply_markup=InlineKeyboardMarkup(
                                market_select_service_menu,
                                resize_keyboard=True),
                            parse_mode='HTML')
    '''
    cat_path_text = ""
    if 'cat_path' in context.user_data[CATEGORY_INFO]:
        cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']
    context.bot.sendMessage(chat_id, f" <b>Рынок (услуги)</b>\n\nВыберите одно из предложений{cat_path_text}",
                            reply_markup=InlineKeyboardMarkup(
                                get_subcat_service_btnlist_by_catid(context, catid,
                                                                    context.user_data[DATA],
                                                                    chat_id),
                                resize_keyboard=True),
                            parse_mode='HTML')
    '''


def button_market_select_service_portfolio(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service = get_service_by_id(context.user_data[SELECT_SERV_ID])
    portfolio = service.portfolio
    if portfolio is None:
        context.bot.sendMessage(chat_id, "У исполнителя нет портфолио к выбранной услуге")
    else:
        context.bot.sendDocument(chat_id, portfolio,
                                 caption=f"Портфолио исполнителя",
                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{back_for_button}  Назад",
                                                                                          callback_data='back_to_market_select_service_menu_portfolio')]]))


def button_market_select_service_order(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service = get_service_by_id(context.user_data[SELECT_SERV_ID])
    if chat_id == service.owner_id:
        return context.bot.sendMessage(chat_id, "Вы не можете заказать услугу у себя")
    if get_user_balance(chat_id) < get_ltc_by_rub(service.min_price):
        return context.bot.sendMessage(chat_id, "У вас недостаточно средств для заказа!")
    menu = []
    if service.eco_description is not None:
        menu.append(
            [InlineKeyboardButton(f"Эконом | {service.eco_price} ₽ | Дней на выполнение - {service.eco_deadline} ",
                                  callback_data=f"market_select_service_packet_eco")])
    if service.standart_description is not None:
        menu.append([InlineKeyboardButton(
            f"Стандарт | {service.standart_price} ₽ | Дней на выполнение - {service.standart_deadline}",
            callback_data=f"market_select_service_packet_standart")])
    if service.biz_description is not None:
        menu.append(
            [InlineKeyboardButton(f"Бизнес | {service.biz_price} ₽ | Дней на выполнение - {service.biz_deadline}",
                                  callback_data=f"market_select_service_packet_biz")])
    menu.append([InlineKeyboardButton(f"Уникальный заказ | от {service.min_price} ₽",
                                      callback_data="market_select_service_packet_unique")])
    menu.append(
        [InlineKeyboardButton(f"{back_for_button}  Назад",
                              callback_data='back_to_market_select_service_menu')])
    update.callback_query.edit_message_text(
        f"<b>Оформление заказа</b>\n\n❓ Выберите один из предлагаемых пакетов или предложите уникальный заказ\n\n",
        reply_markup=InlineKeyboardMarkup(
            menu,
            resize_keyboard=True),
        parse_mode='HTML')


def button_market_select_service_packet_eco(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    if get_user_balance(chat_id) < get_ltc_by_rub(service.eco_price):
        return update.callback_query.edit_message_text("У вас недостаточно средств для выбора этого пакета!",
                                                       reply_markup=InlineKeyboardMarkup(
                                                           [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                                  callback_data='back_to_market_select_service_order')]],
                                                           resize_keyboard=True),
                                                       parse_mode='HTML')
    context.user_data[SELECT_SERV_PACKET] = 1
    update.callback_query.edit_message_text(
        f"   <b>Оформление заказа</b>\n\n"
        f"Вы выбрали пакет 'Эконом'\n\n"
        f"<b>Стоимость пакета:</b>  {service.eco_price} ₽\n\n"
        f"<b>Описание пакета:</b>  {service.eco_description}\n\n"
        f"<b>Срок выполнения:</b>  {service.eco_deadline} дней\n\n"
        f"Отправьте Техническое задание <b>текстом</b> или файлом <b>(txt / word / pdf)</b>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_market_select_service_order')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return CLIENT_SEND_TZ


def button_market_select_service_packet_standart(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    if get_user_balance(chat_id) < get_ltc_by_rub(service.standart_price):
        return update.callback_query.edit_message_text("У вас недостаточно средств для выбора этого пакета!",
                                                       reply_markup=InlineKeyboardMarkup(
                                                           [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                                  callback_data='back_to_market_select_service_order')]],
                                                           resize_keyboard=True),
                                                       parse_mode='HTML')
    context.user_data[SELECT_SERV_PACKET] = 2
    update.callback_query.edit_message_text(
        f"   <b>Оформление заказа</b>\n\n"
        f"Вы выбрали пакет 'Стандарт'\n\n"
        f"<b>Стоимость пакета:</b>  {service.standart_price} ₽\n\n"
        f"<b>Описание пакета:</b>  {service.standart_description}\n\n"
        f"<b>Срок выполнения:</b>  {service.standart_deadline} дней\n\n"
        f"Отправьте Техническое задание <b>текстом</b> или файлом <b>(txt / word / pdf)</b>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_market_select_service_order')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return CLIENT_SEND_TZ


def button_market_select_service_packet_biz(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    if get_user_balance(chat_id) < get_ltc_by_rub(service.biz_price):
        return update.callback_query.edit_message_text("У вас недостаточно средств для выбора этого пакета!",
                                                       reply_markup=InlineKeyboardMarkup(
                                                           [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                                  callback_data='back_to_market_select_service_order')]],
                                                           resize_keyboard=True),
                                                       parse_mode='HTML')
    context.user_data[SELECT_SERV_PACKET] = 3
    update.callback_query.edit_message_text(
        f"   <b>Оформление заказа</b>\n\n"
        f"Вы выбрали пакет 'Бизнес'\n\n"
        f"<b>Стоимость пакета:</b>  {service.biz_price} ₽\n\n"
        f"<b>Описание пакета:</b>  {service.biz_description}\n\n"
        f"<b>Срок выполнения:</b>  {service.biz_deadline} дней\n\n"
        f"Отправьте Техническое задание <b>текстом</b> или файлом <b>(txt / word / pdf)</b>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_market_select_service_order')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return CLIENT_SEND_TZ


def button_market_select_service_packet_unique(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    context.user_data[SELECT_SERV_PACKET] = 4
    update.callback_query.edit_message_text(
        f"   <b>Оформление заказа</b>\n\n"
        f"Вы выбрали уникальный заказ\n\n"
        f"<b>Стоимость и сроки выполнения будут уточнены Исполнителем после изучения ТЗ</b>\n\n"
        f"Отправьте Техническое задание <b>текстом</b> или файлом <b>(txt / word / pdf)</b>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_market_select_service_order')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return CLIENT_SEND_TZ


def button_order_client_cancel(update, context, order_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status > 1:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if order.packet < 4 and order.price_ltc is not None:
        add_user_balance(chat_id, order.price_ltc)
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ отменён, средства возвращены на ваш счёт!</i>"
    else:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ успешно отменён!</i>"
    update.callback_query.edit_message_text(
        f"⚠  <b>Информация о заказе</b>\n\n"
        f"{get_order_info(order_id)}{text_info}",
        parse_mode='HTML')

    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказчик отменил данный заказ!</i>"
    context.bot.sendMessage(order.shop_id,
                            f"{get_order_info(order_id)}{text_info}",
                            parse_mode='HTML')
    order.delete()


def button_order_shop_tz(update, context, order_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    try:
        context.bot.get_file(order.tz)
    except Exception as e:
        if str(e) == 'Invalid file_id':
            context.bot.sendMessage(chat_id, "<b>Техническое задание к заказу</b>\n\n" + order.tz,
                                    reply_markup=InlineKeyboardMarkup(
                                        [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                               callback_data='back_to_shop_order_menu')]],
                                        resize_keyboard=True),
                                    parse_mode='HTML')
    else:
        context.bot.sendDocument(chat_id, order.tz, caption="Техническое задание к заказу",
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                            callback_data='back_to_shop_order_menu')]],
                                     resize_keyboard=True),
                                 parse_mode='HTML')


def button_order_client_tz(update, context, order_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    try:
        context.bot.get_file(order.tz)
    except Exception as e:
        if str(e) == 'Invalid file_id':
            context.bot.sendMessage(chat_id, "<b>Техническое задание к заказу</b>\n\n" + order.tz,
                                    reply_markup=InlineKeyboardMarkup(
                                        [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                               callback_data='back_to_client_order_menu')]],
                                        resize_keyboard=True),
                                    parse_mode='HTML')
    else:
        context.bot.sendDocument(chat_id, order.tz, caption="Техническое задание к заказу",
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                            callback_data='back_to_client_order_menu')]],
                                     resize_keyboard=True),
                                 parse_mode='HTML')


def button_order_shop_cancel(update, context, order_id):
    query = update.callback_query
    query.answer()
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status != 0:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')

    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы отказались от выполнения этого заказа!</i>"

    update.callback_query.edit_message_text(
        f"⚠  <b>Информация о заказе</b>\n\n"
        f"{text_info}",
        parse_mode='HTML')

    if order.packet < 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Исполнитель отказался выполнять данный заказ!</i>\n" \
                    "<i>Средства возвращены на ваш счёт</i>"
        add_user_balance(order.client_id, order.price_ltc)
    else:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Исполнитель отказался выполнять данный заказ!</i>\n"
    context.bot.sendMessage(order.client_id,
                            f"{get_order_info(order_id)}{text_info}",
                            parse_mode='HTML')
    order.delete()


def button_order_shop_accept(update, context, order_id):
    query = update.callback_query
    query.answer()
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status != 0:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if order.packet < 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы подтвердили выполнение данного заказа\n\n" \
                    "Выполните заказ в срок и отправьте материалы Заказчику!</i>"
        now = datetime.now()
        date_start = now
        date_deadline = date_start + timedelta(days=order.deadline_days)
        order.update(date_start=date_start, date_deadline=date_deadline, status=2)
        update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, 2, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
        text_info = f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Исполнитель подтвердил выполнение данного заказа {e_smiling}\nОжидайте отправки файлов выполненного заказа</i>"
        context.bot.sendMessage(order.client_id,
                                f"{get_order_info(order_id)}{text_info}",
                                reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, 2, context),
                                                                  resize_keyboard=True),
                                parse_mode='HTML')
    else:
        if order.price is None or order.price_ltc is None or order.deadline_days is None:
            text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы не оценили данный заказ!</i>"
            update.callback_query.edit_message_text(
                f"{get_order_info(order_id)}{text_info}",
                reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                                  resize_keyboard=True),
                parse_mode='HTML')
            return
        now = datetime.now()
        date_start = now
        date_deadline = date_start + timedelta(days=order.deadline_days)
        order.update(date_start=date_start, date_deadline=date_deadline, status=1)

        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы подтвердили выполнение данного заказа\n\n" \
                    "Ожидайте согласия Заказчика!</i>"

        update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, 1, context),
                                              resize_keyboard=True),
            parse_mode='HTML')

        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Исполнитель оценил и подтвердил заказ\nПосмотрите ещё раз данные о заказе и подтвердите его</i>"
        context.bot.sendMessage(order.client_id,
                                f"{get_order_info(order_id)}{text_info}",
                                reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, 1, context),
                                                                  resize_keyboard=True),
                                parse_mode='HTML')


def button_order_client_confirm(update, context, order_id):
    query = update.callback_query
    query.answer()
    order = get_order_by_id(order_id)
    chat_id = query.message.chat.id
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.packet < 4 or order.price_ltc is None or order.deadline_days is None or order.price is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Ошибка!",
            parse_mode='HTML')
    if order.status != 1:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if get_user_balance(chat_id) < order.price_ltc:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>У вас недостаточно средств для оплаты данного заказа!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    add_user_balance(chat_id, order.price_ltc)

    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы оплатили и подтвердили данный заказ\n\n" \
                "Исполнитель отправит материалы когда выполнит заказ!</i>"
    now = datetime.now()
    date_start = now
    date_deadline = date_start + timedelta(days=order.deadline_days)
    order.update(date_start=date_start, date_deadline=date_deadline, status=2)

    update.callback_query.edit_message_text(
        f"{get_order_info(order_id)}{text_info}",
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, 2, context),
                                          resize_keyboard=True),
        parse_mode='HTML')

    text_info = f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказчик подтвердил данный заказ {e_smiling}\n" \
                "Выполните заказ в срок и отправьте материалы заказчику</i>"
    context.bot.sendMessage(order.shop_id,
                            f"{get_order_info(order_id)}{text_info}",
                            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, 2, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')


def button_order_client_close(update, context, order_id):
    query = update.callback_query
    query.answer()
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status != 2 and order.status != 3:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if order.order_work is None:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Исполнитель ничего вам не отправил!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы завершили данный заказ!</i>"
    order.update(status=4)
    update.callback_query.edit_message_text(
        f"{get_order_info(order_id)}{text_info}",
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, 4, context),
                                          resize_keyboard=True),
        parse_mode='HTML')
    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказчик завершил данный заказ, средства перечислены на счёт Вашего магазина!\n</i>"
    add_shop_balance(order.shop_id, order.price_ltc - (order.price_ltc * commission_per_deals))
    context.bot.sendMessage(order.shop_id,
                            f"{get_order_info(order_id)}{text_info}",
                            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, 4, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    now = datetime.now()
    if now > order.date_deadline:
        order.update(late_deadline=True)


def button_order_client_get_service(update, context, order_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.order_work is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Исполнитель ничего вам не отправлял!",
            parse_mode='HTML')
    context.bot.sendDocument(chat_id, order.order_work, caption="Выполненный заказ")


def button_order_client_dispute(update, context, order_id):
    query = update.callback_query
    query.answer()
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status != 2:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы открыли Диспут по данному заказу.\n" \
                "Решайте проблему с Исполнителем, через час вы сможете вызвать модератора!</i>"
    order.update(status=3)
    update.callback_query.edit_message_text(
        f"{get_order_info(order_id)}{text_info}",
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, 3, context),
                                          resize_keyboard=True),
        parse_mode='HTML')

    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказчик открыл Диспут по данному заказу.\n" \
                "Решайте проблему с Заказчиком, через час он сможет вызвать модератора!</i>"
    context.bot.sendMessage(order.shop_id,
                            f"{get_order_info(order_id)}{text_info}",
                            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, 3, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    job_context = order.id
    new_job = context.job_queue.run_repeating(call_moder_order_add, 3600, context=job_context)
    context.chat_data['job'] = new_job


def call_moder_order_add(context):
    job = context.job
    order_id = job.context
    order = get_order_by_id(order_id)
    if order.status == 3 and order.call_moderator is False:
        order.update(potential=True)
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Теперь вы можете вызвать модератора для данного заказа\n</i>"
        context.bot.sendMessage(order.client_id,
                                f"{get_order_info(order_id)}{text_info}",
                                reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, 3, context),
                                                                  resize_keyboard=True),
                                parse_mode='HTML')
    job.schedule_removal()


def button_order_client_moder_call(update, context, order_id):
    query = update.callback_query
    query.answer()
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(
            f"⚠  <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status != 3 or order.potential is False:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы вызвали модератора для данного заказа. Ожидайте...</i>"
    order.update(call_moderator=True)
    update.callback_query.edit_message_text(
        f"{get_order_info(order_id)}{text_info}",
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                          resize_keyboard=True),
        parse_mode='HTML')

    text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказчик вызвал модератора для данного заказа!</i>"
    moders_alert(context, 'new_order_moder_call')
    context.bot.sendMessage(order.shop_id,
                            f"{get_order_info(order_id)}{text_info}",
                            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')


# ------------ Отзывы в услугах --------------
def button_order_buyer_like(update, context, order_id):
    order = get_order_by_id(order_id)
    if not order:
        return update.callback_query.edit_message_text("Не актуально")
    order.update(like=True)
    order = get_order_by_id(order_id)
    order_info = get_order_info(order_id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<b>Вы поставили Like Магазину</b>\n\n"
    update.callback_query.edit_message_text(
        order_info,
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order_id, order.status, context),
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_order_buyer_dislike(update, context, order_id):
    order = get_order_by_id(order_id)
    if not order:
        return update.callback_query.edit_message_text("Не актуально")
    order.update(like=False)
    order = get_order_by_id(order_id)
    order_info = get_order_info(order_id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<b>Вы поставили Dislike Магазину</b>\n\n"
    update.callback_query.edit_message_text(
        order_info,
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order_id, order.status, context),
                                          resize_keyboard=True),
        parse_mode='HTML')


# ============== Отзывы ===================
def button_select_shop_comments(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    shop_name = get_shop_name(context.user_data[SELECT_ID])
    menu = deepcopy(select_comments_section)
    if check_moderator(chat_id) and context.user_data[SELECT_ID] != chat_id:
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_moder_select_shop_menu')])
    elif context.user_data[SELECT_ID] == chat_id:
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_menu')])
    else:
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_user_select_shop_menu')])
    update.callback_query.edit_message_text(
        f"🗣  <b>Отзывы о магазине  {shop_name}</b>\n\n<b>❓ Выберите раздел</b>",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_market_select_service_comments(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_SERV_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    show_list_text(update, context, "shop_services_comments")


def button_select_comments_section_products(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    show_list_text(update, context, "shop_products_comments")


def button_select_comments_section_services(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    show_list_text(update, context, "shop_services_comments")


# ========================================== РАЗДЕЛ МОДЕРАТОРА ======================================================
def button_section_moderator_handler(update, context):
    update.message.reply_text(f'{e_policeman}   <b>Раздел модератора</b>',
                              reply_markup=InlineKeyboardMarkup(moderator_menu, resize_keyboard=True),
                              parse_mode='HTML')


# Выбор Раздел модератора -> Магазины
def button_submenu_moder_shops(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Магазины</b>\n\nРаздел модерации Магазинов",
        reply_markup=InlineKeyboardMarkup(shop_moder_menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


# Выбор Раздел модератора -> Магазины -> Заявки на открытие
def button_shop_moder_requests(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"<b>Заявки на открытие</b>\n\nСписок заявок на открытие магазина",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "requests"),
                                          resize_keyboard=True),
        parse_mode='HTML')


# Выбор конкретной заявки
def button_req_open_shop(update, context, creator_id):
    query = update.callback_query
    query.answer()
    req_creator_id = creator_id
    user = get_user_obj(req_creator_id)
    req_creator_name = user.username
    shop_req_obj = get_shop_request_obj(req_creator_id)
    shop_name = shop_req_obj.shop_name
    shop_request_date = shop_req_obj.created_at
    shop_why = shop_req_obj.why
    update.callback_query.edit_message_text(
        f"   <b>Управление заявкой</b>\n\n"
        f"Название:  <i>{shop_name}</i>\n"
        f"TG отправителя:  @{req_creator_name}\n"
        f"ID отправителя:  {user.user_id}\n"
        f"Дата отправки:  {shop_request_date}\n\n"
        f"<b>Вид деятельности:</b>  {shop_why}\n"
        f"<b>Ресурс:</b>  {shop_req_obj.res}",
        reply_markup=InlineKeyboardMarkup(shop_moder_requests_approved_menu(req_creator_id),
                                          resize_keyboard=True),
        parse_mode='HTML')
    context.user_data[SELECT_ID] = creator_id


# одобрение заявки и создание магазина
def button_shop_moder_requests_approved_yes(update, context):
    query = update.callback_query
    query.answer()
    req_creator_id = query.data[33:]
    who_approved = query.message.chat.id
    add_new_shop(req_creator_id, who_approved)
    delete_req_open_shop(req_creator_id)
    menu = update_main_menu(req_creator_id)
    context.bot.sendMessage(req_creator_id,
                            "<b>[Оповещение]</b> Ваша заявка на создание магазина была одобрена модератором\n\n"
                            "Для вас открыт раздел <i>'Мой магазин'</i> в главном меню!\n"
                            "Там вы сможете добавить описание, товары и услуги, внести гарант и многое другое\n\n"
                            f"Желаем прибыльной работы с нами в команде {e_winking}", reply_markup=menu,
                            parse_mode='HTML')
    update.callback_query.edit_message_text(
        f"<b>Заявки на открытие</b>\n\nЗаявка успешно одобрена",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "requests"),
                                          resize_keyboard=True, parse_mode='HTML'),
        parse_mode='HTML')
    return


# отклонение заявки на создание магазина
def button_shop_moder_requests_approved_no(update, context):
    query = update.callback_query
    query.answer()
    req_creator_id = query.data[32:]
    delete_req_open_shop(req_creator_id)
    context.bot.sendMessage(req_creator_id,
                            "<b>[Оповещение]</b> Ваша заявка на создание магазина была отклонена модератором",
                            parse_mode='HTML')
    update.callback_query.edit_message_text(
        f"<b>Заявки на открытие</b>\n\nЗаявка успешно отклонена",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "requests"),
                                          resize_keyboard=True), parse_mode='HTML')


# показ списка магазинов
def button_shop_moder_list(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Список магазинов</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "shops"),
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_shop_moder_search(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Поиск магазина</b>",
        reply_markup=InlineKeyboardMarkup(shop_moder_find_menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


# меню поиска пользователя
def button_submenu_moder_users(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Поиск пользователя</b>",
        reply_markup=InlineKeyboardMarkup(moder_find_user_menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


# обработка выбора магазина в списке
def button_moder_select_shop(update, context, owner_id):
    query = update.callback_query
    query.answer()
    text = get_shop_info_text(query.message.chat.id, owner_id)
    update.callback_query.edit_message_text(text,
                                            reply_markup=InlineKeyboardMarkup(get_moder_select_shop_menu(owner_id),
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')
    context.user_data[SELECT_ID] = owner_id


def button_moder_select_shop_ban(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    owner_id = context.user_data[SELECT_ID]
    shop = get_shop_obj(owner_id)
    if shop.banned:
        shop_unban(owner_id)
        update.callback_query.edit_message_text(
            f"   <b>Список магазинов</b>\n\nМагазин <b>{shop.shop_name}</b> успешно разблокирован",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "shops"),
                                              resize_keyboard=True),
            parse_mode='HTML')
        context.bot.sendMessage(owner_id,
                                f"<b>[Оповещение]</b> Ваш магазин был разблокирован модератором {e_smiling}\n"
                                f"Больше не нарушайте правила сервиса!\n",
                                reply_markup=update_main_menu(owner_id),
                                parse_mode='HTML')
    else:
        shop_ban(owner_id)
        update.callback_query.edit_message_text(
            f"   <b>Список магазинов</b>\n\nМагазин <b>{shop.shop_name}</b> успешно заблокирован",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "shops"),
                                              resize_keyboard=True),
            parse_mode='HTML')
        context.bot.sendMessage(owner_id,
                                f"<b>[Оповещение]</b> Ваш магазин был заблокирован модератором за нарушение правил "
                                f"сервиса!\n"
                                f"\n<b>Техническая поддержка</b>:  {url_support}\n\n",
                                reply_markup=update_main_menu(owner_id),
                                parse_mode='HTML')


def button_moder_select_user_ban(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    select_user_id = context.user_data[SELECT_ID]
    select_user_obj = get_user_obj(select_user_id)
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if select_user_obj.banned:
        user_unban(select_user_obj)
        text = get_user_info_text(chat_id, select_user_id)
        update.callback_query.edit_message_text(text,
                                                reply_markup=InlineKeyboardMarkup(moder_select_user_menu,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
        context.bot.sendMessage(select_user_obj.chat_id,
                                f"<b>[Оповещение]</b> Вы были разблокированы модератором {e_smiling}\n"
                                f"Больше не нарушайте правила сервиса!\n",
                                reply_markup=update_main_menu(select_user_obj.chat_id),
                                parse_mode='HTML')

    else:
        if select_user_id == chat_id:
            return context.bot.sendMessage(chat_id,
                                           f"Вы не можете заблокировать сами себя!",
                                           parse_mode='HTML')
        if check_moderator(select_user_id):
            return context.bot.sendMessage(chat_id,
                                           f"Вы не можете заблокировать модератора!",
                                           parse_mode='HTML')
        user_ban(select_user_obj)
        text = get_user_info_text(chat_id, select_user_id)
        update.callback_query.edit_message_text(text,
                                                reply_markup=InlineKeyboardMarkup(moder_select_user_menu,
                                                                                  resize_keyboard=True),
                                                parse_mode='HTML')
        context.bot.sendMessage(select_user_obj.chat_id,
                                f"<b>[Оповещение]</b> Вы были заблокированы модератором за нарушение правил сервиса!"
                                f"\n\n<b>Техническая поддержка:</b> {url_support}\n\n",
                                reply_markup=ReplyKeyboardRemove(),
                                parse_mode='HTML')


def button_moder_select_user_payments(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    show_list_text(update, context, "user_payments")


# def myshop_info(update, context):
#    query = update.callback_query
#    query.answer()
#    owner_id = query.message.chat.id
#    text = e_memo + "  " + get_shop_info_text(owner_id)
#    update.callback_query.edit_message_text(text,
#                                           reply_markup=InlineKeyboardMarkup(myshop_info_menu,
#                                                                              resize_keyboard=True),
#                                           parse_mode='HTML')


def button_moder_select_shop_operations(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    show_list_text(update, context, "shop_operations")


# БУХГАЛТЕРИЯ
def button_submenu_moder_bookkeeping(update, context):
    menu = [[InlineKeyboardButton(
        f'{back_for_button}  Назад',
        callback_data='back_to_moder_menu')]]

    query = update.callback_query
    query.answer()

    coinbase_balance = get_coinbase_balance()
    users_balance = get_users_balance()
    shops_balance = get_shops_balance()
    shops_guarantee = get_shops_guarantee()
    shops_freeze_guarantee = get_shops_freeze_guarantee()
    users_count = get_users_count()

    info = f"Всего пользователей:  <b>{users_count}</b>\n\n" \
           f"Баланс пользователей (сумма):  <b>{round(users_balance, 8)}</b> LTC\n" \
           f"Баланс магазинов (сумма):  <b>{round(shops_balance, 8)}</b> LTC\n" \
           f"Гарант магазинов (сумма):  <b>{round(shops_guarantee, 8)}</b> LTC\n" \
           f"Заморожено гаранта магазинов (сумма):  <b>{round(shops_freeze_guarantee, 8)}</b> LTC\n" \
           f"<b>Сумма:</b>  {round((users_balance + shops_balance + shops_guarantee + shops_freeze_guarantee), 8)} LTC\n\n" \
           f"Баланс COINBASE:  <b>{round(coinbase_balance, 8)}</b> LTC"

    return update.callback_query.edit_message_text(
        f"💰  <b>Бухгалтерия</b>\n\n{info}",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


# ---------- Модератор выбирает продажи магазина ---------------
def button_moder_select_shop_sales(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    shop_id = context.user_data[SELECT_ID]
    query = update.callback_query
    query.answer()
    open_deals = count_open_deals(shop_id)
    open_orders = count_open_sh_orders(shop_id)
    update.callback_query.edit_message_text(
        f"{e_shopping_bags}  <b>Продажи магазина {get_shop_name(shop_id)}  ({get_shop_id(shop_id)})</b>\n\n"
        f"Незавершенные продажи:\n"
        f"\t\tТовары - <b>{open_deals}</b>\n"
        f"\t\tУслуги - <b>{open_orders}</b>\n\n❓ <b>Выберите тип продаж</b>",
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


# ------------------------------  Продажи магазина для модера -----------------------------
# --------- Товары -----------
def button_moder_shop_sales_type_products(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    shop_id = context.user_data[SELECT_ID]
    count_dispute = get_shop_dispute_deals_count(shop_id)
    count_open = get_shop_open_deals_count(shop_id)
    count_close = get_shop_close_deals_count(shop_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text(
            f"{e_shopping_bags}  <b>Продажи магазина {get_shop_name(shop_id)}  ({get_shop_id(shop_id)}) (товары)</b>\n\nУ этого магазина нет сделок",
            reply_markup=
            InlineKeyboardMarkup([[InlineKeyboardButton(
                f'{back_for_button}  Назад',
                callback_data='back_moder_shop_sales_type')]],
                resize_keyboard=True),
            parse_mode='HTML')
    menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_shop_sales")
    update.callback_query.edit_message_text(
        f"{e_shopping_bags}  <b>Продажи магазина {get_shop_name(shop_id)}  ({get_shop_id(shop_id)}) (товары)</b>\n\n<b>❓ Выберите раздел сделки</b>",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_moder_select_section_dispute(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_SALE_SECTION] = "dispute"
    update.callback_query.edit_message_text(
        f"<b>Диспуты (товары)</b>\n\n<b><b>❓ Выберите сделку</b></b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_section_open(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_SALE_SECTION] = "open"
    update.callback_query.edit_message_text(
        f"<b>Незавершенные сделки (товары)</b>\n\n<b><b>❓ Выберите сделку</b></b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_section_close(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_SALE_SECTION] = "close"
    update.callback_query.edit_message_text(
        f"<b>Завершенные сделки (товары)</b>\n\n<b><b>❓ Выберите сделку</b></b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_shop_sales(update, context, deal_id):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    deal = get_deal_by_id(deal_id)
    context.user_data[DEAL_ID] = deal_id
    if deal.call_moderator and deal.status == 2:
        menu = [
            [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_menu_messages'),
             InlineKeyboardButton(f"Товар", callback_data='moder_select_call_menu_content')],
            [InlineKeyboardButton(f"Закрыть сделку", callback_data='moder_select_call_menu_close_deal')],
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_shop_sales_list')]
        ]
    else:
        menu = [
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_shop_sales_list')]
        ]
    deal_info = get_deal_info(deal_id)
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(
            menu,
            resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)


# ----------- Услуги
def button_moder_shop_sales_type_services(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    shop_id = context.user_data[SELECT_ID]
    count_dispute = get_shop_dispute_orders_count(shop_id)
    count_open = get_shop_open_orders_count(shop_id)
    count_close = get_shop_close_orders_count(shop_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text(
            f"{e_shopping_bags}  <b>Продажи магазина {get_shop_name(shop_id)}  ({get_shop_id(shop_id)}) (услуги)</b>\n\nУ этого магазина нет заказов",
            reply_markup=
            InlineKeyboardMarkup([[InlineKeyboardButton(
                f'{back_for_button}  Назад',
                callback_data='back_moder_shop_sales_type')]],
                resize_keyboard=True),
            parse_mode='HTML')
    menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_shop_service_sales")
    update.callback_query.edit_message_text(
        f"{e_shopping_bags}  <b>Продажи магазина {get_shop_name(shop_id)}  ({get_shop_id(shop_id)}) (услуги)</b>\n\n<b>❓ Выберите раздел заказов</b>",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_moder_select_service_section_dispute(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_SALE_SECTION] = "dispute"
    update.callback_query.edit_message_text(
        f"<b>Диспутны (услуги)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_service_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_service_section_open(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_SALE_SECTION] = "open"
    update.callback_query.edit_message_text(
        f"<b>Незавершенные заказы (услуги)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_service_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_service_section_close(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_SALE_SECTION] = "close"
    update.callback_query.edit_message_text(
        f"<b>Завершенные заказы (услуги)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_shop_service_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_shop_service_sales(update, context, order_id):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    if order.call_moderator and order.status == 3:
        menu = [
            [InlineKeyboardButton(f"Техническое задание", callback_data='moder_select_call_order_menu_tz')],
            [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_order_menu_messages'),
             InlineKeyboardButton(f"Закрыть заказ", callback_data='moder_select_call_order_menu_close')],
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_shop_service_sales_list')]
        ]
    else:
        menu = [
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_shop_service_sales_list')]
        ]
    order_info = get_order_info(order_id)
    update.callback_query.edit_message_text(
        order_info,
        reply_markup=InlineKeyboardMarkup(
            menu,
            resize_keyboard=True),
        parse_mode='HTML')


# ---------- Модератор выбирает покупки пользователя ---------------
def button_moder_select_user_buys(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    user_id = context.user_data[SELECT_ID]
    update.callback_query.edit_message_text(
        f"<b>Покупки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)})</b>\n\n❓ Выберите тип покупок",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"📦  Товары",
                                  callback_data='moder_user_buys_type_products'),
             InlineKeyboardButton(f"🤝  Услуги",
                                  callback_data='moder_user_buys_type_services')],
            [InlineKeyboardButton(
                f'{back_for_button}  Назад',
                callback_data='back_moder_select_user_menu')]
        ],
            resize_keyboard=True),
        parse_mode='HTML')


def button_moder_user_buys_type_products(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    user_id = context.user_data[SELECT_ID]
    count_dispute = get_user_dispute_deals_count(user_id)
    count_open = get_user_open_deals_count(user_id)
    count_close = get_user_close_deals_count(user_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text(
            f"<b>Сделки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)</b>\n\nПользователь не делал покупки товаров",
            reply_markup=
            InlineKeyboardMarkup([[InlineKeyboardButton(
                f'{back_for_button}  Назад',
                callback_data='back_moder_select_user_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_user_buys")
    update.callback_query.edit_message_text(
        f"<b>Сделки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)</b>\n\n<b>❓ Выберите раздел сделки</b>",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_moder_select_user_buys_section_dispute(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_BUYS_SECTION] = "dispute"
    user_id = context.user_data[SELECT_ID]
    update.callback_query.edit_message_text(
        f"<b>Диспуты пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_buys"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_user_buys_section_open(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_BUYS_SECTION] = "open"
    user_id = context.user_data[SELECT_ID]
    update.callback_query.edit_message_text(
        f"<b>Незавершенные сделки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_buys"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_user_buys_section_close(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_BUYS_SECTION] = "close"
    user_id = context.user_data[SELECT_ID]
    update.callback_query.edit_message_text(
        f"<b>Завершенные сделки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_buys"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_user_buys(update, context, deal_id):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[DEAL_ID] = deal_id
    deal = get_deal_by_id(deal_id)
    if deal.call_moderator and deal.status == 2:
        menu = [
            [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_menu_messages'),
             InlineKeyboardButton(f"Товар", callback_data='moder_select_call_menu_content')],
            [InlineKeyboardButton(f"Закрыть сделку", callback_data='moder_select_call_menu_close_deal')],
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_user_buys_list')]
        ]
    else:
        menu = [
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_user_buys_list')]
        ]
    deal_info = get_deal_info(deal_id)
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(
            menu,
            resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)


# ------------------------------------ Покупки пользователя (Услуги)
def button_moder_user_buys_type_services(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    user_id = context.user_data[SELECT_ID]
    count_dispute = get_user_dispute_orders_count(user_id)
    count_open = get_user_open_orders_count(user_id)
    count_close = get_user_close_orders_count(user_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text(
            f"<b>Заказы пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (услуги)</b>\n\nПользователь не делал заказы услуг",
            reply_markup=
            InlineKeyboardMarkup([[InlineKeyboardButton(
                f'{back_for_button}  Назад',
                callback_data='back_moder_select_user_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    menu = get_submenu_trades(count_dispute, count_open, count_close, "moder_user_orders")
    update.callback_query.edit_message_text(
        f"<b>Заказы пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (услуги)</b>\n\n<b>❓ Выберите раздел заказа</b>",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_moder_select_user_orders_section_dispute(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_BUYS_SECTION] = "dispute"
    user_id = context.user_data[SELECT_ID]
    update.callback_query.edit_message_text(
        f"<b>Диспутны пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_orders"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_user_orders_section_open(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_BUYS_SECTION] = "open"
    user_id = context.user_data[SELECT_ID]
    update.callback_query.edit_message_text(
        f"<b>Незавершенные заказы пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_orders"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_select_user_orders_section_close(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_BUYS_SECTION] = "close"
    user_id = context.user_data[SELECT_ID]
    update.callback_query.edit_message_text(
        f"<b>Завершенные заказы пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "moder_user_orders"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_moder_user_orders(update, context, order_id):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    if order.call_moderator and order.status == 3:
        menu = [
            [InlineKeyboardButton(f"Техническое задание", callback_data='moder_select_call_order_menu_tz')],
            [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_order_menu_messages'),
             InlineKeyboardButton(f"Закрыть заказ", callback_data='moder_select_call_order_menu_close')],
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_user_orders_list')]
        ]
    else:
        menu = [
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_user_orders_list')]
        ]
    order_info = get_order_info(order_id)
    update.callback_query.edit_message_text(
        order_info,
        reply_markup=InlineKeyboardMarkup(
            menu,
            resize_keyboard=True),
        parse_mode='HTML')


# ------------ Список вызовов -------------
def button_submenu_moder_calls(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Список вызовов</b>\n\n<b>❓ Выберите раздел</b>",
        reply_markup=InlineKeyboardMarkup(select_section_calls,
                                          resize_keyboard=True),
        parse_mode='HTML')


# ----------- Список вызовов СДЕЛКИ ------------
def button_submenu_moder_calls_deals(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Список вызовов (сделки)</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "deal_moder_call"),
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_deal_moder_call(update, context, deal_id):
    context.user_data[DEAL_ID] = deal_id
    deal_info = get_deal_info(deal_id)
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(moder_select_call_menu,
                                          resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)


def button_moder_select_call_menu_close_deal(update, context):
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    if SELECT_SALE_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Закрытие сделки</b>\n\n❓ Выберите в чью пользу желаете закрыть сделку",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Магазина", callback_data='moder_select_call_menu_close_deal_shop'),
                 InlineKeyboardButton(f"Покупателя", callback_data='moder_select_call_menu_close_deal_buyer')],
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data='back_to_moder_select_sale')]
            ],
                resize_keyboard=True),
            parse_mode='HTML')
    elif SELECT_BUYS_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Закрытие сделки</b>\n\n❓ Выберите в чью пользу желаете закрыть сделку",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Магазина", callback_data='moder_select_call_menu_close_deal_shop'),
                 InlineKeyboardButton(f"Покупателя", callback_data='moder_select_call_menu_close_deal_buyer')],
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data='back_to_moder_user_select_buy')]
            ],
                resize_keyboard=True),
            parse_mode='HTML')
    else:
        update.callback_query.edit_message_text(
            f"   <b>Закрытие сделки</b>\n\n❓ Выберите в чью пользу желаете закрыть сделку",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Магазина", callback_data='moder_select_call_menu_close_deal_shop'),
                 InlineKeyboardButton(f"Покупателя", callback_data='moder_select_call_menu_close_deal_buyer')],
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data='back_to_select_deal_call_menu')]
            ],
                resize_keyboard=True),
            parse_mode='HTML')


def button_moder_select_call_menu_close_deal_shop(update, context):
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    deal_id = context.user_data[DEAL_ID]
    d_info = get_deal_info(deal_id)
    deal_info = d_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Сделка была закрыта модератором в пользу Магазина. Оставьте отзыв о Магазине_"
    deal = get_deal_by_id(deal_id)
    deal.update(status=3, messages=None)
    menu = get_buyer_deal_menu(deal, 3, context)
    menu.pop(0)
    context.bot.sendMessage(deal.buyer_id,
                            deal_info,
                            reply_markup=InlineKeyboardMarkup(menu,
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    if deal.payment_method == 'LITECOIN':
        add_shop_balance(deal.shop_id, deal.sum_price_ltc - (deal.sum_price_ltc * commission_per_deals))
        deal_info = d_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Сделка была закрыта модератором в вашу пользу. Средства перечислены на LITECOIN счёт Магазина_"
    else:
        shop = get_shop_obj(deal.shop_id)
        shop.update(freeze_guarantee=shop.freeze_guarantee - deal.sum_price_ltc,
                    guarantee=shop.guarantee + (deal.sum_price_ltc - (deal.sum_price_ltc * commission_per_deals)))
        deal_info = d_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Сделка была закрыта модератором в вашу пользу. Гарант возвращен_"
    context.bot.sendMessage(deal.shop_id,
                            deal_info,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    if SELECT_SALE_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Сделки магазина (товары)</b>\n\nВы успешно закрыли выбранную сделку в пользу Магазина!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{back_for_button}  Назад",
                                                                     callback_data='back_to_moder_select_sale')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif SELECT_BUYS_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Сделки пользователя (товары)</b>\n\nВы успешно закрыли выбранную сделку в пользу Магазина!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{back_for_button}  Назад",
                                                                     callback_data='back_to_user_buys_list')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    else:
        update.callback_query.edit_message_text(
            f"   <b>Список вызовов (сделки)</b>\n\nВы успешно закрыли выбранную сделку!",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "deal_moder_call"),
                                              resize_keyboard=True),
            parse_mode='HTML')


def button_moder_select_call_menu_close_deal_buyer(update, context):
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    deal_id = context.user_data[DEAL_ID]
    d_info = get_deal_info(deal_id)
    deal_info = d_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Сделка была закрыта модератором в вашу пользу. Средства возвращены на счёт LITECOIN\n" \
                         "Оставьте отзыв о Магазине_"
    deal = get_deal_by_id(deal_id)
    deal.update(status=3, messages=None, defeat_dispute=True)
    menu = get_buyer_deal_menu(deal, 3, context)
    menu.pop(0)
    context.bot.sendMessage(deal.buyer_id,
                            deal_info,
                            reply_markup=InlineKeyboardMarkup(menu,
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    if deal.payment_method == 'LITECOIN':
        add_user_balance(deal.buyer_id, deal.sum_price_ltc)
        deal_info = d_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Сделка была закрыта модератором в пользу Покупателя. Средства возвращены покупателю_"
    else:
        shop = get_shop_obj(deal.shop_id)
        shop.update(freeze_guarantee=shop.freeze_guarantee - deal.sum_price_ltc)
        add_user_balance(deal.buyer_id, deal.sum_price_ltc)
        deal_info = d_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Сделка была закрыта модератором в пользу Покупателя. Сумма сделки списана с вашего гаранта_"
    context.bot.sendMessage(deal.shop_id,
                            deal_info,
                            parse_mode=telegram.ParseMode.MARKDOWN)
    if SELECT_SALE_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Сделки магазина (товары)</b>\n\nВы успешно закрыли выбранную сделку в пользу Покупателя!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{back_for_button}  Назад",
                                                                     callback_data='back_to_moder_select_sale')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif SELECT_BUYS_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Сделки пользователя (товары)</b>\n\nВы успешно закрыли выбранную сделку в пользу Покупателя!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{back_for_button}  Назад",
                                                                     callback_data='back_to_user_buys_list')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    else:
        update.callback_query.edit_message_text(
            f"   <b>Список вызовов (сделки)</b>\n\nВы успешно закрыли выбранную сделку в пользу Покупателя!",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "deal_moder_call"),
                                              resize_keyboard=True),
            parse_mode='HTML')


def button_moder_select_call_menu_content(update, context):
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    context.bot.sendDocument(chat_id, deal.file_id, f"{deal.id}.{deal.count} шт.txt",
                             caption=f"Выданный товар [{deal.count} шт.]")
    if deal.change_file_id is not None and deal.change_count is not None:
        context.bot.sendDocument(chat_id, deal.file_id, f"{deal.id}.{deal.change_count} шт.txt",
                                 caption=f"Замена товара [{deal.change_count} шт.]")


def button_moder_select_call_menu_messages(update, context):
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    messages_text = get_deal_messages(deal)
    menu = deepcopy(moder_select_call_menu_messages)
    if SELECT_SALE_SECTION in context.user_data:
        menu.pop(1)
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_select_sale')])
    elif SELECT_BUYS_SECTION in context.user_data:
        menu.pop(1)
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_user_select_buy')])
    update.callback_query.edit_message_text(
        f"   <b>Сообщения в Диспуте</b>\n\n"
        f"Покупатель:  <b>@{get_user_tg_id(deal.buyer_id)}</b>\n"
        f"Владелец магазина:  <b>@{get_user_tg_id(deal.shop_id)}</b>\n\n"
        f"{messages_text}",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


# ------------- Список вызовов ЗАКАЗЫ --------------
def button_submenu_moder_calls_orders(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Список вызовов (заказы)</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "order_moder_call"),
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_select_order_moder_call(update, context, order_id):
    query = update.callback_query
    query.answer()
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text(f"   <b>Список вызовов (заказы)</b>\n\nЗаказ не найден!")
    context.user_data[ORDER_ID] = order_id
    menu = deepcopy(moder_select_call_order_menu)
    if order.order_work is not None:
        menu[0].append(InlineKeyboardButton(f"Выполненный заказ", callback_data='moder_select_call_order_menu_content'))
    update.callback_query.edit_message_text(get_order_info(order_id),
                                            reply_markup=InlineKeyboardMarkup(
                                                menu,

                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_moder_select_call_order_menu_tz(update, context):
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    context.bot.sendDocument(chat_id, order.tz, caption="Техническое задание к заказу")


def button_moder_select_call_order_menu_work(update, context):
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    context.bot.sendDocument(chat_id, order.order_work, caption="Выполненный заказ")


def button_moder_select_call_order_menu_content(update, context):
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    if order.order_work is None:
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}"
            f"<i>Исполнитель ничего не отправлял!</i>",
            parse_mode='HTML')
    context.bot.sendDocument(chat_id, order.order_work, caption="Выполненный заказ")


def button_moder_select_call_order_menu_messages(update, context):
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    menu = deepcopy(moder_select_call_order_menu_messages)
    if SELECT_SALE_SECTION in context.user_data:
        menu.pop(1)
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_select_service_sale')])
    elif SELECT_BUYS_SECTION in context.user_data:
        menu.pop(1)
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_user_select_orders')])
    messages_text = get_order_messages(order)
    update.callback_query.edit_message_text(
        f"   <b>Сообщения в Диспуте</b>\n\n"
        f"Заказчик:  <b>@{get_user_tg_id(order.client_id)}</b>\n"
        f"Исполнитель:  <b>@{get_user_tg_id(order.shop_id)}</b>\n\n"
        f"{messages_text}",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_moder_select_call_order_menu_close(update, context):
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    if SELECT_SALE_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Закрытие заказа</b>\n\n❓ Выберите в чью пользу желаете закрыть заказ",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Исполнителя", callback_data='moder_select_call_order_menu_close_shop'),
                 InlineKeyboardButton(f"Заказчика", callback_data='moder_select_call_order_menu_close_client')],
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data='back_to_moder_select_service_sale')]
            ],
                resize_keyboard=True),
            parse_mode='HTML')
    elif SELECT_BUYS_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Закрытие заказа</b>\n\n❓ Выберите в чью пользу желаете закрыть заказ",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Исполнителя", callback_data='moder_select_call_order_menu_close_shop'),
                 InlineKeyboardButton(f"Заказчика", callback_data='moder_select_call_order_menu_close_client')],
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data='back_to_moder_user_select_orders')]
            ],
                resize_keyboard=True),
            parse_mode='HTML')
    else:
        update.callback_query.edit_message_text(
            f"   <b>Закрытие заказа</b>\n\n❓ Выберите в чью пользу желаете закрыть заказ",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Исполнителя", callback_data='moder_select_call_order_menu_close_shop'),
                 InlineKeyboardButton(f"Заказчика", callback_data='moder_select_call_order_menu_close_client')],
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data='back_to_select_order_call_menu')]
            ],
                resize_keyboard=True),
            parse_mode='HTML')


def button_moder_select_call_order_menu_close_shop(update, context):
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    ord_info = get_order_info(order_id)
    order_info = ord_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ был закрыт модератором в пользу Исполнителя. Оставьте отзыв о Магазине</i>"
    order.update(status=4, messages=None)
    menu = get_client_order_menu(order_id, 4, context)
    context.bot.sendMessage(order.client_id,
                            order_info,
                            reply_markup=InlineKeyboardMarkup(menu,
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    add_shop_balance(order.shop_id, order.price_ltc - (order.price_ltc * commission_per_deals))
    order_info = ord_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ был закрыт модератором в вашу пользу. Средства перечислены на LITECOIN счёт Магазина</i>"

    context.bot.sendMessage(order.shop_id,
                            order_info,
                            parse_mode='HTML')

    if SELECT_SALE_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Заказы магазина</b>\n\nВы успешно закрыли выбранный заказ в пользу Исполнителя!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                     callback_data='back_moder_shop_services_sales_select_section')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif SELECT_BUYS_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Заказы пользователя</b>\n\nВы успешно закрыли выбранный заказ в пользу Исполнителя!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                     callback_data='back_to_user_orders_list')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    else:
        update.callback_query.edit_message_text(
            f"   <b>Список вызовов (заказы)</b>\n\nВы успешно закрыли выбранный заказ в пользу Исполнителя!",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "order_moder_call"),
                                              resize_keyboard=True),
            parse_mode='HTML')

    now = datetime.now()
    if now > order.date_deadline:
        order.update(late_deadline=True)


def button_moder_select_call_order_menu_close_client(update, context):
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    ord_info = get_order_info(order_id)
    order_info = ord_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ был закрыт модератором в вашу пользу.\nСредства возвращены на LITECOIN счёт.\nОставьте отзыв о Магазине</i>"
    add_user_balance(order.client_id, order.price_ltc)
    order.update(status=4, messages=None, defeat_dispute=True)
    menu = get_client_order_menu(order_id, 4, context)
    context.bot.sendMessage(order.client_id,
                            order_info,
                            reply_markup=InlineKeyboardMarkup(menu,
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    order_info = ord_info + "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ был закрыт модератором в пользу Заказчика.\nСредства возвращены на его счёт</i>"

    context.bot.sendMessage(order.shop_id,
                            order_info,
                            parse_mode='HTML')

    if SELECT_SALE_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Заказы магазина</b>\n\nВы успешно закрыли выбранный заказ в пользу Заказчика!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                     callback_data='back_moder_shop_services_sales_select_section')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif SELECT_BUYS_SECTION in context.user_data:
        update.callback_query.edit_message_text(
            f"   <b>Заказы пользователя</b>\n\nВы успешно закрыли выбранный заказ в пользу Заказчика!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                     callback_data='back_to_user_orders_list')]],
                                              resize_keyboard=True),
            parse_mode='HTML')
    else:
        update.callback_query.edit_message_text(
            f"   <b>Список вызовов (заказы)</b>\n\nВы успешно закрыли выбранный заказ в пользу Заказчика!",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "order_moder_call"),
                                              resize_keyboard=True),
            parse_mode='HTML')

    now = datetime.now()
    if now > order.date_deadline:
        order.update(late_deadline=True)


# ============================================= ЛИЧНЫЙ КАБИНЕТ ========================================================
# ----------- ВНЕСТИ LITECOIN -----------
def button_submenu_up_balance(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    user = get_user_obj(chat_id)
    if not user.coinbase_address_id:
        create_coinbase_address(chat_id)
    coinbase_address_id = get_coinbase_address_id(chat_id)
    coinbase_address = get_coinbase_address(coinbase_address_id)
    update.callback_query.edit_message_text(f'   *Внести LITECOIN*\n\n'
                                            f'Для пополнения счёта создан Ваш персональный LITECOIN адрес.\n\n'
                                            f'Чтобы пополнить счет выполните перевод по адресу в сообщении ниже\n\n'
                                            f'После выполнения перевода нажмите кнопку\n*\'Найти перевод\'*\n\n'
                                            f'Ваш баланс автоматически пополнится на отправленную сумму! {e_smiling}',
                                            reply_markup=InlineKeyboardMarkup(up_balance_menu,
                                                                              resize_keyboard=True),
                                            parse_mode=telegram.ParseMode.MARKDOWN)
    context.bot.sendMessage(chat_id, f'<b>{coinbase_address}</b>', parse_mode='HTML')


def button_submenu_balance_menu(update, context):
    update.callback_query.edit_message_text(
        "   <b>Пополнить LITECOIN</b>\n\n<b>Внести</b> - пополнить баланс в боте, если у вас уже есть LITECOIN\n\n"
        "<b>Купить</b> - купить LITECOIN, если у вас ещё его нет",
        reply_markup=InlineKeyboardMarkup(balance_menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


# Проверка пополнений
def button_check_up_balance(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    address_id = get_coinbase_address_id(chat_id)
    transactions = get_transactions_list(address_id)
    sum_amount_add = get_sum_new_transactions(chat_id, transactions)
    if sum_amount_add == 0:
        update.callback_query.edit_message_text("   <b>Внести LITECOIN</b>\n\nНи один новый перевод не найден\n\n"
                                                "Обратите внимание, перевод будет найден после "
                                                "<b>полного завершения</b> транзакции! <i>(до 30 минут)</i>",
                                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                    f'{back_for_button}  Назад',
                                                    callback_data='back_to_submenu_up_balance')]],
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    else:
        add_user_balance(chat_id, sum_amount_add)
        update.callback_query.edit_message_text(
            f"   <b>Внести LITECOIN</b>\n\nПеревод найден\nВаш баланс пополнен на сумму: <b> {sum_amount_add}</b> LITECOIN",
            reply_markup=InlineKeyboardMarkup(up_balance_menu,
                                              resize_keyboard=True),
            parse_mode='HTML')


# -------------------------------


# Открыть магазин
def button_open_shop_handler(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if check_shop_owner(chat_id) and check_shop_stop(chat_id):
        update.callback_query.edit_message_text(
            f"   <b>Восстановить магазин</b>\n\nДля восстановления своего магазина нажмите 'Восстановить'\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_dashboard_menu'),
                  InlineKeyboardButton(f'Восстановить', callback_data='restore_shop')]],
                resize_keyboard=True),
            parse_mode='HTML')
    else:
        update.callback_query.edit_message_text(
            f"   <b>Открыть магазин</b>\n\nДля открытия магазина необходимо пройти модерацию\n\n"
            f"Чтобы оставить заявку на открытие нажмите кнопку <i>'Оставить заявку'</i> и отправьте название Магазина",
            reply_markup=InlineKeyboardMarkup(request_open_shop_menu,
                                              resize_keyboard=True),
            parse_mode='HTML')


def button_restore_shop(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    shop_stop(chat_id, False)
    context.bot.sendMessage(chat_id,
                            f"Ваш магазин успешно восстановлен!\n",
                            reply_markup=update_main_menu(chat_id),
                            parse_mode='HTML')


# История пополнений
def button_up_balance_history(update, context):
    query = update.callback_query
    query.answer()
    show_list_text(update, context, "user_payments")


# --------------------- Мои покупки -------------------------
def button_submenu_my_buys(update, context):
    update.callback_query.edit_message_text("<b>Мои покупки</b>\n\n❓ Выберите тип покупок",
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


def button_my_buys_type_products(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    count_dispute = get_user_dispute_deals_count(chat_id)
    count_open = get_user_open_deals_count(chat_id)
    count_close = get_user_close_deals_count(chat_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text(
            "📦  <b>Мои покупки (товары)</b>\n\nВы не делали покупки товаров",
            reply_markup=
            InlineKeyboardMarkup([[InlineKeyboardButton(
                f'{back_for_button}  Назад',
                callback_data='back_my_buys_select_type')]],
                resize_keyboard=True),
            parse_mode='HTML')
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


def button_my_buys_select_section_dispute(update, context):
    context.user_data[SELECT_BUYS_SECTION] = "dispute"
    update.callback_query.edit_message_text(
        f"<b>Диспутны (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_buys_select_section_open(update, context):
    context.user_data[SELECT_BUYS_SECTION] = "open"
    update.callback_query.edit_message_text(
        f"<b>Незавершенные сделки (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_buys_select_section_close(update, context):
    context.user_data[SELECT_BUYS_SECTION] = "close"
    update.callback_query.edit_message_text(
        f"<b>Завершенные сделки (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_select_my_buy(update, context, deal_id):
    deal_info = get_deal_info(deal_id)
    deal = get_deal_by_id(deal_id)
    context.user_data[DEAL_ID] = deal_id
    menu = get_buyer_deal_menu(deal, deal.status, context)
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)


# -------------------- Мои покупки -> Услуги
def button_my_buys_type_services(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    count_dispute = get_user_dispute_orders_count(chat_id)
    count_open = get_user_open_orders_count(chat_id)
    count_close = get_user_close_orders_count(chat_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text("<b>🤝  Мои заказы (Услуги)</b>\n\nВы не делали заказы услуг",
                                                       reply_markup=
                                                       InlineKeyboardMarkup([[InlineKeyboardButton(
                                                           f'{back_for_button}  Назад',
                                                           callback_data='back_my_buys_select_type')]],
                                                           resize_keyboard=True),
                                                       parse_mode='HTML')
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


def button_my_orders_service_select_section_dispute(update, context):
    context.user_data[SELECT_BUYS_SECTION] = "dispute"
    update.callback_query.edit_message_text(
        f"<b>Диспутны (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys_service"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_orders_service_select_section_open(update, context):
    context.user_data[SELECT_BUYS_SECTION] = "open"
    update.callback_query.edit_message_text(
        f"<b>Незавершенные заказы (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys_service"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_orders_service_select_section_close(update, context):
    context.user_data[SELECT_BUYS_SECTION] = "close"
    update.callback_query.edit_message_text(
        f"<b>Завершенные заказы (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_buys_service"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_select_my_order(update, context, order_id):
    order_info = get_order_info(order_id)
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    menu = get_client_order_menu(order_id, order.status, context)
    update.callback_query.edit_message_text(
        order_info,
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


# =================================================== МОЙ МАГАЗИН ======================================================
def button_my_shop_handler(update, context):
    chat_id = update.message.chat_id
    text = get_shop_info_text(chat_id, chat_id)
    update.message.reply_text(text,
                              reply_markup=InlineKeyboardMarkup(my_shop_menu,
                                                                resize_keyboard=True),
                              parse_mode='HTML')


# ===================== Мои продажи ======================
def button_my_shop_submenu_trades(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    open_deals = count_open_deals(chat_id)
    open_orders = count_open_sh_orders(chat_id)
    update.callback_query.edit_message_text(f"{e_shopping_bags}  <b>Продажи</b>\n\n"
                                            "Незавершенные продажи:\n"
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


def button_my_sales_type_products(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    count_dispute = get_shop_dispute_deals_count(chat_id)
    count_open = get_shop_open_deals_count(chat_id)
    count_close = get_shop_close_deals_count(chat_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text("<b>📦  Продажи (Товары)</b>\n\nУ вас нет продаж товаров",
                                                       reply_markup=
                                                       InlineKeyboardMarkup([[InlineKeyboardButton(
                                                           f'{back_for_button}  Назад',
                                                           callback_data='back_my_sales_select_type')]],
                                                           resize_keyboard=True),
                                                       parse_mode='HTML')
    menu = get_submenu_trades(count_dispute, count_open, count_close, "my_sales")
    update.callback_query.edit_message_text(
        "<b>📦  Продажи (товары)</b>\n\n<u>Завершенные</u> - абсолютно все продажи, которые были завершены в вашем магазине.\n\n"
        "<u>Незавершенные</u> -  продажи, которые на текущий момент являются незавершенными, обычно это проверка "
        "товара, либо ожидание оплаты.\n\n"
        "<u>Диспуты</u> - продажи, в которых у клиента возникли проблемы с вашим товаром.\n\n"
        "<b>❓ Какой раздел вас интересует?</b>",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_my_sales_select_section_dispute(update, context):
    context.user_data[SELECT_SALE_SECTION] = "dispute"
    update.callback_query.edit_message_text(
        f"<b>Диспутны (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_sales_select_section_open(update, context):
    context.user_data[SELECT_SALE_SECTION] = "open"
    update.callback_query.edit_message_text(
        f"<b>Незавершенные сделки (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_sales_select_section_close(update, context):
    context.user_data[SELECT_SALE_SECTION] = "close"
    update.callback_query.edit_message_text(
        f"<b>Завершенные сделки (товары)</b>\n\n<b>❓ Выберите сделку</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_select_my_sale(update, context, deal_id):
    deal_info = get_deal_info(deal_id)
    deal = get_deal_by_id(deal_id)
    context.user_data[DEAL_ID] = deal_id
    menu = get_shop_deal_menu(deal.status, deal, context)
    update.callback_query.edit_message_text(
        deal_info,
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode=telegram.ParseMode.MARKDOWN)


# ------------- Мои продажи (услуги)
def button_my_sales_type_services(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    count_dispute = get_shop_dispute_orders_count(chat_id)
    count_open = get_shop_open_orders_count(chat_id)
    count_close = get_shop_close_orders_count(chat_id)
    if count_dispute == 0 and count_open == 0 and count_close == 0:
        return update.callback_query.edit_message_text("<b>Заказы (услуги)</b>\n\nУ вас нет продаж услуг",
                                                       reply_markup=
                                                       InlineKeyboardMarkup([[InlineKeyboardButton(
                                                           f'{back_for_button}  Назад',
                                                           callback_data='back_my_sales_select_type')]],
                                                           resize_keyboard=True),
                                                       parse_mode='HTML')
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


def button_my_service_sales_select_section_dispute(update, context):
    context.user_data[SELECT_SALE_SECTION] = "dispute"
    update.callback_query.edit_message_text(
        f"<b>Диспуты (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_service_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_service_sales_select_section_open(update, context):
    context.user_data[SELECT_SALE_SECTION] = "open"
    update.callback_query.edit_message_text(
        f"<b>Незавершенные заказы (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_service_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_my_service_sales_select_section_close(update, context):
    context.user_data[SELECT_SALE_SECTION] = "close"
    update.callback_query.edit_message_text(
        f"<b>Завершенные заказы (услуги)</b>\n\n<b>❓ Выберите заказ</b>",
        reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, "my_service_sales"),
                                          resize_keyboard=True), parse_mode='HTML')


def button_select_my_service_sale(update, context, order_id):
    order_info = get_order_info(order_id)
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    menu = get_shop_order_menu(order_id, order.status, context)
    update.callback_query.edit_message_text(
        order_info,
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


#  ------------------------  МОЙ МАГАЗИН -> ФИНАНСЫ ------------------
def button_my_shop_submenu_finance(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    text = get_myshop_finance_text(chat_id)
    update.callback_query.edit_message_text(text,
                                            reply_markup=InlineKeyboardMarkup(my_shop_submenu_finance,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_finance_guarantee(update, context):
    update.callback_query.edit_message_text(f"{e_handshake}   <b>Гарант</b>\n\n"
                                            f"<b>Гарант является уровнем доверия к магазину, вносится по желанию.</b>\n\n"
                                            f"<b>Магазины с  гарантом будут показываться выше в списке товаров.</b>\n\n"
                                            f"<b>При наличии гаранта , вы сможете принимать платежи на личный реквизит.</b>\n\n"
                                            f"⚠  Минимальный размер гаранта = {min_guarantee} LTC\n\n"
                                            f"❓ Хотите внести или вывести гарант?",
                                            reply_markup=InlineKeyboardMarkup(my_shop_finance_guarantee,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_finance_guarantee_up(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"{e_handshake}   <b>Внесение гаранта</b>\n\n"
        "Ваш гарант будет отображаться во всех категориях где вы продаете товар.\n\n"
        "В случае, если магазин не выполнил свои обязательства перед покупателем, «Администрация» вправе возместить средства покупателю из депозита магазина.\n\n"
        "В случае, если таких покупателей много, то сумма депозита делится между всеми в равных долях согласно сумме их потерь.\n\n"
        "Вывести гарант возможно только при отсутствии незавершенных сделок.\n\n"
        f"<b>Минимальный гарант -</b>  {min_guarantee}  LTC",
        reply_markup=InlineKeyboardMarkup(my_shop_finance_guarantee_up_menu,
                                          resize_keyboard=True),
        parse_mode='HTML')


def button_my_shop_finance_operations(update, context):
    query = update.callback_query
    query.answer()
    show_list_text(update, context, "shop_operations")


def button_my_shop_finance_requisites(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if get_guarantee_shop(chat_id) < min_guarantee:
        context.bot.sendMessage(chat_id,
                                f"<b>Доступ закрыт</b>\nНа счету гаранта должно быть не менее {min_guarantee} LITECOIN",
                                parse_mode='HTML')
        return
    update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                            f"<i>Указать и использовать свои реквизиты можно при наличии на счету "
                                            f"минимального гаранта</i> - <b>{min_guarantee}</b> LITECOIN\n\n"
                                            f"При недостаточном балансе гаранта пользователь <b>не сможет</b> выбрать Ваши реквизиты при оплате\n\n"
                                            f"❓ Выберите действие",
                                            reply_markup=InlineKeyboardMarkup(my_shop_finance_requisites,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_finance_requisites_all(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                            f"❓ Выберите реквизит для управления",
                                            reply_markup=InlineKeyboardMarkup(
                                                show_list_menu(update, context, "requisites"),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_finance_requisites_select(update, context, select_id):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    requisite_info = get_requisite_info(owner_id, select_id)
    context.user_data[SELECT_ID] = select_id
    update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                            f"{requisite_info}",
                                            reply_markup=InlineKeyboardMarkup(my_shop_finance_requisites_select_menu,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_finance_requisites_select_edit(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    select_id = context.user_data[SELECT_ID]
    requisite_info = get_requisite_info(owner_id, select_id)
    update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                            f"{requisite_info}\n\n"
                                            f"Что желаете изменить?",
                                            reply_markup=InlineKeyboardMarkup(
                                                my_shop_finance_requisites_select_edit_menu,
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_finance_requisites_select_del(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    select_id = context.user_data[SELECT_ID]
    delete_shop_requisite(owner_id, select_id)
    context.bot.sendMessage(owner_id, '<b>Реквизит</b> успешно удален', parse_mode='HTML')
    update.callback_query.edit_message_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n❓ Выберите действие",
                                            reply_markup=InlineKeyboardMarkup(my_shop_finance_requisites,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_finance_withdrawal(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(f"{e_dollar_banknote}   <b>Вывод</b>\n\n❓ Куда желаете вывести LITECOIN?",
                                            reply_markup=InlineKeyboardMarkup(my_shop_finance_withdrawal,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


# --------------------------------- МОЙ МАГАЗИН -> Мои товары ---------------------------
def button_my_shop_submenu_products(update, context):
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


# Начало выбора категории при добавлении товара
def button_my_shop_products_add(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    context.user_data[CATEGORY_INFO] = {}
    context.user_data[DATA] = 'add'
    update.callback_query.edit_message_text(f"   <b>➕  Добавление товара</b>\n\n❓ <b>Выберите категорию товаров:</b>",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_btnlist_by_catid(context, None, context.user_data[DATA],
                                                                            chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


# Кнопка выбора категории
def button_select_product_cat(update, context, cat_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if CATEGORY_INFO not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    cat = ProductCategory.objects(id=cat_id).first()
    if 'cat_path' in context.user_data[CATEGORY_INFO] and context.user_data[CATEGORY_INFO]['cat_path'].find(
            cat.name) == -1:
        context.user_data[CATEGORY_INFO]['cat_path'] += "\t\t\t\t -> <b>" + cat.name + "</b>\n"
    else:
        context.user_data[CATEGORY_INFO]['cat_path'] = "\t\t<b>" + cat.name + "</b>\n"
    cat_path_text = ""
    if 'cat_path' in context.user_data[CATEGORY_INFO]:
        cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']
    head = ''
    input_info = ''
    sub_cats = ProductCategory.objects(sub_id=cat_id)

    if context.user_data[DATA] == 'add':
        if not sub_cats:
            head = "<b>➕  Добавление товара</b>"
            input_info = "\n❓ <b>Вы хотите добавить товар в выбранную категорию?</b>"
        else:
            head = "<b>➕  Добавление товара</b>"
            input_info = "\n❓ <b>Выберите категорию товара:</b>"
    elif context.user_data[DATA] == 'my_list':
        if not sub_cats:
            head = f"<b>{e_page}  Изменить товар</b>"
            input_info = "\n❓ <b>Выберите товар:</b>"
        else:
            head = f"<b>{e_page}  Изменить товар</b>"
            input_info = "\n❓ <b>Выберите категорию товара:</b>"
    elif context.user_data[DATA] == 'for_user':
        if not sub_cats:
            head = "🏪<b>Магазины</b>\n\n" \
                   "🛍 Ниже представлены все магазины, которые продают данный товар.\n\n" \
                   "⚠ <u>Будьте внимательны</u>, проверяйте отзывы о магазинах и рейтинг магазина." \
                   "Каждый продавец вправе выставить любую цену за товар."
            input_info = "\n✅ <b>Выберите магазин:</b>"
        else:
            head = f"<b>📦 Товары</b>\n\n" \
                   "📂 Вы видите все представленные категории товаров, которые существуют на рынке.\n\n" \
                   "⚠ Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила ведет к потере денежных средств без разбирательств."
            input_info = "\n❓ <b>Выберите категорию товаров:</b>"
    elif context.user_data[DATA] == 'select_shop_prods':
        if not sub_cats:
            head = f"<b>📦 Товары магазина</b>\n\n" \
                   "📂 Вы видите товары, которые есть у магазина в выбранной категории."
            input_info = "\n❓ <b>Выберите товар:</b>"
        else:
            head = f"<b>📦 Товары магазина</b>\n\n" \
                   "📂 Вы видите категории товаров, которые есть у выбранного магазина.\n\n" \
                   "⚠️ Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила ведет к потере денежных средств без разбирательств."
            input_info = "\n❓ <b>Выберите категорию товаров:</b>"
    update.callback_query.edit_message_text(f" {head}{cat_path_text}{input_info}",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_btnlist_by_catid(context, cat_id, context.user_data[DATA],
                                                                            chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


# Список моих товаров, начало выбора категории
def button_my_shop_products_list(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    context.user_data[CATEGORY_PRODS] = []
    context.user_data[CATEGORY_INFO] = {}
    get_cat_my_products_tree(context, update, owner_id)
    context.user_data[DATA] = 'my_list'
    update.callback_query.edit_message_text(
        f"   <b>{e_page}  Изменить товар</b>\n\n❓ <b>Выберите категорию товара:</b>",
        reply_markup=InlineKeyboardMarkup(
            get_subcat_btnlist_by_catid(context, None, context.user_data[DATA],
                                        owner_id),
            resize_keyboard=True),
        parse_mode='HTML')


# Выбор конкретного товара
def button_select_my_product(update, context, product_id):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    if CATEGORY_INFO not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    context.user_data[SELECT_PROD_ID] = product_id
    product_info = get_product_info(owner_id, context, product_id)
    update.callback_query.edit_message_text(f"   <b>Управление товаром</b>{product_info}",
                                            reply_markup=InlineKeyboardMarkup(my_shop_submenu_products_prod_menu,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_select_product(update, context, product_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if CATEGORY_INFO not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    context.user_data[SELECT_PROD_ID] = product_id
    product_info = get_product_info(chat_id, context, product_id)
    update.callback_query.edit_message_text(f"📊 <b>Информация о товаре</b>{product_info}",
                                            reply_markup=InlineKeyboardMarkup(market_select_prod_menu,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_products_prod_edit(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    product_id = context.user_data[SELECT_PROD_ID]
    product_info = get_product_info(owner_id, context, product_id)
    update.callback_query.edit_message_text(f"{e_pencil}   <b>Редактирование товара</b>{product_info}",
                                            reply_markup=InlineKeyboardMarkup(my_shop_product_edit_menu,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_products_prod_del(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(f"{e_cross_mark}   <b>Удаление товара</b>\n\n"
                                            f"Вы уверены, что хотите удалить товар?\n\n"
                                            f"<b>Все единицы товара будут безвозвратно удалены!</b>",
                                            reply_markup=InlineKeyboardMarkup(my_shop_products_prod_del_accept,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_products_prod_del_accept(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    product_id = context.user_data[SELECT_PROD_ID]
    product_del(product_id)
    update.callback_query.edit_message_text(f"{e_cross_mark}   <b>Удаление товара</b>\n\n"
                                            f"Товар успешно удален!\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                       callback_data='back_to_my_shop_submenu_products')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')


# ------------- МОИ УСЛУГИ -------------------------
def button_my_shop_submenu_services(update, context):
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


def button_my_shop_services_add(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    context.user_data[CATEGORY_INFO] = {}
    context.user_data[DATA] = 'add_service'
    update.callback_query.edit_message_text(f"<b>➕  Добавление услуги</b>\n\n❓ <b>Выберите категорию услуги:</b>",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_service_btnlist_by_catid(context, None,
                                                                                    context.user_data[DATA],
                                                                                    chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_select_serv_cat(update, context, cat_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if CATEGORY_INFO not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    cat = ServiceCategory.objects(id=cat_id).first()
    if 'cat_path' in context.user_data[CATEGORY_INFO] and context.user_data[CATEGORY_INFO]['cat_path'].find(
            cat.name) == -1:
        context.user_data[CATEGORY_INFO]['cat_path'] += "\t\t\t\t -> <b>" + cat.name + "</b>\n"
    else:
        context.user_data[CATEGORY_INFO]['cat_path'] = "\t\t<b>" + cat.name + "</b>\n"
    cat_path_text = ""
    if 'cat_path' in context.user_data[CATEGORY_INFO]:
        cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']
    head = ''
    chapter = ''
    sub_cats = ServiceCategory.objects(sub_id=cat_id)
    if context.user_data[DATA] == 'add_service':
        if not sub_cats:
            head = "<b>➕  Добавление услуги</b>"
            chapter = "\n❓ <b>Вы хотите добавить услугу в выбранную категорию?</b>"
        else:
            head = "<b>➕  Добавление услуги</b>"
            chapter = "\n❓ <b>Выберите категорию услуги:</b>"
    elif context.user_data[DATA] == 'my_list_services':
        if not sub_cats:
            head = f"<b>{e_page}  Изменить услугу</b>"
            chapter = "\n❓ <b>Выберите услугу:</b>"
        else:
            head = f"<b>{e_page}  Изменить услугу</b>"
            chapter = "\n❓ <b>Выберите категорию услуги:</b>"
    elif context.user_data[DATA] == 'for_user_services':
        if not sub_cats:
            head = "<b>Категория</b>\n\n👤 Это список из фрилансеров, выберите подходящего и сделайте заказ.\n\n" \
                   "⚠  Напоминаем, что все сделки проводятся исключительно внутри бота, нарушения этого правила может привести к потере денежных средств без разбирательств."
            chapter = f"\n✅  <b>Выберите фрилансера:</b>"
        else:
            head = f"🤝  <b>Услуги</b>\n\n" \
                   f"⚠  Фрилансеры оформляют свои услуги в виде обьявлений, которые можно купить в один клик. То есть работа исполнителей продается как товар, а это экономит массу времени, денег и нервов. Идеально подходит для типовых задач: логотипы, баннеры, SEO и др."
            chapter = f"\n<b>Какой раздел вас интересует❓</b>"
    elif context.user_data[DATA] == 'select_shop_services':
        if not sub_cats:
            head = "🤝  <b>Услуги магазина</b>\n\n" \
                   "📂 Вы видите услуги, которые предоставляет магазин в выбранной категории."
            chapter = f"\n<b>❓ Выберите услугу:</b>"
        else:
            head = "🤝  <b>Услуги магазина</b>\n\n" \
                   "📂 Вы видите категории услуг, которые предоставляет выбранный магазин."
            chapter = f"\n<b>Какой раздел вас интересует❓</b>"
    update.callback_query.edit_message_text(f" {head}{cat_path_text}{chapter}",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_service_btnlist_by_catid(context, cat_id,
                                                                                    context.user_data[DATA],
                                                                                    chat_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_services_list(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    context.user_data[CATEGORY_SERVICES] = []
    context.user_data[CATEGORY_INFO] = {}
    get_cat_my_services_tree(context, update, owner_id)
    context.user_data[DATA] = 'my_list_services'
    update.callback_query.edit_message_text(f"<b>{e_page}  Изменить услугу</b>\n\n❓ <b>Выберите категорию услуг:</b>",
                                            reply_markup=InlineKeyboardMarkup(
                                                get_subcat_service_btnlist_by_catid(context, None,
                                                                                    context.user_data[DATA],
                                                                                    owner_id),
                                                resize_keyboard=True),
                                            parse_mode='HTML')


def button_select_my_service(update, context, service_id):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    context.user_data[SELECT_SERV_ID] = service_id
    serv_info = get_service_info(owner_id, context, service_id)
    picture_id = get_service_picture_id(service_id)
    context.bot.sendPhoto(owner_id, picture_id)
    context.bot.sendMessage(owner_id, f"   <b>Управление услугой</b>{serv_info}",
                            reply_markup=InlineKeyboardMarkup(my_shop_select_service_menu,
                                                              resize_keyboard=True),
                            parse_mode='HTML')


def button_my_shop_service_menu_edit(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(owner_id, "Не актуально")
    service_id = context.user_data[SELECT_SERV_ID]
    serv_info = get_service_info(owner_id, context, service_id)
    context.bot.sendMessage(owner_id, f"{e_pencil}  <b>Редактирование услуги</b>{serv_info}",
                            reply_markup=InlineKeyboardMarkup(my_shop_select_service_menu_edit,
                                                              resize_keyboard=True),
                            parse_mode='HTML')


def button_my_shop_service_menu_packets(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    context.bot.sendMessage(chat_id, f"   <b>Добавление пакетов</b>\n\n"
                                     f"Также вы можете добавить пакеты к своей услуги (Эконом, Стандарт, Бизнес)\n\n"
                                     f"При добавлении пакета вы должны указать:\n"
                                     f"1) Что входит в выбранный пакет\n"
                                     f"2) Стоимость выбранного пакета\n\n",
                            reply_markup=InlineKeyboardMarkup(
                                get_my_service_packets_menu(update, context, chat_id, "my_service"),
                                resize_keyboard=True),
                            parse_mode='HTML')


def button_my_shop_service_menu_portfolio(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service = get_service_by_id(context.user_data[SELECT_SERV_ID])
    portfolio = service.portfolio
    if portfolio is None:
        context.bot.sendMessage(chat_id, "Вы не добавляли портфолио к выбранной услуге\n\n"
                                         "Чтобы добавить перейдите в <b>Редактирование</b>", parse_mode='HTML')
    else:
        context.bot.sendDocument(chat_id, portfolio,
                                 caption=f"Ваше портфолио к выбранной услуги")


def button_my_shop_service_menu_delete(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service_id = context.user_data[SELECT_SERV_ID]
    context.bot.sendMessage(chat_id, "Вы действительно хотите <b>удалить</b> выбранную услугу?",
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                       callback_data='back_to_my_shop_select_service_menu'),
                                  InlineKeyboardButton(f"Подтвердить",
                                                       callback_data=f'my_shop_products_prod_del_accept_{service_id}')]],
                                resize_keyboard=True),
                            parse_mode='HTML')


def button_my_shop_service_menu_del_accept(update, context, service_id):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    service = get_service_by_id(service_id)
    service.delete()
    context.bot.sendMessage(chat_id, "Услуга успешно удалена!")
    context.bot.sendMessage(chat_id,
                            f"🤝  <b>Мои услуги</b>\n\n❓  Хотите посмотреть свои услуги или добавить новую услугу?",
                            reply_markup=InlineKeyboardMarkup(my_shop_submenu_services,
                                                              resize_keyboard=True),
                            parse_mode='HTML')


def button_service_edit_packet_eco(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    context.user_data[DATA] = "edit_eco"
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    update.callback_query.edit_message_text(f'{e_pencil}  <b>Редактирование пакета "Эконом"</b>\n\n'
                                            f'<b>Стоимость:</b>  {service.eco_price} ₽\n\n'
                                            f'<b>Описание:</b>  {service.eco_description}\n\n'
                                            f'<b>Срок выполнения:</b>  {service.eco_deadline} дней',
                                            reply_markup=InlineKeyboardMarkup(my_shop_service_edit_packet,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_service_edit_packet_standart(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    context.user_data[DATA] = "edit_standart"
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    update.callback_query.edit_message_text(f'{e_pencil}  <b>Редактирование пакета "Стандарт"</b>\n\n'
                                            f'<b>Стоимость:</b>  {service.standart_price} ₽\n\n'
                                            f'<b>Описание:</b>  {service.standart_description}\n\n'
                                            f'<b>Срок выполнения:</b>  {service.standart_deadline} дней',
                                            reply_markup=InlineKeyboardMarkup(my_shop_service_edit_packet,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_service_edit_packet_biz(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    context.user_data[DATA] = "edit_biz"
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    update.callback_query.edit_message_text(f'{e_pencil}  <b>Редактирование пакета "Бизнес"</b>\n\n'
                                            f'<b>Стоимость:</b>  {service.biz_price} ₽\n\n'
                                            f'<b>Описание:</b>  {service.biz_description}'
                                            f'<b>Срок выполнения:</b>  {service.biz_deadline} дней',
                                            reply_markup=InlineKeyboardMarkup(my_shop_service_edit_packet,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_service_edit_packet_del(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    if context.user_data[DATA] == "edit_eco":
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(eco_description=None, eco_price=None)
        update.callback_query.edit_message_text(f"{e_pencil}   <b>Редактирование пакета 'Эконом'</b>\n\n"
                                                f"Пакет успешно удалён!\n\n",
                                                reply_markup=InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                           callback_data='back_to_my_service_packets_menu')]],
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    elif context.user_data[DATA] == "edit_standart":
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(standart_description=None, standart_price=None)
        update.callback_query.edit_message_text(f"{e_pencil}   <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                                f"Пакет успешно удалён!\n\n",
                                                reply_markup=InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                           callback_data='back_to_my_service_packets_menu')]],
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    elif context.user_data[DATA] == "edit_biz":
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(biz_description=None, biz_price=None)
        update.callback_query.edit_message_text(f"{e_pencil}   <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                                f"Пакет успешно удалён!\n\n",
                                                reply_markup=InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                           callback_data='back_to_my_service_packets_menu')]],
                                                    resize_keyboard=True),
                                                parse_mode='HTML')
    context.user_data[CATEGORY_INFO]['cat_id'] = context.user_data[CATEGORY_INFO]['cat_id']
    context.user_data[CATEGORY_INFO]['cat_path'] = context.user_data[CATEGORY_INFO]['cat_path']


# -------------- НАСТРОЙКИ ------------------------
def button_my_shop_submenu_settings(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    shop = get_shop_obj(owner_id)
    if shop.terms_trade is None:
        terms_text = "не указаны"
    else:
        terms_text = shop.terms_trade
    update.callback_query.edit_message_text(f'{e_wrench}   <b>Настройки</b>\n\n'
                                            f'<b>⏱  Время проверки товара:</b> {shop.check_buyer_time // 60} минут\n'
                                            f'<b>📑  Условия торговли:</b> {terms_text}',
                                            reply_markup=InlineKeyboardMarkup(get_my_shop_submenu_settings(shop),
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_settings_stop(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    shop = get_shop_obj(owner_id)
    count_deals = count_open_deals(owner_id)
    if shop.guarantee > 0 or count_deals > 0:
        return context.bot.sendMessage(owner_id,
                                       "Перед закрытием магазина необходимо <b>Вывести гарант</b> и <b>Завершить все продажи</b>!",
                                       parse_mode='HTML')
    update.callback_query.edit_message_text(f'{e_cross_mark}   <b>Закрыть магазин</b>\n\n'
                                            f'Вы уверены что хотите закрыть магазин?\n\n'
                                            f'Восстановить его будет <b>невозможно</b>!',
                                            reply_markup=InlineKeyboardMarkup(my_shop_setting_stop_confirmation,
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


def button_my_shop_settings_stop_confirmed(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    shop_stop(owner_id, True)
    context.bot.sendMessage(owner_id, f'<b>Работа вашего магазина остановлена!</b>',
                            reply_markup=update_main_menu(owner_id), parse_mode='HTML')


def button_my_shop_settings_pause_trade(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    shop = get_shop_obj(owner_id)
    if not shop.pause_trade:
        update.callback_query.edit_message_text(
            "Торговля успешно <i>приостановлена</i>, ваши товары <b>не будут отображаться</b> на "
            "Рынке",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    f'{back_for_button}  Назад',
                    callback_data='back_to_my_shop_submenu_settings')]],
                resize_keyboard=True),
            parse_mode='HTML')
        shop.update(pause_trade=True)
    else:
        update.callback_query.edit_message_text(
            "Торговля успешно <i>возобновлена</i>, ваши товары <b>снова будут отображаться</b> на "
            "Рынке",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    f'{back_for_button}  Назад',
                    callback_data='back_to_my_shop_submenu_settings')]],
                resize_keyboard=True),
            parse_mode='HTML')
        shop.update(pause_trade=False)


def button_my_shop_settings_terms(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    shop = get_shop_obj(owner_id)
    terms = shop.terms_trade
    if terms is None:
        terms = "не указаны"
    update.callback_query.edit_message_text(f'<b>📑  Условия торговли</b>\n\n'
                                            f'В данном разделе вы можете указать условия торговли с вашим магазином\n\n'
                                            f'В данном разделе вы указываете краткий свод правил использования ваших товаров или услуг.\n\n'
                                            f'<b>✅  Пример:</b> 1.1 Проданный валидный аккаунт, купон возврату не подлежит (перед покупкой ознакомитесь с описанием товара)\n'
                                            f'1.2 Смена данных или выполнения каких либо действий в купленном аккаунте (аккаунтах) осуществляемые покупателем, в последствии с обращением о замене по каким либо причинам. В таких случаях в замене будет отказано....и т.д\n\n'
                                            f'<b>Максимальное кол-во символов:</b> 3000\n\n'
                                            f'<b>Текущие условия торговли:</b> {terms}',
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Изменить условия",
                                                                                                     callback_data='change_terms_trade')],
                                                                               [InlineKeyboardButton(
                                                                                   f'{back_for_button}  Назад',
                                                                                   callback_data='back_to_my_shop_submenu_settings')]],
                                                                              resize_keyboard=True),
                                            parse_mode='HTML')


# ============================================= ОБЩИЕ ============================================================

# Обработка нажатия кнопок след. страницы и пред. страницы
def button_switcher_list_page(update, context):
    query = update.callback_query
    query.answer()
    text = ""
    if PAGE_INDEX not in context.user_data:
        context.user_data[PAGE_INDEX] = 1
    if query.data[26:30] == "next":
        context.user_data[PAGE_INDEX] += 1
    elif query.data[26:30] == "prev":
        context.user_data[PAGE_INDEX] -= 1
    if DATA not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")

    # СПИСОК В КНОПКАХ
    if context.user_data[DATA] == "requests":
        text = "Заявки на открытие"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "shops":
        text = "Список магазинов"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "requisites":
        text = "Список моих реквизитов"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "my_buys":
        text = "Мои сделки (товары)"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "my_sales":
        text = f"{e_shopping_bags}  Продажи"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "moder_shop_sales":
        shop_id = context.user_data[SELECT_ID]
        text = f"Сделки магазина {get_shop_name(shop_id)}  ({get_shop_id(shop_id)}) (товары)"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "moder_user_buys":
        user_id = context.user_data[SELECT_ID]
        text = f"Сделки пользователя {get_user_name(user_id)}  ({get_user_id(user_id)}) (товары)"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "deal_moder_call_":
        text = "Список вызовов (сделки)"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == "order_moder_call_":
        text = "Список вызовов (заказы)"
        update.callback_query.edit_message_text(
            f"<b>{text}</b>  ",
            reply_markup=InlineKeyboardMarkup(show_list_menu(update, context, context.user_data[DATA]),
                                              resize_keyboard=True),
            parse_mode='HTML')

    # СПИСОК В ТЕКСТЕ
    if context.user_data[DATA] == "user_payments" or context.user_data[DATA] == "shop_operations" or context.user_data[
        DATA] == "shop_comments" or context.user_data[DATA] == "shop_services_comments" or context.user_data[
        DATA] == "shop_products_comments":
        show_list_text(update, context, context.user_data[DATA])
