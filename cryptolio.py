#!/usr/bin/env python3

""" Funky Portfolio for Cryptocurrency """

import time
import random
import requests

from matplotlib import pyplot
from tkinter import Tk, PhotoImage, Label, Button, N, S, E, W


  #####################
 ##### CrYpToLiO #####
### by stOneskull ###
#####################
###  inspired by  ###
 ###   codemy.com  ###
  #####################

__version__ = '0.2.7'

########### - make intro, settings, buttons
## to do ## - add user input for folio details, save data
########### - use data from livecoinwatch.com or coincap.io


Heart = True


class Coin:
    """ machina """
    time = time.time()
    total_paid = 0
    total_now = 0
    show_pie_totals = 0
    user = 0

    def __init__(self, mycoin, coinup):

        self.name = coinup['name']
        self.rank = coinup['rank']

        self.holding = float(mycoin['holding'])
        self.price_now = float(coinup['price_usd'])
        self.price_paid = float(mycoin['price_paid'])

        if self.holding:
            self.profit_per = '{:.2f}'.format(
                self.price_now - self.price_paid)
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
        Coin.total_paid = 0
        Coin.total_now = 0
        Coin.time = time.time()


class Champ:
    def __init__(self):
        Coin.user += 1


def clr(lines=99):
    print('\n' * lines)


def bye():
    global Heart
    Heart = False
    print('\nbye now\n')


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

    labels = [coin for coin in coins if coin not in outs]
    random.shuffle(labels)

    sizes = [coin.total for coin in labels]

    if others:

        if len(outs) > 1:
            strouts = ', '.join(str(out) for out in outs)
            labels.append('\n\nOthers\n(' + strouts + ')')
            sizes.append(float('{:.2f}'.format(others)))
        else:
            uno = outs[0]
            labels.append(str(uno))
            sizes.append(uno.total)

    boom = [
        0.4 if wedge < 5*pc else
        0.2 if wedge < 10*pc else
        0.1 if wedge < 20*pc else
        0.0 for wedge in sizes
        ]

    colors = [
        'red', 'tan', 'powderblue',
        'green', 'olive', 'purple',
        'silver', 'springgreen', 'orange',
        'deepskyblue', 'yellow',
        'blue', 'papayawhip',
        ]

    fig = pyplot.figure()
    fig.canvas.set_window_title('your cryptolio pie')
    fig.set_facecolor('palegreen')

    _, __, wedgetext = pyplot.pie(
        sizes, labels=labels, colors=colors, explode=boom,
        wedgeprops={'linewidth': 2, 'edgecolor': 'darkorange'},
        autopct='', startangle=275, #shadow=True,
        )

    for i, wedge in enumerate(wedgetext):

        wedge.set_text(
            "${}\n{:.1f}%".format(sizes[i], sizes[i] / pc)
            if Coin.show_pie_totals
            else
            "{:.1f}%".format(sizes[i] / pc)
            )

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


def toggle():

    if Coin.show_pie_totals:
        Coin.show_pie_totals = 0
        print('[pie values off]')
    else:
        Coin.show_pie_totals = 1
        print('[pie values on]')


def windolio():

    window = Coin.window


# Column Headers, Row 0 #

    columns = [
        'Rank', 'Name', 'Price Now',
        '1 Hour', '1 Day', '1 Week',
        'Holding', 'Spent', 'Value', 'Profit',
        # 'Price Paid', 'Profit Per',
        ]

    for colnum, colhead in enumerate(columns):

        header = Label(
            window, text=colhead, font='bold',
            bg=['yellow3', 'gold3'][colnum%2]
            )
        header.grid(
            row=0, column=colnum, sticky=N+S+E+W
            )

# Column Headers, Done #


# Row Entries #

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
                fg=color,
                bg=['yellow2', 'gold2'][colnum%2]
                )
            cell.grid(row=the_row, column=colnum, sticky=N+S+E+W)

        the_row += 1

# Row Entries, Done #


# Totals #

    coin_totals = [
        ('Total Spent',
         '${:.2f}'.format(Coin.total_paid)
         ),
        ('Total Value',
         '${:.2f}'.format(Coin.total_now)
         ),
        ('Total Profit',
         '${:.2f}'.format(Coin.total_now - Coin.total_paid)
         ),
        ]

    the_col = (
        columns.index('Spent') if 'Spent' in columns
        else -3
        )

    for label, amount in coin_totals:

        cell = Label(
            window, text=label, bg='silver',
            #font=('bold' if 'Value' in label else None)
            )
        cell.grid(
            row=the_row, column=the_col, sticky=S, pady=5
            )

        the_row += 1

        cell = Label(
            window, text=amount, bg='silver',
            font=('bold' if 'Value' in label else None)
            )
        cell.grid(row=the_row, column=the_col, sticky=N)

        the_row -= 1
        the_col += 1

    the_row += 1

# Totals, Done #


# Refresh Button
    fresh = Button(
        window, text='Refresh', bg='silver',
        command=refresh_it
        )
    fresh.grid(
        row=the_row, column=0,
        padx=5, pady=5
        )

    note = Label(window, text="(once per minute)", fg='grey55')
    note.grid(row=the_row, column=1)

# Pie Button
    graph = Button(
        window, text="Make Pie", bg='silver',
        command=pie
        )
    graph.grid(
        row=the_row,
        column=(
            columns.index('Holding')
            if 'Holding' in columns
            else -4
            )
        )

# Toggle Pie dollar values
    tog = Button(
        window, text="Toggle Pie", bg='silver',
        command=toggle
        )
    tog.grid(
        row=the_row-1,
        column=(
            columns.index('Holding')
            if 'Holding' in columns
            else -4
            ),
        padx=5, pady=5
        )

# Gooey
    window.mainloop()

    return bye


def printscreen():

    print('---------------------------')

    for coin in Coin.coins:

        print(coin)
        print(' Price: $' + str(coin.price_now))
        print(' Rank:', coin.rank)
        print(' Holding:', coin.holding)
        print(' Paid: ${0:.2f}'.format(coin.paid))
        print(' Now: ${}'.format(coin.total))
        print('---------------------------')

    print()
    print('Portfolio value: ${0:.2f}'.format(Coin.total_now))
    print('Portfolio profit: ${0:.2f}'.format(
        Coin.total_now - Coin.total_paid))
    print('---------------------------')
    print()


def pandora():

    # box = []
    # for coin in Coin.data:
        # for mycoin in Coin.folio:
            # if mycoin['symbol'] == coin['symbol']:
                # box.append(Coin(mycoin, coin))

    box = [
        Coin(mycoin, coin)
        for coin in Coin.data
        for mycoin in Coin.folio
        if mycoin['symbol'] == coin['symbol']
        ]

    return box


def lookup():

    lookups = {
        'CoinMarketCap':
        'https://api.coinmarketcap.com/v1/ticker/?start=0&limit=500',
        }
    chose = lookups['CoinMarketCap']

    try:
        data = requests.get(chose)
        return data.json()
    except:
        print('Cannot update - Try later')


def folio():
    'something for now'

    clr(2)
    # porto = []

    # print(
        # ''' intro stuff
# we will be entering in details of each cryptocurrency
# you can choose to watch other coins by entering them and choosing 0 balance
# for the paid price option you can give a rough average
# this average will be used when buying more at a later date
# when buying more you will enter the price paid for that lot

        # ''')

    # print(
        # ''' option text
# enter the ticker name listed on coinmarketcap
# eg. bitcoin is BTC ripple is XRP ethereum is ETH stellar is XLM

        # ''')

    # while Heart:
        # crypto = input('Ticker: ').strip().upper()
        # if crypto == Coin.data['symbol']:
            # something somethimg..


    sample_porto = [
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

    porto = sample_porto
    return porto


def rock():
    Coin.data = lookup()
    if Coin.data is None:
        return bye
    Coin.folio = folio()
    Coin.coins = pandora()
    Coin.window = makewindow()
    printscreen()
    return windolio


def main(dance):
    'rock n roll'
    while Heart is True:
        step = dance()
        dance = step


if __name__ == '__main__':
    user = Champ()
    main(rock)
