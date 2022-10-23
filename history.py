import logging

from logger import log


class History:

    def __init__(self) -> None:
        self.history = []

    def add_to_history(self, timestamp, price):
        log.trace("Adding to history: %s - %s", timestamp, price)
        self.history.append({'date': timestamp, 'price': price})

    @property
    def last_price(self):
        if len(self.history) == 0:
            return 0

        return self.history[-1]['price']

    def is_price_up(self):
        if len(self.history) <= 1:
            return False

        return self.history[-1]['price'] > self.history[-2]['price']

    def is_price_down(self):
        if len(self.history) <= 1:
            return False

        return self.history[-1]['price'] < self.history[-2]['price']