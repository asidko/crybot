import asyncio
import json
import threading
from time import sleep

import websockets

from context import Context, ContextProperties
from logger import log

context = Context(
    ContextProperties(
        symbol='ALPINEUSDT',
        buy_amount=10,
        check_time_seconds=30,
        deal_expire_seconds=300,
        open_deal_when_price_is_up=False,
        open_deal_when_price_is_down_ntimes=True,
        open_deal_when_price_is_down_ntimes_value=3
    )
)


async def exchange_ws_connector():
    global context
    symbol = context.properties.symbol.lower()
    uri = f'wss://stream.binance.com:9443/stream?streams={symbol}@bookTicker'
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            log.trace("Got prices from ws channel")
            data = json.loads(message)['data']
            bid = data['b']
            ask = data['a']
            print(f"📗 Bid price: {bid}, 📕 Ask price: {ask}")
            context.add_history_price(float(ask), float(bid))


def exchange_ws_main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(exchange_ws_connector())
    loop.close()


def main_flow():
    global context
    props = context.properties

    i = 0
    while True:

        if not context.is_ready:
            log.debug("💤 Waiting for prices...")
            sleep(2)
            continue

        i += 1
        print("-- Tick #{0} --".format(i))

        context.refresh_deals()

        if i == 1:
            context.open_deal()

        if context.is_sell_price_up():
            print("🔼 Price is UP")
            if props.open_deal_when_price_is_up:
                context.open_deal()

        if context.is_sell_price_down():
            print("🔻️ Price is DOWN")

        if context.is_sell_price_down_ntimes(props.open_deal_when_price_is_down_ntimes_value):
            print("🔻️ x%s Price is DOWN good time to open a deal" % props.open_deal_when_price_is_down_ntimes_value)
            if props.open_deal_when_price_is_down_ntimes:
                context.open_deal()

        deal_ids = context.get_deals_with_opened_price_less_than_current_sell_price()
        if len(deal_ids):
            print("✅ Got {0} deals with price less than current".format(len(deal_ids)))

            for deal_id in deal_ids:
                context.close_deal(deal_id)
                print("👍 Closed a deal #{0}".format(deal_id))

        deal_ids = context.get_deals_that_expired()
        if len(deal_ids):
            print("❌ Got {0} expired deals".format(len(deal_ids)))

            for deal_id in deal_ids:
                context.close_deal(deal_id)
                print("👎 Closed an expired deal #{0}".format(deal_id))

        context.save_deals_to_file()

        sleep(context.properties.check_time_seconds)


if __name__ == '__main__':
    print("⚡️Started a BOT with params:\n", context.properties.__dict__)

    _thread = threading.Thread(target=exchange_ws_main, name="ws_stream")
    _thread.start()
    main_flow()
    _thread.join()
