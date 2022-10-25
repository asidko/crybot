from dataclasses import dataclass

from logger import log


@dataclass
class HistoryInfo:
    bid: float
    ask: float
    date: str


class History:

    def __init__(self) -> None:
        self.history: list[HistoryInfo] = []

    def add_to_history(self, date, new_ask, new_bid):
        log.trace("Adding to history: %s - bid: %s, ask: %s", date, new_bid, new_ask)

        last = self.history[-1] if len(self.history) > 0 else None
        has_changes = last is not None and last.ask == new_ask and last.bid == new_bid
        if has_changes:
            log.trace("Skip adding to history. Prices were not changed.")
            return

        item = HistoryInfo(new_bid, new_ask, date)
        self.history = self.history[-99:]
        self.history.append(item)

    @property
    def is_empty(self):
        return len(self.history) == 0

    @property
    def last_price_to_buy(self):
        if self.is_empty:
            return 0

        return self.history[-1].ask

    @property
    def last_price_to_sell(self):
        if self.is_empty:
            return 0

        return self.history[-1].bid

    def is_sell_price_up(self):
        if len(self.history) <= 1:
            return False

        return self.history[-1].bid > self.history[-2].bid

    def is_sell_price_down(self):
        if len(self.history) <= 1:
            return False

        return self.history[-1].bid < self.history[-2].bid

    def is_sell_price_down_ntimes(self, n: int) -> bool:
        log.trace(f"Checking sell price down N={n} times")

        if len(self.history) <= n:
            log.trace("Skipping the check since history has only %d items", len(self.history))
            return False

        last_n_items = self.history[-n:]
        log.trace("Sell prices for last N=%d times: %s", n, list(map(lambda x: x.bid, last_n_items)))

        for i, elem in enumerate(last_n_items):
            if (i + 1) < n:
                if last_n_items[i + 1].bid >= last_n_items[i].bid:
                    log.trace("Check failed. Sell price was down %d/%d times in a row", i, n)
                    return False
        return True
