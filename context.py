from dataclasses import dataclass
from datetime import datetime, timedelta

from dealmanager import DealManager
from history import History
from logger import log
from trade import Trade
from util import date_str


@dataclass
class ContextProperties:
    symbol: str = 'ALPINEUSDT'
    buy_amount: float = 10
    check_time_seconds: int = 30
    deal_expire_seconds: int = 300
    open_deal_when_price_is_up: bool = False
    open_deal_when_price_is_down_ntimes: bool = False
    open_deal_when_price_is_down_ntimes_value: int = 3


class Context:

    def __init__(self, properties: ContextProperties = ContextProperties()) -> None:
        self.properties = properties
        self.history = History()
        self.trade = Trade(self.history)
        self.deal_manager = DealManager(self.trade)

    @property
    def is_ready(self):
        return not self.history.is_empty

    def is_sell_price_up(self):
        return self.history.is_sell_price_up()

    def is_sell_price_down(self):
        return self.history.is_sell_price_down()

    def is_sell_price_down_ntimes(self, n: int):
        return self.history.is_sell_price_down_ntimes(n)

    def close_deal(self, deal_id):
        log.trace("Closing a deal: #%s", deal_id)
        self.deal_manager.close_deal(deal_id)

    def get_deals_with_opened_price_less_than_current_sell_price(self):
        log.trace("Getting deals with opened price less than current")
        last_price = self.history.last_price_to_sell
        return self.deal_manager.get_opened_deals_with_opened_price_less_than(last_price)

    def open_deal(self):
        log.trace("Opening a deal")
        self.deal_manager.open_deal(self.properties.buy_amount)

    def save_deals_to_file(self):
        with open('deals.txt', 'w') as f:
            f.writelines(self.deal_manager.get_as_table_str())

    def refresh_deals(self):
        self.deal_manager.refresh_deals()

    def get_deals_that_expired(self):
        log.trace("Looking for expired deals")
        expired_date = datetime.now() - timedelta(seconds=self.properties.deal_expire_seconds)
        return self.deal_manager.get_opened_deals_with_date_less_than(expired_date)

    def add_history_price(self, ask: float, bid: float):
        self.history.add_to_history(date_str(), ask, bid)
