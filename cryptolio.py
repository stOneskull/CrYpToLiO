#!/usr/bin/env python3

#############################
 ####     CrYpToLiO     ####
  ####  by stOneskull  ####
   #######################
  ###### inspired by ######
 ####### codemy.com  #######
##2018#################2018##

""" Funky Portfolio for Cryptocurrency """

__version__ = '0.3.1'

########### - intro, settings
## to do ## - user input for folio details
########### - user configurability


from tkinter import Tk, PhotoImage, N, E
from tkinter import Label, Button, W, S
from matplotlib import pyplot as plot
import webbrowser as web
import requests
import random
import pickle
import time


Heart = True


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


class Champ:
    def __init__(self):
        self.window = makewindow()
        self.folio = folio()


def clr(lines=99):
    print('\n' * lines)


def bye():
    global Heart
    Heart = False
    try:
        with open('cryptdata', 'wb') as jar:
            pickle.dump(user.folio, jar)
    except: pass
    print('\nbye now\n')


def windowtitle():
    return(
        ". .... .. CrYpToLiO .. ... " + __version__
        + time.strftime(
            " .. ... %Y-%m-%d %H:%M:%S ... ", time.localtime()
            )
        )


def makewindow():
    window = Tk()
    window.title(windowtitle())
    window.row = 0
    window.show_pie_totals = 0
    try:
        icon = PhotoImage(file='swirl.gif')
        window.tk.call('wm', 'iconphoto', window._w, icon)
    except: pass
    return window


def pie():
    "Holdings"

    plot.close()

    coins = user.coins

    pc = Coin.total_now * 0.01

    others = [
        coin for coin in coins
        if coin.total and coin.total < 4.9*pc
        ]
    othersum = sum(coin.total for coin in others)

    labels = [coin for coin in coins if coin not in others]
    random.shuffle(labels)

    sizes = [float('{:.2f}'.format(coin.total)) for coin in labels]

    if others:

        if len(others) > 1:
            strothers = ', '.join(str(other) for other in others)
            labels.append('Others\n(' + strothers + ')')
            sizes.append(float('{:.2f}'.format(othersum)))
        else:
            uno = others[0]
            labels.append(str(uno))
            sizes.append(float('{:2f}'.format(uno.total)))

    boom = [
        0.4 if wedge < 6*pc else
        0.2 if wedge < 10*pc else
        0.1 if wedge < 20*pc else
        0.0 for wedge in sizes
        ]

    colors = [
        'palevioletred', 'khaki', 'powderblue',
        'green', 'olive', 'purple',
        'silver', 'springgreen', 'orange',
        'deepskyblue', 'yellow', 'coral',
        'blue', 'papayawhip', 'red',
        ]

    plot.figure(0).canvas.set_window_title(
        'your cryptolio pie '
        + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        )
    plot.figure(0).set_facecolor('palegreen')

    _, __, wedgetext = plot.pie(
        sizes, labels=labels, colors=colors, explode=boom,
        wedgeprops={'linewidth': 2, 'edgecolor': 'darkorange'},
        autopct='', startangle=275, #shadow=True,
        )

    for wedge, text in enumerate(wedgetext):
        size = sizes[wedge]
        text.set_text(
            "${0:.2f}\n{1:.1f}%".format(size, size/pc)
            if user.window.show_pie_totals
            else "{:.1f}%".format(size/pc)
            )

    plot.axis('equal')

    plot.show(block=False)


def windolio():

    window = user.window

    window.columns = [ # keep in blocks
        'Rank', 'Price Now', 'Name', #keep rank first, can switch name/price
        #'Price Paid', 'Profit Per', #can switch both
        '1 Hour', '1 Day', '1 Week', #can switch all
        'Holding',                   #singleton block
        'Spent', 'Value', 'Profit',  #keep spent first, can switch value/profit
        ]


    def print_columns():
        "Column Headers, Row 0"
        for col_num, col_name in enumerate(window.columns):
            header = Label(
                window, text=col_name, font='bold',
                bg=['yellow3', 'gold3'][col_num % 2]
            )
            header.grid(row=0, column=col_num, sticky=N+S+E+W)


    def print_rows():
        "Coin Entries, Row 1 ->"
        window.row = 1
        for coin in user.coins:
            for col_num, col_name in enumerate(window.columns):
                val = coin.columns[col_name]
                cell = Label(
                    window,
                    text=(val if col_name not in [
                        'Price Now', 'Spent', 'Value', 'Profit']
                          else '${:.2f}'.format(val) if val > 1 or val < -1
                          else '${}'.format(val)),
                    fg=('black' if not col_name.startswith('1')
                        else 'red' if float(val[:-2]) < 0
                        else 'green'),
                    bg=['yellow2', 'gold2'][col_num % 2]
                    )
                cell.grid(row=window.row, column=col_num, sticky=N+S+E+W)
            window.row += 1


    def print_totals():
        col_num = window.columns.index('Spent')

        coin_totals = [
            ('Total Spent',
             '${:.2f}'.format(Coin.total_paid)),
            ('Total Value',
             '${:.2f}'.format(Coin.total_now)),
            ('Total Profit',
             '${:.2f}'.format(Coin.total_now - Coin.total_paid)),
            ]

        for label, amount in coin_totals:
            cell = Label(window, text=label, bg='silver')
            cell.grid(row=window.row, column=col_num, sticky=S, pady=5)
            cell = Label(
                window, text=amount, bg='silver',
                font=('bold' if 'Value' in label else None)
                )
            cell.grid(row=window.row+1, column=col_num, sticky=N)
            col_num += 1


    def refresh_button():
        col_num = window.columns.index('Rank')

        refresh = Button(
            window, text='Refresh', bg='silver',
            command=refresh_it
            )
        refresh.grid(row=window.row+1, column=col_num, padx=5, pady=5)

        note = Label(window, text="(once per minute)", fg='grey55')
        note.grid(row=window.row+1, column=col_num+1, sticky=S)


    def cmc_button():
        col_num = window.columns.index('Rank')

        cmc = Button(
            window, text='Visit CMC', bg='silver',
            command=lambda: web.open('https://coinmarketcap.com', new=2)
            )
        cmc.grid(row=window.row, column=col_num, padx=5, pady=5)

        globe = Label(
            window, text="Global Cap", fg='grey55')
        globe.grid(row=window.row, column=col_num+2, sticky=S)

        globe_cap = Label(
            window,
            text='${:.1f} Bil'.format(Coin.globe/1000000000), fg='grey55'
            )
        globe_cap.grid(row=window.row+1, column=col_num+2, sticky=N)


    def pie_buttons():
        col_num = window.columns.index('Holding')

        makepie = Button(window, text="Make Pie", bg='silver', command=pie)
        makepie.grid(row=window.row+1, column=col_num)

        tog = Button(
            window,
            text=("Pie $ on" if window.show_pie_totals
                  else "Pie $ off"),
            bg='silver', command=toggle
            )
        tog.grid(row=window.row, column=col_num, padx=5, pady=5)


    def toggle():
        if window.show_pie_totals:
            window.show_pie_totals = 0
            print('[pie values off]')
        else:
            window.show_pie_totals = 1
            print('[pie values on]')
        pie_buttons()


    def refresh_it():
        window.title(windowtitle())
        watch = time.time() - Coin.time
        if watch < 60:
            print('[..wait {} secs..]'.format(
                int(60-watch if watch > 2 else 2)))
        else:
            Coin.data = lookup()
            if Coin.data:
                Coin.reset()
                pandora()
                print('[data updated]')
                windolio()


    includes = {
        'Spent': [print_totals],
        'Rank': [refresh_button, cmc_button],
        'Holding': [pie_buttons],
        }

    loads = [print_columns, print_rows]

    for col, include in includes.items():
        if col in window.columns:
            loads += include

    for load in loads:
        load()

    window.mainloop()

    return bye


def pandora():
    user.coins = [
        Coin(mycoin, coin)
        for coin in Coin.data
        for mycoin in user.folio
        if mycoin['symbol'] == coin['symbol']
        ]


def lookup(choose='CMC'):

    lookups = {
        'CMC':
        'https://api.coinmarketcap.com/v1/ticker/?start=0&limit=500',
        'Globe':
        'https://api.coinmarketcap.com/v1/global/',
        }

    chose = lookups[choose]

    try:
        data = requests.get(chose)
        return data.json()
    except:
        print('\nCannot update\n')


def folio():
    'something for now'

    try:
        with open('cryptdata', 'rb') as jar:
            return pickle.load(jar)
    except: pass

    print(
        '''

    Hi

    I see you're new here

    Choose an option

        1 - Check out CrYpToLiO with sample data

        2 - Add your own portfolio

'''
    )

    time.sleep(3)

    print(
        '''

chose 1 for now..

sample data used..

'''
        )

    time.sleep(2)

    #chose = input('1 or 2? ')

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
            'holding': 0.23,
            'price_paid': 5000
        },
        {
            'symbol': 'LTC',
            'holding': 1.23,
            'price_paid': 140
        },
        {
            'symbol': 'ETH',
            'holding': 3,
            'price_paid': 350
        },
        {
            'symbol': 'XMR',
            'holding': 4,
            'price_paid': 150
        },
        {
            'symbol': 'KIN',
            'holding': 1000000,
            'price_paid': 0.00015
        },
        {
            'symbol': 'XRP',
            'holding': 2300,
            'price_paid': 0.75
        },
        {
            'symbol': 'ZRX',
            'holding': 150,
            'price_paid': 1.00
        },
        {
            'symbol': 'XLM',
            'holding': 1000,
            'price_paid': 0.42
        },
    ]

    clr(2)

    porto = sample_porto
    return porto


def printscreen():
    print('---------------------------')
    for coin in user.coins:
        print(coin.name)
        print(' Price: $' + str(coin.price_now))
        print(' Rank:', coin.rank)
        print(' Holding:', coin.holding)
        print(' Paid: ${0:.2f}'.format(coin.paid))
        print(' Now: ${}'.format(coin.total))
        print('---------------------------')
        time.sleep(0.23)
    print()
    print('Portfolio value: ${0:.2f}'.format(Coin.total_now))
    print('Portfolio profit: ${0:.2f}'.format(
        Coin.total_now - Coin.total_paid))
    print('---------------------------')
    print()
    return windolio


def step():
    Coin.data = lookup()
    if Coin.data is None: return bye
    Coin.globe = lookup('Globe')["total_market_cap_usd"]
    if Coin.globe is None: return bye
    pandora()
    return printscreen


def main(dance=step):
    'rock n roll'
    while Heart is True:
        step = dance()
        dance = step


if __name__ == '__main__':
    user = Champ()
    main()
