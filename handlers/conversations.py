from copy import deepcopy
from datetime import datetime, timedelta

import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

from res.coinbase_func import send_money
from res.const import SET_REQUEST_SHOP_NAME, e_winking, back_for_button, SET_SEARCH_SHOP_NAME, SELECT_ID, \
    SET_SEARCH_USER_NAME, SET_REQUEST_SHOP_WHY, SET_CHANGE_SHOP_ABOUT, SET_WITHDRAW_PERSONAL_SUM, \
    SET_GUARANTEE_SUM, e_handshake, SET_SEARCH_USER_ID, SET_SEARCH_SHOP_ID, SET_CHANGE_SHOP_NAME, \
    SET_WITHDRAWAL_GUARANTEE_SUM, e_broken_heart, min_withdrawal, SET_WITHDRAWAL_SUM, \
    SET_WITHDRAWAL_ADDRESS, e_dollar_banknote, SET_REQUISITE_NAME, SET_REQUISITE_PAYMENT_SYSTEM, \
    SET_REQUISITE_ACCOUNT_NUMBER, SET_REQUISITE_INFO, e_credit_card, SET_PRODUCT_INFO_NAME, \
    SET_PRODUCT_INFO_DESCRIPTION, SET_PRODUCT_INFO_CONTENT, CATEGORY_INFO, \
    PRODUCT_CHANGE_NAME, PRODUCT_ADD_CONTENT, PRODUCT_CHANGE_DESCRIPTION, PRODUCT_CHANGE_PICTURE, \
    SET_PRODUCT_INFO_PRICE, PRODUCT_CHANGE_PRICE, SELECT_PROD_ID, PRODUCT_COUNT, PRODUCT_SUM_PRICE, \
    PRODUCT_LTC_SUM_PRICE, min_guarantee, SET_CHANGE_SHOP_CHECK_TIME, BUYER_MESSAGE, DEAL_ID, BUYER_REVIEW, \
    SHOP_SEND_MESSAGE, DEAL_SHOP_CHANGE, MODER_MESSAGE, SHOP_ANSWER_MESSAGE, USER_MESSAGE, \
    CALL_MENU_SEND_MESSAGE, SET_SERVICE_NAME, \
    SET_SERVICE_PORTFOLIO, SET_SERVICE_MIN_PRICE, SET_SERVICE_PICTURE, SET_PACKET_DESCRIPTION, SET_PACKET_PRICE, DATA, \
    CAT_ID, SELECT_SERV_ID, CHANGE_SERVICE_NAME, \
    CHANGE_SERVICE_MIN_PRICE, CHANGE_SERVICE_PORTFOLIO, CHANGE_SERVICE_PICTURE, SET_PACKET_DEADLINE, \
    SET_SERVICE_DESCRIPTION, CHANGE_SERVICE_DESCRIPTION, CLIENT_SEND_TZ, SELECT_SERV_PACKET, CLIENT_MESSAGE, ORDER_ID, \
    SHOP_ORDER_MESSAGE, SHOP_ORDER_WORK, SHOP_ORDER_GRADE_PRICE, SHOP_ORDER_GRADE_DEADLINE, \
    CALL_ORDER_MENU_SEND_MESSAGE, CLIENT_ORDER_COMMENT, SELECT_SALE_SECTION, \
    SELECT_BUYS_SECTION, TERMS_TRADE, e_pencil, SET_REQUEST_SHOP_RES, min_input
from res.func import add_request_open_shop, check_open_shop_request, check_shop_owner, moders_alert, \
    check_occupied_shop_name, check_occupied_request_shop_name, search_shop_by_name, get_shop_info_text, \
    search_user_by_username, get_user_info_text, set_shop_about, get_shop_balance, get_user_balance, \
    add_shop_balance, update_user_balance, get_myshop_finance_text, update_shop_guarantee, add_shop_operation, \
    search_user_by_id, search_shop_by_id, set_shop_name, check_date_change_shop_name, set_date_change_shop_name, \
    get_guarantee_shop, check_shop_banned, add_shop_requisite, get_requisite_info, update_requisite_info, \
    add_shop_product, add_product_content, change_product_name, change_product_description, \
    change_product_price, get_product_by_id, get_ltc_by_rub, get_shop_requisites_list, change_shop_check_time, \
    get_deal_info, get_deal_by_id, get_shop_deal_menu, get_buyer_deal_menu, deal_shop_give_change, \
    get_shop_id, get_user_id, get_user_messages_limit, get_user_date_set_limit, update_user_date_set_limit, \
    update_user_massages_limit, get_shop_name, get_user_name, get_deal_messages, get_user_tg_id, \
    add_shop_service, get_my_service_packets_menu, get_service_by_id, add_order, add_user_balance, get_order_info, \
    get_client_order_menu, get_shop_order_menu, get_order_by_id, get_order_messages, get_moder_select_shop_menu, \
    get_shop_obj, check_moderator
from res.menu import moder_select_user_menu, my_shop_menu, my_shop_submenu_finance, \
    my_shop_finance_requisites_select_menu, my_shop_submenu_products, moder_select_call_menu_messages, \
    moder_select_call_order_menu_messages

# ============================================= ЗАЯВКА НА СОЗДАНИЕ МАГАЗИНА ===========================================
from res.schemas import Service


def request_submit(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if check_shop_owner(chat_id):
        update.callback_query.edit_message_text(
            f"   <b>Открыть магазин</b>\n\nВы уже владелец Магазина!\n\n", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_dashboard_menu')]]),
            parse_mode='HTML')
        return
    if check_open_shop_request(chat_id):
        update.callback_query.edit_message_text(
            f"   <b>Открыть магазин</b>\n\nВы уже оставляли заявку на открытие!\n"
            f"Дождитесь рассмотрения заявки", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_dashboard_menu')]]),
            parse_mode='HTML')
        return
    update.callback_query.edit_message_text(
        f"   <b>Открыть магазин</b>\n\nОтправьте название Магазина", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_dashboard_menu')]]),
        parse_mode='HTML')
    return SET_REQUEST_SHOP_NAME


def set_request_shop_name(update, context):
    shop_name = update.message.text
    chat_id = update.message.chat_id
    if len(shop_name) < 3 or len(shop_name) > 14:
        update.message.reply_text(f'   <b>Открыть магазин</b>\n\n'
                                  f'Длина названия должна быть от <i>3 до 14</i> символов\n\n'
                                  f'Отправьте название Магазина ещё раз!',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_dashboard_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_REQUEST_SHOP_NAME
    if check_occupied_shop_name(shop_name):
        update.message.reply_text(f'   <b>Открыть магазин</b>\n\n'
                                  f'Данное название уже занято\n'
                                  f'Отправьте название Магазина ещё раз',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_dashboard_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return
    if check_occupied_request_shop_name(shop_name):
        update.message.reply_text(f'   <b>Открыть магазин</b>\n\n'
                                  f'Заявка на создание Магазина с таким названием уже есть\n\n'
                                  f'Отправьте название Магазина ещё раз или попробуйте позже',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_dashboard_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return
    context.user_data[SET_REQUEST_SHOP_NAME] = shop_name
    update.message.reply_text(
        f"   <b>Открыть магазин</b>\n\n"
        f"Опишите и отправьте предполагаемый вид деятельности вашего магазина.\n\n"
        f"Какие товары/услуги планируете предоставлять в своём магазине?",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_dashboard_menu')]]),
        parse_mode='HTML')
    return SET_REQUEST_SHOP_WHY


def set_request_shop_why(update, context):
    why = update.message.text
    if len(why) < 10 or len(why) > 256:
        update.message.reply_text(f'   <b>Открыть магазин</b>\n\n'
                                  f'Необходимо корректно описать вид деятельности (до 250 сиволов).\n\n'
                                  f'Попробуйте ещё раз!',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_dashboard_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_REQUEST_SHOP_WHY
    context.user_data[SET_REQUEST_SHOP_WHY] = why
    update.message.reply_text(
        f"   <b>Открыть магазин</b>\n\n"
        f"Есть ли у вас свой ресурс (сайт, бот, канал)?\nПрикрепите ссылку, если имеется.\n\n"
        f"Если ресурсов нет, отправьте: \"Нет\"",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_dashboard_menu')]]),
        parse_mode='HTML')
    return SET_REQUEST_SHOP_RES


def set_request_shop_res(update, context):
    chat_id = update.message.chat_id
    res = update.message.text
    if len(res) > 256:
        update.message.reply_text(f'   <b>Открыть магазин</b>\n\n'
                                  f'Необходимо корректно описать свои ресурсы (до 250 сиволов).\n\n'
                                  f'Попробуйте ещё раз!',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_dashboard_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_REQUEST_SHOP_RES
    shop_name = context.user_data[SET_REQUEST_SHOP_NAME]
    why = context.user_data[SET_REQUEST_SHOP_WHY]
    add_request_open_shop(chat_id, shop_name, why, res)
    update.message.reply_text(f'   <b>Открыть магазин</b>\n\n'
                              f'Заявка на открытие магазина успешно отправлена!\n\n'
                              f'Ожидайте одобрения модератором, оповещение будет автоматически отправлено {e_winking}',
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  в Личный кабинет',
                                                         callback_data='back_to_dashboard_menu')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    moders_alert(context, 'new_request_shop')
    return ConversationHandler.END


# ====================================== ВВОД НАЗВАНИЯ МАГАЗИНА ДЛЯ ПОИСКА =============================================
def shop_moder_search(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'moder_shop_search_name':
        update.callback_query.edit_message_text(
            f"   <b>Поиск магазина</b>\n\nОтправьте название Магазина", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_moder_search_shop')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_SEARCH_SHOP_NAME
    elif query.data == 'moder_shop_search_id':
        update.callback_query.edit_message_text(
            f"   <b>Поиск магазина</b>\n\nОтправьте ID Магазина (пример: /s1N0HB25)",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_moder_search_shop')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_SEARCH_SHOP_ID


def set_search_shop_name(update, context):
    shop_name = update.message.text
    chat_id = update.message.chat_id
    shop = search_shop_by_name(shop_name)
    if not shop:
        update.message.reply_text(f'   <b>Поиск магазина</b>\n\nМагазин с таким названием не '
                                  f'найден!\nПопробуйте ещё '
                                  f'раз',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_moder_search_shop')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SEARCH_SHOP_NAME
    else:
        context.user_data[SELECT_ID] = shop.owner_id
        text = get_shop_info_text(chat_id, shop.owner_id)
        update.message.reply_text(text,
                                  reply_markup=InlineKeyboardMarkup(get_moder_select_shop_menu(shop.owner_id),
                                                                    resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END


def set_search_shop_id(update, context):
    shop_id = update.message.text
    chat_id = update.message.chat_id
    shop = search_shop_by_id(shop_id)
    if not shop:
        update.message.reply_text(f'   <b>Поиск магазина</b>\n\nМагазин с таким ID не '
                                  f'найден!\nПопробуйте ещё '
                                  f'раз',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_moder_search_shop')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SEARCH_SHOP_ID
    else:
        context.user_data[SELECT_ID] = shop.owner_id
        text = get_shop_info_text(chat_id, shop.owner_id)
        update.message.reply_text(text,
                                  reply_markup=InlineKeyboardMarkup(get_moder_select_shop_menu(shop.owner_id),
                                                                    resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END


# ========================================= ПОИСК ПОЛЬЗОВАТЕЛЯ ДЛЯ МОДЕРАТОРА ==========================================
def moder_user_search(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'moder_users_search_name':
        update.callback_query.edit_message_text(
            f"   <b>Поиск пользователя</b>\n\nОтправьте имя пользователя TG без '@'",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_moder_search_user')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_SEARCH_USER_NAME
    elif query.data == 'moder_users_search_id':
        update.callback_query.edit_message_text(
            f"   <b>Поиск пользователя</b>\n\nОтправьте ID пользователя (пример: /u1290A0D6)",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_moder_search_user')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_SEARCH_USER_ID


def set_search_user_name(update, context):
    user_name = update.message.text
    chat_id = update.message.chat_id
    user = search_user_by_username(user_name)
    if not user:
        update.message.reply_text(f'   <b>Поиск пользователя</b>\n\nПользователь с таким именем не найден!',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_moder_search_user')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SEARCH_USER_NAME
    else:
        context.user_data[SELECT_ID] = user.chat_id
        text = get_user_info_text(chat_id, user.chat_id)
        update.message.reply_text(text,
                                  reply_markup=InlineKeyboardMarkup(moder_select_user_menu,
                                                                    resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END


def set_search_user_id(update, context):
    find_user_id = update.message.text
    chat_id = update.message.chat_id
    user = search_user_by_id(find_user_id)
    if not user:
        update.message.reply_text(f'   <b>Поиск пользователя</b>\n\nПользователь с таким ID не найден!',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_moder_search_user')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SEARCH_USER_ID
    else:
        context.user_data[SELECT_ID] = user.chat_id
        text = get_user_info_text(chat_id, user.chat_id)
        update.message.reply_text(text,
                                  reply_markup=InlineKeyboardMarkup(moder_select_user_menu,
                                                                    resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END


# ============================================ ИЗМЕНЕНИЕ ОПИСАНИЯ МАГАЗИНА ============================================
def my_shop_settings_about(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Изменить описание Магазина</b>\n\nОтправьте краткое описание вашего магазина, его деятельности.\n\n"
        f"<b>✅ Пример:</b>  БОЛЬШОЙ АССОРТИМЕНТ АККАУНТОВ ВКОНТАКТЕ, ОДНОКЛАССНИКИ, INSTAGRAM, FACEBOOK, TWITTER, AVITO, TELEGRAM, GMAIL, MAIL.\n\n"
        f"<b>Максимальное кол-во символов:</b> 120",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_submenu_settings')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_CHANGE_SHOP_ABOUT


def set_my_shop_about(update, context):
    owner_id = update.message.chat_id
    if check_shop_banned(owner_id):
        return
    shop_about = update.message.text
    if len(shop_about) < 10 or len(shop_about) > 120:
        update.message.reply_text(f'   <b>Изменить описание Магазина</b>\n\n'
                                  f'Длина описания должна быть от <i>10 до 120</i> символов\n\n'
                                  f'Отправьте описание Магазина ещё раз!',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_my_shop_submenu_settings')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_CHANGE_SHOP_ABOUT
    set_shop_about(owner_id, shop_about)
    context.bot.sendMessage(owner_id,
                            f"   <b>Описание успешно изменено</b> {e_winking}",
                            parse_mode='HTML')
    shop_info = get_shop_info_text(owner_id, owner_id)
    update.message.reply_text(shop_info,
                              reply_markup=InlineKeyboardMarkup(my_shop_menu,
                                                                resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


# ============================================ ИЗМЕНЕНИЕ НАЗВАНИЯ МАГАЗИНА ============================================
def my_shop_settings_name(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Изменить название Магазина</b>\n\nОтправьте новое название (3-14 символов)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_submenu_settings')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_CHANGE_SHOP_NAME


def set_my_shop_name(update, context):
    shop_name = update.message.text
    owner_id = update.message.chat_id
    if check_shop_banned(owner_id):
        return
    if len(shop_name) < 3 or len(shop_name) > 14:
        context.bot.sendMessage(owner_id, f'   <b>Изменить название Магазина</b>\n\n'
                                          f'Длина названия должна быть от <i>3 до 14</i> символов\n\n'
                                          f'Отправьте название Магазина ещё раз!',
                                reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_my_shop_submenu_settings')]],
                                    resize_keyboard=True),
                                parse_mode='HTML')
        return SET_CHANGE_SHOP_NAME
    if not check_date_change_shop_name(owner_id):
        context.bot.sendMessage(owner_id,
                                f"<b>Название можно изменять раз в сутки</b> {e_winking}",
                                parse_mode='HTML')
        shop_info = get_shop_info_text(owner_id,
                                       owner_id)
        context.bot.sendMessage(owner_id, shop_info,
                                reply_markup=InlineKeyboardMarkup(my_shop_menu,
                                                                  resize_keyboard=True),
                                parse_mode='HTML')
        return ConversationHandler.END
    if check_occupied_shop_name(shop_name):
        context.bot.sendMessage(owner_id, f'   <b>Изменить название Магазина</b>\n\n'
                                          f'Данное название уже занято\n'
                                          f'Отправьте название Магазина ещё раз',
                                reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_my_shop_submenu_settings')]],
                                    resize_keyboard=True),
                                parse_mode='HTML')
        return SET_CHANGE_SHOP_NAME
    set_shop_name(owner_id, shop_name)
    context.bot.sendMessage(owner_id,
                            f"<b>Название успешно изменено</b> {e_winking}",
                            parse_mode='HTML')
    shop_info = get_shop_info_text(owner_id, owner_id)
    context.bot.sendMessage(owner_id, shop_info,
                            reply_markup=InlineKeyboardMarkup(my_shop_menu,
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    set_date_change_shop_name(owner_id)
    return ConversationHandler.END


# ------------- Изменение времени на проверку товара -----------------
def my_shop_settings_check_time(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        '<b>⏱ Изменить время проверки товара</b>\n\n'
        'Время за которое покупатель сможет проверить товар на валидность.\n\n'
        'Минимальное время - 5 минут\n\n'
        f"Отправьте <b>целое число</b> - время <b>в минутах</b> на проверку товара для Ваших покупателей",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_submenu_settings')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_CHANGE_SHOP_CHECK_TIME


def set_my_shop_check_time(update, context):
    time_text = update.message.text
    chat_id = update.message.chat_id
    try:
        time = int(time_text)
    except ValueError:
        update.message.reply_text(
            f"<b>Некорректное значение минут!</b>\nПопробуй ещё раз {e_winking}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_my_shop_submenu_settings')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_CHANGE_SHOP_CHECK_TIME
    if time < 5:
        update.message.reply_text(
            f"<b>Не меньше 5 минут!</b>\nПопробуй ещё раз {e_winking}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_my_shop_submenu_settings')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_CHANGE_SHOP_CHECK_TIME
    change_shop_check_time(chat_id, time)
    update.message.reply_text(
        f"<b>Время проверки товара успешно изменено</b> {e_winking}",
        parse_mode='HTML')
    shop_info = get_shop_info_text(chat_id, chat_id)
    update.message.reply_text(shop_info,
                              reply_markup=InlineKeyboardMarkup(my_shop_menu,
                                                                resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


# ================================================== ВНЕСЕНИЕ ГАРАНТА ==================================================
def input_guarantee_from_shop_acc(update, context):
    query = update.callback_query
    query.answer()
    owner_id = query.message.chat.id
    shop_balance = get_shop_balance(owner_id)
    update.callback_query.edit_message_text(
        f"<b>{e_handshake}   Внесение гаранта</b>\n\n"
        f"Сумма будет списана со счета <i>вашего Магазина</i>\n\n"
        f"<b>Доступно для внесения:</b>  {shop_balance}  LITECOIN\n"
        f"<b>Минимальная сумма:</b>  {min_input} LITECOIN\n\n"
        f"Отправьте сумму в LITECOIN:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_finance_guarantee')]],
            resize_keyboard=True),
        parse_mode='HTML')
    context.user_data[SET_GUARANTEE_SUM] = "shop"
    return SET_GUARANTEE_SUM


def input_guarantee_from_personal_acc(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.message.chat.id
    user_balance = get_user_balance(user_id)
    update.callback_query.edit_message_text(
        f"<b>{e_handshake}   Внесение гаранта</b>\n\n"
        f"Сумма будет списана с <i>вашего личного</i> счета\n\n"
        f"<b>Доступно для внесения:</b>  {user_balance}  LITECOIN\n"
        f"<b>Минимальная сумма:</b>  {min_input} LITECOIN\n\n"
        f"Отправьте сумму в LITECOIN:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_finance_guarantee')]],
            resize_keyboard=True),
        parse_mode='HTML')
    context.user_data[SET_GUARANTEE_SUM] = "personal"
    return SET_GUARANTEE_SUM


def input_guarantee(update, context):
    chat_id = update.message.chat_id
    summa = update.message.text
    try:
        summa = float(summa)
    except ValueError:
        update.message.reply_text(
            f"<b>Некорректная сумма! Пример: 0.5</b>\nПопробуйте ещё раз {e_winking}",
            parse_mode='HTML')
        return SET_WITHDRAW_PERSONAL_SUM
    if summa < min_input:
        update.message.reply_text(
            f"<b>{e_handshake}   Внесение гаранта</b>\n\n"
            f"<b>Минимальная сумма для внесения:</b>  {min_input} LITECOIN\n\n"
            f"Отправьте сумму в LITECOIN:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_finance_guarantee')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_GUARANTEE_SUM
    if context.user_data[SET_GUARANTEE_SUM] == "shop":
        shop_balance = get_shop_balance(chat_id)
        if summa > shop_balance:
            update.message.reply_text(
                f"<b>{e_handshake}   Внесение гаранта</b>\n\n<b>Недостаточно средств на счету Магазина</b>\n\n"
                f"Отправьте сумму в LITECOIN:",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                           callback_data='back_to_insert_guarantee_menu')]],
                    resize_keyboard=True),
                parse_mode='HTML')
            return SET_GUARANTEE_SUM
        add_shop_operation(chat_id, "Пополнение гаранта со счёта Магазина", summa, 0)
        add_shop_balance(chat_id, -summa)
    elif context.user_data[SET_GUARANTEE_SUM] == "personal":
        user_balance = get_user_balance(chat_id)
        if summa > user_balance:
            update.message.reply_text(
                f"<b>{e_handshake}   Внесение гаранта</b>\n\n"
                f"<b>Недостаточно средств на Личном счету</b>\n\n"
                f"Отправьте сумму в LITECOIN:",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                           callback_data='back_to_insert_guarantee_menu')]],
                    resize_keyboard=True),
                parse_mode='HTML')
            return SET_GUARANTEE_SUM
        add_shop_operation(chat_id, "Пополнение гаранта с Личного счета", summa, 0)
        update_user_balance(chat_id, -summa)
    update_shop_guarantee(chat_id, summa)
    text = get_myshop_finance_text(chat_id)
    update.message.reply_text(
        f"<b>Пополнение гаранта на сумму <i>{summa}</i>  LITECOIN прошло успешно!</b> {e_winking}",
        parse_mode='HTML')
    update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(my_shop_submenu_finance, resize_keyboard=True),
        parse_mode='HTML')
    return ConversationHandler.END


# ================ ВЫВОД с гаранта на счёт магазина ================
def my_shop_finance_guarantee_withdrawal(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    guarantee = get_guarantee_shop(chat_id)
    update.callback_query.edit_message_text(
        f"<b>{e_broken_heart}   Вывод гаранта</b>\n\n"
        f"Сумма будет списана со счета Вашего <i>гаранта</i> и перечислена на счет Магазина\n\n"
        f"Доступно для вывода:  {guarantee}  LITECOIN\n"
        f"<b>Минимальная сумма для вывода:</b>  {min_withdrawal} LITECOIN\n\n"
        f"⚠  <b>Если сумма гаранта станет меньше {min_guarantee} LTC, вы больше не сможете использовать личные реквизиты!</b>\n\n"
        f"Отправьте сумму в LITECOIN:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_finance_guarantee')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_WITHDRAWAL_GUARANTEE_SUM


def input_withdrawal_guarantee(update, context):
    summa = update.message.text
    chat_id = update.message.chat_id
    try:
        summa = float(summa)
    except ValueError:
        update.message.reply_text(
            f"<b>{e_broken_heart}   Вывод гаранта</b>\n\n"
            f"<b>Неверное значение!</b>\n\n"
            f"Отправьте сумму в LITECOIN:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_finance_guarantee')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_WITHDRAWAL_GUARANTEE_SUM
    guarantee_balance = get_guarantee_shop(chat_id)
    if summa <= 0:
        update.message.reply_text(
            f"<b>{e_broken_heart}   Вывод гаранта</b>\n\n"
            f"<b>Неверное значение!</b>\n\n"
            f"Отправьте сумму в LITECOIN:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_finance_guarantee')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_WITHDRAWAL_GUARANTEE_SUM
    if summa > guarantee_balance:
        update.message.reply_text(
            f"<b>{e_broken_heart}   Вывод гаранта</b>\n\n"
            f"<b>Недостаточно средств на балансе Гаранта</b>\n\n"
            f"Отправьте сумму в LITECOIN:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_finance_guarantee')]]),
            parse_mode='HTML')
        return SET_WITHDRAWAL_GUARANTEE_SUM
    add_shop_operation(chat_id, "Вывод Гаранта на счет Магазина", summa, 1)
    update_shop_guarantee(chat_id, -summa)
    add_shop_balance(chat_id, summa)
    text = get_myshop_finance_text(chat_id)
    update.message.reply_text(
        f"<b>Вывод Гаранта на сумму <i>{summa}</i>  LITECOIN прошел успешно!</b> {e_winking}",
        parse_mode='HTML')
    update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(my_shop_submenu_finance, resize_keyboard=True),
        parse_mode='HTML')
    return ConversationHandler.END


# =============== ВЫВОД LITECOIN ИЗ СЕРВИСА =====================
def my_shop_withdrawal_from_service(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    balance = get_shop_balance(chat_id)
    update.callback_query.edit_message_text(
        f"<b>{e_dollar_banknote}   Вывод LITECOIN</b>\n\n"
        f"<b>Минимальная сумма для вывода:</b>  {min_withdrawal} LITECOIN\n"
        f"<b>Доступно для вывода:</b>  {balance}\n\n"
        f"Отправьте сумму в LITECOIN:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_shop_finance_withdrawal')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_WITHDRAWAL_SUM


def input_withdrawal_sum(update, context):
    summa = update.message.text
    chat_id = update.message.chat_id
    try:
        summa = float(summa)
    except ValueError:
        update.message.reply_text(
            f"<b>Некорректная сумма! Пример: 0.5</b>\nПопробуй ещё раз {e_winking}",
            parse_mode='HTML')
        return SET_WITHDRAWAL_SUM
    shop_balance = get_shop_balance(chat_id)
    if summa < min_withdrawal:
        update.message.reply_text(
            f"<b>{e_dollar_banknote}   Вывод LITECOIN</b>\n\n"
            f"<b>Минимальная сумма для перевода:</b>  {min_withdrawal} LITECOIN\n\n"
            f"Отправьте сумму в LITECOIN:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_finance_withdrawal')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_WITHDRAWAL_SUM
    if summa > shop_balance:
        update.message.reply_text(
            f"<b>{e_dollar_banknote}   Вывод LITECOIN</b>\n\nОтправьте сумму в LITECOIN\n\n"
            f"<b>Недостаточно средств на балансе Магазина</b>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_finance_withdrawal')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_WITHDRAWAL_SUM
    context.user_data[SET_WITHDRAWAL_SUM] = summa
    update.message.reply_text(
        f"<b>{e_dollar_banknote}   Вывод LITECOIN</b>\n\n"
        f"Отправьте <b>LITECOIN адрес</b> для вывода\n\n"
        f"Внимательно перепроверьте адрес перед отправкой\n\n"
        f"При вводе учитывайте регистр символов!",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_shop_finance_withdrawal')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_WITHDRAWAL_ADDRESS


def input_withdrawal_address(update, context):
    address = update.message.text
    chat_id = update.message.chat_id
    amount = context.user_data[SET_WITHDRAWAL_SUM]
    if len(address) != 34 and len(address) != 43:
        update.message.reply_text(
            f"<b>{e_dollar_banknote}   Вывод LITECOIN</b>\n\n"
            f"Ошибка в введённом адресе LITECOIN, проверьте!\n"
            f"Отправьте <b>LITECOIN адрес</b> для вывода:\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_finance_withdrawal')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_WITHDRAWAL_ADDRESS

    check_send_money = send_money(chat_id, address, amount)
    if check_send_money:
        update.message.reply_text(
            f"<b>{e_dollar_banknote}   Вывод LITECOIN</b>\n\n"
            f"Вы успешно вывели {amount} LITECOIN на адрес\n\n"
            f"\t\t<b>{address}</b>\n\n"
            f"\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  в Мои финансы',
                                       callback_data='back_to_my_shop_finance_menu')]], resize_keyboard=True),
            parse_mode='HTML')
        add_shop_balance(chat_id, -amount)
        add_shop_operation(chat_id, f"Вывод LITECOIN на адрес <u>{address}</u>", amount, 0)
    else:
        update.message.reply_text(
            f"<b>{e_dollar_banknote}   Вывод LITECOIN</b>\n\n"
            f"Произошла ошибка при выводе\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_my_shop_finance_withdrawal')]], resize_keyboard=True),
            parse_mode='HTML')
    return ConversationHandler.END


# ======================================= ВЫВОД НА ЛИЧНЫЙ СЧЕТ СО СЧЕТА МАГАЗИНА =====================================
def my_shop_withdrawal_to_personal(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    balance = get_shop_balance(chat_id)
    update.callback_query.edit_message_text(
        f"   <b>Перевести на личный счёт</b>\n\n"
        f"Если вы хотите делать покупки в <b>других магазинах</b> - можете перевести LITECOIN на Личный счет\n\n"
        f"<b>Минимальная сумма для вывода:</b>  {min_withdrawal} LITECOIN\n\n"
        f"<b>Доступно для вывода:</b>  {balance}  LITECOIN\n\n"
        f"Отправьте сумму в LITECOIN:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_shop_finance_withdrawal')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_WITHDRAW_PERSONAL_SUM


def withdrawal_to_personal(update, context):
    chat_id = update.message.chat_id
    summa = update.message.text
    try:
        summa = float(summa)
    except ValueError:
        update.message.reply_text(
            f"<b>Некорректная сумма! Пример: 0.5</b>\nПопробуй ещё раз {e_winking}",
            parse_mode='HTML')
        return SET_WITHDRAW_PERSONAL_SUM
    shop_balance = get_shop_balance(chat_id)
    if summa < min_withdrawal:
        update.message.reply_text(
            f"   <b>Перевести на личный счёт</b>\n\n"
            f"<b>Минимальная сумма для перевода:</b>  {min_withdrawal} LITECOIN\n\n"
            f"Отправьте сумму в LITECOIN:\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_finance_withdrawal')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_WITHDRAWAL_GUARANTEE_SUM
    if summa > shop_balance:
        update.message.reply_text(
            f"   <b>Перевести на личный счёт</b>\n\n<b>Недостаточно средств!</b>\n\nОтправьте сумму в LITECOIN:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_finance_withdrawal')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_WITHDRAW_PERSONAL_SUM
    add_shop_balance(chat_id, -summa)
    update_user_balance(chat_id, summa)
    update.message.reply_text(
        f"<b>Вывод <i>{summa}</i> LITECOIN на <i>Личный счет</i> успешно осуществлен!</b> {e_winking}",
        parse_mode='HTML')
    add_shop_operation(chat_id, "Вывод на Личный счёт", summa, 0)
    text = get_myshop_finance_text(chat_id)
    update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(my_shop_submenu_finance, resize_keyboard=True),
        parse_mode='HTML')
    return ConversationHandler.END


# ===================================== ДОБАВЛЕНИЕ РЕКВИЗИТА ==========================================================
def my_shop_finance_requisites_add(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"{e_credit_card}   <b>Добавить реквизит</b>\n\n"
        f"Внимательно указывайте все данные реквизита\n\n"
        f"Если вы допустите ошибку, то покупатель отправит средства не туда!\n\n"
        f"Отправьте <b>Название реквизита</b> \n\n<i>(примеры: основной, резервный...)</i>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_shop_finance_requisites')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_REQUISITE_NAME


def set_requisite_name(update, context):
    chat_id = update.message.chat_id
    requisite_name = update.message.text
    if len(requisite_name) < 1 or len(requisite_name) > 20:
        update.message.reply_text(
            f"{e_credit_card}   <b>Добавить реквизит</b>\n\n"
            f"<b>Название</b> должно быть от 1 до 20 символов!\n"
            f"Попробуйте ещё раз",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_my_shop_finance_requisites')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_REQUISITE_NAME
    context.user_data[SET_REQUISITE_NAME] = requisite_name
    update.message.reply_text(
        f"{e_credit_card}   <b>Добавить реквизит</b>\n\n"
        f"Отправьте <b>Платежную систему</b> \n\n<i>(примеры: QIWI, ЮMoney, Сбербанк...)</i>\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_my_shop_finance_requisites')]], resize_keyboard=True),
        parse_mode='HTML')
    return SET_REQUISITE_PAYMENT_SYSTEM


def set_requisite_payment_system(update, context):
    chat_id = update.message.chat_id
    payment_system = update.message.text
    if len(payment_system) < 3 or len(payment_system) > 30:
        update.message.reply_text(
            f"{e_credit_card}   <b>Добавить реквизит</b>\n\n"
            f"<b>Платежная система</b> должна быть от 3 до 30 символов!\n"
            f"Попробуйте ещё раз..",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_finance_requisites')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_REQUISITE_PAYMENT_SYSTEM
    context.user_data[SET_REQUISITE_PAYMENT_SYSTEM] = payment_system
    update.message.reply_text(
        f"{e_credit_card}   <b>Добавить реквизит</b>\n\n"
        f"Отправьте <b>Номер счета</b> для получения\n\n"
        f"Для QIWI - <i>номер телефона</i>\n"
        f"Для банковской карты - <i>номер карты</i> и т.д.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_my_shop_finance_requisites')]], resize_keyboard=True),
        parse_mode='HTML')
    return SET_REQUISITE_ACCOUNT_NUMBER


def set_requisite_account_number(update, context):
    account_number = update.message.text
    chat_id = update.message.chat_id
    if len(account_number) < 10:
        update.message.reply_text(
            f"{e_credit_card}   <b>Добавить реквизит</b>\n\n"
            f"Слишком короткий <b>Номер счёта</b>!\n"
            f"Попробуйте ещё раз..",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_finance_requisites')]]),
            parse_mode='HTML')
        return SET_REQUISITE_PAYMENT_SYSTEM
    add_shop_requisite(chat_id, context.user_data[SET_REQUISITE_NAME], context.user_data[SET_REQUISITE_PAYMENT_SYSTEM],
                       account_number)
    update.message.reply_text(
        f"{e_credit_card}   <b>Добавить реквизит</b>\n\n"
        f"Реквизит успешно добавлен!\n"
        f"Управлять реквизитом можно в разделе\n<b>'Все реквизиты'</b>\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  в Мои реквизиты',
                                   callback_data='back_to_my_shop_finance_requisites')]]),
        parse_mode='HTML')
    return ConversationHandler.END


def my_shop_finance_requisites_select_edit_name(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"{e_credit_card}   <b>Изменить название</b>\n\n"
        f"Отправьте новое <b>Название</b> реквизита\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_my_shop_finance_requisites_select_menu')]],
            resize_keyboard=True),
        parse_mode='HTML')
    context.user_data[SET_REQUISITE_INFO] = "name"
    return SET_REQUISITE_INFO


def my_shop_finance_requisites_select_edit_payment_system(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"{e_credit_card}   <b>Изменить платежную систему</b>\n\n"
        f"Отправьте новую <b>Платежную систему</b> для реквизита\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_my_shop_finance_requisites_select_menu')]],
            resize_keyboard=True),
        parse_mode='HTML')
    context.user_data[SET_REQUISITE_INFO] = "payment_system"
    return SET_REQUISITE_INFO


def my_shop_finance_requisites_select_edit_account_number(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"{e_credit_card}   <b>Изменить номер счета</b>\n\n"
        f"Отправьте новый <b>Номер счета</b> для реквизита\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_my_shop_finance_requisites_select_menu')]],
            resize_keyboard=True),
        parse_mode='HTML')
    context.user_data[SET_REQUISITE_INFO] = "account_number"
    return SET_REQUISITE_INFO


def set_requisite_info(update, context):
    chat_id = update.message.chat_id
    select_id = context.user_data[SELECT_ID]
    info = context.user_data[SET_REQUISITE_INFO]
    data = update.message.text
    if info == "name":
        if len(data) < 5 or len(data) > 20:
            update.message.reply_text(
                f"{e_credit_card}   <b>Изменить название</b>\n\n"
                f"<b>Название</b> должно быть от 5 до 20 символов!\n"
                f"Попробуйте ещё раз",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                           callback_data='back_to_my_shop_finance_requisites_select_menu')]]),
                parse_mode='HTML')
            return SET_REQUISITE_INFO
        update_requisite_info(chat_id, select_id, info, data)
        requisite_info = get_requisite_info(chat_id, select_id)
        update.message.reply_text('<b>Название</b> реквизита успешно изменено', parse_mode='HTML')
        update.message.reply_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                  f"{requisite_info}",
                                  reply_markup=InlineKeyboardMarkup(
                                      my_shop_finance_requisites_select_menu,
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    elif info == "payment_system":
        if len(data) < 3 or len(data) > 30:
            update.message.reply_text(
                f"{e_credit_card}   <b>Изменить платежную систему</b>\n\n"
                f"<b>Платежная система</b> должна быть от 3 до 30 символов!\n"
                f"Попробуйте ещё раз..",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                           callback_data='back_to_my_shop_finance_requisites_select_menu')]]),
                parse_mode='HTML')
            return SET_REQUISITE_INFO
        update_requisite_info(chat_id, select_id, info, data)
        requisite_info = get_requisite_info(chat_id, select_id)
        update.message.reply_text('<b>Платежная система</b> реквизита успешно изменена', parse_mode='HTML')
        update.message.reply_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                  f"{requisite_info}",
                                  reply_markup=InlineKeyboardMarkup(
                                      my_shop_finance_requisites_select_menu,
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    elif info == "account_number":
        if len(data) < 10:
            update.message.reply_text(
                f"{e_credit_card}   <b>Изменить номер счета</b>\n\n"
                f"Слишком короткий <b>Номер счёта</b>!\n"
                f"Попробуйте ещё раз..",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                           callback_data='back_to_my_shop_finance_requisites_select_menu')]]),
                parse_mode='HTML')
            return SET_REQUISITE_INFO
        update_requisite_info(chat_id, select_id, info, data)
        requisite_info = get_requisite_info(chat_id, select_id)
        update.message.reply_text('<b>Номер счета</b> реквизита успешно изменено', parse_mode='HTML')
        update.message.reply_text(f"{e_credit_card}   <b>Мои реквизиты</b>\n\n"
                                  f"{requisite_info}",
                                  reply_markup=InlineKeyboardMarkup(
                                      my_shop_finance_requisites_select_menu,
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    return ConversationHandler.END


# =========================================== ДОБАВЛЕНИЕ ТОВАРА ==========================================
def start_add_product(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Добавление товара</b>\n\n"
        f"Выбранная категория:  {context.user_data[CATEGORY_INFO]['cat_path']}\n"
        f"Максимально точно указывайте все данные о товаре\n\n"
        f"Отправьте <b>Название товара</b> <u>без упоминания категории</u>\n"
        f"<b>От 5 до 30 символов</b>\n"
        f"<i>(пример: login:pass:api)</i>\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_shop_submenu_products')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_PRODUCT_INFO_NAME


def set_product_info_name(update, context):
    data = update.message.text
    if len(data) < 5 or len(data) > 30:
        update.message.reply_text(
            f"   <b>Добавление товара</b>\n\n"
            f"Отправьте <b>Название товара</b> <u>без упоминания категории</u>\n"
            f"<b>От 5 до 30 символов</b>\n"
            f"<i>(пример: login:pass:api)</i>\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_my_shop_submenu_products')]]),
            parse_mode='HTML')
        return SET_PRODUCT_INFO_NAME
    context.user_data[SET_PRODUCT_INFO_NAME] = data
    update.message.reply_text(
        f"   <b>Добавление товара</b>\n\n"
        f"Отправьте <b>Описание товара (до 100 символов)</b>\n\n<b>(Необязательно)</b> Чтобы пропустить отправьте \"-\" (минус)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_shop_submenu_products')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_PRODUCT_INFO_DESCRIPTION


def set_product_info_description(update, context):
    data = update.message.text
    if len(data) > 100:
        update.message.reply_text(
            f"   <b>Добавление товара</b>\n\n"
            f"<b>До 100 символов</b>\n\n"
            f"Отправьте <b>Описание товара</b>\n\n<b>(Необязательно)</b> Чтобы пропустить отправьте \"-\" (минус)",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_submenu_products')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_PRODUCT_INFO_DESCRIPTION
    if data != '-':
        context.user_data[SET_PRODUCT_INFO_DESCRIPTION] = data
    else:
        context.user_data[SET_PRODUCT_INFO_DESCRIPTION] = ""
    update.message.reply_text(
        f"   <b>Добавление товара</b>\n\n"
        f"Отправьте целое число - стоимость одной единицы товара  (от 1 до 100000)\n\n"
        f"Стоимость указывается <b>в Рублях</b>\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_my_shop_submenu_products')]], resize_keyboard=True),
        parse_mode='HTML')
    return SET_PRODUCT_INFO_PRICE


def set_product_info_price(update, context):
    price = update.message.text
    try:
        price = int(price)
    except ValueError:
        update.message.reply_text(
            f"   <b>Добавление товара</b>\n\n"
            f"Отправьте целое число - стоимость одной единицы товара (от 1 до 100000)\n\n"
            f"Стоимость указывается <b>в Рублях</b>\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_submenu_products')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_PRODUCT_INFO_PRICE
    if price < 1 or price > 100000:
        update.message.reply_text(
            f"   <b>Добавление товара</b>\n\n"
            f"Отправьте целое число - стоимость одной единицы товара (от 1 до 100000)\n\n"
            f"Стоимость указывается <b>в Рублях</b>\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_my_shop_submenu_products')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_PRODUCT_INFO_PRICE
    context.user_data[SET_PRODUCT_INFO_PRICE] = price
    file_id = 'AgACAgIAAxkBAAINHmE7nYLpNt-SKdzhoU_ra1PSR-MKAAIstjEb7kXhSVWpzhx8p1prAQADAgADcwADIAQ'
    context.bot.sendPhoto(update.message.chat_id, file_id)
    update.message.reply_text(
        f"   <b>Добавление товара</b>\n\n"
        f"Отправьте текстовый документ <b>(расширение .txt)</b>, пример содержимого выше.\n\n"
        f"Или простое сообщение в том же формате.\n\n"
        f"<u>Содержимое:</u>  <b>1 строка = 1 единица товара</b>\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_my_shop_submenu_products')]], resize_keyboard=True),
        parse_mode='HTML')
    return SET_PRODUCT_INFO_CONTENT


def set_product_info_content(update, context):
    category_id = context.user_data[CATEGORY_INFO]['cat_id']
    owner_id = update.message.chat_id
    name = context.user_data[SET_PRODUCT_INFO_NAME]
    price = context.user_data[SET_PRODUCT_INFO_PRICE]
    description = "Нет"
    if context.user_data[SET_PRODUCT_INFO_DESCRIPTION] != "":
        description = context.user_data[SET_PRODUCT_INFO_DESCRIPTION]
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    buf = file.download_as_bytearray()
    s = buf.decode()
    content = s.splitlines()
    count = len(content)
    cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']
    add_shop_product(category_id, owner_id, name, description, price, count, content)
    update.message.reply_text(f"   <b>Мои товары</b>\n\nТовар успешно добавлен!"
                              f"{cat_path_text}\n"
                              f"<b>Название: </b>{name}\n"
                              f"<b>Описание: </b>{description}\n"
                              f"<b>Стоимость (1 шт.): </b>{price} ₽\n"
                              f"<b>Количество: </b>{count}",
                              reply_markup=InlineKeyboardMarkup(my_shop_submenu_products,
                                                                resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def set_product_info_content_text(update, context):
    category_id = context.user_data[CATEGORY_INFO]['cat_id']
    owner_id = update.message.chat_id
    name = context.user_data[SET_PRODUCT_INFO_NAME]
    price = context.user_data[SET_PRODUCT_INFO_PRICE]
    description = "Нет"
    if context.user_data[SET_PRODUCT_INFO_DESCRIPTION] != "":
        description = context.user_data[SET_PRODUCT_INFO_DESCRIPTION]
    s = update.message.text
    content = s.splitlines()
    count = len(content)
    cat_path_text = "\n\n<u>Категория</u>\n" + context.user_data[CATEGORY_INFO]['cat_path']
    add_shop_product(category_id, owner_id, name, description, price, count, content)
    update.message.reply_text(f"   <b>Мои товары</b>\n\nТовар успешно добавлен!"
                              f"{cat_path_text}\n"
                              f"<b>Название: </b>{name}\n"
                              f"<b>Описание: </b>{description}\n"
                              f"<b>Стоимость (1 шт.): </b>{price} ₽\n"
                              f"<b>Количество: </b>{count}",
                              reply_markup=InlineKeyboardMarkup(my_shop_submenu_products,
                                                                resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


# ============================= Изменение товара ================================
# Пополнение товара
def button_my_shop_products_prod_count_add(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(f"   <b>Пополнение товара</b>\n\n"
                                            f"Отправьте текстовый документ <b>(расширение .txt)</b>, пример содержимого выше.\n"
                                            f"Или простое сообщение в том же формате.\n\n"
                                            f"<u>Содержимое:</u>  <b>1 строка = 1 единица товара</b>\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                       callback_data='back_to_prod_menu')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return PRODUCT_ADD_CONTENT


def product_add_content(update, context):
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    product_id = context.user_data[SELECT_PROD_ID]
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    buf = file.download_as_bytearray()
    s = buf.decode()
    content = s.splitlines()
    count = len(content)
    add_product_content(product_id, count, content)
    update.message.reply_text(f"   <b>Пополнение товара</b>\n\nТовар успешно пополнен!\n<b>Добавлено: </b>{count} ед.",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_prev_cat_menu')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def product_add_content_text(update, context):
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    product_id = context.user_data[SELECT_PROD_ID]
    s = update.message.text
    content = s.splitlines()
    count = len(content)
    add_product_content(product_id, count, content)
    update.message.reply_text(f"   <b>Пополнение товара</b>\n\nТовар успешно пополнен!\n<b>Добавлено: </b>{count} ед.",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_prev_cat_menu')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


# Изменение названия
def button_change_prod_name(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(f"   <b>Изменение названия товара</b>\n\n"
                                            f"Отправьте <b>Название товара</b> <u>без упоминания категории</u>\n\n"
                                            f"<i>(пример: Свежие кошельки)</i>\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                       callback_data='back_to_products_prod_edit')]],
                                                resize_keyboard=True), parse_mode="HTML")
    return PRODUCT_CHANGE_NAME


def product_name_change(update, context):
    if SELECT_PROD_ID not in context.user_data:
        return update.message.reply_text("Не актуально")
    name = update.message.text
    if len(name) < 5 or len(name) > 30:
        update.message.reply_text(
            f"   <b>Изменение названия товара</b>\n\n"
            f"<b>От 5 до 30 символов</b>\n\n"
            f"Отправьте <b>Название товара</b> <u>без упоминания категории</u>\n\n"
            f"<i>(пример: Свежие кошельки)</i>\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_products_prod_edit')]]),
            parse_mode='HTML')
        return PRODUCT_CHANGE_NAME
    change_product_name(context.user_data[SELECT_PROD_ID], name)
    update.message.reply_text(f"   <b>Изменение названия товара</b>\n\nНазвание товара успешно изменено",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_products_prod_edit')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


# Изменение описания
def button_change_prod_description(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(f"   <b>Изменение описания товара</b>\n\n"
                                            f"Отправьте <b>Описание товара</b>\n\n"
                                            f"Чтобы убрать отправьте \"-\" (минус)",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                       callback_data='back_to_products_prod_edit')]],
                                                resize_keyboard=True), parse_mode="HTML")
    return PRODUCT_CHANGE_DESCRIPTION


def product_description_change(update, context):
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    description = update.message.text
    if description == '-':
        description = "Нет"
    if len(description) > 50:
        update.message.reply_text(
            f"   <b>Изменение описания товара</b>\n\n"
            f"<b>До 50 символов</b>\n\n"
            f"Отправьте <b>Описание товара</b>\n\nЧтобы убрать отправьте \"-\" (минус)",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_products_prod_edit')]]),
            parse_mode='HTML')
        return PRODUCT_CHANGE_DESCRIPTION
    change_product_description(context.user_data[SELECT_PROD_ID], description)
    update.message.reply_text(f"   <b>Изменение описания товара</b>\n\nОписание товара успешно изменено",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_products_prod_edit')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def button_change_prod_picture(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(
        f"   <b>Изменение изображения товара</b>\n\n"
        f"Отправьте <b>Изображение товара</b>\n\n"
        f"Чтобы удалить изображение отправьте \"-\" (минус)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_products_prod_edit')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return PRODUCT_CHANGE_PICTURE


def button_change_prod_price(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(f"   <b>Изменение стоимости товара</b>\n\n"
                                            f"Отправьте целое число - стоимость одной единицы товара\n\n"
                                            f"Стоимость указывается <b>в Рублях</b>\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                       callback_data='back_to_products_prod_edit')]],
                                                resize_keyboard=True), parse_mode="HTML")
    return PRODUCT_CHANGE_PRICE


def product_price_change(update, context):
    price = update.message.text
    chat_id = update.message.chat_id
    try:
        price = int(price)
    except ValueError:
        update.message.reply_text(
            f"   <b>Изменение стоимости товара</b>\n\n"
            f"Отправьте целое число - стоимость одной единицы товара\n\n"
            f"Стоимость указывается <b>в Рублях</b>\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_products_prod_edit')]], resize_keyboard=True),
            parse_mode='HTML')
        return SET_PRODUCT_INFO_PRICE
    if price < 1 or price > 100000:
        update.message.reply_text(
            f"   <b>Изменение товара</b>\n\n"
            f"Отправьте целое число - стоимость одной единицы товара (от 1 до 100000)\n\n"
            f"Стоимость указывается <b>в Рублях</b>\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_products_prod_edit')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SET_PRODUCT_INFO_PRICE
    context.user_data[SET_PRODUCT_INFO_PRICE] = price
    change_product_price(context.user_data[SELECT_PROD_ID], price)
    update.message.reply_text(
        f"   <b>Изменение стоимости товара</b>\n\n"
        f"Стоимость товара успешно изменена!\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_products_prod_edit')]], resize_keyboard=True),
        parse_mode='HTML')
    return ConversationHandler.END


# Начало покупки товара (ввод количества товара)
def button_market_select_prod_buy(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_PROD_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    chat_id = query.message.chat.id
    prod_id = context.user_data[SELECT_PROD_ID]
    prod = get_product_by_id(prod_id)
    if chat_id == prod.owner_id:
        return context.bot.sendMessage(chat_id, "Вы не можете купить свой товар")
    update.callback_query.edit_message_text(f"   <b>Покупка товара</b>\n\n"
                                            f"Отправьте целое число - количество товара\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                       callback_data='back_to_select_product')]],
                                                resize_keyboard=True), parse_mode="HTML")
    return PRODUCT_COUNT


def buy_product_set_count(update, context):
    count = update.message.text
    if SELECT_PROD_ID not in context.user_data or CATEGORY_INFO not in context.user_data:
        return update.message.reply_text("Не актуально")
    try:
        count = int(count)
    except ValueError:
        update.message.reply_text(
            f"   <b>Покупка товара</b>\n\n"
            f"Отправьте <b>целое число</b> - количество товара\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_select_product')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return PRODUCT_COUNT
    if count < 1:
        update.message.reply_text(
            f"   <b>Покупка товара</b>\n\n"
            f"Неверное количество!\n\n"
            f"Отправьте <b>целое число</b> - количество товара\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_select_product')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return PRODUCT_COUNT
    product_id = context.user_data[SELECT_PROD_ID]
    product = get_product_by_id(product_id)
    if product.count < count:
        update.message.reply_text(
            f"   <b>Покупка товара</b>\n\n"
            f"У магазина нет столько выбранного товара!\n\n"
            f"Отправьте <b>целое число</b> - количество товара\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_select_product')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return PRODUCT_COUNT
    owner_id = product.owner_id
    ltc_price = get_ltc_by_rub(product.price)
    context.user_data[PRODUCT_SUM_PRICE] = product.price * count
    context.user_data[PRODUCT_LTC_SUM_PRICE] = get_ltc_by_rub(context.user_data[PRODUCT_SUM_PRICE])
    context.user_data[PRODUCT_COUNT] = count
    count_shop_requisites = len(get_shop_requisites_list(owner_id))
    guarantee = get_guarantee_shop(owner_id)
    if count_shop_requisites == 0 or guarantee < min_guarantee or get_guarantee_shop(owner_id) < context.user_data[
        PRODUCT_LTC_SUM_PRICE]:
        update.message.reply_text(f"⚠  <b>Внимание!</b>\n\n"
                                  f"❕ Вы подтверждаете, что согласны с условиями сервиса и ознакомились с условием объявления.\n\n"
                                  f"🛍 <b>Покупка товара</b>\n\n"
                                  f"<b>Название:</b>  {product.name}\n"
                                  f"<b>Стоимость (1 шт.):</b>  {product.price} ₽  ({ltc_price} LTC)\n"
                                  f"<b>Выбранное количество товара:</b>  {count} шт.\n"
                                  f"<b>Итоговая стоимость:</b>  {context.user_data[PRODUCT_SUM_PRICE]} ₽  ({context.user_data[PRODUCT_LTC_SUM_PRICE]} LTC)\n\n"
                                  f"🔐 <b>Выберите способ оплаты</b>\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton("Оплатить LITECOIN",
                                                             callback_data=f"payment_for_litecoin")],
                                       [InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_select_product')]],
                                      resize_keyboard=True), parse_mode="HTML")
    else:
        update.message.reply_text(f"⚠  <b>Внимание!</b>\n\n"
                                  f"❕ Вы подтверждаете, что согласны с условиями сервиса и ознакомились с условием объявления.\n\n"
                                  f"🛍 <b>Покупка товара</b>\n\n"
                                  f"<b>Название:</b>  {product.name}\n"
                                  f"<b>Стоимость (1 шт.):</b>  {product.price} ₽  ({ltc_price} LTC)\n"
                                  f"<b>Выбранное количество товара:</b>  {count} шт.\n"
                                  f"<b>Итоговая стоимость:</b>  {context.user_data[PRODUCT_SUM_PRICE]} ₽  ({context.user_data[PRODUCT_LTC_SUM_PRICE]} LTC)\n\n"
                                  f"🔐 <b>Выберите способ оплаты</b>\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton("Счет LITECOIN", callback_data=f"payment_for_litecoin"),
                                        InlineKeyboardButton("Реквизиты магазина",
                                                             callback_data=f"payment_shop_requisites_list")],
                                       [InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_select_product')]],
                                      resize_keyboard=True), parse_mode="HTML")
    return ConversationHandler.END


def button_deal_buyer_message(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    context.user_data[DEAL_ID] = query.data[19:]
    deal = get_deal_by_id(query.data[19:])
    if deal.status == 3:
        return update.callback_query.edit_message_text("🔔 Статус этой сделки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Мои сделки (товары)'</b>\n\n"
                                                       "И выберите эту сделку", parse_mode='HTML')
    if deal.call_moderator is False:
        send_button_text = f"Сообщение магазину"
    else:
        send_button_text = f"Сообщение в Диспут с магазином"
    context.bot.sendMessage(chat_id, f"   <b>{send_button_text}</b>\n\n"
                                     f"Отправьте ваше сообщение или изображение/скриншот\n",
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(f'{back_for_button}  В меню сделки',
                                                       callback_data='back_to_buyer_deal_menu')]]), parse_mode="HTML")
    return BUYER_MESSAGE


def deal_buyer_message_send(update, context):
    message = update.message.text
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.call_moderator is False:
        send_button_text = f"Сообщение магазину"
    else:
        send_button_text = f"Сообщение в диспут с магазином"

    send_message = f"*✉️ Сообщение от покупателя*\n\t\t\t\t\t{get_user_id(deal.buyer_id)}\n(сделка /d{deal.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n" \
                   f"➖➖➖\n\n" \
                   f"*{message}*\n\n" \
                   f"➖➖➖\n\n" \
                   f"_Будьте вежливы! Вы общаетесь с людьми {e_winking}_"
    if deal.status == 2:
        deal_messages = deal.messages
        if not deal_messages:
            deal_messages = [f"-\t\t<b>Покупатель:</b>  <i>{message}</i>"]
        else:
            deal_messages.append(f"-\t\t<b>Покупатель:</b>  <i>{message}</i>")
        deal.update(messages=deal_messages)
    context.bot.sendMessage(deal.shop_id,
                            send_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'📩  Написать покупателю',
                                                                                     callback_data=f'deal_shop_message_{deal.id}')]],
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    # get_deal_inf = get_deal_info(deal_id)
    update.message.reply_text(
        f"{send_button_text} <b>{get_shop_id(deal.shop_id)}</b> отправлено\n(сделка <b>/d{deal.id}</b>)\n\n",
        parse_mode='HTML')
    # context.bot.sendMessage(deal.buyer_id,
    #                        get_deal_inf,
    #                        reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
    #                                                          resize_keyboard=True),
    #                        parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END


def deal_buyer_photo_send(update, context):
    photo_id = update.message.photo[0].file_id
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    send_button_text = f"Изображение магазину"

    get_deal_inf = get_deal_info(deal_id)
    send_message = f"\n\n*✉️ Изображение от покупателя*\n\t\t\t\t\t{get_user_id(deal.buyer_id)}\n(сделка /d{deal.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n"

    context.bot.sendPhoto(deal.shop_id, photo_id)
    context.bot.sendMessage(deal.shop_id, send_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'📩  Написать покупателю',
                                                                                     callback_data=f'deal_shop_message_{deal.id}')]],
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    update.message.reply_text(
        f"<b>{send_button_text} {get_shop_id(deal.shop_id)} отправлено\n(сделка /d{deal.id})\n\n</b>",
        parse_mode='HTML')
    # context.bot.sendMessage(deal.buyer_id,
    #                        get_deal_inf,
    #                        reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
    #                                                          resize_keyboard=True),
    #                        parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END


def button_moder_select_shop_message(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(f"   <b>Сообщение магазину</b>\n\n"
                                            f"Отправьте ваше сообщение Магазину\n", reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton(f'{back_for_button}  В меню магазина',
                               callback_data='back_moder_select_shop_menu')]]), parse_mode="HTML")
    return MODER_MESSAGE


def moder_select_shop_message_send(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    chat_id = update.message.chat_id
    message = update.message.text
    shop_id = context.user_data[SELECT_ID]
    send_message = f"*✉️ Сообщение от пользователя*\n\t\t\t\t\t{get_user_id(chat_id)}\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n" \
                   f"➖➖➖\n\n" \
                   f"*{message}*\n\n" \
                   f"➖➖➖\n\n" \
                   f"_Будьте вежливы! Вы общаетесь с людьми {e_winking}_"
    context.bot.sendMessage(shop_id,
                            send_message,
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(f"Ответить", callback_data=f'shop_answer_message_{chat_id}')]],
                                resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(
        f"Сообщение магазину <b>{get_shop_name(shop_id)}  ({get_shop_id(shop_id)})</b> отправлено\n\n",
        parse_mode='HTML')
    return ConversationHandler.END


def button_user_select_shop_message(update, context):
    query = update.callback_query
    query.answer()
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    update.callback_query.edit_message_text(f"   <b>Сообщение магазину</b>\n\n"
                                            f"Отправьте ваше сообщение Магазину\n", reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton(f'{back_for_button}  В меню магазина',
                               callback_data='back_user_select_shop_menu')]]), parse_mode="HTML")
    return USER_MESSAGE


def user_select_shop_message_send(update, context):
    if SELECT_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    chat_id = update.message.chat_id
    message = update.message.text
    messages_limit = get_user_messages_limit(chat_id)
    date_set_limit = get_user_date_set_limit(chat_id)
    if messages_limit >= 10 and date_set_limit is not None:
        now = datetime.now()
        diff = now - date_set_limit
        hours = divmod(diff, timedelta(seconds=3600))[0]
        if hours < 2:
            return update.message.reply_text("<b>Пока что вы не можете отправлять сообщения!</b>",
                                             parse_mode='HTML')
        else:
            messages_limit = 0
            date_set_limit = None
            update_user_date_set_limit(chat_id, date_set_limit)
    messages_limit += 1
    if messages_limit == 10:
        date_set_limit = datetime.now()
        update_user_date_set_limit(chat_id, date_set_limit)
    update_user_massages_limit(chat_id, messages_limit)
    shop_id = context.user_data[SELECT_ID]

    send_message = f"*✉️ Сообщение от пользователя*\n\t\t\t\t\t{get_user_id(chat_id)}\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n" \
                   f"➖➖➖\n\n" \
                   f"*{message}*\n\n" \
                   f"➖➖➖\n\n" \
                   f"_Будьте вежливы! Вы общаетесь с людьми {e_winking}_"
    context.bot.sendMessage(shop_id,
                            send_message,
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(f"Ответить", callback_data=f'shop_answer_message_{chat_id}')]],
                                resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    update.message.reply_text(
        f"Сообщение магазину <b>{get_shop_name(shop_id)}  ({get_shop_id(shop_id)})</b> отправлено\n\n")
    return ConversationHandler.END


# -------- Отправка отзыва -----------

def button_deal_buyer_comment(update, context):
    query = update.callback_query
    query.answer()
    deal_id = query.data[25:]
    deal = get_deal_by_id(deal_id)
    context.user_data[DEAL_ID] = deal_id
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.comment is not None:
        return update.callback_query.edit_message_text("Вы уже оставляли отзыв об этой покупке")
    update.callback_query.edit_message_text(f"🗣  <b>Отзыв о магазине (товары)</b>\n\n"
                                            f"Если бы ваш отзыв ограничивался одной фразой, что бы вы сказали? ("
                                            f"напишите и отправьте)",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_buyer_deal_menu')]]),
                                            parse_mode="HTML")
    return BUYER_REVIEW


def deal_buyer_review_send(update, context):
    comment = update.message.text
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    if not deal:
        return update.callback_query.edit_message_text("Не актуально")
    if deal.comment is not None:
        return update.callback_query.edit_message_text("Вы уже оставляли отзыв об этой покупке")
    if len(comment) > 128:
        update.message.reply_text(f"🗣  <b>Отзыв о магазине</b>\n\n"
                                  f"Слишком длинный комментарий!"
                                  f"Если бы ваш комментарий ограничивался одной фразой, что бы вы сказали? ("
                                  f"напишите и отправьте)",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_buyer_deal_menu')]]),
                                  parse_mode="HTML")
        return BUYER_REVIEW
    elif len(comment) < 3:
        update.message.reply_text(f"🗣  <b>Отзыв о магазине</b>\n\n"
                                  f"Слишком короткий комментарий!"
                                  f"Если бы ваш комментарий ограничивался одной фразой, что бы вы сказали? ("
                                  f"напишите и отправьте)",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_buyer_deal_menu')]]),
                                  parse_mode="HTML")
        return BUYER_REVIEW
    deal.update(comment=comment)
    update.message.reply_text(
        f"🗣  Отзыв о Магазине <b>{get_shop_name(deal.shop_id)}   ({get_shop_id(deal.shop_id)})</b> оставлен\n\n",
        parse_mode='HTML')
    return ConversationHandler.END


# --------------------------------------------------


def button_deal_shop_send_message(update, context):
    query = update.callback_query
    query.answer()
    deal_id = query.data[18:]
    deal = get_deal_by_id(deal_id)
    if deal is None:
        return update.callback_query.edit_message_text("<b>Сделка не найдена</b>\n",
                                                       parse_mode='HTML')

    context.user_data[DEAL_ID] = deal_id
    if deal.call_moderator is False:
        send_button_text = f"Сообщение покупателю"
    else:
        send_button_text = f"Сообщение в диспут с покупателем"
    update.callback_query.edit_message_text(f"   <b>{send_button_text}</b>\n\n"
                                            f"Отправьте ваше сообщение или изображение/скриншот\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  В меню сделки',
                                                                       callback_data='back_to_shop_deal_menu')]]),
                                            parse_mode="HTML")
    return SHOP_SEND_MESSAGE


def deal_shop_message_send(update, context):
    message = update.message.text
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    if deal.status == 3:
        return update.callback_query.edit_message_text("🔔 Статус этой сделки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Мои сделки (товары)'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')
    if deal.call_moderator is False:
        send_button_text = f"Сообщение покупателю"
    else:
        send_button_text = f"Сообщение в диспут с покупателем"
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)

    send_message = f"*✉️ Сообщение от покупателя*\n\t\t\t\t\t{get_user_id(deal.buyer_id)}\n(сделка /d{deal.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n" \
                   f"➖➖➖\n\n" \
                   f"*{message}*\n\n" \
                   f"➖➖➖\n\n" \
                   f"_Будьте вежливы! Вы общаетесь с людьми {e_winking}_"

    if deal.status == 2:
        deal_messages = deal.messages
        if not deal_messages:
            deal_messages = [f"-\t\t<b>Магазин:</b>  <i>{message}</i>"]
        else:
            deal_messages.append(f"-\t\t<b>Магазин</b>:  <i>{message}</i>")
        deal.update(messages=deal_messages)
    context.bot.sendMessage(deal.buyer_id,
                            send_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩  Написать магазину",
                                                                                     callback_data=f"deal_buyer_message_{deal_id}")]],
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    update.message.reply_text(
        f"<b>{send_button_text} {get_user_id(deal.buyer_id)} отправлено\n(сделка /d{deal.id})\n\n</b>",
        parse_mode='HTML')
    # context.bot.sendMessage(deal.shop_id,
    #                        get_deal_inf,
    #                        reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(deal.status, deal, context),
    #                                                          resize_keyboard=True),
    #                        parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END


def deal_shop_photo_send(update, context):
    photo_id = update.message.photo[0].file_id
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    if deal.status == 3:
        return update.callback_query.edit_message_text("🔔 Статус этой сделки уже изменился!\n\nПосетите раздел:\n"
                                                       "\t\t\t\t<b>'Личный кабинет -> Мои покупки -> Мои сделки (товары)'</b>\n\n"
                                                       "И выберите эту покупку", parse_mode='HTML')
    send_button_text = f"Изображение покупателю"
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    get_deal_inf = get_deal_info(deal_id)

    send_message = f"\n\n*✉️ Изображение от магазина*\n\t\t\t\t\t{get_user_id(deal.shop_id)}\n(сделка /d{deal.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n"

    context.bot.sendPhoto(deal.buyer_id, photo_id)
    context.bot.sendMessage(deal.buyer_id, send_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩  Написать магазину",
                                                                                     callback_data=f"deal_buyer_message_{deal_id}")]],
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    update.message.reply_text(
        f"{send_button_text} <b>{get_user_name(deal.buyer_id)}\n({get_user_id(deal.buyer_id)})</b> отправлено\n\n",
        parse_mode='HTML')
    context.bot.sendMessage(deal.shop_id,
                            get_deal_inf,
                            reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(deal.status, deal, context),
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END


def button_shop_answer_message(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.data[20:]
    context.user_data[SELECT_ID] = user_id
    update.callback_query.edit_message_text(f"   <b>Ответ пользователю</b>\n\n"
                                            f"Отправьте ваше сообщение пользователю\n",
                                            parse_mode="HTML")
    return SHOP_ANSWER_MESSAGE


def shop_answer_message_send(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    user_id = context.user_data[SELECT_ID]
    send_message = f"*✉️ Ответ от магазина*\n\t\t\t\t\t{get_shop_name(chat_id)}  ({get_shop_id(chat_id)})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n" \
                   f"➖➖➖\n\n" \
                   f"*{message}*\n\n" \
                   f"➖➖➖\n\n" \
                   f"_Будьте вежливы! Вы общаетесь с людьми {e_winking}_"
    if check_moderator(user_id):
        context.bot.sendMessage(user_id,
                                send_message, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"📩  Написать сообщение",
                                       callback_data=f'moder_shop_send_message_{chat_id}')]]),
                                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.sendMessage(user_id,
                                send_message, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"📩  Написать сообщение",
                                       callback_data=f'user_shop_send_message_{chat_id}')]]),
                                parse_mode=telegram.ParseMode.MARKDOWN)

    update.message.reply_text(
        f"Ответ пользователю <b>{get_user_name(user_id)}\n({get_user_id(user_id)})</b> отправлен\n\n",
        parse_mode='HTML')
    return ConversationHandler.END


def button_deal_shop_give_change(update, context):
    query = update.callback_query
    query.answer()
    deal_id = query.data[17:]
    context.user_data[DEAL_ID] = deal_id
    deal = get_deal_by_id(deal_id)
    if deal.status != 2:
        return update.callback_query.edit_message_text("Статус этой сделки уже изменился! Посетите раздел:\n"
                                                       "\t\t\t\t<b>'Мой магазин' -> 'Продажи' -> 'Мои сделки (товары)'</b>\n"
                                                       "И выберите эту продажу", parse_mode='HTML')
    if deal.change_file_id is not None or deal.change_count is not None:
        return update.callback_query.edit_message_text("Вы уже делали замену товара по данной продаже!",
                                                       parse_mode='HTML')
    update.callback_query.edit_message_text(f"   <b>Выдача замены товара</b>\n\n"
                                            f"Отправьте количество товара для замены (целое число)\n\nВыдача осуществляется из "
                                            f"той же позиции товара\n\n"
                                            f"Если у вас нет нужного количества данного товара - пополните его в разделе <b>'Мой магазин' -> 'Мои товары'</b>",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                       callback_data='back_to_shop_deal_menu')]]),
                                            parse_mode="HTML")
    return DEAL_SHOP_CHANGE


def deal_shop_change_give(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    try:
        count = int(message)
    except ValueError:
        update.message.reply_text(
            f"   <b>Выдача замены товара</b>\n\n"
            f"Отправьте <b>целое число</b> - количество товара для замены\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_shop_deal_menu')]]),
            parse_mode="HTML")
        return DEAL_SHOP_CHANGE
    if count < 1:
        update.message.reply_text(
            f"   <b>Выдача замены товара</b>\n\n"
            f"Неверное значение!\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_shop_deal_menu')]]),
            parse_mode="HTML")
        return DEAL_SHOP_CHANGE
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    if deal.status == 3:
        return update.callback_query.edit_message_text("Статус этой сделки уже изменился! Посетите раздел:\n"
                                                       "\t\t\t\t<b>'Мой магазин' -> 'Продажи' -> 'Мои сделки (товары)'</b>\n"
                                                       "И выберите эту продажу", parse_mode='HTML')
    product = get_product_by_id(deal.product_id)
    if count > product.count:
        update.message.reply_text(
            f"   <b>Выдача замены товара</b>\n\n"
            f"У вас нет столько товара этой позиции\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_shop_deal_menu')]]),
            parse_mode="HTML")
        return DEAL_SHOP_CHANGE
    if count > deal.count:
        update.message.reply_text(
            f"   <b>Выдача замены товара</b>\n\n"
            f"Вы не можете заменить больше товара, чем было куплено\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                       callback_data='back_to_shop_deal_menu')]]),
            parse_mode="HTML")
        return DEAL_SHOP_CHANGE
    deal_info = get_deal_info(deal_id) + f"\n\n* замену товара в количестве [{count} шт.]*"
    context.bot.sendMessage(deal.buyer_id,
                            deal_info,
                            reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    deal_shop_give_change(deal, product, count, context, deal.buyer_id)
    update.message.reply_text(
        f"   <b>Выдача замены товара</b>\n\n"
        f"Замена выполнена в количестве <b>[{count} шт.]</b>\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                   callback_data='back_to_shop_deal_menu')]]),
        parse_mode="HTML")
    return ConversationHandler.END


def button_call_menu_send_message(update, context):
    query = update.callback_query
    query.answer()
    if DEAL_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    if SELECT_SALE_SECTION in context.user_data:
        menu = InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_moder_select_sale')]])
    elif SELECT_BUYS_SECTION in context.user_data:
        menu = InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_moder_user_select_buy')]])
    else:
        menu = InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_call_menu_messages')]])
    update.callback_query.edit_message_text(f"   <b>Сообщение в Диспут</b>\n\n"
                                            f"Ваше сообщение будет отправлено Покупателю и Магазину\n",
                                            reply_markup=menu,
                                            parse_mode="HTML")
    return CALL_MENU_SEND_MESSAGE


def call_menu_message_send(update, context):
    message = update.message.text
    deal_id = context.user_data[DEAL_ID]
    deal = get_deal_by_id(deal_id)
    deal_info = get_deal_info(deal_id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n_Сообщение от Модератора:_\n\t\t\t\t*{message}*"

    context.bot.sendMessage(deal.buyer_id,
                            deal_info,
                            reply_markup=InlineKeyboardMarkup(get_buyer_deal_menu(deal, deal.status, context),
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    context.bot.sendMessage(deal.shop_id,
                            deal_info,
                            reply_markup=InlineKeyboardMarkup(get_shop_deal_menu(deal.status, deal, context),
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(
        "<b>Ваше сообщение было отправлено!</b>", parse_mode='HTML')

    deal_messages = deal.messages
    if not deal_messages:
        deal_messages = [f"-\t\t<b>Модератор:</b>  <i>{message}</i>"]
    else:
        deal_messages.append(f"-\t\t<b>Модератор:</b>  <i>{message}</i>")
    deal.update(messages=deal_messages)
    menu = deepcopy(moder_select_call_menu_messages)
    if SELECT_SALE_SECTION in context.user_data:
        menu.pop(1)
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_select_sale')])
    deal = get_deal_by_id(deal_id)
    messages_text = get_deal_messages(deal)
    update.message.reply_text(
        f"   <b>Сообщения в Диспуте</b>\n\n"
        f"Покупатель:  <b>@{get_user_tg_id(deal.buyer_id)}</b>\n"
        f"Владелец магазина:  <b>@{get_user_tg_id(deal.shop_id)}</b>\n\n"
        f"{messages_text}",
        reply_markup=InlineKeyboardMarkup(menu,
                                          resize_keyboard=True),
        parse_mode='HTML')
    return ConversationHandler.END


# -------------------- Добавление услуги ----------------------
def my_shop_services_start_add(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    serv = Service.objects(owner_id=chat_id, category_id=context.user_data[CATEGORY_INFO]['cat_id']).first()
    if serv:
        update.callback_query.edit_message_text(
            f"   <b>Добавление услуги</b>\n\n"
            f"Вы можете добавить в каждую категорию только по одной услуге!\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                       callback_data='back_to_prev_serv_cat_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return
    update.callback_query.edit_message_text(
        f"   <b>Добавление услуги</b>\n\n"
        f"Выбранная категория:  {context.user_data[CATEGORY_INFO]['cat_path']}\n"
        f"Максимально точно указывайте все данные об услуге\n\n"
        f"Отправьте <b>Название услуги</b> <u>от 5 до 25 символов</u>\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_prev_serv_cat_menu')]],
            resize_keyboard=True),
        parse_mode='HTML')
    context.user_data[CAT_ID] = context.user_data[CATEGORY_INFO]['cat_id']
    return SET_SERVICE_NAME


def set_add_service_name(update, context):
    message = update.message.text
    if len(message) < 5:
        update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                                  f"Слишком короткое название!\n\n"
                                  f"Отправьте <b>Название услуги</b> <u>от 5 до 25 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_prev_serv_cat_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SERVICE_NAME
    if len(message) > 25:
        update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                                  f"Слишком длинное название!\n\n"
                                  f"Отправьте <b>Название услуги</b> <u>от 5 до 25 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_prev_serv_cat_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SERVICE_NAME
    context.user_data[SET_SERVICE_NAME] = message
    update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                              f"Отправьте <b>описание услуги</b> <u>от 150 до 500 символов</u>\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                         callback_data='back_to_prev_serv_cat_menu')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return SET_SERVICE_DESCRIPTION


def set_add_service_description(update, context):
    message = update.message.text
    if len(message) < 150:
        update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                                  f"Слишком короткое описание!\n\n"
                                  f"Отправьте <b>описание услуги</b> <u>от 150 до 500 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_prev_serv_cat_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SERVICE_DESCRIPTION
    if len(message) > 500:
        update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                                  f"Слишком длинное описание!\n\n"
                                  f"Отправьте <b>описание услуги</b> <u>от 150 до 500 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_prev_serv_cat_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SERVICE_DESCRIPTION
    context.user_data[SET_SERVICE_DESCRIPTION] = message
    update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                              f"Отправьте <b>ваше портфолио</b> <u>файл в формате pdf/word</u> (Необязательно)\n\n"
                              f"Чтобы пропустить отправьте \"-\" (минус)",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                         callback_data='back_to_prev_serv_cat_menu')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return SET_SERVICE_PORTFOLIO


def set_add_service_portfolio(update, context):
    file_id = update.message.document.file_id
    context.user_data[SET_SERVICE_PORTFOLIO] = file_id
    update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                              f"Отправьте <b>минимальную стоимость заказа</b> <u>целое число - в рублях (от 10 до 100000)</u>\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                         callback_data='back_to_prev_serv_cat_menu')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return SET_SERVICE_MIN_PRICE


def set_add_service_portfolio_skip(update, context):
    text = update.message.text
    if text == '-':
        context.user_data[SET_SERVICE_PORTFOLIO] = None
        update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                                  f"Отправьте <b>минимальную стоимость заказа</b> <u>целое число - в рублях (от 10 до 100000)</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_prev_serv_cat_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SERVICE_MIN_PRICE


def set_add_service_min_price(update, context):
    chat_id = update.message.chat_id
    price = update.message.text
    try:
        price = int(price)
    except ValueError:
        update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                                  f"Отправьте <b>минимальную стоимость заказа</b> <u>целое число - в рублях (от 10 до 100000)</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_prev_serv_cat_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SERVICE_MIN_PRICE
    if price < 10 or price > 100000:
        update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                                  f"Отправьте <b>минимальную стоимость заказа</b> <u>целое число - в рублях (от 10 до 100000)</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_prev_serv_cat_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_SERVICE_MIN_PRICE
    context.user_data[SET_SERVICE_MIN_PRICE] = price
    update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                              f"Отправьте <b>изображение-визитку</b> <u>png/jpg</u>\n\n"
                              f"Оно должно презентовать вашу услугу\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                         callback_data='back_to_prev_serv_cat_menu')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return SET_SERVICE_PICTURE


def set_add_service_picture(update, context):
    context.user_data[SET_SERVICE_PICTURE] = update.message.photo[0].file_id
    category_id = context.user_data[CAT_ID]
    owner_id = update.message.chat_id
    service = add_shop_service(category_id, owner_id, context.user_data[SET_SERVICE_NAME],
                               context.user_data[SET_SERVICE_DESCRIPTION],
                               context.user_data[SET_SERVICE_PORTFOLIO],
                               context.user_data[SET_SERVICE_MIN_PRICE],
                               context.user_data[SET_SERVICE_PICTURE])
    context.user_data[SELECT_SERV_ID] = service.id
    update.message.reply_text(f"   <b>Добавление услуги</b>\n\n"
                              f"<b>Услуга успешно добавлена!</b>\n\n"
                              f"Также вы можете добавить пакеты к своей услуги (Эконом, Стандарт, Бизнес)\n\n"
                              f"При добавлении пакета вы должны указать:\n"
                              f"1) Что входит в выбранный пакет\n"
                              f"2) Стоимость выбранного пакета\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  get_my_service_packets_menu(update, context, owner_id, "add_service"),
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def my_shop_add_service_eco_packet(update, context):
    context.user_data[DATA] = "add_eco"
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Добавление пакета 'Эконом'</b>\n\n"
        f"Отправьте <b>стоимость пакета 'Эконом'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_PACKET_PRICE


def my_shop_add_service_standart_packet(update, context):
    context.user_data[DATA] = "add_standart"
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
        f"Отправьте <b>стоимость пакета 'Стандарт'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_PACKET_PRICE


def my_shop_add_service_biz_packet(update, context):
    context.user_data[DATA] = "add_biz"
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
        f"Отправьте <b>стоимость пакета 'Бизнес'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return SET_PACKET_PRICE


def my_shop_edit_service_packet_price(update, context):
    if DATA not in context.user_data or SELECT_SERV_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    if context.user_data[DATA] == 'edit_eco':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
            f"Отправьте <b>стоимость пакета 'Эконом'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == 'edit_standart':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
            f"Отправьте <b>стоимость пакета 'Стандарт'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == 'edit_biz':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
            f"Отправьте <b>стоимость пакета 'Бизнес'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    return SET_PACKET_PRICE


def my_shop_edit_service_packet_description(update, context):
    if DATA not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    if context.user_data[DATA] == 'edit_eco':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
            f"Отправьте <b>описание и содержимое пакета 'Эконом'</b> <u>от 150 до 500 символов</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == 'edit_standart':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
            f"Отправьте <b>описание и содержимое пакета 'Стандарт'</b> <u>от 150 до 500 символов</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == 'edit_biz':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
            f"Отправьте <b>описание и содержимое пакета 'Бизнес'</b> <u>от 150 до 500 символов</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    return SET_PACKET_DESCRIPTION


def my_shop_edit_service_packet_deadline(update, context):
    if DATA not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    if context.user_data[DATA] == 'edit_eco':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
            f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == 'edit_standart':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
            f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    elif context.user_data[DATA] == 'edit_biz':
        update.callback_query.edit_message_text(
            f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
            f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_my_service_packets_menu')]],
                resize_keyboard=True),
            parse_mode='HTML')
    return SET_PACKET_DEADLINE


def set_packet_price(update, context):
    if DATA not in context.user_data:
        return update.message.reply_text("Не актуально")
    chat_id = update.message.chat_id
    price = update.message.text
    if context.user_data[DATA] == "add_eco":
        try:
            price = int(price)
        except ValueError:
            update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Эконом'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if price < 10 or price > 100000:
            update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Эконом'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        context.user_data[SET_PACKET_PRICE] = price
        update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                  f"Отправьте <b>описание и содержимое пакета 'Эконом'</b> <u>от 150 до 500 символов</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_PACKET_DESCRIPTION
    elif context.user_data[DATA] == "add_standart":
        try:
            price = int(price)
        except ValueError:
            update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Стандарт'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if price < 10 or price > 100000:
            update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Стандарт'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        context.user_data[SET_PACKET_PRICE] = price
        update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                  f"Отправьте <b>описание и содержимое пакета 'Стандарт'</b> <u>от 150 до 500 символов</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_PACKET_DESCRIPTION
    elif context.user_data[DATA] == "add_biz":
        try:
            price = int(price)
        except ValueError:
            update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Бизнес'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if price < 10 or price > 100000:
            update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Бизнес'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        context.user_data[SET_PACKET_PRICE] = price
        update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                  f"Отправьте <b>описание и содержимое пакета 'Бизнес'</b> <u>от 150 до 500 символов</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_PACKET_DESCRIPTION
    elif context.user_data[DATA] == "edit_eco":
        try:
            price = int(price)
        except ValueError:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Эконом'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_eco')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if price < 10 or price > 100000:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Эконом'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_eco')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if SELECT_SERV_ID not in context.user_data:
            return update.message.reply_text("Не актуально")
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(eco_price=price)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                  f"<b>Стоимость пакета 'Эконом'</b> <u>успешно изменена</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_eco')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END
    elif context.user_data[DATA] == "edit_standart":
        try:
            price = int(price)
        except ValueError:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Стандарт'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_standart')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if price < 10 or price > 100000:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Стандарт'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_standart')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if SELECT_SERV_ID not in context.user_data:
            return update.message.reply_text("Не актуально")
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(standart_price=price)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                  f"<b>Стоимость пакета 'Стандарт'</b> <u>успешно изменена</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_standart')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END
    elif context.user_data[DATA] == "edit_biz":
        try:
            price = int(price)
        except ValueError:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Бизнес'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_biz')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if price < 10 or price > 100000:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>стоимость пакета 'Бизнес'</b> <u>целое число - в рублях (от 10 до 100000)</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_biz')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if SELECT_SERV_ID not in context.user_data:
            return update.message.reply_text("Не актуально")
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(biz_price=price)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                  f"<b>Стоимость пакета 'Бизнес'</b> <u>успешно изменена</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_biz')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END
    context.user_data[CATEGORY_INFO]['cat_id'] = context.user_data[CATEGORY_INFO]['cat_id']
    context.user_data[CATEGORY_INFO]['cat_path'] = context.user_data[CATEGORY_INFO]['cat_path']


def set_packet_description(update, context):
    message = update.message.text
    if context.user_data[DATA] == "add_eco":
        if len(message) < 150:
            update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                      f"Cлишком короткое описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Эконом'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        if len(message) > 500:
            update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                      f"Cлишком длинное описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Эконом'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        context.user_data[SET_PACKET_DESCRIPTION] = message
        update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                  f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_PACKET_DEADLINE
    elif context.user_data[DATA] == "add_standart":
        if len(message) < 150:
            update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                      f"Cлишком короткое описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Стандарт'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        if len(message) > 500:
            update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                      f"Cлишком длинное описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Стандарт'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        context.user_data[SET_PACKET_DESCRIPTION] = message
        update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                  f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_PACKET_DEADLINE
    elif context.user_data[DATA] == "add_biz":
        if len(message) < 150:
            update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                      f"Cлишком короткое описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Бизнес'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        if len(message) > 500:
            update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                      f"Cлишком длинное описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Бизнес'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        context.user_data[SET_PACKET_DESCRIPTION] = message
        update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                  f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return SET_PACKET_DEADLINE
    elif context.user_data[DATA] == "edit_eco":
        if len(message) < 150:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                      f"Cлишком короткое описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Эконом'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_eco')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        if len(message) > 500:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                      f"Cлишком длинное описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Эконом'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_eco')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(eco_description=message)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                  f"Описание пакета успешно изменено!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_eco')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    elif context.user_data[DATA] == "edit_standart":
        if len(message) < 150:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                      f"Cлишком короткое описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Стандарт'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_standart')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        if len(message) > 500:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                      f"Cлишком длинное описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Стандарт'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_standart')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(standart_description=message)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                  f"Описание пакета успешно изменено!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_standart')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    elif context.user_data[DATA] == "edit_biz":
        if len(message) < 150:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                      f"Cлишком короткое описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Бизнес'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_biz')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        if len(message) > 500:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                      f"Cлишком длинное описание пакета\n\n"
                                      f"Отправьте <b>описание и содержимое пакета 'Бизнес'</b> <u>от 150 до 500 символов</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_service_edit_packet_biz')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DESCRIPTION
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(biz_description=message)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                  f"Описание пакета успешно изменено!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_biz')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    return ConversationHandler.END


def set_packet_deadline(update, context):
    if DATA not in context.user_data:
        return update.message.reply_text("Не актуально")
    chat_id = update.message.chat_id
    deadline = update.message.text
    if context.user_data[DATA] == "add_eco":
        try:
            deadline = int(deadline)
        except ValueError:
            update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DEADLINE
        if deadline < 1 or deadline > 30:
            update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DEADLINE
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(eco_price=context.user_data[SET_PACKET_PRICE],
                       eco_description=context.user_data[SET_PACKET_DESCRIPTION], eco_deadline=deadline)
        update.message.reply_text(f"   <b>Добавление пакета 'Эконом'</b>\n\n"
                                  f"Пакет успешно добавлен!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END
    elif context.user_data[DATA] == "add_standart":
        try:
            deadline = int(deadline)
        except ValueError:
            update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DEADLINE
        if deadline < 1 or deadline > 30:
            update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_DEADLINE
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(standart_price=context.user_data[SET_PACKET_PRICE],
                       standart_description=context.user_data[SET_PACKET_DESCRIPTION], standart_deadline=deadline)
        update.message.reply_text(f"   <b>Добавление пакета 'Стандарт'</b>\n\n"
                                  f"Пакет успешно добавлен!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END
    elif context.user_data[DATA] == "add_biz":
        try:
            deadline = int(deadline)
        except ValueError:
            update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if deadline < 1 or deadline > 30:
            update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(biz_price=context.user_data[SET_PACKET_PRICE],
                       biz_description=context.user_data[SET_PACKET_DESCRIPTION], biz_deadline=deadline)
        update.message.reply_text(f"   <b>Добавление пакета 'Бизнес'</b>\n\n"
                                  f"Пакет успешно добавлен!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_my_service_packets_menu')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return ConversationHandler.END
    elif context.user_data[DATA] == "edit_eco":
        try:
            deadline = int(deadline)
        except ValueError:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if deadline < 1 or deadline > 30:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(eco_deadline=deadline)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Эконом'</b>\n\n"
                                  f"Срок выполнения для пакета успешно изменен!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_eco')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    elif context.user_data[DATA] == "edit_standart":
        try:
            deadline = int(deadline)
        except ValueError:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if deadline < 1 or deadline > 30:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(standart_deadline=deadline)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Стандарт'</b>\n\n"
                                  f"Срок выполнения для пакета успешно изменен!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_eco')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    elif context.user_data[DATA] == "edit_biz":
        try:
            deadline = int(deadline)
        except ValueError:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        if deadline < 1 or deadline > 30:
            update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                      f"Отправьте <b>срок выполнения услуги для пакета</b> <u>целое число от 1 до 30</u>",
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                 callback_data='back_to_my_service_packets_menu')]],
                                          resize_keyboard=True),
                                      parse_mode='HTML')
            return SET_PACKET_PRICE
        service_id = context.user_data[SELECT_SERV_ID]
        service = get_service_by_id(service_id)
        service.update(biz_deadline=deadline)
        update.message.reply_text(f"{e_pencil}  <b>Редактирование пакета 'Бизнес'</b>\n\n"
                                  f"Срок выполнения для пакета успешно изменен!\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                             callback_data='back_to_service_edit_packet_eco')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
    return ConversationHandler.END


# ===================== ИЗМЕНЕНИЕ УСЛУГИ ===========================
def button_my_shop_service_menu_edit_name(update, context):
    if SELECT_SERV_ID not in context.user_data:
        return update.message.reply_text("Не актуально")
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(
        f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
        f"Отправьте новое <b>Название услуги</b> <u>от 5 до 25 символов</u>\n\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_select_service_menu_edit')]],
            resize_keyboard=True),
        parse_mode='HTML')
    return CHANGE_SERVICE_NAME


def service_name_change(update, context):
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage("Не актуально")
    chat_id = update.message.chat_id
    message = update.message.text
    if len(message) < 5:
        update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                  f"Слишком короткое название!\n\n"
                                  f"Отправьте новое <b>Название услуги</b> <u>от 5 до 25 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_select_service_menu_edit')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return CHANGE_SERVICE_NAME
    if len(message) > 25:
        update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                  f"Слишком длинное название!\n\n"
                                  f"Отправьте новое <b>Название услуги</b> <u>от 5 до 25 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_select_service_menu_edit')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return CHANGE_SERVICE_NAME
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    service.update(name=message)
    update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                              f"Название услуги успешно отредактировано\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_select_service_menu_edit')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def button_service_change_description(update, context):
    if SELECT_SERV_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                            f"Отправьте новое <b>описание услуги</b> <u>от 150 до 500 символов</u>\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_select_service_menu_edit')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return CHANGE_SERVICE_DESCRIPTION


def service_description_change(update, context):
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage("Не актуально")
    chat_id = update.message.chat_id
    message = update.message.text
    if len(message) < 150:
        update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                  f"Слишком короткое описание!\n\n"
                                  f"Отправьте новое <b>описание услуги</b> <u>от 150 до 500 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_select_service_menu_edit')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return CHANGE_SERVICE_DESCRIPTION
    if len(message) > 500:
        update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                  f"Слишком длинное описание!\n\n"
                                  f"Отправьте новое <b>описание услуги</b> <u>от 150 до 500 символов</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_select_service_menu_edit')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return CHANGE_SERVICE_DESCRIPTION
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    service.update(description=message)
    update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                              f"Описание услуги успешно изменено!\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_select_service_menu_edit')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def button_service_change_min_price(update, context):
    if SELECT_SERV_ID not in context.user_data:
        return update.message.reply_text("Не актуально")
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                            f"Отправьте <b>минимальную стоимость заказа</b> <u>целое число - в рублях (от 10 до 100000)</u>\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_select_service_menu_edit')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return CHANGE_SERVICE_MIN_PRICE


def service_min_price_change(update, context):
    if SELECT_SERV_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    price = update.message.text
    try:
        price = int(price)
    except ValueError:
        update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                  f"Отправьте <b>минимальную стоимость заказа</b> <u>целое число - в рублях (от 10 до 100000)</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_select_service_menu_edit')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return CHANGE_SERVICE_MIN_PRICE
    if price < 10 or price > 100000:
        update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                  f"Отправьте <b>минимальную стоимость заказа</b> <u>целое число - в рублях (от 10 до 100000)</u>\n\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_select_service_menu_edit')]],
                                      resize_keyboard=True),
                                  parse_mode='HTML')
        return CHANGE_SERVICE_MIN_PRICE
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    service.update(min_price=price)
    update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                              f"Минимальная стоимость заказа успешно изменена\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_select_service_menu_edit')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def button_service_change_portfolio(update, context):
    if SELECT_SERV_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                            f"Отправьте <b>ваше новое портфолио</b> <u>файл в формате pdf/word</u>\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_select_service_menu_edit')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return CHANGE_SERVICE_PORTFOLIO


def service_portfolio_change(update, context):
    if SELECT_SERV_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    file_id = update.message.document.file_id
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    service.update(portfolio=file_id)
    update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                              f"Портфолио успешно изменено\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_select_service_menu_edit')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def button_service_change_picture(update, context):
    if SELECT_SERV_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                                            f"Отправьте <b>изображение-визитку</b> <u>png/jpg</u>\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_select_service_menu_edit')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return CHANGE_SERVICE_PICTURE


def service_picture_change(update, context):
    if SELECT_SERV_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    photo_id = update.message.photo[0].file_id
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    service.update(picture=photo_id)
    update.message.reply_text(f"{e_pencil}  <b>Редактирование услуги</b>\n\n"
                              f"Изображение-визитка успешно изменена\n\n",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                         callback_data='back_to_select_service_menu_edit')]],
                                  resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def service_tz_send_text(update, context):
    if SELECT_SERV_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    chat_id = update.message.chat_id
    service = get_service_by_id(context.user_data[SELECT_SERV_ID])
    tz_text = update.message.text

    if context.user_data[SELECT_SERV_PACKET] == 1:
        price = service.eco_price
        ltc_price = get_ltc_by_rub(price)
        deadline_days = service.eco_deadline
    elif context.user_data[SELECT_SERV_PACKET] == 2:
        price = service.standart_price
        ltc_price = get_ltc_by_rub(price)
        deadline_days = service.standart_deadline
    elif context.user_data[SELECT_SERV_PACKET] == 3:
        price = service.biz_price
        ltc_price = get_ltc_by_rub(price)
        deadline_days = service.biz_deadline
    else:
        price = None
        ltc_price = None
        deadline_days = None

    if context.user_data[SELECT_SERV_PACKET] < 4:
        if get_user_balance(chat_id) < ltc_price:
            context.bot.sendMessage(chat_id, "У вас недостаточно средств для заказа!")
            return ConversationHandler.END
        add_user_balance(chat_id, -ltc_price)
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ успешно создан и оплачен\nОжидайте подтверждения заказа Исполнителем</i>"
    else:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ успешно создан\nОжидайте уточнение информации Исполнителем</i>"

    order = add_order(service.owner_id, chat_id, service.id, context.user_data[CATEGORY_INFO]['cat_path'], price,
                      ltc_price,
                      tz_text, context.user_data[SELECT_SERV_PACKET], 0, deadline_days)

    update.message.reply_text(
        f"{get_order_info(order.id)}{text_info}",
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                          resize_keyboard=True),
        parse_mode='HTML')

    if context.user_data[SELECT_SERV_PACKET] < 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>К вам поступил новый заказ и был оплачен заказчиком!\n\nОзнакомьтесь с техническим заданием, " \
                    "подтвердите заказ и приступайте к выполнению!\n\n" \
                    "Для уточнения деталей можете общаться с заказчиком (только внутри бота!)</i>"
    else:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>К вам поступил новый заказ!\n\nОзнакомьтесь с техническим заданием, оцените заказ: " \
                    "уточните стоимость, сроки выполнения, а после подтвердите заказ!\n\n" \
                    "Для уточнения деталей можете общаться с заказчиком (только внутри бота!)</i>"
    context.bot.sendMessage(order.shop_id,
                            f"<b>Заказ на выполнение услуги</b>\n\n{get_order_info(order.id)}{text_info}",
                            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    return ConversationHandler.END


def service_tz_send(update, context):
    if SELECT_SERV_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    chat_id = update.message.chat_id
    service = get_service_by_id(context.user_data[SELECT_SERV_ID])
    file_id = update.message.document.file_id
    context.user_data[CLIENT_SEND_TZ] = file_id

    if context.user_data[SELECT_SERV_PACKET] == 1:
        price = service.eco_price
        ltc_price = get_ltc_by_rub(price)
        deadline_days = service.eco_deadline
    elif context.user_data[SELECT_SERV_PACKET] == 2:
        price = service.standart_price
        ltc_price = get_ltc_by_rub(price)
        deadline_days = service.standart_deadline
    elif context.user_data[SELECT_SERV_PACKET] == 3:
        price = service.biz_price
        ltc_price = get_ltc_by_rub(price)
        deadline_days = service.biz_deadline
    else:
        price = None
        ltc_price = None
        deadline_days = None

    if context.user_data[SELECT_SERV_PACKET] < 4:
        if get_user_balance(chat_id) < ltc_price:
            context.bot.sendMessage(chat_id, "У вас недостаточно средств для заказа!")
            return ConversationHandler.END
        add_user_balance(chat_id, -ltc_price)
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ успешно создан и оплачен\nОжидайте подтверждения заказа Исполнителем</i>"
    else:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Заказ успешно создан\nОжидайте уточнение информации Исполнителем</i>"

    order = add_order(service.owner_id, chat_id, service.id, context.user_data[CATEGORY_INFO]['cat_path'], price,
                      ltc_price,
                      file_id, context.user_data[SELECT_SERV_PACKET], 0, deadline_days)

    update.message.reply_text(
        f"{get_order_info(order.id)}{text_info}",
        reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                          resize_keyboard=True),
        parse_mode='HTML')

    if context.user_data[SELECT_SERV_PACKET] < 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>К вам поступил новый заказ и был оплачен заказчиком!\n\nОзнакомьтесь с техническим заданием, " \
                    "подтвердите заказ и приступайте к выполнению!\n\n" \
                    "Для уточнения деталей можете общаться с заказчиком (только внутри бота!)</i>"
    else:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>К вам поступил новый заказ!\n\nОзнакомьтесь с техническим заданием, оцените заказ: " \
                    "уточните стоимость, сроки выполнения, а после подтвердите заказ!\n\n" \
                    "Для уточнения деталей можете общаться с заказчиком (только внутри бота!)</i>"
    context.bot.sendMessage(order.shop_id,
                            f"<b>Заказ на выполнение услуги</b>\n\n{get_order_info(order.id)}{text_info}",
                            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    return ConversationHandler.END


def button_order_client_message(update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data[21:]
    context.user_data[ORDER_ID] = order_id
    order = get_order_by_id(order_id)
    if order is None:
        return update.callback_query.edit_message_text("Не актуально")
    if order.status == 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if order.call_moderator is True:
        head_text = "Сообщение в Диспут с Исполнителем"
    else:
        head_text = "Сообщение Исполнителю"
    update.callback_query.edit_message_text(f"   <b>{head_text}</b>\n\n"
                                            f"Отправьте ваше сообщение или изображение/скриншот\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  В меню заказа',
                                                                       callback_data='back_to_client_order_menu')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return CLIENT_MESSAGE


def order_client_message_send(update, context):
    message = update.message.text
    if ORDER_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    if order is None:
        return update.message.reply_text(
            f"   <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')

    send_message = f"*✉️ Сообщение от заказчика*\n\t\t\t\t\t{get_user_id(order.client_id)}\n(заказ /o{order.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n" \
                   f"➖➖➖\n\n" \
                   f"*{message}*\n\n" \
                   f"➖➖➖\n\n" \
                   f"_Будьте вежливы! Вы общаетесь с людьми {e_winking}_"

    context.bot.sendMessage(order.shop_id, send_message,
                            reply_markup=InlineKeyboardMarkup([[
                                InlineKeyboardButton(f"📩  Написать заказчику",
                                                     callback_data=f'order_shop_message_{order_id}')]],
                                resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    if order.status == 3:
        order_messages = order.messages
        if not order_messages:
            order_messages = [f"-\t\t<b>Заказчик:</b>  <i>{message}</i>"]
        else:
            order_messages.append(f"-\t\t<b>Заказчик:</b>  <i>{message}</i>")
        order.update(messages=order_messages)

    if order.call_moderator is True:
        send_button_text = f"Сообщение в диспут с Исполнителем"
    else:
        send_button_text = f"Сообщение Исполнителю"
    update.message.reply_text(
        f"{send_button_text} <b>{get_shop_id(order.shop_id)}</b> отправлено\n(заказ <b>/o{order.id}</b>)",
        parse_mode='HTML')

    return ConversationHandler.END


def order_client_photo_send(update, context):
    photo_id = update.message.photo[0].file_id
    if ORDER_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    if order is None:
        return update.message.reply_text(
            f"   <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status == 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')

    send_message = f"\n\n*✉️ Изображение от заказчика*\n\t\t\t\t\t{get_user_id(order.client_id)}\n(заказ /o{order.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n"

    context.bot.sendPhoto(order.shop_id, photo_id)
    context.bot.sendMessage(order.shop_id, send_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"📩  Написать заказчику",
                                                                                     callback_data=f'order_shop_message_{order_id}')]],
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    update.message.reply_text(
        f"Изображение исполнителю <b>{get_shop_id(order.shop_id)}</b> отправлено\n(заказ <b>/o{order.id}</b>)",
        parse_mode='HTML')
    return ConversationHandler.END


def button_order_shop_message(update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data[19:]
    context.user_data[ORDER_ID] = order_id
    order = get_order_by_id(order_id)
    if order.call_moderator is True:
        head_text = "Сообщение в диспут с Заказчиком"
    else:
        head_text = "Сообщение Заказчику"
    update.callback_query.edit_message_text(f"   <b>{head_text}</b>\n\n"
                                            f"Отправьте ваше сообщение или изображение/скриншот\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  В меню заказа',
                                                                       callback_data='back_to_shop_order_menu')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return SHOP_ORDER_MESSAGE


def order_shop_message_send(update, context):
    message = update.message.text
    if ORDER_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    if order is None:
        return update.message.reply_text(
            f"   <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status == 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    if order.call_moderator is True:
        send_button_text = f"Сообщение в диспут с Заказчиком"
    else:
        send_button_text = f"Сообщение Заказчику"
    update.message.reply_text(
        f"{send_button_text} <b>{get_user_id(order.client_id)}</b> отправлено\n(заказ <b>/o{order.id}</b>)",
        parse_mode='HTML')

    # update.message.reply_text(f"{get_order_info(order_id)}{text_info}",
    #                          reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
    #                                                            resize_keyboard=True),
    #                          parse_mode='HTML')

    send_message = f"*✉️ Сообщение от исполнителя*\n\t\t\t\t\t{get_shop_id(order.shop_id)}\n(заказ /o{order.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n" \
                   f"➖➖➖\n\n" \
                   f"*{message}*\n\n" \
                   f"➖➖➖\n\n" \
                   f"_Будьте вежливы! Вы общаетесь с людьми {e_winking}_"
    if order.status == 3:
        order_messages = order.messages
        if not order_messages:
            order_messages = [f"-\t\t<b>Исполнитель:</b>  <i>{message}</i>"]
        else:
            order_messages.append(f"-\t\t<b>Исполнитель:</b>  <i>{message}</i>")
        order.update(messages=order_messages)
    context.bot.sendMessage(order.client_id, send_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"📩  Написать исполнителю",
                                                                                     callback_data=f'order_client_message_{order_id}')]],
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END


def order_shop_photo_send(update, context):
    photo_id = update.message.photo[0].file_id
    if ORDER_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    if order is None:
        return update.message.reply_text(
            f"   <b>Информация о заказе</b>\n\n"
            f"Заказ не найден",
            parse_mode='HTML')
    if order.status == 4:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')

    send_message = f"\n\n*✉️ Изображение от исполнителя*\n\t\t\t\t\t{get_user_id(order.client_id)}\n(заказ /o{order.id})\n\n" \
                   f"⚠️ Это личная переписка, сервис не имеет отношения к содержимому!\n\n"

    context.bot.sendPhoto(order.shop_id, photo_id)
    context.bot.sendMessage(order.shop_id, send_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"📩  Написать исполнителю",
                                                                                     callback_data=f'order_client_message_{order_id}')]],
                                                              resize_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    update.message.reply_text(
        f"Изображение заказчику <b>{get_shop_id(order.client_id)}</b> отправлено\n(заказ <b>/o{order.id}</b>)",
        parse_mode='HTML')
    return ConversationHandler.END


def button_order_shop_send_order_work(update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data[27:]
    context.user_data[ORDER_ID] = order_id
    order = get_order_by_id(order_id)
    if order.status != 2 and order.status != 3:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    update.callback_query.edit_message_text(f"   <b>Отправка выполненного заказа</b>\n\n"
                                            f"Отправьте одним файлом все материалы выполненного заказа (архив .rar, "
                                            f".zip, документ word, pdf и т.д.)\n\n",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_shop_order_menu')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return SHOP_ORDER_WORK


def order_shop_send_work(update, context):
    if update.message.document is None:
        update.message.reply_text("Неверный формат файла, попробуйте ещё раз", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                   callback_data='back_to_shop_order_menu')]],
            resize_keyboard=True),
                                  parse_mode='HTML')
        return SHOP_ORDER_WORK
    file_id = update.message.document.file_id
    if ORDER_ID not in context.user_data:
        update.message.reply_text("Не актуально")
        return ConversationHandler.END
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    order.update(order_work=file_id)
    text_info = f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Файл отправлен Заказчику, ожидайте пока он проверит работу\n\n" \
                f"Вносите правки, исправляйте замечания, пока Заказчик не завершит данный заказ\n" \
                f"Чтобы заменить отправленный файл, воспользуйтесь тем же пунктом меню!</i>"
    update.message.reply_text(f"{get_order_info(order_id)}{text_info}",
                              reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                                                resize_keyboard=True),
                              parse_mode='HTML')

    text_info = f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Исполнитель отправил файл с выполненным заказом</i>\n\n" \
                f"1. Скачайте его, проверьте на вирусы (на всякий случай)\n" \
                f"2. Проверьте качество выполнения работы, если всё впорядке - <b>Завершите заказ</b>\n" \
                f"3. Если есть правки - договоритесь с Исполнителем - <b>Написать исполнителю</b>\n" \
                f"4. Если возникли проблемы - вы можете открыть <b>Диспут с Исполнителем</b>\n" \
                f"5. Если проблему решить не удастся в течение часа после открытия Диспута - <b>Вызвать модератора</b>"
    context.bot.sendMessage(order.client_id, f"{get_order_info(order_id)}{text_info}",
                            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order.id, order.status, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    context.bot.sendDocument(order.client_id, file_id, caption="Выполненный заказ")
    return ConversationHandler.END


# ------------------ Отзыв услуга -----------------
def button_order_client(update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data[27:]
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    if not order:
        return update.callback_query.edit_message_text("Не актуально")
    if order.comment is not None:
        return update.callback_query.edit_message_text("Вы уже оставляли отзыв об этой покупке")
    update.callback_query.edit_message_text(f"🗣  <b>Отзыв о магазине (услуги)</b>\n\n"
                                            f"Если бы ваш отзыв ограничивался одной фразой, что бы вы сказали? ("
                                            f"напишите и отправьте)",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_client_order_menu')]]),
                                            parse_mode="HTML")
    return CLIENT_ORDER_COMMENT


def order_review_client(update, context):
    comment = update.message.text
    if ORDER_ID not in context.user_data:
        return update.message.reply_text("Не актуально")
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    if not order:
        return update.message.reply_text("Не актуально")
    if order.comment is not None:
        return update.message.reply_text("Вы уже оставляли отзыв об этой покупке")
    if len(comment) > 128:
        update.message.reply_text(f"🗣  <b>Отзыв о магазине</b>\n\n"
                                  f"Слишком длинный комментарий!"
                                  f"Если бы ваш комментарий ограничивался одной фразой, что бы вы сказали? ("
                                  f"напишите и отправьте)",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_client_order_menu')]]),
                                  parse_mode="HTML")
        return CLIENT_ORDER_COMMENT
    elif len(comment) < 3:
        update.message.reply_text(f"🗣  <b>Отзыв о магазине</b>\n\n"
                                  f"Слишком короткий комментарий!"
                                  f"Если бы ваш комментарий ограничивался одной фразой, что бы вы сказали? ("
                                  f"напишите и отправьте)\n\n ",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_client_order_menu')]]),
                                  parse_mode="HTML")
        return CLIENT_ORDER_COMMENT
    order.update(comment=comment)
    update.message.reply_text(
        f"🗣  Отзыв о Магазине <b>{get_shop_name(order.shop_id)}   ({get_shop_id(order.shop_id)})</b> оставлен\n\n",
        parse_mode='HTML')
    return ConversationHandler.END


# ------------------------------------------
def button_order_shop_grade(update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data[17:]
    order = get_order_by_id(order_id)
    context.user_data[ORDER_ID] = order_id
    if not order:
        return update.callback_query.edit_message_text("Не актуально")
    if order.status != 0 and order.status != 1:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Статус данного заказа уже изменился!</i>"
        return update.callback_query.edit_message_text(
            f"{get_order_info(order_id)}{text_info}",
            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                              resize_keyboard=True),
            parse_mode='HTML')
    update.callback_query.edit_message_text(f"   <b>Оценка заказа</b>\n\n"
                                            f"Отправьте стоимость заказа, которую хотите предложить Заказчику  "
                                            f"<u>целое число - в рублях (от 10 до 100000)</u>",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                                       callback_data='back_to_shop_order_menu')]]),
                                            parse_mode="HTML")
    return SHOP_ORDER_GRADE_PRICE


def order_grade_shop_price(update, context):
    price = update.message.text
    try:
        price = int(price)
    except ValueError:
        update.message.reply_text(f"   <b>Оценка заказа</b>\n\n"
                                  f"Отправьте стоимость заказа, которую хотите предложить Заказчику  "
                                  f"<u>целое число - в рублях (от 10 до 100000)</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_shop_order_menu')]]),
                                  parse_mode="HTML")
        return SHOP_ORDER_GRADE_PRICE
    if price < 10 or price > 100000:
        update.message.reply_text(f"   <b>Оценка заказа</b>\n\n"
                                  f"Отправьте стоимость заказа, которую хотите предложить Заказчику  "
                                  f"<u>целое число - в рублях (от 10 до 100000)</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_shop_order_menu')]]),
                                  parse_mode="HTML")
        return SHOP_ORDER_GRADE_PRICE
    context.user_data[SHOP_ORDER_GRADE_PRICE] = price
    update.message.reply_text(f"   <b>Оценка заказа</b>\n\n"
                              f"Отправьте время выполнения заказа, которое хотите предложить Заказчику  "
                              f"<u>целое число - в днях (1-30)</u>",
                              reply_markup=InlineKeyboardMarkup(
                                  [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                         callback_data='back_to_shop_order_menu')]]), parse_mode="HTML")
    return SHOP_ORDER_GRADE_DEADLINE


def order_grade_shop_deadline(update, context):
    days = update.message.text
    try:
        days = int(days)
    except ValueError:
        update.message.reply_text(f"   <b>Оценка заказа</b>\n\n"
                                  f"Отправьте время выполнения заказа, которое хотите предложить Заказчику  "
                                  f"<u>целое число - в днях (1-30)</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_shop_order_menu')]]),
                                  parse_mode="HTML")
        return SHOP_ORDER_GRADE_DEADLINE
    if days < 1 or days > 30:
        update.message.reply_text(f"   <b>Оценка заказа</b>\n\n"
                                  f"Отправьте время выполнения заказа, которое хотите предложить Заказчику  "
                                  f"<u>целое число - в днях (1-30)</u>",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(f'{back_for_button}  Отмена',
                                                             callback_data='back_to_shop_order_menu')]]),
                                  parse_mode="HTML")
        return SHOP_ORDER_GRADE_DEADLINE
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    price = context.user_data[SHOP_ORDER_GRADE_PRICE]
    price_ltc = get_ltc_by_rub(price)
    if order.price is not None or order.price_ltc is not None or order.deadline_days is not None:
        text_info = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Исполнитель изменил оценку данного заказа! Будьте внимательны</i>"
        context.bot.sendMessage(order.client_id,
                                f"{get_order_info(order_id)}{text_info}",
                                reply_markup=InlineKeyboardMarkup(
                                    get_client_order_menu(order.id, order.status, context),
                                    resize_keyboard=True),
                                parse_mode='HTML')
    order.update(deadline_days=days, price=price, price_ltc=price_ltc)
    if order.price is not None or order.price_ltc is not None or order.deadline_days is not None:
        text_info = f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Вы изменили оценку данного заказа!</i>\n\n"
    else:
        text_info = f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Теперь вы можете принять заказ!</i>\n\n"
    update.message.reply_text(f"{get_order_info(order_id)}{text_info}",
                              reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order.id, order.status, context),
                                                                resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END


def button_moder_select_call_order_menu_send_message(update, context):
    query = update.callback_query
    query.answer()
    if ORDER_ID not in context.user_data:
        return update.callback_query.edit_message_text("Не актуально")

    if SELECT_SALE_SECTION in context.user_data:
        menu = InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_moder_select_service_sale')]],
                                    resize_keyboard=True)
    elif SELECT_BUYS_SECTION in context.user_data:
        menu = InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_moder_user_select_orders')]],
                                    resize_keyboard=True)
    else:
        menu = InlineKeyboardMarkup([[InlineKeyboardButton(f'{back_for_button}  Назад',
                                                           callback_data='back_to_call_order_menu_messages')]],
                                    resize_keyboard=True)

    update.callback_query.edit_message_text(f"   <b>Сообщение в Диспут</b>\n\n"
                                            f"Ваше сообщение будет отправлено Заказчику и Исполнителю\n",
                                            reply_markup=menu,
                                            parse_mode="HTML")
    return CALL_ORDER_MENU_SEND_MESSAGE


def call_order_menu_message_send(update, context):
    message = update.message.text
    order_id = context.user_data[ORDER_ID]
    order = get_order_by_id(order_id)
    order_info = get_order_info(
        order_id) + f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n<i>Сообщение от Модератора:</i>\n\t\t\t\t<b>{message}</b>"
    context.bot.sendMessage(order.client_id,
                            order_info,
                            reply_markup=InlineKeyboardMarkup(get_client_order_menu(order_id, order.status, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    context.bot.sendMessage(order.shop_id,
                            order_info,
                            reply_markup=InlineKeyboardMarkup(get_shop_order_menu(order_id, order.status, context),
                                                              resize_keyboard=True),
                            parse_mode='HTML')
    update.message.reply_text(
        "<b>Ваше сообщение было отправлено!</b>", parse_mode='HTML')

    order_messages = order.messages
    if not order_messages:
        order_messages = [f"-\t\t<b>Модератор:</b>  <i>{message}</i>"]
    else:
        order_messages.append(f"-\t\t<b>Модератор:</b>  <i>{message}</i>")
    order.update(messages=order_messages)
    order = get_order_by_id(order_id)
    messages_text = get_order_messages(order)
    update.message.reply_text(
        f"   <b>Сообщения в Диспуте</b>\n\n"
        f"Покупатель:  <b>@{get_user_tg_id(order.client_id)}</b>\n"
        f"Владелец магазина:  <b>@{get_user_tg_id(order.shop_id)}</b>\n\n"
        f"{messages_text}",
        reply_markup=InlineKeyboardMarkup(moder_select_call_order_menu_messages,
                                          resize_keyboard=True),
        parse_mode='HTML')
    return ConversationHandler.END


def button_change_terms_trade(update, context):
    query = update.callback_query
    query.answer()
    update.callback_query.edit_message_text(f'<b>Условия торговли</b>\n\n'
                                            f'Отправьте условия торговли с Вашим магазином (до 3000 символов):\n\n',
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                f'{back_for_button}  Отмена',
                                                callback_data='back_to_change_terms_trade')]],
                                                resize_keyboard=True),
                                            parse_mode='HTML')
    return TERMS_TRADE


def change_terms_trade_send(update, context):
    message = update.message.text
    chat_id = update.message.chat_id
    shop = get_shop_obj(chat_id)
    shop.update(terms_trade=message)
    shop = get_shop_obj(chat_id)
    terms = shop.terms_trade
    if terms is None:
        terms = "Нет данных"
    update.message.reply_text(f'<b>Условия торговли</b>\n\n'
                              f'В данном разделе вы можете указать условия торговли с вашим магазином\n\n'
                              f'В данном разделе вы указываете краткий свод правил использования ваших товаров или услуг.\n\n'
                              f'<b>✅  Пример:</b> 1.1 Проданный валидный аккаунт, купон возврату не подлежит (перед покупкой ознакомитесь с описанием товара)\n'
                              f'1.2 Смена данных или выполнения каких либо действий в купленном аккаунте (аккаунтах) осуществляемые покупателем, в последствии с обращением о замене по каким либо причинам. В таких случаях в замене будет отказано....и т.д\n\n'
                              f'<b>Максимальное кол-во символов:</b> 3000\n\n'
                              f'<b>Текущие условия торговли:</b> {terms}',
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Изменить условия",
                                                                                       callback_data='change_terms_trade')],
                                                                 [InlineKeyboardButton(f'{back_for_button}  Назад',
                                                                                       callback_data='back_to_my_shop_submenu_settings')]],
                                                                resize_keyboard=True),
                              parse_mode='HTML')
    return ConversationHandler.END
