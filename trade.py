from dataclasses import dataclass

from history import History
from logger import log
from util import date, generate_id


@dataclass
class Order:
    id: int = 0
    date: str = ''
    price: float = 0
    amount: float = 0


class Trade:
    def __init__(self, history: History) -> None:
        self.history = history
        self.buys = {}
        self.sells = {}

    def buy(self, amount) -> Order:
        log.trace("Placing a BUY order for amount: %s", amount)

        # TODO: this is a mock, we're buying by market price and will get it from API
        buy_price = self.history.last_price

        buy = Order(
            id=generate_id(),
            date=date(),
            price=buy_price,
            amount=amount
        )
        self.buys[buy.id] = buy

        return buy

    def sell(self, amount) -> Order:
        log.trace("Placing a SEL order by amount: %s", amount)
        # TODO: this is a mock, we're buying by market price and will get it from API
        sell_price = self.history.last_price

        sell = Order(
            id=generate_id(),
            date=date(),
            price=sell_price,
            amount=amount
        )

        self.sells[sell.id] = sell

        return sell
