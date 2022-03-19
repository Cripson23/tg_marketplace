import datetime
import logging
import os
import sys

formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)\n' \
            '============================================================\n\n'
logging.basicConfig(
    filename=f'logs/bot-from-{datetime.datetime.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING
)

token = os.environ.get("token")
host_db = os.environ.get("host_db")
API_KEY_COINBASE = os.environ.get("API_KEY_COINBASE")
API_SECRET_COINBASE = os.environ.get("API_SECRET_COINBASE")
MAIN_ACCOUNT_COINBASE = os.environ.get("MAIN_ACCOUNT_COINBASE")
