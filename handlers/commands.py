from copy import deepcopy

import telegram
from bson.objectid import ObjectId
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from res.const import e_smiling, e_stop_sign, SELECT_ID, DEAL_ID, ORDER_ID, \
    url_support
from res.func import get_user_obj, search_user_by_id, get_user_info_text, check_moderator, get_shop_info_text, \
    search_shop_by_id, check_shop_banned, get_deal_by_id, get_buyer_deal_menu, get_deal_info, \
    get_shop_deal_menu, get_order_by_id, get_order_info, get_client_order_menu, get_shop_order_menu, \
    get_moder_select_shop_menu
from res.func import update_main_menu
from res.menu import reg_menu, moder_select_user_menu, my_shop_menu, user_select_shop_menu


def start_handler(update, context):
    chat_id = update.message.chat_id
    user = get_user_obj(chat_id)

    if not user:
        update.message.reply_text(
            f'👋  Приветствую в <b>Nassau</b>, здесь Вы можете свободно покупать и продавать товары или услуги.\n\n'
            'Откройте <b>свой магазин</b> абсолютно бесплатно всего в 2 нажатия!\n\n'
            'Бот выступает в качестве гаранта для сделок, а Вы торгуете непосредственно с людьми.\n\n'
            'Перед началом использования желательно указать Имя пользователя в профиле Telegram!\n\n'
            '⚠  <b>Наш сервис имеет ряд правил, с ними вы можете ознакомиться ниже по ссылке.</b>',
            reply_markup=InlineKeyboardMarkup(reg_menu, resize_keyboard=True), parse_mode='HTML')
    else:
        if user.banned:
            return update.message.reply_text(f'К сожалению, Ваш профиль <i>заблокирован</i> {e_stop_sign}\n'
                                             f'Обратитесь в <b>Техническую поддержку</b>',
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Тех. поддержка",
                                                                                                      url=url_support, resize_keyboard=True)]]),
                                             parse_mode='HTML')
        first_name = update.message.chat.first_name
        menu = update_main_menu(chat_id)
        update.message.reply_text(f'Рады снова Вас видеть, {first_name}! {e_smiling}\nОткрываем главное меню..\n',
                                  reply_markup=menu)


def not_reg_start(chat_id, context):
    context.bot.sendMessage(chat_id,
        f'👋  Приветствую в <b>Nassau</b>, здесь Вы можете свободно покупать и продавать товары или услуги.\n\n'
        'Откройте <b>свой магазин</b> абсолютно бесплатно всего в 2 нажатия!\n\n'
        'Бот выступает в качестве гаранта для сделок, а Вы торгуете непосредственно с людьми.\n\n'
        'Перед началом использования желательно указать Имя пользователя в профиле Telegram!\n\n'
        '⚠  <b>Наш сервис имеет ряд правил, с ними вы можете ознакомиться ниже по ссылке.</b>',
        reply_markup=InlineKeyboardMarkup(reg_menu, resize_keyboard=True), parse_mode='HTML')


def user_command_handler(update, context):
    chat_id = update.message.chat_id
    user_id = update.message.text
    user_obj = search_user_by_id(user_id)
    if user_obj is None:
        return update.message.reply_text(f'Пользователь не найден')
    text = get_user_info_text(chat_id, user_obj.chat_id)
    if check_moderator(chat_id):
        menu = moder_select_user_menu.copy()
        menu.pop(2)
        context.user_data[SELECT_ID] = user_obj.chat_id
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(menu, resize_keyboard=True),
                                  parse_mode='HTML')
    else:
        update.message.reply_text(text, parse_mode='HTML')


def shop_command_handler(update, context):
    chat_id = update.message.chat_id
    shop_id = update.message.text
    shop_obj = search_shop_by_id(shop_id)
    if shop_obj is None:
        return update.message.reply_text(f'Магазин не найден')
    text = get_shop_info_text(chat_id, shop_obj.owner_id)
    if check_moderator(chat_id):
        context.user_data[SELECT_ID] = shop_obj.owner_id
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(get_moder_select_shop_menu(shop_obj.owner_id),
                                                                          resize_keyboard=True),
                                  parse_mode='HTML')
    elif shop_obj.owner_id == chat_id and not check_shop_banned(chat_id):
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(my_shop_menu, resize_keyboard=True),
                                  parse_mode='HTML')
    else:
        context.user_data[SELECT_ID] = shop_obj.owner_id
        menu = deepcopy(user_select_shop_menu)
        menu[1].append(InlineKeyboardButton(f"📩  Написать сообщение",
                                            callback_data=f'user_shop_send_message_{shop_obj.owner_id}'))
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(user_select_shop_menu, resize_keyboard=True),
                                  parse_mode='HTML')


def deal_command_handler(update, context):
    chat_id = update.message.chat_id
    deal_id = update.message.text[2:]
    deal_obj = get_deal_by_id(deal_id)
    if deal_obj is None:
        return update.message.reply_text(f'Сделка не найдена')
    deal_info = get_deal_info(deal_id)
    moder = check_moderator(chat_id)
    if deal_obj is None or (deal_obj.buyer_id != chat_id and deal_obj.shop_id != chat_id and not moder):
        return update.message.reply_text(f'Сделка не найдена')
    if deal_obj.buyer_id == chat_id:
        menu = deepcopy(get_buyer_deal_menu(deal_obj, deal_obj.status, context))
        update.message.reply_text(deal_info, reply_markup=InlineKeyboardMarkup(menu, resize_keyboard=True),
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    elif deal_obj.shop_id == chat_id:
        menu = deepcopy(get_shop_deal_menu(deal_obj.status, deal_obj, context))

        update.message.reply_text(deal_info, reply_markup=InlineKeyboardMarkup(menu, resize_keyboard=True),
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    elif moder:
        deal_info = get_deal_info(deal_id)
        if deal_obj.call_moderator and deal_obj.status == 2:
            menu = [
                [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_menu_messages'),
                 InlineKeyboardButton(f"Товар", callback_data='moder_select_call_menu_content')],
                [InlineKeyboardButton(f"Закрыть сделку", callback_data='moder_select_call_menu_close_deal')]
            ]
        else:
            menu = []
        update.callback_query.edit_message_text(
            deal_info,
            reply_markup=InlineKeyboardMarkup(
                menu,
                resize_keyboard=True),
            parse_mode=telegram.ParseMode.MARKDOWN)
    context.user_data[DEAL_ID] = deal_id


def order_command_handler(update, context):
    chat_id = update.message.chat_id
    order_id = update.message.text[2:]
    if len(order_id) != 24:
        return update.message.reply_text(f'Заказ не найден')
    order_obj = get_order_by_id(ObjectId(order_id))
    order_info = get_order_info(order_id)
    moder = check_moderator(chat_id)
    if order_obj is None or (order_obj.client_id != chat_id and order_obj.shop_id != chat_id and not moder):
        return update.message.reply_text(f'Сделка не найдена')
    if order_obj.client_id == chat_id:
        menu = deepcopy(get_client_order_menu(order_id, order_obj.status, context))
        update.message.reply_text(order_info, reply_markup=InlineKeyboardMarkup(menu, resize_keyboard=True),
                                  parse_mode='HTML')
    elif order_obj.shop_id == chat_id:
        menu = deepcopy(get_shop_order_menu(order_id, order_obj.status, context))
        update.message.reply_text(order_info, reply_markup=InlineKeyboardMarkup(menu, resize_keyboard=True),
                                  parse_mode='HTML')
    elif moder:
        order_info = get_order_info(order_id)
        if order_obj.call_moderator and order_obj.status == 2:
            menu = [
                [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_menu_messages'),
                 InlineKeyboardButton(f"Товар", callback_data='moder_select_call_menu_content')],
                [InlineKeyboardButton(f"Закрыть сделку", callback_data='moder_select_call_menu_close_deal')]
            ]
        else:
            menu = []
        update.callback_query.edit_message_text(
            order_info,
            reply_markup=InlineKeyboardMarkup(
                menu,
                resize_keyboard=True),
            parse_mode='HTML')
    context.user_data[ORDER_ID] = order_id
