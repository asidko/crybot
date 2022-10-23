from time import sleep

from context import Context

context = Context()

if __name__ == '__main__':
    for i in range(1000000000):
        context.refresh_last_price()
        context.refresh_deals()

        if i == 0:
            buy_id = context.open_deal()

        if context.is_price_up():
            print("⏫️Price is UP")
            buy_id = context.open_deal()

        if context.is_price_down():
            print("🔻️ Price is DOWN")

        deals = context.get_deals_with_opened_price_less_than_current()
        if len(deals):
            print("✅ Got {0} deals with price less than current".format(len(deals)))

        for deal_id in deals:
            context.close_deal(deal_id)
            print("👍 Closed a deal #{0}".format(deal_id))

        context.save_deals_to_file()

        sleep(30)

