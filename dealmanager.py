import datetime

from trade import Trade
from logger import log
from util import generate_id, date, date_to_str


class DealInfo:
    def __init__(self):
        self.id = generate_id()
        self.buy_price: float = 0
        self.sell_price: float = 0
        self.amount: float = 0
        self.total_buy: float = 0
        self.total_sell: float = 0
        self.profit: float = 0
        self.status: str = 'none'
        self.open_date: datetime.datetime = None
        self.close_date: datetime.datetime = None

    def open_deal(self, buy_price: float, amount: float, buy_date: str) -> None:
        self.status = 'opened'
        self.open_date = datetime.datetime.fromisoformat(buy_date)
        self.buy_price = buy_price
        self.amount = amount
        self.total_buy = amount * buy_price

    def close_deal(self, sell_price: float, sell_date: str):
        self.status = 'closed'
        self.close_date = datetime.datetime.fromisoformat(sell_date)
        self.sell_price = sell_price
        self.total_sell = sell_price * self.amount
        self.profit = self.total_sell - self.total_buy

    @property
    def is_open(self):
        return self.status == 'opened'

    def set_profit_based_on_price(self, price):
        total_price = self.amount * price
        self.profit = total_price - self.total_buy


class DealManager:

    def __init__(self, trade: Trade) -> None:
        self.deals: dict[int, DealInfo] = {}
        self.trade = trade

    def refresh_deals(self):
        last_price = self.trade.history.last_price
        for deal in self.deals.values():
            if deal.is_open:
                deal.set_profit_based_on_price(last_price)

    def open_deal(self, amount) -> int:
        log.trace("Opening a new deal for %s amount", amount)

        buy = self.trade.buy(amount)

        deal = DealInfo()
        deal.open_deal(buy.price, buy.amount, buy.date)
        log.debug("Opened a new deal with buy_price: %s", deal.buy_price)

        self.deals[deal.id] = deal

        return deal.id

    def close_deal(self, deal_id: int) -> None:
        log.trace("Closing a deal: #%s", deal_id)

        deal = self.deals[deal_id]
        sell = self.trade.sell(deal.amount)

        deal.close_deal(sell.price, sell.date)
        log.debug("Closed a deal: #%s with sell_price: %s, profit: %s", deal.id, deal.sell_price, deal.profit)

    def get_opened_deals_with_price_less_than(self, price) -> list[int]:
        log.trace("Getting deals with price less than: %s", price)

        ids = []
        open_deals_count = 0
        for (id, deal) in self.deals.items():
            if deal.is_open:
                open_deals_count += 1
                if deal.buy_price < price:
                    ids.append(id)

        log.debug("Found %s/%s open deals with price less than: %s", len(ids), open_deals_count, price)

        return ids

    def get_as_table_str(self) -> list[str]:
        result_list = list(map(lambda v: "{:<5} {:<20} {:<20} {:<24} {:<24}\n"
                               .format(v.id, v.status, round(v.profit, 4), date_to_str(v.open_date), date_to_str(v.close_date)),
                               self.deals.values()))
        result_list.insert(0, "{:<5} {:<20} {:<20} {:<24} {:<24}\n"
                           .format("id", 'status', 'profit', 'open_date', 'close_date'))
        total_profit = sum(map(lambda v: v.profit, self.deals.values()))
        result_list.append("TOTAL PROFIT: {0}".format(round(total_profit, 4)))
        return result_list

    def get_opened_deals_with_date_less_than(self, date: datetime.datetime) -> list[int]:
        log.trace("Getting deals with date less than: %s", date)

        ids = []
        open_deals_count = 0
        for (id, deal) in self.deals.items():
            if deal.is_open:
                open_deals_count += 1
                if deal.open_date < date:
                    ids.append(id)

        log.debug("Found %s/%s open deals with date less than: %s", len(ids), open_deals_count, date)

        return ids
