import string
from copy import deepcopy
from random import *

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import requests

from res.const import e_briefcase, max_in_list_page, backhand_right, \
    back_for_button, backhand_left, CATEGORY_INFO, CATEGORY_PRODS, SELECT_PROD_ID, e_star, SELECT_SALE_SECTION, \
    CATEGORY_SERVICES, SELECT_SERV_ID, e_like, e_dislike, SELECT_BUYS_SECTION, e_stop_sign, e_shopping_bags
from res.schemas import Requisites, ProductCategory, Product, Deal, ServiceCategory, Service, Order
from res.menu import main_menu, button_my_shop, dashboard_menu, button_section_moderator
import traceback
from datetime import datetime, timedelta
from res.const import PAGE_INDEX, PAGE_MAX_INDEX, e_money_bag, min_guarantee, e_handshake, DATA, \
    SELECT_ID, e_store, e_dollar_banknote, commission_per_deals
from res.schemas import User, Payment, RequestOpenShop, Shop, ShopOperations, Withdrawal


def get_course():
    res = requests.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,RUB')
    rates = res.json()
    return rates


def get_money_balance(balance):
    rates = get_course()
    money_balance = [balance * rates['USD'], balance * rates['RUB']]
    return money_balance


def get_ltc_by_rub(summa):
    rates = get_course()
    return round(summa / rates['RUB'], 8)


def get_rub_by_ltc(summa):
    rates = get_course()
    return round(summa * rates['RUB'], 2)


def convert_base(num, to_base=10, from_base=10):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]


def id_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(choice(chars) for _ in range(size))


# ------------ ПОКАЗАТЬ МЕНЮ ЛИЧНОГО КАБИНЕТА ----------
def show_dashboard_menu(chat_id, update):
    user = get_user_obj(chat_id)
    address_info = ""
    coinbase_address = user.coinbase_address_id
    balance = user.balance
    if not coinbase_address:
        address_info = "У вас не создан персональный LITECOIN адрес для пополнения счета в сервисе\n\nДля создания " \
                       "перейдите в раздел 'Внести LITECOIN' "
    if balance is None:
        return update.message.reply_text(f'Произошла ошибка! Код: notbalance')
    money_balance = get_money_balance(balance)
    update.callback_query.edit_message_text(f'{e_briefcase}   <b>Личный кабинет</b>\n\n'
                                            f'<b>Ваш ID:</b> {user.user_id}\n\n'
                                            f'{e_money_bag}\t\t<b>Баланс</b>\n\t\t<i>{round(balance, 8)}</i>\t\tLITECOIN\n\n'
                                            f'{e_dollar_banknote}\t\t<b>В валюте</b>\n'
                                            f'\t\t<i>{round(money_balance[0], 2)}</i>\t\tUSD\n'
                                            f'\t\t<i>{round(money_balance[1], 2)}</i>\t\tRUB'
                                            f'\n\n<b>Незавершенные покупки:</b>\n'
                                            f'\t\tСделки (товары) - <b>{count_open_buys(chat_id)}</b>\n'
                                            f'\t\tЗаказы (услуги) - <b>{count_open_cl_orders(chat_id)}</b>'
                                            f'\n\n{address_info}',
                                            reply_markup=InlineKeyboardMarkup(dashboard_menu, resize_keyboard=True),
                                            parse_mode='HTML')


# ВЫВОД СПИСКА В ВИДЕ МЕНЮ ДЛЯ ВЫБОРА
def show_list_menu(update, context, name):
    menu = [[]]
    data = []
    start = 0
    end = 0

    # Определение данных
    if name == 'requests':
        data = get_requests_open_shop_list()

    elif name == 'shops':
        data = get_shops_list()

    elif name == 'requisites':
        owner_id = update.callback_query.message.chat.id
        data = get_shop_requisites_list(owner_id)

    # ------------- Мои покупки (товары)
    elif name == 'my_buys':
        if SELECT_BUYS_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_BUYS_SECTION]
        buyer_id = update.callback_query.message.chat.id
        if sale_section == "dispute":
            data = get_user_dispute_deals(buyer_id)
        elif sale_section == "open":
            data = get_user_open_deals(buyer_id)
        elif sale_section == "close":
            data = get_user_close_deals(buyer_id)

    # ------------ Мои покупки (услуги)
    elif name == 'my_buys_service':
        if SELECT_BUYS_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_BUYS_SECTION]
        client_id = update.callback_query.message.chat.id
        if sale_section == "dispute":
            data = get_user_dispute_orders(client_id)
        elif sale_section == "open":
            data = get_user_open_orders(client_id)
        elif sale_section == "close":
            data = get_user_close_orders(client_id)

    # --------------- Мои продажи (товары)
    elif name == 'my_sales':
        if SELECT_SALE_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_SALE_SECTION]
        owner_id = update.callback_query.message.chat.id
        if sale_section == "dispute":
            data = get_shop_dispute_deals(owner_id)
        elif sale_section == "open":
            data = get_shop_open_deals(owner_id)
        elif sale_section == "close":
            data = get_shop_close_deals(owner_id)

    # --------------- Мои продажи (услуги)
    elif name == 'my_service_sales':
        if SELECT_SALE_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        sale_section = context.user_data[SELECT_SALE_SECTION]
        owner_id = update.callback_query.message.chat.id
        if sale_section == "dispute":
            data = get_shop_dispute_orders(owner_id)
        elif sale_section == "open":
            data = get_shop_open_orders(owner_id)
        elif sale_section == "close":
            data = get_shop_close_orders(owner_id)

    # --------------- Модер смотрит продажи (товары)
    elif name == 'moder_shop_sales':
        if SELECT_SALE_SECTION not in context.user_data or SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        owner_id = context.user_data[SELECT_ID]
        sale_section = context.user_data[SELECT_SALE_SECTION]
        if sale_section == "dispute":
            data = get_shop_dispute_deals(owner_id)
        elif sale_section == "open":
            data = get_shop_open_deals(owner_id)
        elif sale_section == "close":
            data = get_shop_close_deals(owner_id)

    # ------------- Модер смотрит продажи (услуги)
    elif name == 'moder_shop_service_sales':
        if SELECT_SALE_SECTION not in context.user_data or SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        owner_id = context.user_data[SELECT_ID]
        sale_section = context.user_data[SELECT_SALE_SECTION]
        if sale_section == "dispute":
            data = get_shop_dispute_orders(owner_id)
        elif sale_section == "open":
            data = get_shop_open_orders(owner_id)
        elif sale_section == "close":
            data = get_shop_close_orders(owner_id)

    # -------------- Модер смотрит покупки (товары)
    elif name == 'moder_user_buys':
        buyer_id = context.user_data[SELECT_ID]
        if SELECT_BUYS_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        buys_section = context.user_data[SELECT_BUYS_SECTION]
        if buys_section == "dispute":
            data = get_user_dispute_deals(buyer_id)
        elif buys_section == "open":
            data = get_user_open_deals(buyer_id)
        elif buys_section == "close":
            data = get_user_close_deals(buyer_id)

    # ------------- Модер смотрит покупки (услуги)
    elif name == 'moder_user_orders':
        buyer_id = context.user_data[SELECT_ID]
        if SELECT_BUYS_SECTION not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        buys_section = context.user_data[SELECT_BUYS_SECTION]
        if buys_section == "dispute":
            data = get_user_dispute_orders(buyer_id)
        elif buys_section == "open":
            data = get_user_open_orders(buyer_id)
        elif buys_section == "close":
            data = get_user_close_orders(buyer_id)

    # ----------- Список вызовов по сделкам
    elif name == 'deal_moder_call':
        data = get_deals_moder_call()

    # ----------- Список вызовов по заказам
    elif name == 'order_moder_call':
        data = get_orders_moder_call()

    # Определение индексов страницы
    if PAGE_INDEX not in context.user_data:
        context.user_data[PAGE_INDEX] = 1
    if PAGE_MAX_INDEX not in context.user_data:
        context.user_data[PAGE_MAX_INDEX] = len(data) // max_in_list_page
        # Если кол-во на странице не кратно общему кол-ву, то добавляем последнюю страницу
        if len(data) % max_in_list_page > 0:
            context.user_data[PAGE_MAX_INDEX] += 1

    if context.user_data[PAGE_INDEX] > context.user_data[PAGE_MAX_INDEX]:
        context.user_data[PAGE_INDEX] = context.user_data[PAGE_MAX_INDEX]

    # Определение индексов для вывода
    if context.user_data[PAGE_INDEX] == 1:
        start = 0
        if len(data) > max_in_list_page:
            end = max_in_list_page - 1
        else:
            end = len(data) - 1
    elif len(data) > max_in_list_page and context.user_data[PAGE_INDEX] == context.user_data[PAGE_MAX_INDEX]:
        start = (context.user_data[PAGE_INDEX] - 1) * max_in_list_page
        if len(data) % max_in_list_page == 0:
            end = context.user_data[PAGE_INDEX] * max_in_list_page - 1
        else:
            end = start + len(data) % max_in_list_page - 1
    elif 1 < context.user_data[PAGE_INDEX] < context.user_data[PAGE_MAX_INDEX]:
        start = (context.user_data[PAGE_INDEX] - 1) * max_in_list_page
        end = start + (max_in_list_page - 1)

    # Вывод
    for i in range(start, end + 1):
        if len(data) == 0:
            break
        if name == 'requests':
            menu.append(
                [InlineKeyboardButton(data[i].shop_name, callback_data=f"req_open_shop_select_{data[i].creator_id}")])
        elif name == 'shops':
            menu.append(
                [InlineKeyboardButton(data[i].shop_name, callback_data=f"moder_select_shop_{data[i].owner_id}")])
        elif name == 'requisites':
            menu.append(
                [InlineKeyboardButton(data[i].name + " | " + data[i].payment_system,
                                      callback_data=f"my_shop_finance_requisites_id_{data[i].id}")])
        # Мои покупки (товары)
        elif name == 'my_buys':
            shop = get_shop_obj(data[i].shop_id)
            status_text = get_deal_status_text(data[i].status)
            if data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                                          callback_data=f"my_buys_{data[i].id}")])
            elif data[i].status == 2 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [М]",
                                          callback_data=f"my_buys_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"my_buys_{data[i].id}")])

        # Мои покупки (услуги)
        elif name == 'my_buys_service':
            shop = get_shop_obj(data[i].shop_id)
            status_text = get_order_status_text(data[i].status)
            if data[i].status == 2:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                                          callback_data=f"my_orders_{data[i].id}")])
            elif data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | [{status_text}]",
                                          callback_data=f"my_orders_{data[i].id}")])
            elif data[i].status == 3 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [М]",
                                          callback_data=f"my_orders_{data[i].id}")])
            elif data[i].status == 3:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"my_orders_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date_start.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"my_orders_{data[i].id}")])

        # Мои продажи (товары)
        elif name == 'my_sales':
            buyer_user = get_user_obj(data[i].buyer_id)
            status_text = get_deal_status_text(data[i].status)
            if data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(buyer_user.first_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                                          callback_data=f"my_sales_{data[i].id}")])
            elif data[i].status == 2 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(buyer_user.first_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [М]",
                                          callback_data=f"my_sales_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(buyer_user.first_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"my_sales_{data[i].id}")])

        # Мои продажи (услуги)
        elif name == 'my_service_sales':
            client_user = get_user_obj(data[i].client_id)
            status_text = get_order_status_text(data[i].status)
            if data[i].status == 2:
                menu.append(
                    [InlineKeyboardButton(client_user.first_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                                          callback_data=f"my_service_sales_{data[i].id}")])
            elif data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(client_user.first_name + f" | [{status_text}]",
                                          callback_data=f"my_service_sales_{data[i].id}")])
            elif data[i].status == 3 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(client_user.first_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [М]",
                                          callback_data=f"my_service_sales_{data[i].id}")])
            elif data[i].status == 3:
                menu.append(
                    [InlineKeyboardButton(client_user.first_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"my_service_sales_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(client_user.first_name + f" | {data[i].date_start.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"my_service_sales_{data[i].id}")])

        # Модер смотрит продажи магаза (товары)
        elif name == 'moder_shop_sales':
            buyer_user = get_user_obj(data[i].buyer_id)
            status_text = get_deal_status_text(data[i].status)
            if data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(buyer_user.first_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                                          callback_data=f"moder_shop_sales_{data[i].id}")])
            elif data[i].status == 2 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(buyer_user.first_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [М]",
                                          callback_data=f"moder_shop_sales_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(buyer_user.first_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"moder_shop_sales_{data[i].id}")])

        # Модер смотрит продажи магаза (услуги)
        elif name == 'moder_shop_service_sales':
            client_user = get_user_obj(data[i].client_id)
            status_text = get_order_status_text(data[i].status)
            if data[i].status == 2:
                menu.append(
                    [InlineKeyboardButton(
                        client_user.first_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                        callback_data=f"moder_shop_service_sales_{data[i].id}")])
            elif data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(client_user.first_name + f" | [{status_text}]",
                                          callback_data=f"moder_shop_service_sales_{data[i].id}")])
            elif data[i].status == 3 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(
                        client_user.first_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [М]",
                        callback_data=f"moder_shop_service_sales_{data[i].id}")])
            elif data[i].status == 3:
                menu.append(
                    [InlineKeyboardButton(
                        client_user.first_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')}",
                        callback_data=f"moder_shop_service_sales_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(
                        client_user.first_name + f" | {data[i].date_start.strftime('%d-%m-%Y %H:%M')}",
                        callback_data=f"moder_shop_service_sales_{data[i].id}")])

        # Модер смотрит покупки пользователя (товары)
        elif name == 'moder_user_buys':
            shop = get_shop_obj(data[i].shop_id)
            status_text = get_deal_status_text(data[i].status)
            if data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                                          callback_data=f"moder_user_buys_{data[i].id}")])
            elif data[i].status == 2 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')} [М]",
                                          callback_data=f"moder_user_buys_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"moder_user_buys_{data[i].id}")])

        # Модер смотрит покупки пользователя (услуги)
        elif name == 'moder_user_orders':
            shop = get_shop_obj(data[i].shop_id)
            status_text = get_order_status_text(data[i].status)
            if data[i].status == 2:
                menu.append(
                    [InlineKeyboardButton(
                        shop.shop_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [{status_text}]",
                        callback_data=f"moder_user_orders_{data[i].id}")])
            elif data[i].status < 2:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | [{status_text}]",
                                          callback_data=f"moder_user_orders_{data[i].id}")])
            elif data[i].status == 3 and data[i].call_moderator:
                menu.append(
                    [InlineKeyboardButton(
                        shop.shop_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')} [М]",
                        callback_data=f"moder_user_orders_{data[i].id}")])
            elif data[i].status == 3:
                menu.append(
                    [InlineKeyboardButton(
                        shop.shop_name + f" | DLine: {data[i].date_deadline.strftime('%d-%m-%Y %H:%M')}",
                        callback_data=f"moder_user_orders_{data[i].id}")])
            else:
                menu.append(
                    [InlineKeyboardButton(shop.shop_name + f" | {data[i].date_start.strftime('%d-%m-%Y %H:%M')}",
                                          callback_data=f"moder_user_orders_{data[i].id}")])

        # Список вызовов в сделках
        elif name == 'deal_moder_call':
            shop = get_shop_obj(data[i].shop_id)
            buyer = get_user_obj(data[i].buyer_id)
            menu.append(
                [InlineKeyboardButton(shop.shop_name + f" | {buyer.username}",
                                      callback_data=f"deal_moder_call_{data[i].id}")])

        # Список вызовов в заказах
        elif name == 'order_moder_call':
            shop = get_shop_obj(data[i].shop_id)
            client = get_user_obj(data[i].client_id)
            menu.append(
                [InlineKeyboardButton(shop.shop_name + f" | {client.username}",
                                      callback_data=f"order_moder_call_{data[i].id}")])

    # Кнопки перелистывания
    if context.user_data[PAGE_INDEX] == 1 and len(data) > max_in_list_page:
        menu.append(
            [InlineKeyboardButton(f"[ {context.user_data[PAGE_INDEX]} ]", callback_data="now_page"),
             InlineKeyboardButton(
                 f"{backhand_right}  [ {context.user_data[PAGE_INDEX] + 1} / {context.user_data[PAGE_MAX_INDEX]} ]",
                 callback_data='button_switcher_list_page_next')])
    elif len(data) > max_in_list_page and context.user_data[PAGE_INDEX] == context.user_data[PAGE_MAX_INDEX]:
        menu.append(
            [InlineKeyboardButton(
                f"[ {context.user_data[PAGE_INDEX] - 1} / {context.user_data[PAGE_MAX_INDEX]} ]  {backhand_left}",
                callback_data='button_switcher_list_page_prev'),
                InlineKeyboardButton(f"[ {context.user_data[PAGE_INDEX]} ]", callback_data="now_page")])
    elif 1 < context.user_data[PAGE_INDEX] < context.user_data[PAGE_MAX_INDEX]:
        menu.append(
            [InlineKeyboardButton(
                f"[ {context.user_data[PAGE_INDEX] - 1} / {context.user_data[PAGE_MAX_INDEX]} ]  {backhand_left}",
                callback_data='button_switcher_list_page_prev'),
                InlineKeyboardButton(f"[ {context.user_data[PAGE_INDEX]} ]", callback_data="now_page"),
                InlineKeyboardButton(
                    f"{backhand_right}  [ {context.user_data[PAGE_INDEX] + 1} / {context.user_data[PAGE_MAX_INDEX]} ]",
                    callback_data='button_switcher_list_page_next')])
    context.user_data[DATA] = name

    # Кнопки назад
    if name == 'my_buys':
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_buys_select_section')])
    elif name == 'my_buys_service':
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_service_buys_select_section')])
    elif name == 'my_sales':
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_sales_select_section')])
    elif name == 'my_service_sales':
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_service_sales_select_section')])
    elif name == 'moder_shop_sales':
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_shop_sales_select_section')])
    elif name == 'moder_shop_service_sales':
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_shop_services_sales_select_section')])
    elif name == 'moder_user_buys':
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_user_buys_select_section')])
    elif name == 'moder_user_orders':
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_user_orders_select_section')])
    elif name == 'deal_moder_call' or name == 'order_moder_call':
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_select_section_calls')])
    else:
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_show_list')])
    return menu


# ВЫВОД СПИСКА ТЕКСТОМ
def show_list_text(update, context, name):
    data = []
    start = 0
    end = 0
    text = ""
    menu = [[]]
    chat_id = update.callback_query.message.chat.id
    shop_id = None

    if SELECT_ID in context.user_data:
        chat_id = context.user_data[SELECT_ID]

    # Определение данных
    if name == 'user_payments':
        data = get_user_payments(chat_id)
    elif name == 'shop_operations':
        data = get_shop_operations(chat_id)
    elif name == 'shop_products_comments':
        shop_id = context.user_data[SELECT_ID]
        chat_id = update.callback_query.message.chat.id
        data = get_shop_deals_comments(shop_id)
    elif name == 'shop_services_comments':
        shop_id = context.user_data[SELECT_ID]
        chat_id = update.callback_query.message.chat.id
        data = get_shop_orders_comments(shop_id)
    # Определение индексов страницы
    if PAGE_INDEX not in context.user_data:
        context.user_data[PAGE_INDEX] = 1

    context.user_data[PAGE_MAX_INDEX] = len(data) // max_in_list_page
    # Если кол-во на странице не кратно общему кол-ву, то добавляем последнюю страницу
    if (len(data) % max_in_list_page) != 0:
        context.user_data[PAGE_MAX_INDEX] += 1

    if context.user_data[PAGE_INDEX] > context.user_data[PAGE_MAX_INDEX]:
        context.user_data[PAGE_INDEX] = context.user_data[PAGE_MAX_INDEX]

    # Определение индексов для вывода
    if context.user_data[PAGE_INDEX] == 1:
        start = 0
        if len(data) > max_in_list_page:
            end = max_in_list_page - 1
        else:
            end = len(data) - 1
    elif len(data) > max_in_list_page and context.user_data[PAGE_INDEX] == context.user_data[PAGE_MAX_INDEX]:
        start = (context.user_data[PAGE_INDEX] - 1) * max_in_list_page
        if len(data) % max_in_list_page == 0:
            end = context.user_data[PAGE_INDEX] * max_in_list_page - 1
        else:
            end = start + len(data) % max_in_list_page - 1
    elif 1 < context.user_data[PAGE_INDEX] < context.user_data[PAGE_MAX_INDEX]:
        start = (context.user_data[PAGE_INDEX] - 1) * max_in_list_page
        end = start + (max_in_list_page - 1)

    # Получение данных
    for i in range(start, end + 1):
        if len(data) == 0:
            break
        if name == 'user_payments':
            payment_amount = data[i].amount
            date = data[i].credited_at
            date = date.strftime("%d-%m-%Y  %H:%M:%S")
            text += f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                    f"<b>Сумма:</b>  <i>{payment_amount}</i> (LITECOIN)\n" \
                    f"<b>Дата зачисления:</b>  <i>{date}</i>\n"

        elif name == 'shop_operations':
            shop_name = data[i].name
            type = data[i].type
            type_text = ""
            sum = data[i].sum
            date = data[i].date.strftime("%d-%m-%Y  %H:%M:%S")  # форматирование даты
            if type == 0:
                type_text = "Списание"
            elif type == 1:
                type_text = "Пополнение"
            text += f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                    f"<b>Название:</b>  <i>{shop_name}</i>\n" \
                    f"<b>Тип:</b>  <i>{type_text}</i>\n" \
                    f"<b>Сумма:</b>  <i>{sum}</i>\n" \
                    f"<b>Дата:</b>  <i>{date}</i>\n"

        elif name == 'shop_products_comments':
            buyer_id = data[i].buyer_id
            buyer_obj = get_user_obj(buyer_id)
            if data[i].comment is not None:
                comment_text = f"<b>Комментарий:</b>    <i>{data[i].comment}</i>\n"
            else:
                comment_text = ""
            if data[i].like is True:
                like_text = f"{e_like}"
            else:
                like_text = f"{e_dislike}"
            text += f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                    f"<b>Покупатель:</b>    <i>{buyer_obj.first_name}</i>  ({buyer_obj.user_id})\n" \
                    f"<b>Сумма:</b>   <i>{data[i].sum_price} ₽ </i>\n" \
                    f"<b>Оценка:</b>    {like_text}\n" \
                    f"{comment_text}" \
                    f"<b>Дата покупки:</b>    <i>{data[i].date.strftime('%d-%m-%Y %H:%M')}</i>\n"

        elif name == 'shop_services_comments':
            client_id = data[i].client_id
            client_obj = get_user_obj(client_id)
            if data[i].comment is not None:
                comment_text = f"<b>Комментарий:</b>    <i>{data[i].comment}</i>\n"
            else:
                comment_text = ""
            if data[i].like is True:
                like_text = f"{e_like}"
            else:
                like_text = f"{e_dislike}"
            text += f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                    f"<b>Покупатель:</b>    <i>{client_obj.first_name}</i>  ({client_obj.user_id})\n" \
                    f"<b>Сумма:</b>   <i>{data[i].price} ₽ </i>\n" \
                    f"<b>Оценка:</b>    {like_text}\n" \
                    f"{comment_text}" \
                    f"<b>Дата завершения:</b>    <i>{data[i].date_deadline.strftime('%d-%m-%Y %H:%M')}</i>\n"

    # Кнопки перелистывания
    if context.user_data[PAGE_INDEX] == 1 and len(data) > max_in_list_page:
        menu.append(
            [InlineKeyboardButton(f"[ {context.user_data[PAGE_INDEX]} ]", callback_data="now_page"),
             InlineKeyboardButton(
                 f"{backhand_right}  [ {context.user_data[PAGE_INDEX] + 1} / {context.user_data[PAGE_MAX_INDEX]} ]",
                 callback_data='button_switcher_list_page_next')])
    elif len(data) > max_in_list_page and context.user_data[PAGE_INDEX] == context.user_data[PAGE_MAX_INDEX]:
        menu.append(
            [InlineKeyboardButton(
                f"[ {context.user_data[PAGE_INDEX] - 1} / {context.user_data[PAGE_MAX_INDEX]} ]  {backhand_left}",
                callback_data='button_switcher_list_page_prev'),
                InlineKeyboardButton(f"[ {context.user_data[PAGE_INDEX]} ]", callback_data="now_page")])
    elif 1 < context.user_data[PAGE_INDEX] < context.user_data[PAGE_MAX_INDEX]:
        menu.append(
            [InlineKeyboardButton(
                f"[ {context.user_data[PAGE_INDEX] - 1} / {context.user_data[PAGE_MAX_INDEX]} ]  {backhand_left}",
                callback_data='button_switcher_list_page_prev'),
                InlineKeyboardButton(f"[ {context.user_data[PAGE_INDEX]} ]", callback_data="now_page"),
                InlineKeyboardButton(
                    f"{backhand_right}  [ {context.user_data[PAGE_INDEX] + 1} / {context.user_data[PAGE_MAX_INDEX]} ]",
                    callback_data='button_switcher_list_page_next')])

    # ВЫВОД
    if name == 'user_payments':
        if SELECT_ID not in context.user_data:
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_dashboard_menu')])
            select_user_obj = get_user_obj(chat_id)
            user_id = select_user_obj.user_id
        else:
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_select_user_menu')])
            check_user_obj = get_user_obj(chat_id)
            user_id = check_user_obj.user_id
        if text == "":
            text = "\n<i>Нет пополнений</i>"
        update.callback_query.edit_message_text(
            f"<b>История пополнений</b>\n\nПополнения счёта пользователя {user_id}\n"
            f"{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    elif name == 'shop_operations':
        if SELECT_ID not in context.user_data:
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_shop_finance_menu')])
            select_shop_obj = get_shop_obj(chat_id)
            check_shop_name = select_shop_obj.shop_name
        else:
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_select_shop_menu')])
            select_shop_obj = get_shop_obj(chat_id)
            check_shop_name = select_shop_obj.shop_name
        if text == "":
            text = "\n<i>Нет операций</i>"
        update.callback_query.edit_message_text(
            f"<b>История операций</b>\n\nОперации по счету Магазина <b>{check_shop_name}</b>\n{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
    elif name == 'shop_products_comments':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        else:
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_comments_select_section')])
            shop = get_shop_obj(shop_id)
            if text == "":
                text = "<i>Нет отзывов</i>"
            rating = get_sum_shop_deal_rating(shop.owner_id)
            likes = get_count_likes_deal(shop.owner_id)
            dislikes = get_count_dislikes_deal(shop.owner_id)
            if len(data) > 0:
                rating_text = f"<b>Рейтинг:</b>    {e_star * int_r(rating / 20)}" \
                              f"      {e_like} <b>{likes}</b>      {e_dislike} <b>{dislikes}</b>\n" \
                              f"<b>Рекомендуют:</b>     {int_r(rating)}%     ({len(data)} голосов)\n\n"
            else:
                rating_text = ""
            update.callback_query.edit_message_text(
                f"🗣  <b>Отзывы о магазине {shop.shop_name}  (товары)</b>\n\n"
                f"{rating_text}{text}",
                reply_markup=InlineKeyboardMarkup(menu,
                                                  resize_keyboard=True),
                parse_mode='HTML')
    elif name == 'shop_services_comments':
        if SELECT_ID not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        else:
            if SELECT_SERV_ID not in context.user_data:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад",
                                          callback_data='back_to_comments_select_section')])
            else:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад",
                                          callback_data='back_to_market_select_service_menu')])
            shop = get_shop_obj(shop_id)
            if text == "":
                text = "<i>Нет отзывов</i>"
            rating = get_sum_shop_order_rating(shop.owner_id)
            likes = get_count_likes_order(shop.owner_id)
            dislikes = get_count_dislikes_order(shop.owner_id)
            if len(data) > 0:
                rating_text = f"<b>Рейтинг:</b>    {e_star * (int_r(rating / 20))}" \
                              f"      {e_like} <b>{likes}</b>      {e_dislike} <b>{dislikes}</b>\n" \
                              f"<b>Рекомендуют:</b>     {int_r(rating)}%     ({len(data)} голосов)\n\n"
            else:
                rating_text = ""
            update.callback_query.edit_message_text(
                f"🗣  <b>Отзывы о магазине {shop.shop_name}  (услуги)</b>\n\n"
                f"{rating_text}{text}",
                reply_markup=InlineKeyboardMarkup(menu,
                                                  resize_keyboard=True),
                parse_mode='HTML')
    context.user_data[DATA] = name


def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num


def update_main_menu(chat_id):
    user = get_user_obj(chat_id)
    menu = deepcopy(main_menu)
    if check_shop_owner(chat_id) and not check_shop_banned(chat_id) and not check_shop_stop(chat_id):
        menu['keyboard'].append([KeyboardButton(button_my_shop)])
    if user.moderator:
        menu['keyboard'].append([KeyboardButton(button_section_moderator)])
    return menu


# ================================================== ФУНКЦИИ РАБОТА С БАЗОЙ ===========================================

# ============================================== ПОЛЬЗОВАТЕЛЬ ==========================================================

# получение объекта юзера по chat_id
def get_user_obj(chat_id):
    user = User.objects(chat_id=chat_id).first()
    return user


def get_user_messages_limit(chat_id):
    mes_limit = User.objects(chat_id=chat_id).first().messages_limit
    return mes_limit


def get_user_date_set_limit(chat_id):
    date_set_limit = User.objects(chat_id=chat_id).first().date_set_limit
    return date_set_limit


def add_user(chat_id, username, first_name):
    now = datetime.now()
    user_id = "/u" + str(convert_base(chat_id, 16, 10))
    User(chat_id=chat_id, user_id=user_id, username=username, first_name=first_name,
         reg_date=now).save()


def check_user_banned(chat_id):
    user = get_user_obj(chat_id)
    if user and user.banned:
        return True
    else:
        return False


def add_user_balance(chat_id, amount):
    user = get_user_obj(chat_id)
    balance = user.balance + amount
    user.update(balance=balance)


def get_sum_new_transactions(chat_id, transactions):
    sum_amount_new = 0
    for transaction in transactions:
        payment = Payment.objects(chat_id=chat_id, trans_id=transaction['id'])
        if not payment and transaction['status'] == "completed":
            add_payment(chat_id, transaction['id'], transaction['amount'].amount, transaction['created_at'])
            sum_amount_new += float(transaction['amount'].amount)
    return sum_amount_new


def add_payment(chat_id, trans_id, amount, created_at):
    credited_at = datetime.now()
    Payment(chat_id=chat_id, trans_id=trans_id, amount=amount, created_at=created_at, credited_at=credited_at).save()


def add_request_open_shop(creator_id, shop_name, why, res):
    now = datetime.now()
    created_at = now.strftime("%d-%m-%Y %H:%M")
    RequestOpenShop(creator_id=creator_id, shop_name=shop_name, created_at=created_at, why=why, res=res).save()


def check_open_shop_request(creator_id):
    request = RequestOpenShop.objects(creator_id=creator_id)
    if request:
        return True
    else:
        return False


def check_shop_owner(chat_id):
    shop = Shop.objects(owner_id=chat_id).first()
    return shop


def check_moderator(chat_id):
    user = get_user_obj(chat_id)
    return user.moderator


def get_username(chat_id):
    user = get_user_obj(chat_id)
    return user


def get_user_balance(chat_id):
    user = get_user_obj(chat_id)
    balance = user.balance
    return balance


def update_username(chat_id, username):
    user = get_user_obj(chat_id)
    if user is not None:
        return user.update(username=username)
    return None


def get_requests_open_shop_list():
    return RequestOpenShop.objects()


def get_shops_list():
    return Shop.objects()


def get_shop_request_obj(req_creator_id):
    request = RequestOpenShop.objects(creator_id=req_creator_id).first()
    return request


def get_shop_obj(owner_id):
    shop = Shop.objects(owner_id=owner_id).first()
    return shop


def get_shop_id(owner_id):
    shop = Shop.objects(owner_id=owner_id).first()
    return shop.shop_id


def get_shop_name(owner_id):
    shop = Shop.objects(owner_id=owner_id).first()
    return shop.shop_name


def delete_req_open_shop(req_creator_id):
    request = get_shop_request_obj(req_creator_id)
    request.delete()


def add_new_shop(creator_id, who_approved):
    request = get_shop_request_obj(creator_id)
    now = datetime.now()
    created_at = now.strftime("%d-%m-%Y %H:%M")
    shop_id = "/s" + str(convert_base(creator_id, 32, 10))
    Shop(owner_id=creator_id, shop_id=shop_id, shop_name=request.shop_name,
         created_at=created_at, who_approved=who_approved).save()


def moders_alert(context, name):
    moders = User.objects(moderator=True)
    mes = ""
    if name == "new_request_shop":
        mes = "<b>[Оповещение]</b> Появилась новая заявка на создание магазина"
    if name == 'new_deal_moder_call':
        mes = "<b>[Оповещение]</b> Поступил новый вызов модератора (Сделка)"
    if name == 'new_order_moder_call':
        mes = "<b>[Оповещение]</b> Поступил новый вызов модератора (Заказ)"
    if name == 'new_req_cat_prod':
        mes = "<b>[Оповещение]</b> Появилась новая заявка на добавление категории (Товары)"
    if name == 'new_req_cat_serv':
        mes = "<b>[Оповещение]</b> Появилась новая заявка на добавление категории (Услуги)"
    for moder in moders:
        context.bot.sendMessage(moder.chat_id,
                                mes, parse_mode='HTML')


def clear_user_data(context):
    if PAGE_INDEX in context.user_data:
        context.user_data.pop(PAGE_INDEX)
    if PAGE_MAX_INDEX in context.user_data:
        context.user_data.pop(PAGE_MAX_INDEX)
    if DATA in context.user_data:
        context.user_data.pop(DATA)
    if SELECT_ID in context.user_data:
        context.user_data.pop(SELECT_ID)
    if SELECT_PROD_ID in context.user_data:
        context.user_data.pop(SELECT_PROD_ID)
    if CATEGORY_INFO in context.user_data:
        context.user_data.pop(CATEGORY_INFO)
    if CATEGORY_PRODS in context.user_data:
        context.user_data.pop(CATEGORY_PRODS)
    if SELECT_SALE_SECTION in context.user_data:
        context.user_data.pop(SELECT_SALE_SECTION)
    if SELECT_BUYS_SECTION in context.user_data:
        context.user_data.pop(SELECT_BUYS_SECTION)



def check_occupied_shop_name(shop_name):
    shops = Shop.objects()
    for shop in shops:
        if shop.shop_name.lower() == shop_name.lower():
            return True
    return False


def check_occupied_request_shop_name(shop_name):
    reqs = RequestOpenShop.objects()
    for req in reqs:
        if req.shop_name.lower() == shop_name.lower():
            return True
    return False


def check_date_change_shop_name(owner_id):
    shop = get_shop_obj(owner_id)
    date = shop.date_change_name
    now = datetime.now()
    if date is None:
        return True
    diff = now - date
    hours = divmod(diff, timedelta(seconds=3600))[0]
    if hours < 24:
        return False
    return True


def update_user_date_set_limit(chat_id, date_set_limit):
    user = get_user_obj(chat_id=chat_id)
    user.update(date_set_limit=date_set_limit)


def update_user_massages_limit(chat_id, messages_limit):
    user = get_user_obj(chat_id=chat_id)
    user.update(messages_limit=messages_limit)


def set_date_change_shop_name(owner_id):
    shop = get_shop_obj(owner_id)
    now = datetime.now()
    shop.update(date_change_name=now)


def shop_ban(owner_id):
    shop = get_shop_obj(owner_id)
    shop.update(banned=True)


def shop_stop(owner_id, stop):
    shop = get_shop_obj(owner_id)
    shop.update(stop=stop)


def shop_unban(owner_id):
    shop = get_shop_obj(owner_id)
    shop.update(banned=False)


def set_shop_about(owner_id, shop_about):
    shop = get_shop_obj(owner_id)
    shop.update(shop_about=shop_about)


def set_shop_name(owner_id, shop_name):
    shop = get_shop_obj(owner_id)
    shop.update(shop_name=shop_name)


def check_shop_banned(owner_id):
    shop = get_shop_obj(owner_id)
    if shop.banned:
        return True
    else:
        return False


def check_shop_stop(owner_id):
    shop = get_shop_obj(owner_id)
    if shop.stop:
        return True
    else:
        return False


def check_shop_pause(owner_id):
    shop = get_shop_obj(owner_id)
    if shop.pause_trade:
        return True
    else:
        return False


def get_shop_balance(owner_id):
    shop_obj = get_shop_obj(owner_id)
    balance = shop_obj.balance
    return balance


def get_user_id(chat_id):
    user = get_user_obj(chat_id)
    return user.user_id


def get_user_name(chat_id):
    user = get_user_obj(chat_id)
    return user.first_name


def get_user_tg_id(chat_id):
    user = get_user_obj(chat_id)
    return user.username


def get_shop_info_text(query_chat_id, chat_id):
    shop_obj = get_shop_obj(chat_id)
    balance = shop_obj.balance
    money_balance = get_money_balance(balance)
    guarantee = shop_obj.guarantee
    shop_name = shop_obj.shop_name
    shop_date = shop_obj.created_at
    shop_about = shop_obj.shop_about
    shop_banned = shop_obj.banned
    shop_banned_text = ''
    balance_text = ''
    message_text = 'Желаем приятных продаж 😊'
    owner_id = shop_obj.owner_id
    if shop_banned:
        shop_banned_text = "\n<b>Заблокирован</b>"
    guarantee_text = "<i>" + str(guarantee) + "</i>  LITECOIN" if guarantee > 0 else "Не внесён\n"
    if query_chat_id == chat_id or check_moderator(query_chat_id):
        balance_text = f'➖➖➖➖➖➖\n<b>Баланс магазина:</b>\n\t\t<i>{round(balance, 8)}</i>\t\tLITECOIN (<i>{round(money_balance[1], 2)}</i>\t\t₽)\n\n'
        if guarantee > 0:
            guarantee_money_balance = get_money_balance(guarantee)
            guarantee_text += f" (<i>{round(guarantee_money_balance[1], 2)}</i>\t\t₽)\n"

    text = f'{e_store}   <b>Информация о магазине</b>\n\n' \
           f'<b>ID:</b>  {shop_obj.shop_id}\n' \
           f'<b>Владелец:</b>  {get_user_id(owner_id)}\n' \
           f'<b>Название:</b>  <i>{shop_name}</i>\n' \
           f'<b>Описание:</b>  <i>{shop_about}</i>\n' \
           f'<b>Дата создания:</b>  {shop_date}\n\n' \
           f'{balance_text}' \
           f'<b>Гарант магазина:</b>\n  {guarantee_text}' \
           f'➖➖➖➖➖➖\n\n{message_text}{shop_banned_text}'
    return text


def search_shop_by_name(shop_name):
    shops = Shop.objects()
    for shop in shops:
        if shop.shop_name.lower() == shop_name.lower():
            return shop
    return None


def get_guarantee_shop(owner_id):
    shop_obj = get_shop_obj(owner_id)
    return shop_obj.guarantee


def search_shop_by_id(shop_id):
    shops = Shop.objects(shop_id=shop_id).first()
    return shops


def search_user_by_username(user_name):
    users = User.objects()
    for user in users:
        if user.username.lower() == user_name.lower():
            return user
    return None


def get_user_count_buys(chat_id):
    deals = Deal.objects(buyer_id=chat_id).count()
    orders = Order.objects(client_id=chat_id).count()
    return deals + orders


def get_user_info_text(query_chat_id, chat_id):
    user_obj = get_user_obj(chat_id)
    username = user_obj.username
    tgname_text = ""
    banned = user_obj.banned
    balance = round(user_obj.balance, 8)
    reg_date = user_obj.reg_date.strftime("%d-%m-%Y %H:%M")
    shop_owned = check_shop_owner(chat_id)
    count_buys = get_user_count_buys(chat_id)
    shop_owned_text = ""
    user_banned_text = ""
    balance_text = ""
    if shop_owned is not None:
        shop_owned_text = f"\n<b>Владелец магазина:</b>  {shop_owned.shop_id}"
    if banned:
        user_banned_text = "\n\n<b>Заблокирован</b>"
    if check_moderator(query_chat_id):
        tgname_text = f"<b>Имя TG:</b>  <i>@{username}</i>\n"
        balance_text = f"<b>Баланс:</b>  {get_rub_by_ltc(balance)} ₽  ({balance} LITECOIN)\n"
    text = f"<b>Информация о пользователе</b>\n\n<b>ID:</b>  <i>{user_obj.user_id}</i>\n" \
           f"<b>Имя:</b>  <i>{user_obj.first_name}</i>\n{tgname_text}{balance_text}" \
           f"<b>Дата регистрации:</b>  <i>{reg_date}</i>{shop_owned_text}{user_banned_text}\n" \
           f"<b>Всего покупок:</b>  {count_buys}"
    return text


def add_shop_balance(chat_id, sum):
    shop_obj = get_shop_obj(chat_id)
    new_balance = round(shop_obj.balance + sum, 8)
    shop_obj.update(balance=new_balance)


def update_user_balance(chat_id, sum):
    user_obj = get_user_obj(chat_id)
    new_balance = round(user_obj.balance + sum, 8)
    user_obj.update(balance=new_balance)


def update_shop_guarantee(chat_id, sum):
    shop_obj = get_shop_obj(chat_id)
    new_guarantee = round(shop_obj.guarantee + sum, 8)
    shop_obj.update(guarantee=new_guarantee)


def user_ban(user):
    user.update(banned=True)


def user_unban(user):
    user.update(banned=False)


def get_myshop_finance_text(chat_id):
    shop = get_shop_obj(chat_id)
    shop_balance = shop.balance
    user_balance = get_user_balance(chat_id)
    guarantee = shop.guarantee
    freeze = shop_sum_freeze_deals_money(chat_id)
    open_deals = count_open_deals(chat_id)
    open_orders = count_open_sh_orders(chat_id)
    freeze_orders = shop_sum_freeze_orders_money(chat_id)
    guarantee_text = "<i>" + str(guarantee) + f"</i>  LITECOIN  ({get_rub_by_ltc(guarantee)} ₽)" if guarantee > 0 else "Не внесён"
    deals_info = f'<b>Незавершенных продаж:  </b>\n' \
                     f'\t\tСделки (товары) - <b>{open_deals}</b>\n' \
                 f'\t\t\t\t<b>Заморожено:  {freeze} ₽  ({get_ltc_by_rub(freeze)}  LITECOIN)</b>\n' \
                 f'\t\t\t\t<b>Заморожен гарант:  {get_rub_by_ltc(shop.freeze_guarantee)} ₽  ({round(shop.freeze_guarantee, 8)}  LITECOIN) </b>\n\n' \
                 f'\t\tЗаказы (услуги) - <b>{open_orders}</b>\n' \
                 f'\t\t\t\t<b>Заморожено:  {freeze_orders} ₽  ({get_ltc_by_rub(freeze_orders)}  LITECOIN)</b>\n'

    text = f"{e_money_bag}  <b>Финансы</b>\n\n" \
           f"<b>Баланс вашего магазина</b>\n  <i>{round(shop_balance, 8)}</i>  LITECOIN\n\n" \
           f"{deals_info}\n" \
           f"<b>Баланс личного счета</b>\n  <i>{round(user_balance, 8)}</i>  LITECOIN\n\n" \
           f"<b>{e_handshake}  Гарант</b>\n  {guarantee_text}"
    return text


def get_user_payments(chat_id):
    payments = Payment.objects(chat_id=chat_id).order_by('-credited_at')
    return payments


def add_shop_operation(owner_id, name, sum, type):
    date = datetime.now()
    ShopOperations(owner_id=owner_id, sum=sum, date=date, name=name, type=type).save()


def get_shop_operations(chat_id):
    operations = ShopOperations.objects(owner_id=chat_id).order_by('-date')
    return operations


def get_shop_deals_comments(shop_id):
    deals = Deal.objects(shop_id=shop_id, like__ne=None).order_by('-date')
    return deals


def get_shop_orders_comments(shop_id):
    orders = Order.objects(shop_id=shop_id, like__ne=None).order_by('-date_deadline')
    return orders


def search_user_by_id(find_user_id):
    users = User.objects(user_id=find_user_id).first()
    return users


def add_withdrawal(chat_id, trans_id, to_address, amount, currency, created_at, status):
    try:
        date = datetime.now()
        Withdrawal(chat_id=chat_id, trans_id=trans_id, to_address=to_address, amount=amount, currency=currency,
                   created_at=date, status=status).save()
    except Exception:
        print('Error add_withdrawal:\n', traceback.format_exc())


def get_shop_requisites_list(owner_id):
    requisites = Requisites.objects(owner_id=owner_id)
    return requisites


def add_shop_requisite(owner_id, requisite_name, payment_system, account_number):
    try:
        Requisites(owner_id=owner_id, name=requisite_name, payment_system=payment_system,
                   account_number=account_number).save()
    except Exception:
        print('Error add_shop_requisite:\n', traceback.format_exc())


def get_requisite_info(owner_id, select_id):
    requisite = Requisites.objects(id=select_id, owner_id=owner_id).first()
    requisite_info = f"<b>Название:</b>  {requisite.name}\n" \
                     f"<b>Платежная система:</b>  {requisite.payment_system}\n" \
                     f"<b>Номер счета:</b>  {requisite.account_number}"
    return requisite_info


def get_requisite_by_id(requisite_id):
    requisite = Requisites.objects(id=requisite_id).first()
    return requisite


def update_requisite_info(chat_id, select_id, info, data):
    requisite = Requisites.objects(id=select_id, owner_id=chat_id).first()
    if info == 'name':
        requisite.update(name=data)
    elif info == 'payment_system':
        requisite.update(payment_system=data)
    elif info == 'account_number':
        requisite.update(account_number=data)


def delete_shop_requisite(owner_id, select_id):
    requisites = Requisites.objects(owner_id=owner_id)
    requisite = requisites[int(select_id)]
    requisite.delete()


def sort_by_guarantee(shop):
    return shop.guarantee


def get_subcat_btnlist_by_catid(context, catid, data, chat_id):
    menu = [[]]
    list_cat = []
    context.user_data[CATEGORY_INFO]['cat_id'] = catid
    if catid is None:
        all_list = ProductCategory.objects()
        for cat in all_list:
            if str(type(cat.sub_id)) == "<class 'NoneType'>":
                if data == 'my_list' or data == 'for_user' or data == 'select_shop_prods':
                    try:
                        context.user_data[CATEGORY_PRODS].index(cat.id)
                    except Exception:
                        continue
                    else:
                        list_cat.append(cat)
                else:
                    list_cat.append(cat)
    else:
        if data == 'my_list' or data == 'for_user' or data == 'select_shop_prods':
            list_sub = ProductCategory.objects(sub_id=catid)
            for cat in list_sub:
                try:
                    context.user_data[CATEGORY_PRODS].index(cat.id)
                except Exception:
                    continue
                else:
                    list_cat.append(cat)
        else:
            list_cat = ProductCategory.objects(sub_id=catid)

    for cat in list_cat:
        menu.append([InlineKeyboardButton(f"{cat.name}", callback_data=f"select_cat_{cat.id}")])

    if len(list_cat) == 0:
        if catid is not None:
            if data == 'my_list':
                products = Product.objects(category_id=catid, owner_id=chat_id)
                for prod in products:
                    menu.append([InlineKeyboardButton(f"{prod.name}  |  {prod.price} ₽  [{prod.count} шт.]",
                                                      callback_data=f"select_my_product_{prod.id}")])
            elif data == 'for_user':
                products = Product.objects(category_id=catid)
                check_shops_id = set()
                shops = []
                for prod in products:
                    shop = get_shop_by_prod(prod)
                    if shop.shop_id not in check_shops_id and prod.count > 0 and not shop.pause_trade and not check_shop_banned(
                            shop.owner_id) and not shop.stop:
                        shops.append(shop)
                        check_shops_id.add(shop.shop_id)

                shops_guarantee_zero = []
                shops_guarantee = []

                for s in shops:
                    if s.guarantee == 0:
                        shops_guarantee_zero.append(s)
                    else:
                        shops_guarantee.append(s)

                shops_guarantee.sort(reverse=True, key=sort_by_guarantee)

                for s in shops_guarantee:
                    menu.append([InlineKeyboardButton(f"{s.shop_name}  * Гарант {get_rub_by_ltc(s.guarantee)} ₽ *",
                                                  callback_data=f"select_shop_prods_bycat_{s.owner_id}")])

                while len(shops_guarantee_zero) > 0:
                    s = choice(shops_guarantee_zero)
                    menu.append([InlineKeyboardButton(f"{s.shop_name}  * Не внесён *",
                                                      callback_data=f"select_shop_prods_bycat_{s.owner_id}")])
                    shops_guarantee_zero.remove(s)

            elif data == 'select_shop_prods':
                products = Product.objects(category_id=catid, owner_id=context.user_data[SELECT_ID])
                for prod in products:
                    if prod.count > 0:
                        menu.append([InlineKeyboardButton(f"{prod.name} |{prod.price} ₽|{prod.count}шт|",
                                                      callback_data=f"select_product_{prod.id}")])
            elif data == 'add':
                menu.append([InlineKeyboardButton(f"Добавить товар", callback_data=f"start_add_product")])
    if catid is None:
        if data == 'for_user':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_select_market_section')])
        elif data == 'select_shop_prods':
            if check_moderator(chat_id):
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_select_shop_menu')])
            else:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_user_select_shop_menu')])
        elif data == 'my_list' or data == 'add':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_my_shop_submenu_products")])
    else:
        if data == 'for_user':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_cat_menu"),
                 InlineKeyboardButton(f"{back_for_button}  Выбор раздела",
                                      callback_data='back_to_select_market_section')])
        elif data == 'select_shop_prods':
            if check_moderator(chat_id):
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_cat_menu"),
                     InlineKeyboardButton(f"{back_for_button}  Основное меню",
                                          callback_data="back_moder_select_shop_menu")])
            else:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_cat_menu"),
                     InlineKeyboardButton(f"{back_for_button}  Основное меню",
                                          callback_data="back_user_select_shop_menu")])
        elif data == 'my_list' or data == 'add':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_cat_menu"),
                 InlineKeyboardButton(f"{back_for_button}  в Мои товары",
                                      callback_data="back_to_my_shop_submenu_products")])

    return menu


def sort_by_rating(shop):
    return get_sum_shop_order_rating(shop['shop'].owner_id)


def get_subcat_service_btnlist_by_catid(context, catid, data, chat_id):
    menu = [[]]
    list_cat = []
    context.user_data[CATEGORY_INFO]['cat_id'] = catid
    if catid is None:
        all_list = ServiceCategory.objects()
        for cat in all_list:
            if str(type(cat.sub_id)) == "<class 'NoneType'>":
                if data == 'my_list_services' or data == 'for_user_services' or data == 'select_shop_services':
                    try:
                        context.user_data[CATEGORY_SERVICES].index(cat.id)
                    except Exception:
                        continue
                    else:
                        list_cat.append(cat)
                else:
                    list_cat.append(cat)
    else:
        if data == 'my_list_services' or data == 'for_user_services' or data == 'select_shop_services':
            list_sub = ServiceCategory.objects(sub_id=catid)
            for cat in list_sub:
                try:
                    context.user_data[CATEGORY_SERVICES].index(cat.id)
                except Exception:
                    continue
                else:
                    list_cat.append(cat)
        else:
            list_cat = ServiceCategory.objects(sub_id=catid)

    for cat in list_cat:
        menu.append([InlineKeyboardButton(f"{cat.name}", callback_data=f"select_serv_cat_{cat.id}")])

    if len(list_cat) == 0:
        if catid is not None:
            if data == 'my_list_services':
                services = Service.objects(category_id=catid, owner_id=chat_id)
                for serv in services:
                    menu.append([InlineKeyboardButton(f"{serv.name} | от {serv.min_price} ₽",
                                                      callback_data=f"select_my_service_{serv.id}")])
            elif data == 'for_user_services':
                services = Service.objects(category_id=catid)
                shops = []
                for serv in services:
                    shop = get_shop_by_serv(serv)
                    if not shop.pause_trade and not check_shop_banned(
                            shop.owner_id) and not check_shop_stop(shop.owner_id):
                        shops.append({
                            'shop': shop,
                            'serv': serv,
                        })
                shops.sort(reverse=True, key=sort_by_rating)
                shops_no_rating = []
                for s in shops:
                    shop = s['shop']
                    serv = s['serv']
                    rating = get_sum_shop_order_rating(shop.owner_id)
                    if rating > 0:
                        menu.append(
                            [InlineKeyboardButton(f"{shop.shop_name}  | {e_star * int_r(rating / 20)} | от {serv.min_price} ₽",
                                                  callback_data=f"select_service_{serv.id}")])
                    else:
                        shops_no_rating.append(s)
                while len(shops_no_rating) > 0:
                    s = choice(shops_no_rating)
                    menu.append(
                        [InlineKeyboardButton(f"{s['shop'].shop_name}  | Нет рейтинга | от {s['serv'].min_price} ₽",
                                              callback_data=f"select_service_{s['serv'].id}")])
                    shops_no_rating.remove(s)

            elif data == 'select_shop_services':
                serv = Service.objects(category_id=catid, owner_id=context.user_data[SELECT_ID]).first()
                menu.append([InlineKeyboardButton(f"{serv.name} | от {serv.min_price} ₽",
                                                  callback_data=f"select_service_{serv.id}")])
            elif data == 'add_service':
                menu.append([InlineKeyboardButton(f"➕  Добавить услугу", callback_data=f"start_add_service")])

    if catid is None:
        if data == 'for_user_services':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_select_market_section')])
        elif data == 'select_shop_services':
            if check_moderator(chat_id):
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_select_shop_menu')])
            else:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_user_select_shop_menu')])
        elif data == 'my_list_services' or data == 'add_service':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_my_shop_submenu_services")])
    else:
        if data == 'for_user_services':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_serv_cat_menu"),
                 InlineKeyboardButton(f"{back_for_button}  Выбор раздела",
                                      callback_data='back_to_select_market_section')])
        elif data == 'select_shop_services':
            if check_moderator(chat_id):
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_serv_cat_menu"),
                     InlineKeyboardButton(f"{back_for_button}  Основное меню",
                                          callback_data="back_moder_select_shop_menu")])
            else:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_serv_cat_menu"),
                     InlineKeyboardButton(f"{back_for_button}  Основное меню",
                                          callback_data="back_user_select_shop_menu")])
        elif data == 'my_list_services' or data == 'add_service':
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data="back_to_prev_serv_cat_menu"),
                 InlineKeyboardButton(f"{back_for_button}  в Мои услуги",
                                      callback_data="back_to_my_shop_submenu_services")])

    return menu


def get_shop_by_prod(prod):
    shop = Shop.objects(owner_id=prod.owner_id).first()
    return shop


def get_shop_by_serv(serv):
    shop = Shop.objects(owner_id=serv.owner_id).first()
    return shop


def add_shop_product(category_id, owner_id, name, description, price, count, content):
    date = datetime.now()
    Product(category_id=category_id, owner_id=owner_id, name=name, description=description,
            price=price, count=count, content=content, date_last_update=date).save()


def add_shop_service(category_id, owner_id, name, description, portfolio, price, picture):
    return Service(category_id=category_id, owner_id=owner_id, name=name, description=description,
                   portfolio=portfolio, min_price=price, picture=picture).save()


def add_product_content(product_id, add_count, new_content):
    date = datetime.now()
    product = Product.objects(id=product_id).first()
    count = product.count + add_count
    content = product.content
    for c in new_content:
        content.append(c)
    product.update(content=content, count=count, date_last_update=date)


def get_cat_my_products_tree(context, update, owner_id):
    products = Product.objects(owner_id=owner_id)
    for prod in products:
        try:
            context.user_data[CATEGORY_PRODS].index(prod.category_id)
        except Exception:
            get_prods_sub_category(context, prod.category_id)


def get_cat_products_tree(context, update, chat_id):
    products = Product.objects()
    for prod in products:
        if not check_shop_banned(prod.owner_id) and not check_shop_stop(prod.owner_id) and not check_shop_pause(prod.owner_id) and prod.count > 0:
            try:
                context.user_data[CATEGORY_PRODS].index(prod.category_id)
            except Exception:
                get_prods_sub_category(context, prod.category_id)


def get_cat_products_shop_tree(context, update):
    chat_id = update.callback_query.message.chat.id
    owner_id = context.user_data[SELECT_ID]
    products = Product.objects(owner_id=owner_id)
    for prod in products:
        if not check_shop_banned(prod.owner_id) and not check_shop_stop(prod.owner_id) and not check_shop_pause(prod.owner_id) and prod.count > 0:
            try:
                context.user_data[CATEGORY_PRODS].index(prod.category_id)
            except Exception:
                get_prods_sub_category(context, prod.category_id)


def get_prods_sub_category(context, cat_id):
    cat = ProductCategory.objects(id=cat_id).first()
    if not cat:
        return
    context.user_data[CATEGORY_PRODS].append(cat.id)
    if cat.sub_id is None:
        return
    return get_prods_sub_category(context, cat.sub_id)


def get_product_info(owner_id, context, product_id):
    product = Product.objects(id=product_id).first()
    if not product:
        context.bot.sendMessage(owner_id, "Ошибка")
        return print('Ошибка в выбранном id товара')
    shop = Shop.objects(owner_id=product.owner_id).first()
    shop_name = shop.shop_name
    shop_id = shop.shop_id
    ltc_price = get_ltc_by_rub(product.price)
    date = product.date_last_update.strftime("%d-%m-%Y %H:%M")
    info = f"\n\n🏪 <b>Магазин:</b>  {shop_name} ({shop_id})\n\n" \
           f"<b>📂 Категория:</b>\n{context.user_data[CATEGORY_INFO]['cat_path']}\n" \
           f"<b>Название:</b>  {product.name}\n" \
           f"<b>Описание:</b>  {product.description}\n" \
           f"<b>Стоимость (1 шт.):</b>  {product.price} ₽  ({ltc_price} LITECOIN)\n" \
           f"<b>Количество:</b>  {product.count} шт.\n" \
           f"<b>Последнее пополнение:</b>  {date}"
    return info


def get_product_by_id(product_id):
    return Product.objects(id=product_id).first()


def change_product_name(product_id, name):
    product = Product.objects(id=product_id).first()
    product.update(name=name)


def change_product_description(product_id, description):
    product = Product.objects(id=product_id).first()
    product.update(description=description)


def change_product_price(product_id, price):
    product = Product.objects(id=product_id).first()
    product.update(price=price)


def product_del(product_id):
    product = Product.objects(id=product_id).first()
    product.delete()


def get_requisite_list(update, context, owner_id):
    menu = [[]]
    requisites = Requisites.objects(owner_id=owner_id)
    for req in requisites:
        menu.append(
            [InlineKeyboardButton(req.payment_system, callback_data=f"requisite_payment_select_{req.id}")])
    menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_select_payment_method')])
    return menu


def add_deal(shop_id, buyer_id, product_id, category, sum_price, payment_method, sum_price_ltc, count, file_id, status):
    now = datetime.now()
    deal = Deal(shop_id=shop_id, buyer_id=buyer_id, product_id=product_id, category=category, sum_price=sum_price,
                sum_price_ltc=sum_price_ltc, count=count, file_id=file_id, status=status, date=now,
                payment_method=payment_method).save()
    return deal


def get_product_content_bytes(product_id, count):
    product = Product.objects(id=product_id).first()
    product_content = product.content
    count_prod = product.count
    str_content = ""
    for _, item in zip(range(count), reversed(product_content)):
        str_content += item + "\n"
        product_content.remove(item)
    product.update(content=product_content, count=count_prod - count)
    bytes_prod = str_content.encode('utf-8')
    return bytes_prod


def get_deal_info(deal_id):
    deal = Deal.objects(id=deal_id).first()
    shop = Shop.objects(owner_id=deal.shop_id).first()
    buyer = User.objects(chat_id=deal.buyer_id).first()
    buyer_id = buyer.user_id
    date = deal.date.strftime('%d-%m-%Y %H:%M')
    status = deal.status
    status_text = get_deal_status_text(status)
    if deal.status == 2 and deal.call_moderator is True:
        status_text += "  _[Вызван модератор]_"
    change_text = ""
    payment_info = ""
    category = deal.category.replace('<b>', '*').replace('</b>', '*')
    if deal.change_count is not None:
        change_text = f"\n\nВыдана замена: *{deal.change_count} шт.*"
    if deal.payment_method != 'LITECOIN':
        payment_info = f"\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                       f"Счет для оплаты:   *{deal.payment_method}*\n" \
                       f"Комментарий к оплате:   `{deal.id}`"
    info = f"⚠  *Информация о сделке*\n" \
           f"(/d{deal_id})\n\n" \
           f"🏪  *Магазин:*  {shop.shop_name}  ({shop.shop_id})\n" \
           f"👤  *Покупатель:*  {buyer.first_name}  ({buyer_id})\n\n" \
           f"*Категория:*  \n{category}\n" \
           f"*Количество:*  {deal.count} шт.\n" \
           f"*Стоимость:*  {deal.sum_price} ₽  ({deal.sum_price_ltc} LITECOIN)\n" \
           f"*Способ оплаты:*  {deal.payment_method}\n" \
           f"*Статус:*  {status_text}\n" \
           f"*Дата создания:*  {date}{payment_info}{change_text}\n"
    return info


def get_deal_status_text(status):
    if status == 0:
        return "Оплата"
    elif status == 1:
        return "Товар получен"
    elif status == 2:
        return "Диспут"
    elif status == 3:
        return "Завершена"


def get_buyer_deal_menu(deal, deal_status, context):
    menu = [[]]
    deal_id = deal.id
    if deal_status == 0:
        menu = []
        if not get_deal_proof_payment(deal_id):
            menu.append([InlineKeyboardButton(f"Оплатил", callback_data=f'deal_buyer_confirm_payment_{deal_id}')])
        menu.append([InlineKeyboardButton(f"Отменить покупку", callback_data=f'deal_buyer_cancel_{deal_id}')])
        menu.append([InlineKeyboardButton(f"📩  Написать магазину", callback_data=f'deal_buyer_message_{deal_id}')])
    elif deal_status == 1:
        menu = [[InlineKeyboardButton(f"Завершить покупку", callback_data=f'deal_buyer_close_{deal_id}')],
                [InlineKeyboardButton(f"Открыть Диспут", callback_data=f'deal_buyer_dispute_{deal_id}')],
                [InlineKeyboardButton(f"📩  Написать магазину", callback_data=f'deal_buyer_message_{deal_id}')]]
    elif deal_status == 2:
        if deal.call_moderator is False:
            send_button_text = f"📩  Написать магазину"
        else:
            send_button_text = f"📩  Написать в Диспут"
        menu = [[InlineKeyboardButton(f"Завершить покупку", callback_data=f'deal_buyer_close_{deal_id}')],
                [InlineKeyboardButton(f"{send_button_text}", callback_data=f'deal_buyer_message_{deal_id}')]]
        now = datetime.now()
        if ((deal.potential is True) or (now > (deal.date + timedelta(days=1)))) and deal.call_moderator is False:
            menu.append([InlineKeyboardButton(f"Вызвать модератора", callback_data=f'deal_buyer_moder_call_{deal_id}')])
    elif deal_status == 3:
        menu = [[InlineKeyboardButton(f"Товар", callback_data=f'deal_buyer_get_product')]]
        if deal.like is None:
            menu.append(
                                                    [InlineKeyboardButton(f'Like  {e_like}',
                                                                          callback_data=f'button_deal_buyer_like_{deal_id}'),
                                                     InlineKeyboardButton(f'Dislike  {e_dislike}',
                                                                          callback_data=f'button_deal_buyer_dislike_{deal_id}')
                                                     ])
        if deal.comment is None:
            menu.append([InlineKeyboardButton(f"🗣  Оставить отзыв", callback_data=f'button_deal_buyer_review_{deal_id}')])
    if context.user_data is not None and SELECT_BUYS_SECTION in context.user_data:
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_buys_list')])
    return menu


def get_shop_deal_menu(deal_status, deal, context):
    menu = [[]]
    deal_id = deal.id
    if deal_status == 0:
        if get_deal_proof_payment(deal_id):
            menu.append([InlineKeyboardButton(f"Получил оплату", callback_data=f'deal_shop_confirm_payment_{deal_id}')])
        menu.append([InlineKeyboardButton(f"📩  Написать покупателю", callback_data=f'deal_shop_message_{deal_id}')])
    if deal_status == 1:
        menu = [[InlineKeyboardButton(f"📩  Написать покупателю", callback_data=f'deal_shop_message_{deal_id}')]]
    elif deal_status == 2:
        if deal.call_moderator is False:
            send_button_text = f"📩  Написать покупателю"
        else:
            send_button_text = f"📩  Написать в Диспут"
        if get_deal_change_count(deal_id) is None:
            menu.append([InlineKeyboardButton(f"Сделать замену", callback_data=f'deal_shop_change_{deal_id}')])
        menu.append([InlineKeyboardButton(f"{send_button_text}", callback_data=f'deal_shop_message_{deal_id}')])
    if context.user_data is not None and SELECT_SALE_SECTION in context.user_data:
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_sales_list')])
    return menu


def get_deal_proof_payment(deal_id):
    deal = Deal.objects(id=deal_id).first()
    return deal.proof_payment


def get_deal_change_count(deal_id):
    deal = Deal.objects(id=deal_id).first()
    return deal.change_count


def get_deal_by_id(deal_id):
    deal = Deal.objects(id=deal_id).first()
    return deal


def change_shop_check_time(chat_id, time):
    shop = Shop.objects(owner_id=chat_id).first()
    shop.update(check_buyer_time=time * 60)


def get_shop_check_time(owner_id):
    shop = Shop.objects(owner_id=owner_id).first()
    return shop.check_buyer_time


def deal_set_comment(deal, message):
    deal.update(comment=message)


# Выдача замены товара
def deal_shop_give_change(deal, product, count, context, buyer_id):
    content_bytes = get_product_content_bytes(product.id, count)
    message = context.bot.sendDocument(buyer_id, content_bytes, f"{deal.shop_id}.{count}.txt",
                                       caption=f"Выдача замены товара [{count} шт.]")
    file_id = message.document.file_id
    deal.update(change_count=count, change_file_id=file_id)


def get_shop_two_comments(owner_id):
    shop_deals = Deal.objects(shop_id=owner_id, like__ne=None).order_by('-date')[:2]
    if len(shop_deals) == 0:
        return ""

    buyer_obj = get_user_obj(shop_deals[0].buyer_id)
    if len(shop_deals) == 1:
        if shop_deals[0].comment is not None:
            comment_text = f"<b>Комментарий:</b>    <i>{shop_deals[0].comment}</i>\n"
        else:
            comment_text = ""
        if shop_deals[0].like is True:
            like_text = f"{e_like}"
        else:
            like_text = f"{e_dislike}"
        return "<b>Последний отзыв:</b>\n" + \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>Покупатель:</b>    <i>{buyer_obj.first_name}</i>  ({buyer_obj.user_id})\n" \
               f"<b>Сумма:</b>   <i>{shop_deals[0].sum_price} ₽ </i>\n" \
               f"<b>Оценка:</b>    {like_text}\n" \
               f"{comment_text}" \
               f"<b>Дата покупки:</b>    <i>{shop_deals[0].date.strftime('%d-%m-%Y %H:%M')}</i>\n\n"
    else:
        comments_text = "<b>Последние отзывы:</b>\n\n"
        for deal in shop_deals:
            if deal.comment is not None:
                comment_text = f"<b>Комментарий:</b>    <i>{deal.comment}</i>\n"
            else:
                comment_text = ""
            if deal.like is True:
                like_text = f"{e_like}"
            else:
                like_text = f"{e_dislike}"

            comments_text += f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                             f"<b>Покупатель:</b>    <i>{buyer_obj.first_name}</i>  ({buyer_obj.user_id})\n" \
                             f"<b>Сумма:</b>   <i>{deal.sum_price} ₽ </i>\n" \
                             f"<b>Оценка:</b>    {like_text}\n" \
                             f"{comment_text}" \
                             f"<b>Дата покупки:</b>    <i>{deal.date.strftime('%d-%m-%Y %H:%M')}</i>\n\n"
        return comments_text


def get_user_buys(buyer_id):
    deals = Deal.objects(buyer_id=buyer_id)
    return list(reversed(deals))


# --------- Сделки магазина по id владельца -----------
def get_shop_deals(owner_id):
    deals = Deal.objects(shop_id=owner_id)
    return list(reversed(deals))


def get_shop_dispute_deals(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=2)
    return list(reversed(deals))


def get_shop_open_deals(owner_id):
    deals = Deal.objects(shop_id=owner_id, status__lt=2)
    return list(reversed(deals))


def get_shop_close_deals(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=3)
    return list(reversed(deals))


# Кол-во
def get_shop_dispute_deals_count(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=2).count()
    return deals


def get_shop_open_deals_count(owner_id):
    deals = Deal.objects(shop_id=owner_id, status__lt=2).count()
    return deals


def get_shop_close_deals_count(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=3).count()
    return deals


# ---------------Сделки юзера по id -------------------
def get_user_dispute_deals(buyer_id):
    deals = Deal.objects(buyer_id=buyer_id, status=2)
    return list(reversed(deals))


def get_user_open_deals(buyer_id):
    deals = Deal.objects(buyer_id=buyer_id, status__lt=2)
    return list(reversed(deals))


def get_user_close_deals(buyer_id):
    deals = Deal.objects(buyer_id=buyer_id, status=3)
    return list(reversed(deals))


# ---------------------Кол-во--------------------------

def get_user_dispute_deals_count(buyer_id):
    deals = Deal.objects(buyer_id=buyer_id, status=2).count()
    return deals


def get_user_open_deals_count(buyer_id):
    deals = Deal.objects(buyer_id=buyer_id, status__lt=2).count()
    return deals


def get_user_close_deals_count(buyer_id):
    deals = Deal.objects(buyer_id=buyer_id, status=3).count()
    return deals


# ---------------------- Заказы магазина по id владельца --------------
def get_shop_dispute_orders(owner_id):
    orders = Order.objects(shop_id=owner_id, status=3)
    return list(reversed(orders))


def get_shop_open_orders(owner_id):
    orders = Order.objects(shop_id=owner_id, status__lt=3)
    return list(reversed(orders))


def get_shop_close_orders(owner_id):
    orders = Order.objects(shop_id=owner_id, status=4)
    return list(reversed(orders))


# ---------------------- Кол-во
def get_shop_dispute_orders_count(owner_id):
    orders = Order.objects(shop_id=owner_id, status=3).count()
    return orders


def get_shop_open_orders_count(owner_id):
    orders = Order.objects(shop_id=owner_id, status__lt=3).count()
    return orders


def get_shop_close_orders_count(owner_id):
    orders = Order.objects(shop_id=owner_id, status=4).count()
    return orders


# ----------------------- Заказы юзера по id --------------------------
def get_user_dispute_orders(chat_id):
    orders = Order.objects(client_id=chat_id, status=3)
    return list(reversed(orders))


def get_user_open_orders(chat_id):
    orders = Order.objects(client_id=chat_id, status__lt=3)
    return list(reversed(orders))


def get_user_close_orders(chat_id):
    orders = Order.objects(client_id=chat_id, status=4)
    return list(reversed(orders))


# ------------------------Кол-во заказов по id --------------------------
def get_user_dispute_orders_count(chat_id):
    orders = Order.objects(client_id=chat_id, status=3).count()
    return orders


def get_user_open_orders_count(chat_id):
    orders = Order.objects(client_id=chat_id, status__lt=3).count()
    return orders


def get_user_close_orders_count(chat_id):
    orders = Order.objects(client_id=chat_id, status=4).count()
    return orders


# ------------------------------------------------------------------
def shop_sum_freeze_deals_money(shop_id):
    sum_price = Deal.objects(shop_id=shop_id, status__ne=3, payment_method="LITECOIN").sum('sum_price')
    return sum_price


def get_sum_shop_order_rating(owner_id):
    orders = Order.objects(shop_id=owner_id, status=4, like__ne=None)
    likes = 0
    if len(orders) > 0:
        for order in orders:
            if order.like is True:
                likes += 1
    else:
        return 0
    return likes / len(orders) * 100


def get_sum_shop_deal_rating(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=3, like__ne=None)
    likes = 0
    if len(deals) > 0:
        for deal in deals:
            if deal.like is True:
                likes += 1
    else:
        return 0
    return likes / len(deals) * 100


def get_count_likes_deal(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=3, like=True).count()
    return deals


def get_count_dislikes_deal(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=3, like=False).count()
    return deals


def get_count_likes_order(owner_id):
    orders = Order.objects(shop_id=owner_id, status=4, like=True).count()
    return orders


def get_count_dislikes_order(owner_id):
    orders = Order.objects(shop_id=owner_id, status=4, like=False).count()
    return orders


def shop_sum_freeze_orders_money(owner_id):
    sum_price = Order.objects(shop_id=owner_id, status__ne=4).sum('price')
    return sum_price


def count_open_buys(user_id):
    deals = Deal.objects(buyer_id=user_id, status__ne=3).count()
    return deals


def count_open_deals(shop_id):
    deals = Deal.objects(shop_id=shop_id, status__ne=3).count()
    return deals


def count_open_cl_orders(user_id):
    orders = Order.objects(client_id=user_id, status__ne=4).count()
    return orders


def count_open_sh_orders(owner_id):
    orders = Order.objects(shop_id=owner_id, status__ne=4).count()
    return orders


def get_deals_moder_call():
    deals = Deal.objects(status=2, potential=True, call_moderator=True)
    return deals


def get_orders_moder_call():
    orders = Order.objects(status=3, potential=True, call_moderator=True)
    return orders


def get_deal_messages(deal):
    messages = deal.messages
    if not messages:
        return "<i>Нет сообщений</i>"
    messages_text = ""
    for mes in messages:
        messages_text += mes + "\n"
    return messages_text


def get_order_messages(order):
    messages = order.messages
    if not messages:
        return "<i>Нет сообщений</i>"
    messages_text = ""
    for mes in messages:
        messages_text += mes + "\n"
    return messages_text


def get_service_by_id(service_id):
    service = Service.objects(id=service_id).first()
    return service


def get_my_service_packets_menu(update, context, chat_id, name):
    menu = [[]]
    if SELECT_SERV_ID not in context.user_data:
        return context.bot.sendMessage(chat_id, "Не актуально")
    service_id = context.user_data[SELECT_SERV_ID]
    service = get_service_by_id(service_id)
    if not service.eco_description:
        menu.append([InlineKeyboardButton(f'➕  Добавить пакет "Эконом"', callback_data='service_add_packet_eco')])
    else:
        menu.append([InlineKeyboardButton(f'Редактировать пакет "Эконом"', callback_data='service_edit_packet_eco')])
    if not service.standart_description:
        menu.append([InlineKeyboardButton(f'➕  Добавить пакет "Стандарт"', callback_data='service_add_packet_standart')])
    else:
        menu.append(
            [InlineKeyboardButton(f'Редактировать пакет "Стандарт"', callback_data='service_edit_packet_standart')])
    if not service.biz_description:
        menu.append([InlineKeyboardButton(f'➕  Добавить пакет "Бизнес"', callback_data='service_add_packet_biz')])
    else:
        menu.append([InlineKeyboardButton(f'Редактировать пакет "Бизнес"', callback_data='service_edit_packet_biz')])
    if name == "add_service":
        menu.append([InlineKeyboardButton(f'{back_for_button}  К услуге',
                                          callback_data='back_to_my_shop_select_service_menu')])
    elif name == "my_service":
        context.user_data[DATA] = 'my_list_services'
        context.user_data[CATEGORY_INFO]['cat_id'] = context.user_data[CATEGORY_INFO]['cat_id']
        context.user_data[CATEGORY_INFO]['cat_path'] = context.user_data[CATEGORY_INFO]['cat_path']
        menu.append([InlineKeyboardButton(f'{back_for_button}  К услуге',
                                          callback_data='back_to_my_shop_select_service_menu')])
    return menu


def get_cat_my_services_tree(context, update, owner_id):
    services = Service.objects(owner_id=owner_id)
    for serv in services:
        try:
            context.user_data[CATEGORY_SERVICES].index(serv.category_id)
        except Exception:
            get_services_sub_category(context, serv.category_id)


def get_cat_services_tree(context, update, chat_id):
    services = Service.objects()
    for serv in services:
        if not check_shop_banned(serv.owner_id) and not check_shop_stop(serv.owner_id) and not check_shop_pause(serv.owner_id):
            try:
                context.user_data[CATEGORY_SERVICES].index(serv.category_id)
            except Exception:
                get_services_sub_category(context, serv.category_id)


def get_cat_services_shop_tree(context, update):
    chat_id = update.callback_query.message.chat.id
    owner_id = context.user_data[SELECT_ID]
    services = Service.objects(owner_id=owner_id)
    for serv in services:
        if not check_shop_banned(serv.owner_id) and not check_shop_stop(serv.owner_id) and not check_shop_pause(serv.owner_id):
            try:
                context.user_data[CATEGORY_PRODS].index(serv.category_id)
            except Exception:
                get_services_sub_category(context, serv.category_id)


def get_services_sub_category(context, cat_id):
    cat = ServiceCategory.objects(id=cat_id).first()
    if not cat:
        return
    context.user_data[CATEGORY_SERVICES].append(cat.id)
    if cat.sub_id is None:
        return
    return get_services_sub_category(context, cat.sub_id)


def get_service_info(owner_id, context, service_id):
    service = Service.objects(id=service_id).first()
    if not service:
        context.bot.sendMessage(owner_id, "Ошибка")
        return print('Ошибка в выбранном id услуги')
    if CATEGORY_INFO not in context.user_data:
        return context.bot.sendMessage(owner_id, "Не актуально")
    shop = Shop.objects(owner_id=service.owner_id).first()
    shop_name = shop.shop_name
    shop_id = shop.shop_id
    ltc_price = get_ltc_by_rub(service.min_price)
    if service.eco_description:
        eco_packet = "Добавлен"
    else:
        eco_packet = "Отсутствует"
    if service.standart_description:
        standart_packet = "Добавлен"
    else:
        standart_packet = "Отсутствует"
    if service.biz_description:
        biz_packet = "Добавлен"
    else:
        biz_packet = "Отсутствует"
    info = f"\n\n<b>Магазин:</b>  {shop_name}  ({shop_id})\n\n" \
           f"Категория:\n{context.user_data[CATEGORY_INFO]['cat_path']}\n" \
           f"<b>Название:</b>  {service.name}\n\n" \
           f"<b>Описание:</b>  {service.description}\n\n" \
           f"<b>Минимальная стоимость:</b>  {service.min_price} ₽  ({ltc_price} LITECOIN)\n" \
           f"<b>Пакет эконом:</b>  {eco_packet}\n" \
           f"<b>Пакет стандарт:</b>  {standart_packet}\n" \
           f"<b>Пакет бизнес:</b>  {biz_packet}"
    return info


def get_service_picture_id(service_id):
    serv = Service.objects(id=service_id).first()
    return serv.picture


def add_order(shop_id, client_id, service_id, category, price, price_ltc, tz, packet, status, deadline_days):
    return Order(shop_id=shop_id, client_id=client_id, service_id=service_id, category=category, price=price,
                 price_ltc=price_ltc, tz=tz,
                 packet=packet, status=status, deadline_days=deadline_days).save()


def get_order_status_text(status):
    if status == 0:
        return "Ожидает подтверждение исполнителя"
    elif status == 1:
        return "Ожидает подтверждение заказчика"
    elif status == 2:
        return "В работе"
    elif status == 3:
        return "Диспут"
    elif status == 4:
        return "Завершен"


def get_client_order_menu(order_id, order_status, context):
    menu = [[]]
    order = get_order_by_id(order_id)
    if order_status == 0:
        menu = [[InlineKeyboardButton(f"📩  Написать исполнителю",
                                      callback_data=f'order_client_message_{order_id}')],
                [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_client_tz_{order_id}')],
                [InlineKeyboardButton(f"Отменить", callback_data=f'order_client_cancel_{order_id}')]]
    elif order_status == 1:
        menu = [[InlineKeyboardButton(f"Подтвердить", callback_data=f'order_client_confirm_{order_id}'),
                 InlineKeyboardButton(f"Отменить", callback_data=f'order_client_cancel_{order_id}')],
                [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_client_tz_{order_id}')],
                [InlineKeyboardButton(f"📩  Написать исполнителю",
                                      callback_data=f'order_client_message_{order_id}')]]
    elif order_status == 2:
        menu = [
            [InlineKeyboardButton(f"📩  Написать исполнителю", callback_data=f'order_client_message_{order_id}')],
            [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_client_tz_{order_id}')],
            [InlineKeyboardButton(f"Завершить заказ", callback_data=f'order_client_close_{order_id}')]
        ]
        now = datetime.now()
        if now > order.date_deadline or order.order_work is not None:
            menu.append([InlineKeyboardButton(f"Открыть Диспут", callback_data=f'order_client_dispute_{order_id}')])
        if order.order_work is not None:
            menu.append(
                [InlineKeyboardButton(f"Выполненный заказ", callback_data=f'order_client_get_service_{order_id}')])
    elif order_status == 3:
        if order.call_moderator is False:
            send_button_text = f"📩  Написать исполнителю"
        else:
            send_button_text = f"📩  Написать в Диспут"

        menu = [[InlineKeyboardButton(f"Завершить заказ", callback_data=f'order_client_close_{order_id}')],
                [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_client_tz_{order_id}')],
                [InlineKeyboardButton(f"{send_button_text}", callback_data=f'order_client_message_{order_id}')]]

        if order.order_work is not None:
            menu.append(
                [InlineKeyboardButton(f"Выполненный заказ", callback_data=f'order_client_get_service_{order_id}')])
        now = datetime.now()
        if ((order.potential is True) or (now > (order.date_deadline + timedelta(days=1)))) and order.call_moderator is False:
            menu.append([InlineKeyboardButton(f"Вызвать модератора",
                                              callback_data=f'order_client_moder_call_{order_id}')])
    elif order_status == 4:
        menu = [[InlineKeyboardButton(f"Выполненный заказ", callback_data=f'order_client_get_service_{order_id}')],
                [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_client_tz_{order_id}')]]
        if order.like is None:
            menu.append([InlineKeyboardButton(f'Like  {e_like}',
                                                                          callback_data=f'button_order_buyer_like_{order_id}'),
                                                     InlineKeyboardButton(f'Dislike  {e_dislike}',
                                                                          callback_data=f'button_order_buyer_dislike_{order_id}')
                                                     ])
        if order.comment is None:
            menu.append([InlineKeyboardButton(f"🗣  Оставить отзыв", callback_data=f'button_order_client_review_{order_id}')])

    if context.user_data is not None and SELECT_BUYS_SECTION in context.user_data:
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_orders_list')])
    return menu


def get_order_by_id(order_id):
    order = Order.objects(id=order_id).first()
    return order


def get_shop_order_menu(order_id, order_status, context):
    menu = [[]]
    order = get_order_by_id(order_id)
    if order_status == 0:
        if order.packet < 4:
            menu = [
                [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_shop_tz_{order_id}')],
                [InlineKeyboardButton(f"Принять заказ", callback_data=f'order_shop_accept_{order_id}'),
                 InlineKeyboardButton(f"Отказаться", callback_data=f'order_shop_cancel_{order_id}')],
                [InlineKeyboardButton(f"📩  Написать заказчику", callback_data=f'order_shop_message_{order_id}')]
            ]
        else:
            menu = [
                [InlineKeyboardButton(f"Оценить", callback_data=f'order_shop_grade_{order_id}'),
                 InlineKeyboardButton(f"Тех. задание", callback_data=f'order_shop_tz_{order_id}')],
                [InlineKeyboardButton(f"Принять заказ", callback_data=f'order_shop_accept_{order_id}'),
                 InlineKeyboardButton(f"Отказаться", callback_data=f'order_shop_cancel_{order_id}')],
                [InlineKeyboardButton(f"📩  Написать заказчику", callback_data=f'order_shop_message_{order_id}')]
            ]
    elif order_status == 1:
        menu = [[InlineKeyboardButton(f"Изменить оценку", callback_data=f'order_shop_grade_{order_id}')],
                [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_shop_tz_{order_id}')],
                [InlineKeyboardButton(f"📩  Написать заказчику", callback_data=f'order_shop_message_{order_id}')]]
    elif order_status == 2:
        menu = [
            [InlineKeyboardButton(f"Отправить заказ", callback_data=f'order_shop_send_order_work_{order_id}')],
            [InlineKeyboardButton(f"Тех. задание", callback_data=f'order_shop_tz_{order_id}')],
            [InlineKeyboardButton(f"📩  Написать заказчику", callback_data=f'order_shop_message_{order_id}')]
        ]
    elif order_status == 3:
        if order.call_moderator is False:
            send_button_text = f"📩  Написать заказчику"
        else:
            send_button_text = f"📩  Написать в Диспут"
        menu.append(
            [InlineKeyboardButton(f"Отправить заказ", callback_data=f'order_shop_send_order_work_{order_id}')])
        menu.append(
            [InlineKeyboardButton(f"{send_button_text}", callback_data=f'order_shop_message_{order_id}')])
    if context.user_data is not None and SELECT_SALE_SECTION in context.user_data:
        menu.append([InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_service_sales_list')])
    return menu


def get_order_info(order_id):
    order = get_order_by_id(order_id)
    if order is None:
        return "Заказ не найден"
    shop = get_shop_obj(order.shop_id)
    client = get_user_obj(order.client_id)
    service = get_service_by_id(order.service_id)
    if order.price is not None:
        price_info = str(order.price) + f" ₽  ({order.price_ltc} LITECOIN)"
    else:
        price_info = "Пока неизвестна"

    if order.packet == 1:
        packet_info = "Эконом"
        packet_description = service.eco_description
    elif order.packet == 2:
        packet_info = "Стандарт"
        packet_description = service.standart_description
    elif order.packet == 3:
        packet_info = "Бизнес"
        packet_description = service.biz_description
    elif order.packet == 4:
        packet_description = service.description
        packet_info = "Уникальный заказ"
    else:
        packet_description = "Ошибка"
        packet_info = "Ошибка"

    if order.deadline_days is not None:
        deadline_days_info = f"{order.deadline_days} дней"
    else:
        deadline_days_info = "Пока неизвестна"

    if order.date_start is not None:
        date_start_info = f"{order.date_start.strftime('%d-%m-%Y %H:%M')}"
    else:
        date_start_info = "Пока неизвестна"

    if order.date_deadline is not None:
        date_deadline_info = f"{order.date_deadline.strftime('%d-%m-%Y %H:%M')}"
    else:
        date_deadline_info = "Пока неизвестна"

    order_work_text = ""
    if order.status > 1:
        if order.order_work is None:
            order_work_text = "<b>Выполненная работа:</b> Не отправлена\n\n"
        else:
            order_work_text = "<b>Выполненная работа:</b> Отправлена\n\n"

    call_moder_text = ""
    if order.status == 3 and order.call_moderator is True:
        call_moder_text = "  <i>[Вызван модератор]</i>"

    info = f"⚠  <b>Информация о заказе</b>\n" \
           f"(/o{order.id})\n\n" \
           f"🏪  <b>Магазин:</b>  {shop.shop_name}  ({shop.shop_id})\n" \
           f"👤  <b>Заказчик:</b>  {client.first_name}  ({client.user_id})\n\n" \
           f"<b>Категория:</b>  {order.category}\n" \
           f"🤝  <b>Услуга:</b>  {service.name}\n\n" \
           f"<b>Пакет:</b>  {packet_info}\n" \
           f"<b>Описание:</b>  {packet_description}\n\n" \
           f"<b>Стоимость:</b>  {price_info}\n" \
           f"<b>Срок выполения:</b>  {deadline_days_info}\n\n" \
           f"<b>Статус:</b>  {get_order_status_text(order.status) + call_moder_text}\n\n" \
           f"<b>Дата начала выполнения:</b>  {date_start_info}\n" \
           f"<b>Крайняя дата готовности:</b>  {date_deadline_info}\n\n{order_work_text}"
    return info


# ------------ Список/поиск магазинов --------------
def get_moder_select_shop_menu(shop_id):
    shop = get_shop_obj(shop_id)
    if not shop.banned:
        menu = [
            [InlineKeyboardButton(f"{e_shopping_bags}  Продажи", callback_data='moder_select_shop_sales'),
             InlineKeyboardButton(f"История операций", callback_data='moder_select_shop_operations')],
            [InlineKeyboardButton(f"📦  Товары", callback_data='select_shop_products'),
             InlineKeyboardButton(f"🤝  Услуги", callback_data='select_shop_services')],
            [InlineKeyboardButton(f"🗣  Отзывы", callback_data='select_shop_comments'),
             InlineKeyboardButton(f"{e_stop_sign}  Заблокировать", callback_data='moder_select_shop_ban')],
            [InlineKeyboardButton(f"📩  Написать сообщение", callback_data=f'moder_shop_send_message_{shop_id}')],
            [InlineKeyboardButton(f"{back_for_button}  Список магазинов", callback_data='back_moder_select_shop')],
        ]
    else:
        menu = [
            [InlineKeyboardButton(f"{e_shopping_bags}  Продажи", callback_data='moder_select_shop_sales'),
             InlineKeyboardButton(f"История операций", callback_data='moder_select_shop_operations')],
            [InlineKeyboardButton(f"📦  Товары", callback_data='select_shop_products'),
             InlineKeyboardButton(f"🤝  Услуги", callback_data='select_shop_services')],
            [InlineKeyboardButton(f"🗣  Отзывы", callback_data='select_shop_comments'),
             InlineKeyboardButton(f"✳  Разблокировать", callback_data='moder_select_shop_ban')],
            [InlineKeyboardButton(f"📩  Написать сообщение", callback_data=f'moder_shop_send_message_{shop_id}')],
            [InlineKeyboardButton(f"{back_for_button}  Список магазинов", callback_data='back_moder_select_shop')],
        ]
    return menu


def get_shop_defeat_dispute(owner_id):
    deals = Deal.objects(shop_id=owner_id, defeat_dispute=True).count()
    return deals


def get_shop_successful_deals(owner_id):
    deals = Deal.objects(shop_id=owner_id, status=3, defeat_dispute=None).count()
    return deals


def update_last_active(owner_id):
    shop = get_shop_obj(owner_id)
    now = datetime.now()
    shop.update(last_active=now)


def get_users_balance():
    sum_balance = User.objects().sum('balance')
    return sum_balance


def get_shops_balance():
    sum_balance = Shop.objects().sum('balance')
    return sum_balance


def get_shops_guarantee():
    sum_get_shops_guarantee = Shop.objects().sum('guarantee')
    return sum_get_shops_guarantee


def get_shops_freeze_guarantee():
    shops_freeze_guarantee = Shop.objects().sum('freeze_guarantee')
    return shops_freeze_guarantee


def get_users_count():
    count = User.objects().count()
    return count

# def update(context, update):
#    users = User.objects()
#    shops = Shop.objects()
#    for user in users:
#        user.update(user_id="/u" + convert_base(user.chat_id, 16, 10))
#    for shop in shops:
#        shop.update(shop_id="/s" + convert_base(shop.owner_id, 32, 10))
