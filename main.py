import os

from mongoengine.connection import connect
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

from config import host_db, token
from handlers.buttons import button_market_select_service_packet_eco, button_market_select_service_packet_standart, \
    button_market_select_service_packet_biz, button_market_select_service_packet_unique
from handlers.commands import start_handler
from handlers.conversations import request_submit, set_request_shop_name, shop_moder_search, set_search_shop_name, \
    moder_user_search, set_search_user_name, set_request_shop_why, my_shop_settings_about, set_my_shop_about, \
    withdrawal_to_personal, input_guarantee_from_shop_acc, \
    input_guarantee_from_personal_acc, input_guarantee, set_search_user_id, set_search_shop_id, my_shop_settings_name, \
    set_my_shop_name, my_shop_finance_guarantee_withdrawal, input_withdrawal_guarantee, \
    input_withdrawal_sum, input_withdrawal_address, my_shop_withdrawal_from_service, my_shop_withdrawal_to_personal, \
    my_shop_finance_requisites_add, set_requisite_name, set_requisite_payment_system, set_requisite_account_number, \
    my_shop_finance_requisites_select_edit_name, my_shop_finance_requisites_select_edit_payment_system, \
    my_shop_finance_requisites_select_edit_account_number, set_requisite_info, start_add_product, set_product_info_name, \
    set_product_info_description, set_product_info_content, \
    product_add_content, button_my_shop_products_prod_count_add, button_change_prod_name, product_name_change, \
    button_change_prod_description, product_description_change, set_product_info_price, button_change_prod_price, \
    product_price_change, \
    set_product_info_content_text, product_add_content_text, button_market_select_prod_buy, buy_product_set_count, \
    my_shop_settings_check_time, set_my_shop_check_time, button_deal_buyer_message, deal_buyer_message_send, \
    deal_buyer_review_send, button_deal_shop_send_message, deal_shop_message_send, \
    button_deal_shop_give_change, deal_shop_change_give, button_moder_select_shop_message, \
    moder_select_shop_message_send, button_shop_answer_message, shop_answer_message_send, user_select_shop_message_send, \
    button_user_select_shop_message, button_call_menu_send_message, call_menu_message_send, my_shop_services_start_add, \
    set_add_service_name, \
    set_add_service_portfolio, set_add_service_min_price, set_add_service_picture, set_packet_price, \
    my_shop_add_service_eco_packet, set_packet_description, my_shop_add_service_standart_packet, \
    my_shop_add_service_biz_packet, my_shop_edit_service_packet_price, my_shop_edit_service_packet_description, \
    button_my_shop_service_menu_edit_name, service_name_change, \
    service_description_change, \
    button_service_change_min_price, service_min_price_change, button_service_change_portfolio, \
    service_portfolio_change, button_service_change_picture, service_picture_change, set_packet_deadline, \
    my_shop_edit_service_packet_deadline, set_add_service_description, button_service_change_description, \
    service_tz_send, button_order_client_message, order_client_message_send, button_order_shop_message, \
    order_shop_message_send, button_order_shop_send_order_work, order_shop_send_work, \
    order_review_client, button_order_shop_grade, order_grade_shop_price, order_grade_shop_deadline, \
    button_moder_select_call_order_menu_send_message, call_order_menu_message_send, \
    button_deal_buyer_comment, button_order_client, service_tz_send_text, button_change_terms_trade, \
    change_terms_trade_send, deal_shop_photo_send, deal_buyer_photo_send, order_client_photo_send, \
    order_shop_photo_send, set_request_shop_res, set_add_service_portfolio_skip
from handlers.others import echo_handler, query_handler, photo_handler, document_handler
from res.const import SET_REQUEST_SHOP_NAME, SET_SEARCH_SHOP_NAME, SET_SEARCH_USER_NAME, SET_REQUEST_SHOP_WHY, \
    SET_CHANGE_SHOP_ABOUT, SET_WITHDRAW_PERSONAL_SUM, SET_GUARANTEE_SUM, SET_SEARCH_USER_ID, SET_SEARCH_SHOP_ID, \
    SET_CHANGE_SHOP_NAME, SET_WITHDRAWAL_GUARANTEE_SUM, SET_WITHDRAWAL_SUM, SET_WITHDRAWAL_ADDRESS, SET_REQUISITE_NAME, \
    SET_REQUISITE_PAYMENT_SYSTEM, SET_REQUISITE_ACCOUNT_NUMBER, SET_REQUISITE_INFO, SET_PRODUCT_INFO_NAME, \
    SET_PRODUCT_INFO_DESCRIPTION, SET_PRODUCT_INFO_CONTENT, \
    PRODUCT_ADD_CONTENT, PRODUCT_CHANGE_NAME, PRODUCT_CHANGE_DESCRIPTION, \
    SET_PRODUCT_INFO_PRICE, PRODUCT_CHANGE_PRICE, PRODUCT_COUNT, SET_CHANGE_SHOP_CHECK_TIME, BUYER_MESSAGE, \
    BUYER_REVIEW, SHOP_SEND_MESSAGE, DEAL_SHOP_CHANGE, MODER_MESSAGE, SHOP_ANSWER_MESSAGE, USER_MESSAGE, \
    CALL_MENU_SEND_MESSAGE, SET_SERVICE_NAME, \
    SET_SERVICE_PORTFOLIO, SET_SERVICE_MIN_PRICE, SET_SERVICE_PICTURE, SET_PACKET_PRICE, SET_PACKET_DESCRIPTION, \
    CHANGE_SERVICE_NAME, CHANGE_SERVICE_MIN_PRICE, \
    CHANGE_SERVICE_PORTFOLIO, CHANGE_SERVICE_PICTURE, SET_PACKET_DEADLINE, SET_SERVICE_DESCRIPTION, \
    CHANGE_SERVICE_DESCRIPTION, CLIENT_SEND_TZ, CLIENT_MESSAGE, SHOP_ORDER_MESSAGE, SHOP_ORDER_WORK, \
    SHOP_ORDER_GRADE_PRICE, SHOP_ORDER_GRADE_DEADLINE, CALL_ORDER_MENU_SEND_MESSAGE, CLIENT_ORDER_COMMENT, TERMS_TRADE, \
    SET_REQUEST_SHOP_RES
from res.moderCategory import ModerCategoryProducts, ModerCategoryServices
from res.suggestCategory import SuggestCategory

connect('marketplace', host=host_db)
PORT = int(os.environ.get('PORT', '8443'))
TOKEN = token


def main():
    if connect:
        print('DB connected.')
    else:
        print('DB not connected.')
    print('Bot was started.')
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # ======= conv handlers =========
    # ============ Ввод названия магазина для отправки заявки на создание ========
    input_request_shop_name = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(request_submit, pattern='^' + 'request_submit' + '$', run_async=True)
        ],
        states={
            SET_REQUEST_SHOP_NAME: [
                MessageHandler(Filters.text, set_request_shop_name, True, run_async=True)
            ],
            SET_REQUEST_SHOP_WHY: [
                MessageHandler(Filters.text, set_request_shop_why, True, run_async=True)
            ],
            SET_REQUEST_SHOP_RES: [
                MessageHandler(Filters.text, set_request_shop_res, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler, run_async=True),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_request_shop_name)

    # ============ Ввод названия магазина для поиска ========
    input_search_shop_name = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(shop_moder_search, pattern='^' + 'moder_shop_search_name' + '$', run_async=True),
            CallbackQueryHandler(shop_moder_search, pattern='^' + 'moder_shop_search_id' + '$', run_async=True)
        ],
        states={
            SET_SEARCH_SHOP_NAME: [
                MessageHandler(Filters.text, set_search_shop_name, True, run_async=True)
            ],
            SET_SEARCH_SHOP_ID: [
                MessageHandler(Filters.text, set_search_shop_id, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler, run_async=True),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_search_shop_name)

    # ===============================
    # ============ Ввод имени пользователя для поиска ========
    input_search_user_name = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(moder_user_search, pattern='^' + 'moder_users_search_name' + '$', run_async=True),
            CallbackQueryHandler(moder_user_search, pattern='^' + 'moder_users_search_id' + '$', run_async=True)
        ],
        states={
            SET_SEARCH_USER_NAME: [
                MessageHandler(Filters.text, set_search_user_name, True, run_async=True)
            ],
            SET_SEARCH_USER_ID: [
                MessageHandler(Filters.text, set_search_user_id, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler, run_async=True),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_search_user_name)

    # ===============================
    # ============ Ввод описания/названия магазина для изменения ========
    input_change_myshop = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(my_shop_settings_about, pattern='^' + 'my_shop_settings_about' + '$', run_async=True),
            CallbackQueryHandler(my_shop_settings_name, pattern='^' + 'my_shop_settings_name' + '$', run_async=True),
            CallbackQueryHandler(my_shop_settings_check_time, pattern='^' + 'my_shop_settings_check_time' + '$',
                                 run_async=True)
        ],
        states={
            SET_CHANGE_SHOP_ABOUT: [
                MessageHandler(Filters.text, set_my_shop_about, True, run_async=True)
            ],
            SET_CHANGE_SHOP_NAME: [
                MessageHandler(Filters.text, set_my_shop_name, True, run_async=True)
            ],
            SET_CHANGE_SHOP_CHECK_TIME: [
                MessageHandler(Filters.text, set_my_shop_check_time, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler, run_async=True),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_change_myshop)

    # ============ Ввод суммы для внесения/вывода гаранта ========
    input_guarantee_sum = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(input_guarantee_from_shop_acc, pattern='^' + 'insert_guarantee_shop_acc' + '$',
                                 run_async=True),
            CallbackQueryHandler(input_guarantee_from_personal_acc, pattern='^' + 'insert_guarantee_personal_acc' + '$',
                                 run_async=True),
            CallbackQueryHandler(my_shop_finance_guarantee_withdrawal,
                                 pattern='^' + 'my_shop_finance_guarantee_withdrawal' + '$', run_async=True)
        ],
        states={
            SET_GUARANTEE_SUM: [
                MessageHandler(Filters.text, input_guarantee, True, run_async=True)
            ],
            SET_WITHDRAWAL_GUARANTEE_SUM: [
                MessageHandler(Filters.text, input_withdrawal_guarantee, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler, run_async=True),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(input_guarantee_sum)

    # ============ Ввод суммы и адреса для вывода LITECOIN ========
    input_withdrawal_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(my_shop_withdrawal_from_service, pattern='^' + 'my_shop_withdrawal_from_service' + '$',
                                 run_async=True),
        ],
        states={
            SET_WITHDRAWAL_SUM: [
                MessageHandler(Filters.text, input_withdrawal_sum, True, run_async=True)
            ],
            SET_WITHDRAWAL_ADDRESS: [
                MessageHandler(Filters.text, input_withdrawal_address, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler, run_async=True),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_withdrawal_handler)

    # ============ Ввод суммы для вывода на личный счёт ========
    input_sum_withdrawal_to_personal = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(my_shop_withdrawal_to_personal, pattern='^' + 'my_shop_withdrawal_to_personal' + '$')
        ],
        states={
            SET_WITHDRAW_PERSONAL_SUM: [
                MessageHandler(Filters.text, withdrawal_to_personal, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler, run_async=True),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_sum_withdrawal_to_personal)

    # ============ Добавление реквизита ========
    input_info_for_add_requisite = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(my_shop_finance_requisites_add, pattern='^' + 'my_shop_finance_requisites_add' + '$')
        ],
        states={
            SET_REQUISITE_NAME: [
                MessageHandler(Filters.text, set_requisite_name, True, run_async=True)
            ],
            SET_REQUISITE_PAYMENT_SYSTEM: [
                MessageHandler(Filters.text, set_requisite_payment_system, True, run_async=True)
            ],
            SET_REQUISITE_ACCOUNT_NUMBER: [
                MessageHandler(Filters.text, set_requisite_account_number, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_info_for_add_requisite)

    # ============ Ввод инфы для редактирования реквизита ========
    input_edit_requisite_info = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(my_shop_finance_requisites_select_edit_name,
                                 pattern='^' + 'my_shop_finance_requisites_select_edit_name' + '$',
                                 run_async=True),
            CallbackQueryHandler(my_shop_finance_requisites_select_edit_payment_system,
                                 pattern='^' + 'my_shop_finance_requisites_select_edit_payment_system' + '$',
                                 run_async=True),
            CallbackQueryHandler(my_shop_finance_requisites_select_edit_account_number,
                                 pattern='^' + 'my_shop_finance_requisites_select_edit_account_number' + '$',
                                 run_async=True)
        ],
        states={
            SET_REQUISITE_INFO: [
                MessageHandler(Filters.text, set_requisite_info, True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(input_edit_requisite_info)

    # ============ Ввод инфы для добавления товара ========
    input_add_product_info = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_add_product,
                                 pattern='^' + 'start_add_product' + '$',
                                 run_async=True)
        ],
        states={
            SET_PRODUCT_INFO_NAME: [
                MessageHandler(Filters.text, set_product_info_name, True)
            ],
            SET_PRODUCT_INFO_DESCRIPTION: [
                MessageHandler(Filters.text, set_product_info_description, True)
            ],
            SET_PRODUCT_INFO_CONTENT: [
                MessageHandler(Filters.document, set_product_info_content, True),
                MessageHandler(Filters.text, set_product_info_content_text, True)
            ],
            SET_PRODUCT_INFO_PRICE: [
                MessageHandler(Filters.text, set_product_info_price, True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(input_add_product_info)

    # Изменение названия товара
    product_change_name = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_change_prod_name, pattern='^' + 'change_prod_name' + '$')
        ],
        states={
            PRODUCT_CHANGE_NAME: [
                MessageHandler(Filters.text, product_name_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(product_change_name)

    # Изменение описания товара
    product_change_description = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_change_prod_description, pattern='^' + 'change_prod_description' + '$')
        ],
        states={
            PRODUCT_CHANGE_DESCRIPTION: [
                MessageHandler(Filters.text, product_description_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(product_change_description)

    # Изменение стоимости товара
    product_change_price = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_change_prod_price, pattern='^' + 'change_prod_price' + '$')
        ],
        states={
            PRODUCT_CHANGE_PRICE: [
                MessageHandler(Filters.text, product_price_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(product_change_price)

    # Пополнение товара
    product_content_add = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_my_shop_products_prod_count_add,
                                 pattern='^' + 'my_shop_products_prod_count_add' + '$')
        ],
        states={
            PRODUCT_ADD_CONTENT: [
                MessageHandler(Filters.document, product_add_content, True, run_async=True),
                MessageHandler(Filters.text, product_add_content_text, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(product_content_add)

    # Ввод количества товара
    product_count_input = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_market_select_prod_buy,
                                 pattern='^' + 'market_select_prod_buy' + '$')
        ],
        states={
            PRODUCT_COUNT: [
                MessageHandler(Filters.text, buy_product_set_count, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(product_count_input)

    # Написать магазину
    deal_buyer_send_message = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_deal_buyer_message,
                                 pattern='^deal_buyer_message_[0-9, A-Z, a-z]+'),
            CallbackQueryHandler(button_moder_select_shop_message,
                                 pattern='^' + 'moder_shop_send_message_[0-9, A-Z, a-z]+' + '$'),
            CallbackQueryHandler(button_user_select_shop_message,
                                 pattern='^' + 'user_shop_send_message_[0-9, A-Z, a-z]+' + '$')
        ],
        states={
            BUYER_MESSAGE: [
                MessageHandler(Filters.text, deal_buyer_message_send, True, run_async=True),
                MessageHandler(Filters.photo, deal_buyer_photo_send, True, run_async=True)
            ],
            MODER_MESSAGE: [
                MessageHandler(Filters.text, moder_select_shop_message_send, True, run_async=True)
            ],
            USER_MESSAGE: [
                MessageHandler(Filters.text, user_select_shop_message_send, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(deal_buyer_send_message)

    # Оставить отзыв
    deal_buy_review = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_deal_buyer_comment,
                                 pattern='^button_deal_buyer_review_[0-9, A-Z, a-z]+')
        ],
        states={
            BUYER_REVIEW: [
                MessageHandler(Filters.text, deal_buyer_review_send, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(deal_buy_review)

    # Написать покупателю
    deal_shop_send_message = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_deal_shop_send_message,
                                 pattern='^deal_shop_message_[0-9, A-Z, a-z]+'),
            CallbackQueryHandler(button_shop_answer_message,
                                 pattern='^shop_answer_message_[0-9, A-Z, a-z]+'),
        ],
        states={
            SHOP_SEND_MESSAGE: [
                MessageHandler(Filters.text, deal_shop_message_send, True, run_async=True),
                MessageHandler(Filters.photo, deal_shop_photo_send, True, run_async=True)
            ],
            SHOP_ANSWER_MESSAGE: [
                MessageHandler(Filters.text, shop_answer_message_send, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(deal_shop_send_message)

    # Сделать замену
    deal_shop_give_change = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_deal_shop_give_change,
                                 pattern='^deal_shop_change_[0-9, A-Z, a-z]+')
        ],
        states={
            DEAL_SHOP_CHANGE: [
                MessageHandler(Filters.text, deal_shop_change_give, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(deal_shop_give_change)

    # Написать в спор (модератор)
    call_menu_send_message = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_call_menu_send_message,
                                 pattern='moder_select_call_menu_send_message'),
        ],
        states={
            CALL_MENU_SEND_MESSAGE: [
                MessageHandler(Filters.text, call_menu_message_send, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(call_menu_send_message)

    # ============ Добавление услуги ========
    input_info_for_add_service = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(my_shop_services_start_add, pattern='^' + 'start_add_service' + '$')
        ],
        states={
            SET_SERVICE_NAME: [
                MessageHandler(Filters.text, set_add_service_name, True, run_async=True)
            ],
            SET_SERVICE_DESCRIPTION: [
                MessageHandler(Filters.text, set_add_service_description, True, run_async=True)
            ],
            SET_SERVICE_PORTFOLIO: [
                MessageHandler(Filters.document, set_add_service_portfolio, True, run_async=True),
                MessageHandler(Filters.text, set_add_service_portfolio_skip, True, run_async=True)
            ],
            SET_SERVICE_MIN_PRICE: [
                MessageHandler(Filters.text, set_add_service_min_price, True, run_async=True)
            ],
            SET_SERVICE_PICTURE: [
                MessageHandler(Filters.photo, set_add_service_picture, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )

    dp.add_handler(input_info_for_add_service)

    # Добавление пакета
    add_service_packet = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(my_shop_add_service_eco_packet, pattern='^' + 'service_add_packet_eco' + '$'),
            CallbackQueryHandler(my_shop_add_service_standart_packet,
                                 pattern='^' + 'service_add_packet_standart' + '$'),
            CallbackQueryHandler(my_shop_add_service_biz_packet, pattern='^' + 'service_add_packet_biz' + '$'),
            CallbackQueryHandler(my_shop_edit_service_packet_price,
                                 pattern='^' + 'my_shop_service_edit_packet_price' + '$'),
            CallbackQueryHandler(my_shop_edit_service_packet_description,
                                 pattern='^' + 'my_shop_service_edit_packet_description' + '$'),
            CallbackQueryHandler(my_shop_edit_service_packet_deadline,
                                 pattern='^' + 'my_shop_service_edit_packet_deadline' + '$')
        ],
        states={
            SET_PACKET_PRICE: [
                MessageHandler(Filters.text, set_packet_price, True, run_async=True)
            ],
            SET_PACKET_DESCRIPTION: [
                MessageHandler(Filters.text, set_packet_description, True, run_async=True)
            ],
            SET_PACKET_DEADLINE: [
                MessageHandler(Filters.text, set_packet_deadline, True, run_async=True)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(add_service_packet)

    # Изменение названия услуги
    service_change_name = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_my_shop_service_menu_edit_name,
                                 pattern='^' + 'my_shop_service_menu_edit_name' + '$')
        ],
        states={
            CHANGE_SERVICE_NAME: [
                MessageHandler(Filters.text, service_name_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(service_change_name)

    # Изменение описания услуги
    service_change_description = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_service_change_description,
                                 pattern='^' + 'my_shop_service_menu_edit_description' + '$')
        ],
        states={
            CHANGE_SERVICE_DESCRIPTION: [
                MessageHandler(Filters.text, service_description_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(service_change_description)

    # Изменение минимальной стоимости услуги
    service_change_min_price = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_service_change_min_price,
                                 pattern='^' + 'my_shop_service_menu_edit_price' + '$')
        ],
        states={
            CHANGE_SERVICE_MIN_PRICE: [
                MessageHandler(Filters.text, service_min_price_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(service_change_min_price)

    # Изменение портфолио
    service_change_portfolio = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_service_change_portfolio,
                                 pattern='^' + 'my_shop_service_menu_edit_portfolio' + '$')
        ],
        states={
            CHANGE_SERVICE_PORTFOLIO: [
                MessageHandler(Filters.document, service_portfolio_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(service_change_portfolio)

    # Изменение изображения
    service_change_picture = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_service_change_picture,
                                 pattern='^' + 'my_shop_service_menu_edit_picture' + '$')
        ],
        states={
            CHANGE_SERVICE_PICTURE: [
                MessageHandler(Filters.photo, service_picture_change, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(service_change_picture)

    # Отправка ТЗ
    service_send_tz = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_market_select_service_packet_eco,
                                 pattern='^' + 'market_select_service_packet_eco' + '$'),
            CallbackQueryHandler(button_market_select_service_packet_standart,
                                 pattern='^' + 'market_select_service_packet_standart' + '$'),
            CallbackQueryHandler(button_market_select_service_packet_biz,
                                 pattern='^' + 'market_select_service_packet_biz' + '$'),
            CallbackQueryHandler(button_market_select_service_packet_unique,
                                 pattern='^' + 'market_select_service_packet_unique' + '$')
        ],
        states={
            CLIENT_SEND_TZ: [
                MessageHandler(Filters.document, service_tz_send, True, run_async=True),
                MessageHandler(Filters.text, service_tz_send_text, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(service_send_tz)

    # Написать исполнителю
    order_client_message = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_order_client_message,
                                 pattern='^order_client_message_[0-9, A-Z, a-z]+'),
        ],
        states={
            CLIENT_MESSAGE: [
                MessageHandler(Filters.text, order_client_message_send, True, run_async=True),
                MessageHandler(Filters.photo, order_client_photo_send, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(order_client_message)

    # Написать заказчику
    order_shop_message = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_order_shop_message,
                                 pattern='^order_shop_message_[0-9, A-Z, a-z]+'),
        ],
        states={
            SHOP_ORDER_MESSAGE: [
                MessageHandler(Filters.text, order_shop_message_send, True, run_async=True),
                MessageHandler(Filters.photo, order_shop_photo_send, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(order_shop_message)

    # Отправка заказа заказчику
    order_shop_send_order_work = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_order_shop_send_order_work,
                                 pattern='^order_shop_send_order_work_[0-9, A-Z, a-z]+'),
        ],
        states={
            SHOP_ORDER_WORK: [
                MessageHandler(Filters.all, order_shop_send_work, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(order_shop_send_order_work)

    # Отзыв об услуге
    order_client_review = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_order_client,
                                 pattern='^button_order_client_review_[0-9, A-Z, a-z]+'),
        ],
        states={
            CLIENT_ORDER_COMMENT: [
                MessageHandler(Filters.text, order_review_client, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(order_client_review)

    # Оценка заказа Исполнителем
    order_grade_shop = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_order_shop_grade,
                                 pattern='^order_shop_grade_[0-9, A-Z, a-z]+'),
        ],
        states={
            SHOP_ORDER_GRADE_PRICE: [
                MessageHandler(Filters.text, order_grade_shop_price, True, run_async=True)
            ],
            SHOP_ORDER_GRADE_DEADLINE: [
                MessageHandler(Filters.text, order_grade_shop_deadline, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(order_grade_shop)

    # Написать в спор ЗАКАЗ (модератор)
    call_order_menu_send_message = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_moder_select_call_order_menu_send_message,
                                 pattern='moder_select_call_order_menu_send_message'),
        ],
        states={
            CALL_ORDER_MENU_SEND_MESSAGE: [
                MessageHandler(Filters.text, call_order_menu_message_send, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(call_order_menu_send_message)

    # Условия торговли
    change_terms_trade = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_change_terms_trade,
                                 pattern='change_terms_trade'),
        ],
        states={
            TERMS_TRADE: [
                MessageHandler(Filters.text, change_terms_trade_send, True, run_async=True)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(query_handler),
            MessageHandler(Filters.text, echo_handler, run_async=True)
        ],

        run_async=True
    )
    dp.add_handler(change_terms_trade)

    # Добавление категории
    dp.add_handler(ModerCategoryProducts.get_conv_add())
    dp.add_handler(ModerCategoryServices.get_conv_add())
    dp.add_handler(SuggestCategory.get_conv_add())

    # commands
    dp.add_handler(CommandHandler("start", start_handler, run_async=True))

    # message handler
    dp.add_handler(MessageHandler(filters=Filters.text | Filters.dice, callback=echo_handler, run_async=True))

    # photo handler
    dp.add_handler(MessageHandler(filters=Filters.photo, callback=photo_handler, run_async=True))

    # file handler
    dp.add_handler(MessageHandler(filters=Filters.document, callback=document_handler, run_async=True))

    # query handler
    dp.add_handler(CallbackQueryHandler(query_handler, run_async=True))

    updater.start_webhook(listen='0.0.0.0',
                          port=8443,
                          url_path=TOKEN,
                          key='/etc/ssl/private/nassau_ink.key',
                          cert='/etc/ssl/certs/nassau_ink.pem',
                          webhook_url=f'https://nassau.ink:8443/{TOKEN}')

    print('Webhook was starting.')

    #updater.start_polling()
    #updater.idle()


if __name__ == '__main__':
    main()
