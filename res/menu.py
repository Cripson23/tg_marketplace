from telegram import ReplyKeyboardMarkup, InlineKeyboardButton
from res.const import e_shopping_bags, e_briefcase, e_info, e_credit_card, e_store, e_policeman, url_user_agreement, \
    e_check_mark, e_money_bag, e_dollar_banknote, back_for_button, \
    e_loudspeaker, e_memo, e_find_loop, e_pencil, e_page, url_news_channel, url_chat, \
    e_top, e_handshake, e_stop_sign, e_wrench, e_broken_heart, \
    url_changer, e_waving_hand, e_cross_mark, SELECT_ID, url_support

# ============================================== РЕГИСТРАЦИЯ ==========================================================

reg_menu = [
    [InlineKeyboardButton(f"Пользовательское соглашение", url=url_user_agreement)],
    [InlineKeyboardButton(f"Ознакомился, согласен   {e_check_mark}", callback_data='user_agree')],
]

# ============================================== ГЛАВНОЕ МЕНЮ =========================================================

# -------- КНОПКИ -------

button_market = f'🛒   Рынок'
button_dashboard = f'{e_briefcase}   Личный кабинет'
button_settings = f'{e_wrench}   Настройки [В разработке]'
button_about = f'{e_info}   О сервисе'
button_my_shop = f'{e_store}   Мой магазин'
button_section_moderator = f'{e_policeman}   Раздел модератора'

# -------- МЕНЮ --------
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [button_market, button_dashboard],
        [button_settings, button_about],
    ],
    resize_keyboard=True
)

# ========================================= РЫНОК ======================================================

select_market_section = [
    [InlineKeyboardButton(f"📦  Товары", callback_data='select_market_section_products'),
     InlineKeyboardButton(f"🤝  Услуги", callback_data='select_market_section_services')],
]

market_select_prod_menu = [
    [InlineKeyboardButton(f"Купить товар", callback_data='market_select_prod_buy')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_prev_cat_menu')],
]

market_select_service_menu = [
    [InlineKeyboardButton(f"🗣  Отзывы", callback_data='market_select_service_comments')],
    [InlineKeyboardButton(f"Портфолио", callback_data='market_select_service_portfolio')],
    [InlineKeyboardButton(f"Сделать заказ", callback_data='market_select_service_order')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_prev_serv_cat_menu')],
]

# ========================================== ЛИЧНЫЙ КАБИНЕТ ============================================================
dashboard_menu = [
    [InlineKeyboardButton(f"{e_credit_card}  Пополнить баланс", callback_data='balance_menu')],
    [InlineKeyboardButton(f"🏦  История пополнений", callback_data='submenu_up_balance_history')],
    [InlineKeyboardButton(f"{e_shopping_bags}  История покупок", callback_data='submenu_my_buys')],
    [InlineKeyboardButton(f"{e_waving_hand}  Открыть магазин", callback_data='submenu_open_shop')],
    # [InlineKeyboardButton(f"Реферальная система", callback_data='submenu_ref_system')],
]

# ------------ Пополнить LITECOIN ---------------
balance_menu = [
    [InlineKeyboardButton(f'Внести', callback_data='submenu_up_balance'),
     InlineKeyboardButton(f'Купить', url=url_changer)],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_dashboard_menu')]
]

# ------------ Внести LITECOIN ---------------
up_balance_menu = [
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_submenu_balance_menu'),
     InlineKeyboardButton(f'Найти перевод', callback_data='check_up_balance')]
]

# ------------ Открыть магазин ---------------
request_open_shop_menu = [
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_dashboard_menu'),
     InlineKeyboardButton(f'Оставить заявку', callback_data='request_submit')],
]

# =========================================== НАСТРОЙКИ =========================================================
settings_menu = [

]

# ============================================== О СЕРВИСЕ =============================================================
about_service_menu = [
    [InlineKeyboardButton(f"Новости", url=url_news_channel), InlineKeyboardButton(f"Общий чат", url=url_chat)],
    [InlineKeyboardButton(f"Пользов. соглашение", url=url_user_agreement),
     InlineKeyboardButton(f"Тех. поддержка", url=url_support)]
]

# ============================================== МОЙ МАГАЗИН  ======================================================
my_shop_menu = [
    [InlineKeyboardButton(f"{e_shopping_bags}  Продажи", callback_data='my_shop_submenu_trades')],
    [InlineKeyboardButton(f"📦  Мои товары", callback_data='my_shop_submenu_products'),
     InlineKeyboardButton(f"🤝  Мои услуги", callback_data='my_shop_submenu_services')],
    [InlineKeyboardButton(f"{e_money_bag}  Финансы", callback_data='my_shop_submenu_finance'),
     InlineKeyboardButton(f"{e_loudspeaker}  Реклама [В разработке]", callback_data='my_shop_submenu_adv')],
    [InlineKeyboardButton(f"🗣  Отзывы", callback_data='my_shop_comments'),
     InlineKeyboardButton(f"{e_wrench}  Настройки", callback_data='my_shop_submenu_settings')]
]

# ---------------------- МОИ ТОВАРЫ -------------------------
my_shop_submenu_products = [
    [InlineKeyboardButton(f"{e_page}  Изменить товар", callback_data='my_shop_products_list'),
     InlineKeyboardButton(f"➕  Добавить товар", callback_data='my_shop_products_add')],
    [InlineKeyboardButton(f"🆕  Предложить категорию", callback_data='my_shop_suggest_category_products')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_menu')]
]

my_shop_submenu_products_prod_menu = [
    [InlineKeyboardButton(f"{e_pencil}  Редактировать", callback_data='my_shop_products_prod_edit'),
     InlineKeyboardButton(f"➕  Пополнить", callback_data='my_shop_products_prod_count_add')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_prev_cat_menu'),
     InlineKeyboardButton(f'{e_cross_mark}  Удалить', callback_data='my_shop_products_prod_del')]
]

my_shop_product_edit_menu = [
    [InlineKeyboardButton(f"Название", callback_data='change_prod_name'),
     InlineKeyboardButton(f"Описание", callback_data='change_prod_description')],
    [InlineKeyboardButton(f"Стоимость", callback_data='change_prod_price')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_prod_menu')]
]

my_shop_products_prod_del_accept = [
    [InlineKeyboardButton(f'{back_for_button}  Отмена', callback_data='back_to_prod_menu'),
     InlineKeyboardButton(f"Подтвердить", callback_data='my_shop_products_prod_del_accept')]
]

# ---------------------- МОИ УСЛУГИ -------------------------
my_shop_submenu_services = [
    [InlineKeyboardButton(f"{e_page}  Изменить услугу", callback_data='my_shop_services_list'),
     InlineKeyboardButton(f"➕  Добавить услугу", callback_data='my_shop_services_add')],
    [InlineKeyboardButton(f"🆕  Предложить категорию", callback_data='my_shop_suggest_category_services')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_menu')]
]

my_shop_select_service_menu = [
    [InlineKeyboardButton(f"Портфолио", callback_data='my_shop_service_menu_portfolio'),
     InlineKeyboardButton(f"Пакеты", callback_data='my_shop_service_menu_packets')],
    [InlineKeyboardButton(f"{e_pencil}  Редактировать", callback_data='my_shop_service_menu_edit'),
     InlineKeyboardButton(f"{e_cross_mark}  Удалить", callback_data='my_shop_service_menu_delete')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_prev_serv_cat_menu')]
]

my_shop_select_service_menu_edit = [
    [InlineKeyboardButton(f"Название", callback_data='my_shop_service_menu_edit_name'),
     InlineKeyboardButton(f"Описание", callback_data='my_shop_service_menu_edit_description')],
    [InlineKeyboardButton(f"Мин. стоимость", callback_data='my_shop_service_menu_edit_price')],
    [InlineKeyboardButton(f"Портфолио", callback_data='my_shop_service_menu_edit_portfolio'),
     InlineKeyboardButton(f"Изображение", callback_data='my_shop_service_menu_edit_picture')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_select_service_menu')]
]

my_shop_service_edit_packet = [
    [InlineKeyboardButton(f"Изменить стоимость", callback_data='my_shop_service_edit_packet_price'),
     InlineKeyboardButton(f"Изменить описание", callback_data='my_shop_service_edit_packet_description')],
    [InlineKeyboardButton(f'{e_cross_mark}  Удалить', callback_data='my_shop_service_edit_packet_del'),
     InlineKeyboardButton(f'Изменить срок выполнения', callback_data='my_shop_service_edit_packet_deadline')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_service_packets_menu')]
]

# ------------- Финансы -------------------
my_shop_submenu_finance = [
    [InlineKeyboardButton(f"{e_dollar_banknote}  Вывод", callback_data='my_shop_finance_withdrawal'),
     InlineKeyboardButton(f"{e_handshake}  Гарант", callback_data='my_shop_finance_guarantee')],
    [InlineKeyboardButton(f"{e_credit_card}   Мои реквизиты", callback_data='my_shop_finance_requisites'),
     InlineKeyboardButton(f"История операций", callback_data='my_shop_finance_operations')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_menu')]
]

# РЕКЛАМА
my_shop_submenu_adv = [
    [InlineKeyboardButton(f"Рассылка покупателям", callback_data='my_shop_adv_mailing'),
     [InlineKeyboardButton(f"Промокод на скидку", callback_data='my_shop_adv_promo')]],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_menu')]
]

# Вывод
my_shop_finance_withdrawal = [
    [InlineKeyboardButton(f"Вывод из сервиса", callback_data='my_shop_withdrawal_from_service'),
     InlineKeyboardButton(f"Вывод на Личный счет", callback_data='my_shop_withdrawal_to_personal')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_finance_menu')]
]

# Мои реквизиты
my_shop_finance_requisites = [
    [InlineKeyboardButton(f"{e_page}  Все реквизиты", callback_data='my_shop_finance_requisites_all'),
     InlineKeyboardButton(f"Добавить реквизит", callback_data='my_shop_finance_requisites_add')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_shop_finance_menu')]
]

my_shop_finance_requisites_select_menu = [
    [InlineKeyboardButton(f"{e_pencil}  Редактировать", callback_data='my_shop_finance_requisites_select_edit'),
     InlineKeyboardButton(f"{e_cross_mark}  Удалить", callback_data='my_shop_finance_requisites_select_del')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_shop_finance_requisites')]
]

my_shop_finance_requisites_select_edit_menu = [
    [InlineKeyboardButton(f"Название", callback_data='my_shop_finance_requisites_select_edit_name'),
     InlineKeyboardButton(f"Платежную систему", callback_data='my_shop_finance_requisites_select_edit_payment_system')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_my_shop_finance_requisites_select_menu'),
     InlineKeyboardButton(f"Номер счёта", callback_data='my_shop_finance_requisites_select_edit_account_number')]
]

# Гарант
my_shop_finance_guarantee = [
    [InlineKeyboardButton(f"{e_handshake}  Внести гарант", callback_data='my_shop_finance_guarantee_up'),
     InlineKeyboardButton(f"{e_broken_heart}  Вывести гарант", callback_data='my_shop_finance_guarantee_withdrawal')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_finance_menu')]
]

# Внесение гаранта
my_shop_finance_guarantee_up_menu = [
    [InlineKeyboardButton(f"{e_top}  Со счета магазина", callback_data='insert_guarantee_shop_acc'),
     InlineKeyboardButton(f"С личного счета  {e_top}", callback_data='insert_guarantee_personal_acc')],
    [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_finance_guarantee')]
]


def get_my_shop_submenu_settings(shop):
    if not shop.pause_trade:
        my_shop_submenu_settings = [
            [InlineKeyboardButton(f"{e_pencil}  Изменить название", callback_data='my_shop_settings_name')],
            [InlineKeyboardButton(f"{e_memo}  Изменить описание", callback_data='my_shop_settings_about')],
            [InlineKeyboardButton(f"⏱  Время проверки товара", callback_data='my_shop_settings_check_time')],
            [InlineKeyboardButton(f"⏸  Остановить торговлю", callback_data='my_shop_settings_pause_trade')],
            [InlineKeyboardButton(f"📑  Условия торговли", callback_data='my_shop_settings_terms')],
            [InlineKeyboardButton(f"{e_cross_mark}  Закрыть магазин", callback_data='my_shop_settings_stop')],
            [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_menu')]
        ]
    else:
        my_shop_submenu_settings = [
            [InlineKeyboardButton(f"{e_pencil}  Изменить название", callback_data='my_shop_settings_name')],
            [InlineKeyboardButton(f"{e_memo}  Изменить описание", callback_data='my_shop_settings_about')],
            [InlineKeyboardButton(f"⏱  Время проверки товара", callback_data='my_shop_settings_check_time')],
            [InlineKeyboardButton(f"▶  Возобновить торговлю", callback_data='my_shop_settings_pause_trade')],
            [InlineKeyboardButton(f"📑  Условия торговли", callback_data='my_shop_settings_terms')],
            [InlineKeyboardButton(f"{e_cross_mark}  Закрыть магазин", callback_data='my_shop_settings_stop')],
            [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_to_my_shop_menu')]
        ]
    return my_shop_submenu_settings


# Подтверждение остановки торговли
my_shop_setting_stop_confirmation = [
    [InlineKeyboardButton(f"{e_check_mark}   Подтверждаю", callback_data='my_shop_settings_stop_confirmed'),
     InlineKeyboardButton(f"{back_for_button}   Отмена", callback_data='back_to_my_shop_submenu_settings')],
]

# =========================================== РАЗДЕЛ МОДЕРАТОРА =======================================================
moderator_menu = [
    [InlineKeyboardButton(f"{e_page}  Список вызовов", callback_data='submenu_moder_calls'),
     InlineKeyboardButton(f"{e_find_loop}  Поиск пользователя", callback_data='submenu_moder_users')],
    [InlineKeyboardButton(f"💣  Категории", callback_data='moder_category_select_section'),
     InlineKeyboardButton(f"{e_store}  Магазины", callback_data='submenu_moder_shops')],
    [InlineKeyboardButton(f"💰  Бухгалтерия", callback_data='submenu_moder_bookkeeping')]
]

select_section_calls = [
    [InlineKeyboardButton(f"Сделки", callback_data='submenu_moder_calls_deals'),
     InlineKeyboardButton(f"Заказы", callback_data='submenu_moder_calls_orders')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_menu')]
]

# ----------- Поиск пользователя (выбор способа) ----------
moder_find_user_menu = [
    [InlineKeyboardButton(f"Поиск по имени TG", callback_data='moder_users_search_name'),
     InlineKeyboardButton(f"Поиск по ID", callback_data='moder_users_search_id')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_menu')]
]

# ----------- Поиск магазина (выбор способа) ----------
shop_moder_find_menu = [
    [InlineKeyboardButton(f"Поиск по названию", callback_data='moder_shop_search_name'),
     InlineKeyboardButton(f"Поиск по ID", callback_data='moder_shop_search_id')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_search_shop')]
]

# ------------- МАГАЗИНЫ ------------------
shop_moder_menu = [
    [InlineKeyboardButton(f"{e_page}  Список магазинов", callback_data='shop_moder_list'),
     InlineKeyboardButton(f"{e_find_loop}  Поиск магазина", callback_data='shop_moder_search')],
    [InlineKeyboardButton(f"{e_waving_hand}  Заявки на открытие", callback_data='shop_moder_requests'),
     InlineKeyboardButton(f"🆕  Заявки на категории", callback_data='shop_moder_category_suggest_select_section')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_menu')]
]

# ------------ Поиск пользователя --------------
moder_select_user_menu = [
    [InlineKeyboardButton(f"Покупки", callback_data='moder_select_user_buys'),
     InlineKeyboardButton(f"История пополнений", callback_data='moder_select_user_payments')],
    [InlineKeyboardButton(f"{e_stop_sign}  Заблокировать", callback_data='moder_select_user_ban')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_search_user')]
]

# ----------- Выбор сделки-вызова ---------------
moder_select_call_menu = [
    [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_menu_messages'),
     InlineKeyboardButton(f"Товар", callback_data='moder_select_call_menu_content')],
    [InlineKeyboardButton(f"Закрыть сделку", callback_data='moder_select_call_menu_close_deal')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_call_list_deals')]
]

moder_select_call_menu_messages = [
    [InlineKeyboardButton(f"📩  Написать сообщение", callback_data='moder_select_call_menu_send_message')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_select_deal_call_menu')]
]

# -------- Выбор заказа-вызова ------------
moder_select_call_order_menu = [
    [InlineKeyboardButton(f"Техническое задание", callback_data='moder_select_call_order_menu_tz'),
     InlineKeyboardButton(f"Выполненный заказ", callback_data='moder_select_call_order_menu_work')],
    [InlineKeyboardButton(f"Сообщения", callback_data='moder_select_call_order_menu_messages'),
     InlineKeyboardButton(f"Закрыть заказ", callback_data='moder_select_call_order_menu_close')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_call_list_orders')]
]

moder_select_call_order_menu_messages = [
    [InlineKeyboardButton(f"📩  Написать сообщение", callback_data='moder_select_call_order_menu_send_message')],
    [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_select_order_call_menu')]
]


# -------------- Меню для одобрения/отклонения заявки ---------------
def shop_moder_requests_approved_menu(shop_creator_id):
    menu = [
        [InlineKeyboardButton(f"Одобрить заявку", callback_data=f'shop_moder_requests_approved_yes_{shop_creator_id}'),
         InlineKeyboardButton(f"Отклонить заявку", callback_data=f'shop_moder_requests_approved_no_{shop_creator_id}')],
        [InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_shop_moder_requests_approved_menu')]
    ]
    return menu


# ==================== Просмотр инфы о магазине ==============================
# ---------- Меню выбора магазина -----------
user_select_shop_menu = [
    [InlineKeyboardButton(f"📦  Товары", callback_data='select_shop_products'),
     InlineKeyboardButton(f"🤝  Услуги", callback_data='select_shop_services')],
    [InlineKeyboardButton(f"🗣  Отзывы", callback_data='select_shop_comments')],
]


# =========== Получить меню выбора категории покупки/продажи ===============
def get_submenu_trades(count_dispute, count_open, count_close, name):
    menu = []
    if name == 'my_sales':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='my_sales_select_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_sales_select_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='my_sales_select_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_sales_select_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='my_sales_select_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_my_sales_select_type')])
    elif name == 'my_buys':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='my_buys_select_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_buys_select_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='my_buys_select_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_buys_select_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='my_buys_select_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_my_buys_select_type')])
    elif name == 'moder_shop_sales':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='moder_select_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='moder_select_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='moder_select_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='moder_select_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='moder_select_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_moder_shop_sales_type')])
    elif name == 'moder_user_buys':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='moder_select_user_buys_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='moder_select_user_buys_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='moder_select_user_buys_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='moder_select_user_buys_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='moder_select_user_buys_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='moder_select_user_buys')])

        # ------------ Услуги ------------
    elif name == 'my_buys_service':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='my_orders_service_select_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_orders_service_select_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='my_orders_service_select_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_orders_service_select_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='my_orders_service_select_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_my_buys_select_type')])
    elif name == 'my_sales_service':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='my_service_sales_select_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_service_sales_select_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='my_service_sales_select_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='my_service_sales_select_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='my_service_sales_select_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_my_sales_select_type')])
    elif name == 'moder_shop_service_sales':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='moder_select_service_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='moder_select_service_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='moder_select_service_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Открытые", callback_data='moder_select_service_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='moder_select_service_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='back_moder_shop_sales_type')])
    elif name == 'moder_user_orders':
        if count_dispute > 0:
            menu.append([InlineKeyboardButton(f"Диспуты", callback_data='moder_select_user_orders_section_dispute')])
        if count_open > 0 and count_close > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='moder_select_user_orders_section_open'),
                         InlineKeyboardButton(f"Завершенные", callback_data='moder_select_user_orders_section_close')])
        elif count_open > 0:
            menu.append([InlineKeyboardButton(f"Незавершенные", callback_data='moder_select_user_orders_section_open')])
        elif count_close > 0:
            menu.append([InlineKeyboardButton(f"Завершенные", callback_data='moder_select_user_orders_section_close')])
        menu.append([InlineKeyboardButton(f'{back_for_button}  Назад', callback_data='moder_select_user_buys')])
    return menu


select_comments_section = [
    [InlineKeyboardButton(f"📦  Товары", callback_data='select_comments_section_products'),
     InlineKeyboardButton(f"🤝  Услуги", callback_data='select_comments_section_services')],
]
