from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from res.const import back_for_button
from res.schemas import ProductCategory, ServiceCategory, Product, Service


class ModerCategory(object):
    MODER_CATEGORY = 81
    MODER_CATEGORY_NAME = 82

    def __init__(self, update, context, query):
        self.update = update
        self.context = context
        self.query = query
        self.button_moder_category()

    def button_moder_category(self):
        if self.query == 'select_section':
            self.select_section()
        elif self.query[:8] == 'products':
            ModerCategoryProducts(self.update, self.context, self.query[9:])
        elif self.query[:8] == 'services':
            ModerCategoryServices(self.update, self.context, self.query[9:])

    def select_section(self):
        head = "Категории"
        text = "Выберите раздел категорий:"
        menu = [
            [InlineKeyboardButton(f"Товары", callback_data='moder_category_products'),
             InlineKeyboardButton(f"Услуги", callback_data='moder_category_services')],
            [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data='back_to_moder_menu')]
        ]
        return self.update.callback_query.edit_message_text(
            f"<b>{head}\n\n</b>{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    @staticmethod
    def get_cat_text(context):
        cat_text = ""
        i = 1
        for cat_path in context.user_data[ModerCategory.MODER_CATEGORY]['CAT_PATH']:
            cat_text += f"{'➖ ' * i}<b>" + cat_path + f"</b>\n"
            i += 1
        if cat_text != "":
            cat_text += "\n"
        return cat_text


class ModerCategoryProducts(ModerCategory):
    def __init__(self, update, context, query):
        super().__init__(update, context, query)
        self.button_moder_category_products()

    def button_moder_category_products(self):
        if self.query == 'delete':
            self.product_cat_delete()
        elif self.query == 'del_accept':
            self.product_cat_acc_delete()
        elif self.query == 'del_cancel':
            self.product_cat_cancel_delete()
        else:
            self.category_shifter()

    def category_shifter(self):
        if self.query == "":
            menu = self.products_get_subcats(None)
            self.context.user_data[self.MODER_CATEGORY] = {
                'CAT_PATH': [],
                'SELECT_ID': ""
            }
        elif self.query == "shifter_back":
            if self.MODER_CATEGORY not in self.context.user_data:
                return self.update.callback_query.edit_message_text("Не актуально")
            select_cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']
            cat = ProductCategory.objects(id=select_cat_id).first()
            menu = self.products_get_subcats(cat.sub_id)
            self.context.user_data[self.MODER_CATEGORY]['SELECT_ID'] = cat.sub_id
            self.context.user_data[self.MODER_CATEGORY]['CAT_PATH'].pop()
        else:
            if self.MODER_CATEGORY not in self.context.user_data:
                return self.update.callback_query.edit_message_text("Не актуально")
            cat_id = self.query
            menu = self.products_get_subcats(cat_id)
            self.context.user_data[self.MODER_CATEGORY]['SELECT_ID'] = cat_id
            cat = ProductCategory.objects(id=cat_id).first()
            self.context.user_data[self.MODER_CATEGORY]['CAT_PATH'].append(cat.name)

        head = "Категории (товары)\n\n"
        text = "Выберите действие/категорию/подкатегорию:"
        cat_text = self.get_cat_text(self.context)

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    @staticmethod
    def products_get_subcats(cat_id):
        menu = []
        if cat_id is None:
            cats = ProductCategory.objects()
            for cat in cats:
                if cat.sub_id is None:
                    menu.append([InlineKeyboardButton(cat.name, callback_data=f'moder_category_products_{cat.id}')])
            menu.append([InlineKeyboardButton(f"➕  Добавить категорию", callback_data=f'moder_category_product_add')])
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data=f'moder_category_select_section')])
        else:
            cats = ProductCategory.objects(sub_id=cat_id)
            for cat in cats:
                menu.append([InlineKeyboardButton(cat.name, callback_data=f'moder_category_products_{cat.id}')])
            menu.append([InlineKeyboardButton(f"➕  Добавить категорию", callback_data=f'moder_category_product_add')])
            menu.append([InlineKeyboardButton(f"➖  Удалить выбранную", callback_data=f'moder_category_products_delete')])
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data=f'moder_category_products_shifter_back'),
                 InlineKeyboardButton(f"{back_for_button}  В начало",
                                      callback_data=f'moder_category_products')
                 ])
        return menu

    def product_cat_delete(self):
        if self.MODER_CATEGORY not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        select_cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']

        query = self.update.callback_query
        query.answer()

        cat_text = self.get_cat_text(self.context)

        prod_count = self.count_products(select_cat_id)

        head = "➖  Удаление категории"
        menu = [
            [InlineKeyboardButton(f'{back_for_button}  Отмена',
                                  callback_data=f'moder_category_products_del_cancel'),
             InlineKeyboardButton(f"Подтвердить", callback_data='moder_category_products_del_accept')]
        ]

        if prod_count != 0:
            text = "<b>⚠  В данной категории/её подкатегориях есть товары!</b>\n\n" \
                   "Вы действительно хотите удалить данную категорию и все её подкатегории?\n\n" \
                   "<b>ТОВАРЫ</b> будут недоступны, но не удалены из базы!"
        else:
            text = "Вы действительно хотите удалить данную категорию и все её подкатегории?"

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def product_cat_acc_delete(self):
        if self.MODER_CATEGORY not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        select_cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']

        query = self.update.callback_query
        query.answer()

        cat = ProductCategory.objects(id=select_cat_id).first()
        sub_cats = ProductCategory.objects(sub_id=select_cat_id)
        sub_id = cat.sub_id
        cat.delete()
        sub_cats.delete()

        self.context.user_data[self.MODER_CATEGORY]['CAT_PATH'].pop()
        self.context.user_data[self.MODER_CATEGORY]['SELECT_ID'] = sub_id

        menu = self.products_get_subcats(sub_id)
        head = "➖  Удаление категории"
        text = "<b>Категория и все её подкатегории успешно удалены</b>"
        cat_text = self.get_cat_text(self.context)

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def product_cat_cancel_delete(self):
        if self.MODER_CATEGORY not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']
        menu = self.products_get_subcats(cat_id)
        head = "Категории (товары)\n\n"
        text = "Выберите категорию/подкатегорию:"
        cat_text = self.get_cat_text(self.context)

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def count_products(self, select_cat):
        sub_cats = ProductCategory.objects(sub_id=select_cat)
        if not sub_cats:
            prods = Product.objects(category_id=select_cat)
            return len(prods)
        else:
            for sub in sub_cats:
                return self.count_products(sub.id)

    @staticmethod
    def get_conv_add():
        add_moder_category = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(ModerCategoryProducts.moder_category_products_name_input,
                                     pattern='moder_category_product_add'),
            ],
            states={
                ModerCategory.MODER_CATEGORY_NAME: [
                    MessageHandler(Filters.text, ModerCategoryProducts.moder_category_add, True, run_async=True)
                ],
            },
            fallbacks=[
                CallbackQueryHandler(ModerCategoryProducts.moder_category_add_cancel,
                                     pattern='moder_category_add_cancel'),
            ],

            run_async=True
        )
        return add_moder_category

    # CONV
    @staticmethod
    def moder_category_products_name_input(update, context):
        head = "➕  Добавление категории"
        text = "Отправьте название категории для добавления"
        update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"{back_for_button}  Назад", callback_data=f'moder_category_add_cancel')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return ModerCategory.MODER_CATEGORY_NAME

    # CONV
    @staticmethod
    def moder_category_add(update, context):
        name = update.message.text
        head = "➕  Добавление категории"
        if len(name) < 1 or len(name) > 64:
            text = "Отправьте название категории для добавления"
            error = "Слишком длинное название категории\n"
            update.message.reply_text(f"<b>{head}</b>\n\n{error}{text}")
            return ModerCategoryProducts.MODER_CATEGORY_NAME

        if ModerCategoryProducts.MODER_CATEGORY not in context.user_data:
            return update.message.reply_text("Не актуально")
        sub_id = context.user_data[ModerCategoryProducts.MODER_CATEGORY]['SELECT_ID']
        if sub_id == "":
            sub_id = None
        ProductCategory(name=name, sub_id=sub_id).save()
        cat_text = ModerCategory.get_cat_text(context)

        menu = ModerCategoryProducts.products_get_subcats(sub_id)

        text = "Категория успешно добавлена"
        update.message.reply_text(
            f"<b>{head}</b>\n\n{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END

    # CONV
    @staticmethod
    def moder_category_add_cancel(update, context):
        if ModerCategoryProducts.MODER_CATEGORY not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        cat_id = context.user_data[ModerCategoryProducts.MODER_CATEGORY]['SELECT_ID']
        if cat_id == "":
            cat_id = None
        menu = ModerCategoryProducts.products_get_subcats(cat_id)
        head = "Категории (товары)\n\n"
        text = "Выберите категорию/подкатегорию:"
        cat_text = ModerCategoryProducts.get_cat_text(context)

        update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END


class ModerCategoryServices(ModerCategory):
    def __init__(self, update, context, query):
        super().__init__(update, context, query)
        self.button_moder_category_services()

    def button_moder_category_services(self):
        if self.query == 'delete':
            self.service_cat_delete()
        elif self.query == 'del_accept':
            self.service_cat_acc_delete()
        elif self.query == 'del_cancel':
            self.services_cat_cancel_delete()
        else:
            self.category_shifter()

    def category_shifter(self):
        if self.query == "":
            menu = self.services_get_subcats(None)
            self.context.user_data[self.MODER_CATEGORY] = {
                'CAT_PATH': [],
                'SELECT_ID': ""
            }
        elif self.query == "shifter_back":
            if self.MODER_CATEGORY not in self.context.user_data:
                return self.update.callback_query.edit_message_text("Не актуально")
            select_cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']
            cat = ServiceCategory.objects(id=select_cat_id).first()
            menu = self.services_get_subcats(cat.sub_id)
            self.context.user_data[self.MODER_CATEGORY]['SELECT_ID'] = cat.sub_id
            self.context.user_data[self.MODER_CATEGORY]['CAT_PATH'].pop()
        else:
            if self.MODER_CATEGORY not in self.context.user_data:
                return self.update.callback_query.edit_message_text("Не актуально")
            cat_id = self.query
            menu = self.services_get_subcats(cat_id)
            self.context.user_data[self.MODER_CATEGORY]['SELECT_ID'] = cat_id
            cat = ServiceCategory.objects(id=cat_id).first()
            self.context.user_data[self.MODER_CATEGORY]['CAT_PATH'].append(cat.name)

        head = "Категории (услуги)\n\n"
        text = "Выберите категорию/подкатегорию:"
        cat_text = self.get_cat_text(self.context)

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    @staticmethod
    def services_get_subcats(cat_id):
        menu = []
        if cat_id is None:
            cats = ServiceCategory.objects()
            for cat in cats:
                if cat.sub_id is None:
                    menu.append([InlineKeyboardButton(cat.name, callback_data=f'moder_category_services_{cat.id}')])
            menu.append([InlineKeyboardButton(f"➕  Добавить категорию", callback_data=f'moder_category_service_add')])
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад", callback_data=f'moder_category_select_section')])
        else:
            cats = ServiceCategory.objects(sub_id=cat_id)
            for cat in cats:
                menu.append([InlineKeyboardButton(cat.name, callback_data=f'moder_category_services_{cat.id}')])
            menu.append([InlineKeyboardButton(f"➕  Добавить категорию", callback_data=f'moder_category_service_add')])
            menu.append([InlineKeyboardButton(f"➖  Удалить выбранную", callback_data=f'moder_category_services_delete')])
            menu.append(
                [InlineKeyboardButton(f"{back_for_button}  Назад",
                                      callback_data=f'moder_category_services_shifter_back'),
                 InlineKeyboardButton(f"{back_for_button}  В начало",
                                      callback_data=f'moder_category_services')
                 ])
        return menu

    def service_cat_delete(self):
        if self.MODER_CATEGORY not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        select_cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']

        query = self.update.callback_query
        query.answer()

        cat_text = self.get_cat_text(self.context)

        serv_count = self.count_services(select_cat_id)

        head = "➖  Удаление категории"
        menu = [
            [InlineKeyboardButton(f'{back_for_button}  Отмена',
                                  callback_data=f'moder_category_services_del_cancel'),
             InlineKeyboardButton(f"Подтвердить", callback_data='moder_category_services_del_accept')]
        ]

        if serv_count != 0:
            text = "<b>⚠  В данной категории/её подкатегориях есть услуги!</b>\n\n" \
                   "Вы действительно хотите удалить данную категорию и все её подкатегории?\n\n" \
                   "<b>УСЛУГИ</b> будут недоступны, но не удалены из базы!"
        else:
            text = "Вы действительно хотите удалить данную категорию и все её подкатегории?"

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def service_cat_acc_delete(self):
        if self.MODER_CATEGORY not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        select_cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']

        query = self.update.callback_query
        query.answer()

        cat = ServiceCategory.objects(id=select_cat_id).first()
        sub_cats = ServiceCategory.objects(sub_id=select_cat_id)
        sub_id = cat.sub_id
        cat.delete()
        sub_cats.delete()

        self.context.user_data[self.MODER_CATEGORY]['CAT_PATH'].pop()
        self.context.user_data[self.MODER_CATEGORY]['SELECT_ID'] = sub_id

        menu = self.services_get_subcats(sub_id)
        head = "➖  Удаление категории"
        text = "<b>Категория и все её подкатегории успешно удалены</b>"
        cat_text = self.get_cat_text(self.context)

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def services_cat_cancel_delete(self):
        if self.MODER_CATEGORY not in self.context.user_data:
            return self.update.callback_query.edit_message_text("Не актуально")
        cat_id = self.context.user_data[self.MODER_CATEGORY]['SELECT_ID']
        menu = self.services_get_subcats(cat_id)
        head = "Категории (товары)\n\n"
        text = "Выберите категорию/подкатегорию:"
        cat_text = self.get_cat_text(self.context)

        self.update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')

    def count_services(self, select_cat):
        sub_cats = ServiceCategory.objects(sub_id=select_cat)
        if not sub_cats:
            servs = Service.objects(category_id=select_cat)
            return len(servs)
        else:
            for sub in sub_cats:
                return self.count_services(sub.id)

    @staticmethod
    def get_conv_add():
        add_moder_category = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(ModerCategoryServices.moder_category_services_name_input,
                                     pattern='moder_category_service_add'),
            ],
            states={
                ModerCategory.MODER_CATEGORY_NAME: [
                    MessageHandler(Filters.text, ModerCategoryServices.moder_category_add, True, run_async=True)
                ],
            },
            fallbacks=[
                CallbackQueryHandler(ModerCategoryServices.moder_category_add_cancel,
                                     pattern='moder_category_add_cancel'),
            ],

            run_async=True
        )
        return add_moder_category

    # CONV
    @staticmethod
    def moder_category_services_name_input(update, context):
        head = "➕  Добавление категории"
        text = "Отправьте название категории для добавления"
        update.callback_query.edit_message_text(
            f"<b>{head}</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"{back_for_button}  Назад", callback_data=f'moder_category_add_cancel')]],
                resize_keyboard=True),
            parse_mode='HTML')
        return ModerCategory.MODER_CATEGORY_NAME

    # CONV
    @staticmethod
    def moder_category_add(update, context):
        name = update.message.text
        head = "➕  Добавление категории"
        if len(name) < 1 or len(name) > 64:
            text = "Отправьте название категории для добавления"
            error = "Слишком длинное название категории\n"
            update.message.reply_text(f"<b>{head}</b>\n\n{error}{text}")
            return ModerCategoryServices.MODER_CATEGORY_NAME

        if ModerCategoryServices.MODER_CATEGORY not in context.user_data:
            return update.message.reply_text("Не актуально")
        sub_id = context.user_data[ModerCategoryServices.MODER_CATEGORY]['SELECT_ID']
        if sub_id == "":
            sub_id = None
        ServiceCategory(name=name, sub_id=sub_id).save()
        cat_text = ModerCategory.get_cat_text(context)

        menu = ModerCategoryServices.services_get_subcats(sub_id)

        text = "Категория успешно добавлена"
        update.message.reply_text(
            f"<b>{head}</b>\n\n{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END

    # CONV
    @staticmethod
    def moder_category_add_cancel(update, context):
        if ModerCategoryServices.MODER_CATEGORY not in context.user_data:
            return update.callback_query.edit_message_text("Не актуально")
        cat_id = context.user_data[ModerCategoryServices.MODER_CATEGORY]['SELECT_ID']
        if cat_id == "":
            cat_id = None
        menu = ModerCategoryServices.services_get_subcats(cat_id)
        head = "Категории (услуги)\n\n"
        text = "Выберите категорию/подкатегорию:"
        cat_text = ModerCategoryServices.get_cat_text(context)

        update.callback_query.edit_message_text(
            f"<b>{head}</b>{cat_text}{text}",
            reply_markup=InlineKeyboardMarkup(menu,
                                              resize_keyboard=True),
            parse_mode='HTML')
        return ConversationHandler.END