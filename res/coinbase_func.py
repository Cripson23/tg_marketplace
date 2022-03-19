import traceback

from coinbase.wallet.client import Client

from config import API_KEY_COINBASE, API_SECRET_COINBASE, MAIN_ACCOUNT_COINBASE

from res.func import get_user_obj, add_withdrawal, id_generator

client = Client(API_KEY_COINBASE, API_SECRET_COINBASE)
account_id = MAIN_ACCOUNT_COINBASE


def get_coinbase_address_id(chat_id):
    user = get_user_obj(chat_id)
    return user.coinbase_address_id


def get_coinbase_address(address_id):
    data = client.get_address(account_id, address_id)
    address = data['address']
    return address


def create_coinbase_address(chat_id):
    data = client.create_address(account_id, name=chat_id)
    address_id = data['id']
    user = get_user_obj(chat_id)
    user.update(coinbase_address_id=address_id)


def get_transactions_list(address_id):
    transactions = client.get_address_transactions(account_id, address_id).data
    return transactions


def get_transaction_info_by_id(trans_id):
    tx = client.get_transaction(account_id, trans_id)
    print(tx)


def send_money(chat_id, address, amount):
    try:
        tx = client.send_money(account_id,
                               to=address,
                               amount=amount,
                               currency='LTC',
                               idem=id_generator())
    except Exception:
        print('Error send_money:\n', traceback.format_exc())
    else:
        if not tx:
            print('Error get tx send_money [Empty]')
            return False
        trans_id = tx['id']
        currency = tx['amount']['currency']
        created_at = tx['created_at']
        status = tx['status']
        to_address = tx['to']['address']
        try:
            add_withdrawal(chat_id, trans_id, to_address, amount, currency, created_at, status)
        except Exception:
            print('Error add_withdrawal:\n', traceback.format_exc())
        else:
            return True


def get_coinbase_balance():
    account = client.get_account(MAIN_ACCOUNT_COINBASE)
    return float(account['balance']['amount'])
