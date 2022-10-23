import logging
from dataclasses import dataclass

import requests

from history import History
from dealmanager import DealManager
from logger import log
from trade import Trade
from util import date


def get_last_price():
    r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ALPINEUSDT')
    return float(r.json()['price'])


@dataclass
class ContextProperties:
    buy_amount: float = 10


class Context:

    def __init__(self, properties: ContextProperties = ContextProperties()) -> None:
        self.properties = properties
        self.history = History()
        self.trade = Trade(self.history)
        self.deal_manager = DealManager(self.trade)

    def refresh_last_price(self):
        price = get_last_price()
        timestamp = date()
        self.history.add_to_history(timestamp, price)
        print("☀️Last price: {0}".format(price))

    def is_price_up(self):
        return self.history.is_price_up()

    def is_price_down(self):
        return self.history.is_price_down()

    def is_price_down_for(self, deal_id):
        deal = self.deal_manager.deals[deal_id]
        return self.history.last_price < deal.buy_price

    def close_deal(self, deal_id):
        log.trace("Closing a deal: #%s", deal_id)
        self.deal_manager.close_deal(deal_id)

    def get_deals_with_opened_price_less_than_current(self):
        log.trace("Getting deals with opened price less than current")
        last_price = self.history.last_price
        return self.deal_manager.get_opened_deals_with_price_less_than(last_price)

    def open_deal(self):
        log.trace("Opening a deal")
        self.deal_manager.open_deal(self.properties.buy_amount)

    def save_deals_to_file(self):
        with open('deals.txt', 'w') as f:
            f.writelines(self.deal_manager.get_as_table_str())

    def refresh_deals(self):
        self.deal_manager.refresh_deals()
