from dataclasses import asdict
from time import sleep

from context import Context

context = Context()

if __name__ == '__main__':
    print("⚡️Started a BOT with params:\n", context.properties.__dict__)
    i = 0
    while True:
        i += 1
        print("-- Tick #{0}".format(i))

        context.refresh_last_price()
        context.refresh_deals()

        if i == 1:
            buy_id = context.open_deal()

        if context.is_price_up():
            print("⏫️Price is UP")
            buy_id = context.open_deal()

        if context.is_price_down():
            print("🔻️ Price is DOWN")

        deal_ids = context.get_deals_with_opened_price_less_than_current()
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
