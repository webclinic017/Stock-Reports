import math
import requests, json
from config import *
from bs4 import BeautifulSoup

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

def get_account():
    r = requests.get(ACCOUNT_URL, headers = HEADERS)
    return json.loads(r.cash)

def create_order(ticker, quantity, side, type, time_in_force):
    data = {
        "symbol": ticker,
        "qty": quantity,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json = data, headers = HEADERS)
    return json.loads(r.content)

def get_orders():
    r = requests.get(ORDERS_URL, headers = HEADERS)
    return json.loads(r.content)

def get_positions(ticker):
    URL = POSITIONS_URL + '/' + ticker
    r = requests.get(URL, headers = HEADERS)
    resp = r.json()
    qty = int(resp['qty'])

def portfolio_allocation():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    resp = r.json()
    cash = int(float(resp['cash']))
    portfolio_value = int(float(resp['portfolio_value']))
    allocation = cash / portfolio_value * 100
    return allocation
