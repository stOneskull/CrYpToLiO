#!/usr/bin/env python3

""" Funky Portfolio for Cryptocurrency """

import time
import random
from tkinter import Tk, PhotoImage, Label, Button, N, S, E, W
from matplotlib import pyplot
import requests


  #####################
 ##### CrYpToLiO #####
### by stOneskull ###
#####################
###  inspired by  ###
 ###   codemy.com  ###
  #####################

__version__ = '0.2.5'

########### - make intro
## to do ## - add user input for folio details
########### - use data from livecoinwatch.com / coincap.io


Heart = True


class Coin:
    """ machina """
    time = time.time()
    total_paid = 0
    total_now = 0

    def __init__(self, mycoin, coinup):

        self.name = coinup['name']
        self.rank = coinup['rank']

        self.holding = float(mycoin['holding'])
        self.price_now = float(coinup['price_usd'])
        self.price_paid = float(mycoin['price_paid'])

        if self.holding:
            self.profit_per = '{:.2f}'.format(
                self.price_now - self.price_paid
                )
        else:
            self.profit_per = 0

        self.one_hour = '{:.2f}%'.format(
            float(coinup['percent_change_1h']))
        self.one_day = '{:.2f}%'.format(
            float(coinup['percent_change_24h']))
        self.one_week = '{:.2f}%'.format(
            float(coinup['percent_change_7d']))

        self.total = float('{:.2f}'.format(
            self.holding * self.price_now))
        self.paid = float('{:.2f}'.format(
            self.holding * self.price_paid))
        self.profit = float('{:.2f}'.format(
            self.total - self.paid))

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
        Coin.total_paid, Coin.total_now = 0, 0
        Coin.time = time.time()


def clr(lines=99):
    print('\n' * lines)


def bye():
    global Heart
    Heart = False
    print('bye now')


def makewindow(): ########title info

    window = Tk()
    window.title('.... .. CrYpToLiO .. ...')

    icon = PhotoImage(file='swirl.gif')
    window.tk.call('wm', 'iconphoto', window._w, icon)

    return window


def pie():

    coins = Coin.coins

    pc = Coin.total_now * 0.01

    outs = [
        coin for coin in coins if coin.total
        and coin.total < 4.6*pc
        ]

    others = sum(coin.total for coin in outs)

    labels = [coin for coin in coins if coin.total >= 4.6*pc]
    random.shuffle(labels)

    sizes = [coin.total for coin in labels]

    if others:

        if len(outs) > 1:
            strouts = ', '.join(str(out) for out in outs)
            labels.append('Others\n(' + strouts + ')')
            sizes.append(float('{:.2f}'.format(others)))
        else:
            uno = outs[0]
            labels.append(str(uno))
            sizes.append(uno.total)

    boom = [
        0.6 if wedge < 4*pc else
        0.2 if wedge < 10*pc else
        0.1 if wedge < 15*pc else
        0.0 for wedge in sizes
        ]

    colors = [
        'red', 'tan', 'powderblue',
        'green', 'olive', 'purple',
        'silver', 'springgreen', 'orange',
        'deepskyblue', 'yellow',
        'blue', 'papayawhip',
        ]

    pyplot.figure().canvas.set_window_title('your cryptolio pie')

    _, __, wedgetext = pyplot.pie(
        sizes, labels=labels, colors=colors, explode=boom,
        wedgeprops={'linewidth': 2, 'edgecolor': 'darkorange'},
        autopct='', startangle=275, #shadow=True,
        )

    for i, wedge in enumerate(wedgetext):
        wedge.set_text(
            "{:.1f}%".format(sizes[i] / Coin.total_now * 100)
            )

            # "${}\n{:.1f}%".format(
                # sizes[i], sizes[i] / Coin.total_now * 100))

    pyplot.axis('equal')

    pyplot.show()


def wait_a_bit(more):

    if more < 2: more = 2
    print('[..wait {} secs..]'.format(int(more)))


def refresh_it():

    watch = time.time() - Coin.time

    if watch < 60:
        wait_a_bit(60-watch)

    else:
        Coin.data = lookup()
        if Coin.data is not None:
            Coin.reset()
            Coin.folio = folio()
            Coin.coins = pandora()
            print('[data updated]')
            windolio()


def windolio():

    window = Coin.window

    columns = [
        'Rank', 'Name', 'Price Now',
        '1 Hour', '1 Day', '1 Week',
        'Holding', 'Spent', 'Value', 'Profit',
        ] # 'Price Paid', 'Profit Per',

    for colnum, colhead in enumerate(columns):

        header = Label(window, text=colhead, font='bold',
                       bg=['yellow3', 'gold3'][colnum%2])
        header.grid(row=0, column=colnum, sticky=N+S+E+W)

    the_row = 1

    for coin in Coin.coins:

        for colnum, colval in enumerate(columns):

            if colval.startswith('1'):
                if float(coin.columns[colval][:-2]) < 0:
                    color = 'red'
                else:
                    color = 'green'
            else:
                color = 'black'

            cell = Label(
                window, text=coin.columns[colval],
                fg=color, bg=['yellow2', 'gold2'][colnum%2]
            )
            cell.grid(row=the_row, column=colnum, sticky=N+S+E+W)

        the_row += 1


    coin_totals = [
        (
            'Total Spent',
            '${:.2f}'.format(Coin.total_paid)
        ),
        (
            'Total Value',
            '${:.2f}'.format(Coin.total_now)
        ),
        (
            'Total Profit',
            '${:.2f}'.format(Coin.total_now - Coin.total_paid)
        ),
        ]

    the_col = 7

    for label, amount in coin_totals:

        cell = Label(window, text=label, bg='silver')
        cell.grid(row=the_row, column=the_col, sticky=S)

        the_row += 1

        cell = Label(window, text=amount, bg='silver')
        cell.grid(row=the_row, column=the_col)

        the_row -= 1
        the_col += 1

    the_row += 1

    fresh = Button(window, text='Refresh', bg='silver', command=refresh_it)
    fresh.grid(row=the_row, column=0)

    note = Label(window, text="(once per minute)", fg='grey55')
    note.grid(row=the_row, column=1)

    graph = Button(window, text="Make Pie", bg='silver', command=pie)
    graph.grid(row=the_row, column=6)

    window.mainloop()

    return bye


def printscreen():

    print('---------------------------')

    for coin in Coin.coins:

        print(coin.name)
        print(' Price: $' + str(coin.price_now))
        print(' Rank:', coin.rank)
        print(' Holding:', coin.holding)
        print(' Paid: ${0:.2f}'.format(coin.paid))
        print(' Now: ${}'.format(coin.total))

        print('---------------------------')

    print()

    print(
        'Portfolio value: ${0:.2f}'.format(Coin.total_now))

    print('Portfolio profit: ${0:.2f}'.format(
        Coin.total_now - Coin.total_paid))

    print('---------------------------')

    print()

    return windolio


def pandora():

    return [
        Coin(mycoin, coin)
        for mycoin in Coin.folio
        for coin in Coin.data
        if mycoin['symbol'] == coin['symbol']
        ]


def lookup():

    lookups = {
        'CoinMarketCap':
        'https://api.coinmarketcap.com/v1/ticker/?start=0&limit=300',
        }

    chose = lookups['CoinMarketCap']

    try:
        data = requests.get(chose)
        return data.json()
    except:
        print('Cannot update - Try later')
        return None


def folio():
    'something for now'

    clr(2)
    # porto = []

    # print(
        # ''' intro stuff


        # ''')

    # print(
        # ''' option text


        # ''')

    # while True:
        # crypto = input('Ticker: ').strip().upper()
        # if crypto == Coin.data['symbol']:
            # something somethimg..


    porto = [
        {
            'symbol': 'BTC',
            'holding': 0.42,
            'price_paid': 5000
        },
        {
            'symbol': 'LTC',
            'holding': 1,
            'price_paid': 140
        },
        {
            'symbol': 'ETH',
            'holding': 1,
            'price_paid': 350
        },
        {
            'symbol': 'XMR',
            'holding': 1,
            'price_paid': 150
        },
        {
            'symbol': 'KIN',
            'holding': 1000000,
            'price_paid': 0.00015
        },
        {
            'symbol': 'XRP',
            'holding': 2100,
            'price_paid': 0.50
        },
        {
            'symbol': 'ZRX',
            'holding': 230,
            'price_paid': 1.00
        },
        {
            'symbol': 'XLM',
            'holding': 1000,
            'price_paid': 0.25
        },
        ]

    return porto


def stone():

    Coin.data = lookup()

    if Coin.data is None:
        return bye

    Coin.folio = folio()

    Coin.coins = pandora()

    Coin.window = makewindow()

    return printscreen


def wonderwall(dance):
    'rock n roll'
    while Heart is True:
        step = dance()
        dance = step


if __name__ == '__main__':

    wonderwall(stone)
