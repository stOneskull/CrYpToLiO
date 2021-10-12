import time


class Coin:
    """ machina """
    time = time.time()
    total_paid = 0
    total_now = 0

    def __init__(self, mycoin, jsoncoin):

        self.name = jsoncoin['name']
        self.rank = jsoncoin['rank']
        self.price_now = float(jsoncoin['price_usd'])

        self.holding = float(mycoin['holding'])
        self.price_paid = float(mycoin['price_paid'])

        self.profit_per = (
            '{:.2f}'.format(self.price_now - self.price_paid)
            if self.holding else 0
        )

        self.one_hour = '{:.2f}%'.format(float(jsoncoin['percent_change_1h']))
        self.one_day = '{:.2f}%'.format(float(jsoncoin['percent_change_24h']))
        self.one_week = '{:.2f}%'.format(float(jsoncoin['percent_change_7d']))

        self.total = float('{:.2f}'.format(self.holding * self.price_now))
        self.paid = float('{:.2f}'.format(self.holding * self.price_paid))
        self.profit = float('{:.2f}'.format(self.total - self.paid))

        Coin.total_paid += self.paid
        Coin.total_now += self.total

        self.columns = {
            'Name': self.name,
            'Rank': self.rank,
            'Holding': self.holding,
            'Price Now': self.price_now,
            'Price Paid': self.price_paid,
            'Profit Per': self.profit_per,
            '1 Hour': self.one_hour,
            '1 Day': self.one_day,
            '1 Week': self.one_week,
            'Spent': self.paid,
            'Value': self.total,
            'Profit': self.profit,
            }

    def __repr__(self):
        return self.name

    @staticmethod
    def reset():
        Coin.total_paid = 0
        Coin.total_now = 0
        Coin.time = time.time()