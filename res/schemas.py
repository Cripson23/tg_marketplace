from mongoengine.base.fields import ObjectIdField
from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, FloatField, BooleanField, DateTimeField, ListField


class User(Document):
    chat_id = IntField(required=True)
    user_id = StringField(required=True)
    username = StringField(required=True)
    first_name = StringField(required=True)
    coinbase_address_id = StringField()
    balance = FloatField(default=0)
    moderator = BooleanField(default=False)
    banned = BooleanField(default=False)
    reg_date = DateTimeField(required=True)
    messages_limit = IntField(default=0)
    date_set_limit = DateTimeField(default=None)


class Payment(Document):
    chat_id = IntField(required=True)
    trans_id = StringField(required=True)
    amount = FloatField(required=True)
    created_at = StringField(required=True)
    credited_at = DateTimeField(required=True)


class Withdrawal(Document):
    chat_id = IntField(required=True)
    trans_id = StringField(required=True)
    to_address = StringField(required=True)
    amount = FloatField(required=True)
    currency = StringField(required=True)
    created_at = DateTimeField(required=True)
    status = StringField(required=True)


class RequestOpenShop(Document):
    creator_id = IntField(required=True)
    shop_name = StringField(required=True)
    created_at = StringField(required=True)
    why = StringField(required=True)
    res = StringField(required=True)


class Shop(Document):
    owner_id = IntField(required=True)
    shop_id = StringField(required=True)
    shop_name = StringField(required=True)
    shop_about = StringField(default=None)
    balance = FloatField(default=0)
    created_at = StringField(required=True)
    who_approved = IntField(required=True)
    guarantee = FloatField(default=0)
    banned = BooleanField(default=False)
    date_change_name = DateTimeField(default=None)
    check_buyer_time = IntField(required=True, default=300)
    pause_trade = BooleanField(default=False)
    last_active = DateTimeField(default=None)
    terms_trade = StringField(default=None)
    freeze_guarantee = FloatField(default=0)
    stop = BooleanField(default=False)


class ShopOperations(Document):
    owner_id = IntField(required=True)
    sum = FloatField(required=True)
    date = DateTimeField(required=True)
    name = StringField(required=True)
    type = IntField(required=True)


class Requisites(Document):
    owner_id = IntField(required=True)
    name = StringField(required=True)
    payment_system = StringField(required=True)
    account_number = StringField(required=True)


class ProductCategory(Document):
    sub_id = ObjectIdField(default=None)
    name = StringField(required=True)


class Product(Document):
    category_id = ObjectIdField(required=True)
    owner_id = IntField(required=True)
    name = StringField(required=True)
    description = StringField()
    count = IntField(required=True)
    content = ListField(required=True)
    price = IntField(required=True)
    date_last_update = DateTimeField()


class Deal(Document):
    shop_id = IntField(required=True)
    buyer_id = IntField(required=True)
    product_id = ObjectIdField(required=True)
    category = StringField(required=True)
    sum_price = IntField(required=True)
    sum_price_ltc = FloatField(required=True)
    count = IntField(required=True)
    file_id = StringField(default=None)
    change_file_id = StringField(default=None)
    change_count = IntField(default=None)
    payment_method = StringField(required=True, default="LITECOIN")
    status = IntField(required=True)
    date = DateTimeField(required=True)
    like = BooleanField(default=None)
    comment = StringField(default=None)
    potential = BooleanField(default=False)
    proof_payment = BooleanField(default=False)
    call_moderator = BooleanField(default=False)
    messages = ListField(default=None)
    defeat_dispute = BooleanField(default=None)


class ServiceCategory(Document):
    sub_id = ObjectIdField(default=None)
    name = StringField(required=True)


class Service(Document):
    category_id = ObjectIdField(required=True)
    owner_id = IntField(required=True)
    name = StringField(required=True, max_length=30)
    description = StringField(required=True, max_length=500)
    portfolio = StringField(default=None)
    min_price = IntField(required=True)
    picture = StringField(required=True)
    eco_price = IntField(default=None)
    eco_description = StringField(default=None)
    eco_deadline = IntField(default=None)
    standart_price = IntField(default=None)
    standart_description = StringField(default=None)
    standart_deadline = IntField(default=None)
    biz_price = IntField(default=None)
    biz_description = StringField(default=None)
    biz_deadline = IntField(default=None)


class Order(Document):
    shop_id = IntField(required=True)
    client_id = IntField(required=True)
    service_id = ObjectIdField(required=True)
    category = StringField(required=True)
    price = IntField(default=None)
    price_ltc = FloatField(default=None)
    tz = StringField(required=True)
    packet = IntField(required=True)
    status = IntField(required=True)
    date_start = DateTimeField(default=None)
    deadline_days = IntField(default=None)
    date_deadline = DateTimeField(default=None)
    call_moderator = BooleanField(default=False)
    messages = ListField(default=None)
    comment = StringField(default=None)
    like = BooleanField(default=None)
    rating = IntField(default=None)
    potential = BooleanField(default=False)
    order_work = StringField(default=None)
    late_deadline = IntField(default=False)
    defeat_dispute = BooleanField(default=None)


class SugCategory(Document):
    shop_id = IntField(required=True)
    name = StringField(required=True)
    sub_id = StringField(default=None)
    cat_path = StringField(required=True)
    type = IntField(required=True)
