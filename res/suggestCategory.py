from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from res.const import back_for_button
from res.func import get_shop_name, get_shop_id, moders_alert
from res.schemas import ProductCategory, ServiceCategory, SugCategory


class SuggestCategory(object):
    SUGGEST_CATEGORY = 84
    SUGGEST_CATEGORY_NAME = 85
    SUGGEST_CATEGORY_TYPE = 86
    type = None

    def __init__(self, update, context, query):
        self.update = update
        self.context = context
        self.query = query
        self.button_suggest_category()

    def button_suggest_category(self):
        if self.query[:8] == 'products':
            self.type = 1
        elif self.query[:8] == 'services':
            self.type = 2
        self.query = self.query[9:]
        self.button_suggest_category_select()

    def button_suggest_category_select(self):
        if self.query == "":
            menu = self.get_subcats(None, self.type)
            self.context.user_data[self.SUGGEST_CATEGORY] = {
                'CAT_PATH': [],
                'SELECT_ID': "",
                'TYPE': self.type
            }
        elif self.query == "back":
            if self.SUGGEST_CATEGORY not in self.context.user_data:
                return self.update.callback_query.edit_message_text("Не актуально")
            select_cat_id = self.context.user_data[self.SUGGEST_CATEGORY]['SELECT_ID']
            if self.type == 1:
                cat = ProductCategory.objects(id=select_cat_id).first()
            else:
                cat = ServiceCategory.objects(id=select_cat_id).first()

            menu = self.get_subcats(cat.sub_id, self.type)
            self.context.user_data[self.SUGGEST_CATEGORY]['SELECT_ID'] = cat.sub_id
            self.context.user_data[self.SUGGEST_CATEGORY]['CAT_PATH'].pop()
        else:
            if self.SUGGEST_CATEGORY not in self.context.user_data:
                return self.update.callback_query.edit_message_text("Не актуально")
            cat_id = self.query
            menu = self.get_subcats(cat_id, self.type)
            self.context.user_data[self.SUGGEST_CATEGORY]['SELECT_ID'] = cat_id
            if self.type == 1:
                cat = ProductCategory.objects(id=cat_id).first()
            else:
                cat = ServiceCategory.objects(id=cat_id).first()
            self.context.user_data[self.SUGGEST_CATEGORY]['CAT_PATH'].append(cat.name)

        if self.type == 1:
            head = "🆕  Предложение категории (товары)\n\n"
        else:
            head = "🆕  Предложение категории (услуги)\n\n"
        text = "Выберите категорию/подкатегорию:"
        cat_text = self.get_cat_text(self.context)

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    @staticmethod
    def get_subcats(cat_id, type):
        menu = []
        if cat_id is None:
            if type == 1:
                cats = ProductCategory.objects()
            else:
                cats = ServiceCategory.objects()
            for cat in cats:
                if cat.sub_id is None:
                    if type == 1:
                        menu.append(
                            [InlineKeyboardButton(cat.name,
                                                  callback_data=f'my_shop_suggest_category_products_{cat.id}')])
                    else:
                        menu.append(
                            [InlineKeyboardButton(cat.name,
                                                  callback_data=f'my_shop_suggest_category_services_{cat.id}')])

            menu.append([InlineKeyboardButton(f"🆕  Предложить категорию",
                                              callback_data=f'my_shop_suggest_category_new')])
            if type == 1:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад",
                                          callback_data=f'back_to_my_shop_submenu_products')])
            else:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад",
                                          callback_data=f'back_to_my_shop_submenu_services')])
        else:
            if type == 1:
                cats = ProductCategory.objects(sub_id=cat_id)
            else:
                cats = ServiceCategory.objects(sub_id=cat_id)
            for cat in cats:
                if type == 1:
                    menu.append(
                        [InlineKeyboardButton(cat.name, callback_data=f'my_shop_suggest_category_products_{cat.id}')])
                else:
                    menu.append(
                        [InlineKeyboardButton(cat.name, callback_data=f'my_shop_suggest_category_services_{cat.id}')])

            menu.append([InlineKeyboardButton(f"🆕  Предложить категорию",
                                              callback_data=f'my_shop_suggest_category_new')])
            if type == 1:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад",
                                          callback_data=f'my_shop_suggest_category_products_back'),
                     InlineKeyboardButton(f"{back_for_button}  В начало",
                                          callback_data=f'my_shop_suggest_category_products')
                     ])
            else:
                menu.append(
                    [InlineKeyboardButton(f"{back_for_button}  Назад",
                                          callback_data=f'my_shop_suggest_category_services_back'),
                     InlineKeyboardButton(f"{back_for_button}  В начало",
                                          callback_data=f'my_shop_suggest_category_services')
                     ])
        return menu

    @staticmethod
    def get_cat_text(context):
        cat_text = ""
        i = 1
        for cat_path in context.user_data[SuggestCategory.SUGGEST_CATEGORY]['CAT_PATH']:
            cat_text += f"{'➖ ' * i}<b>" + cat_path + f"</b>\n"
            i += 1
        if cat_text != "":
            cat_text += "\n"
        return cat_text

    @staticmethod
    def get_conv_add():
        suggest_category = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(SuggestCategory.suggest_category_name_input,
                                     pattern='my_shop_suggest_category_new'),
            ],
            states={
                SuggestCategory.SUGGEST_CATEGORY_NAME: [
                    MessageHandler(Filters.text, SuggestCategory.suggest_category_add, True, run_async=True)
                ],
            },
            fallbacks=[
                CallbackQueryHandler(SuggestCategory.suggest_category_add_cancel,
                                     pattern='my_shop_suggest_category_new_cancel'),
            ],

            run_async=True
        )
        return suggest_category

    # CONV
    @staticmethod
    def suggest_category_name_input(update, context):
        type = context.user_data[SuggestCategory.SUGGEST_CATEGORY]['TYPE']
        if type == 1:
            head = "🆕  Предложение категории (товары)\n\n"
        else:
            head = "🆕  Предложение категории (услуги)\n\n"
        text = "Отправьте название категории, которую хотите отправить на модерацию, " \
               "для добавления в выбранную подкатегорию"
        cat_text = SuggestCategory.get_cat_text(context)
        update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"{back_for_button}  Назад",
                                       callback_data=f'my_shop_suggest_category_new_cancel')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return SuggestCategory.SUGGEST_CATEGORY_NAME

    # CONV
    @staticmethod
    def suggest_category_add(update, context):
        chat_id = update.message.chat_id
        name = update.message.text
        type = context.user_data[SuggestCategory.SUGGEST_CATEGORY]['TYPE']

        if type == 1:
            head = "🆕  Предложение категории (товары)\n\n"
            moders_alert(context, 'new_req_cat_prod')
        else:
            head = "🆕  Предложение категории (услуги)\n\n"
            moders_alert(context, 'new_req_cat_serv')

        if len(name) < 1 or len(name) > 64:
            text = "Отправьте название категории для добавления"
            error = "Слишком длинное название категории\n"
            update.message.reply_text(f"<b>{head}</b>\n\n{error}{text}")
            return SuggestCategory.SUGGEST_CATEGORY_NAME

        if SuggestCategory.SUGGEST_CATEGORY not in context.user_data:
            return update.message.reply_text("Не актуально")
        sub_id = context.user_data[SuggestCategory.SUGGEST_CATEGORY]['SELECT_ID']
        if sub_id == "":
            sub_id = None

        cat_text = SuggestCategory.get_cat_text(context)
        SugCategory(shop_id=chat_id, name=name, sub_id=sub_id,
                    cat_path=cat_text,
                    type=type).save()

        menu = SuggestCategory.get_subcats(sub_id, type)

        text = "Заявка на добавление категории успешно отправлена, ожидайте прохождение модерации."
        update.message.reply_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END

    # CONV
    @staticmethod
    def suggest_category_add_cancel(update, context):
        if SuggestCategory.SUGGEST_CATEGORY not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        type = context.user_data[SuggestCategory.SUGGEST_CATEGORY]['TYPE']
        cat_id = context.user_data[SuggestCategory.SUGGEST_CATEGORY]['SELECT_ID']
        if cat_id == "":
            cat_id = None
        menu = SuggestCategory.get_subcats(cat_id, type)
        if type == 1:
            head = "🆕  Предложение категории (товары)\n\n"
        else:
            head = "🆕  Предложение категории (услуги)\n\n"
        text = "Выберите категорию/подкатегорию:"
        cat_text = SuggestCategory.get_cat_text(context)

        update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END


class ModerSuggestCategory(object):
    type = None
    SUGGEST_REQ_SELECT = 87

    def __init__(self, update, context, query):
        self.update = update
        self.context = context
        self.query = query
        self.button_moder_suggest()

    def button_moder_suggest(self):
        if self.query[:14] == 'select_section':
            return self.select_section()
        elif self.query[:8] == 'products':
            self.type = 1
            self.query = self.query[9:]
            self.list_item()
        elif self.query[:8] == 'services':
            self.type = 2
            self.query = self.query[9:]
            self.list_item()
        elif self.query[:3] == 'yes':
            self.select_req_yes()
        elif self.query[:2] == 'no':
            self.select_req_no()
        else:
            self.select_item()

    def select_section(self):
        head = "🆕  Заявки на добавление категории"
        text = "Выберите раздел:"
        menu = [
            [InlineKeyboardButton(f"Товары", callback_data='shop_moder_category_suggest_products'),
             InlineKeyboardButton(f"Услуги", callback_data='shop_moder_category_suggest_services')],
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_moder_search_shop')]
        ]
        return self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def list_item(self):
        menu = self.get_suggest_list()
        head = "🆕  Заявки на добавление категории"
        text = "Выберите заявку:"
        return self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def select_item(self):
        menu = [
            [InlineKeyboardButton(f"Одобрить", callback_data='shop_moder_category_suggest_yes'),
             InlineKeyboardButton(f"Отклонить", callback_data='shop_moder_category_suggest_no')]
        ]

        head = "🆕  Заявка на добавление категории"

        sug_req = SugCategory.objects(id=self.query).first()
        self.context.user_data[self.SUGGEST_REQ_SELECT] = self.query

        if sug_req.type == 1:
            menu.append([InlineKeyboardButton(f"{back_for_button}  Назад",
                                              callback_data='shop_moder_category_suggest_products')])
        else:
            menu.append([InlineKeyboardButton(f"{back_for_button}  Назад",
                                              callback_data='shop_moder_category_suggest_services')])

        shop_id = get_shop_id(sug_req.shop_id)
        if sug_req.cat_path == "":
            cat_path = "Нет"
        else:
            cat_path = sug_req.cat_path
        text = f"<b>Магазин:</b>  {shop_id}\n" \
               f"<b>Название категории:</b>  {sug_req.name}\n" \
               f"<b>Подкатегория:</b>\n     {cat_path}"

        return self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def select_req_yes(self):
        if self.SUGGEST_REQ_SELECT not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        sug_id = self.context.user_data[self.SUGGEST_REQ_SELECT]
        sug_req = SugCategory.objects(id=sug_id).first()
        if sug_req.type == 1:
            ProductCategory(name=sug_req.name, sub_id=sug_req.sub_id).save()
        else:
            ServiceCategory(name=sug_req.name, sub_id=sug_req.sub_id).save()
        sug_req.delete()

        menu = []
        head = "🆕  Заявка одобрена"
        text = "Вы успешно одобрили заявку на добавление категории.\n" \
               "Категория автоматически создана."

        if sug_req.type == 1:
            menu.append([InlineKeyboardButton(f"{back_for_button}  Назад",
                                              callback_data='shop_moder_category_suggest_products')])
        else:
            menu.append([InlineKeyboardButton(f"{back_for_button}  Назад",
                                              callback_data='shop_moder_category_suggest_services')])

        self.context.bot.sendMessage(sug_req.shop_id,
                                     f"<b>[Оповещение]</b> Ваша заявка на добавление категории: <b>{sug_req.name}</b>"
                                     f" - <i>одобрена</i>, категория добавлена", parse_mode='HTML')

        return self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def select_req_no(self):
        if self.SUGGEST_REQ_SELECT not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        sug_id = self.context.user_data[self.SUGGEST_REQ_SELECT]
        sug_req = SugCategory.objects(id=sug_id).first()
        sug_req.delete()

        menu = []
        head = "🆕  Заявка отклонена"
        text = "Вы успешно отклонили заявку на добавление категории."

        if sug_req.type == 1:
            menu.append([InlineKeyboardButton(f"{back_for_button}  Назад",
                                              callback_data='shop_moder_category_suggest_products')])
        else:
            menu.append([InlineKeyboardButton(f"{back_for_button}  Назад",
                                              callback_data='shop_moder_category_suggest_services')])

        self.context.bot.sendMessage(sug_req.shop_id,
                                     f"<b>[Оповещение]</b> Ваша заявка на добавление категории: <b>{sug_req.name}</b>"
                                     f" - <i>отклонена</i>", parse_mode='HTML')

        return self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def get_suggest_list(self):
        menu = []
        if self.type == 1:
            data = SugCategory.objects(type=1)
        else:
            data = SugCategory.objects(type=2)
        for cat in data:
            shop = get_shop_name(cat.shop_id)
            menu.append(
                [InlineKeyboardButton(shop + " | " + cat.name, callback_data=f'shop_moder_category_suggest_{cat.id}')])
        menu.append(
            [InlineKeyboardButton(f"{back_for_button}  Назад",
                                  callback_data=f'shop_moder_category_suggest_select_section')])
        return menu
