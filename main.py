import MetaTrader5 as mt5
import time
from scripts.mt5_trade_functions import market_order, close_all_positions
import json

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == '__main__':

    config = load_config('config.json')

    username = int(config['username'])
    password = str(config['password'])
    server = str(config['server'])
    GridSize = float(config['GridSize'])
    print(f"Username: {username}, Server: {server} GridSize: {GridSize}")


    print('Program Stratred....')
    # open your own trading account: https://icmarkets.com/?camp=60457
    login = username#88548079
    #password = password
    #server = 'MetaQuotes-Demo'

    mt5.initialize()
    mt5.login(login, password, server)

    """
    Trading bot logic
    
    1) Opens a Trade on EURUSD 1 lot
    2) Strategy waits 5 seconds and then closes the position
    """

    OrdersBuyPrices = []
    OrdersSellPrices = []
    #GridSize = 0.5
    Volume = 0.01
    symbol = mt5.symbol_info("XAUUSD")

    nextSellOrderTrigerPrice = 0.00
    nextBuyOrderTrigerPrice = 0.00

    lastOrderPrice = symbol.ask
    nextBuyOrderTrigerPrice = symbol.ask
    nextSellOrderTrigerPrice = symbol.ask


    while True:
        symbol = mt5.symbol_info("XAUUSD")
        if nextBuyOrderTrigerPrice < symbol.ask:
            print('\nOrder Triggerd.')
            market_order(symbol.name,Volume,'buy')
            lastOrderPrice = nextBuyOrderTrigerPrice
            if nextBuyOrderTrigerPrice not in OrdersBuyPrices:
                OrdersBuyPrices.append(nextBuyOrderTrigerPrice)
            i = 0
            noNewVal = True
            while noNewVal:
                print('Try to set new buy')
                nextBuyOrderTrigerPrice = lastOrderPrice + GridSize * i
                if nextBuyOrderTrigerPrice in OrdersBuyPrices:
                    i = i + 1
                else:
                    noNewVal = False
            noNewVal = True
            while noNewVal:
                print('Try to set new sell')
                nextSellOrderTrigerPrice = lastOrderPrice - GridSize * i
                if nextSellOrderTrigerPrice in OrdersSellPrices:
                    i = i + 1
                else:
                    noNewVal = False                    

        if nextSellOrderTrigerPrice > symbol.ask :
            print('\nOrder Triggerd.')
            market_order(symbol.name,Volume,'sell')
            lastOrderPrice = nextSellOrderTrigerPrice
            if nextSellOrderTrigerPrice not in OrdersSellPrices:
                OrdersSellPrices.append(nextSellOrderTrigerPrice)
            i = 0
            noNewVal = True
            while noNewVal:
                print('Try to set new buy')
                nextBuyOrderTrigerPrice = lastOrderPrice + GridSize * i
                if nextBuyOrderTrigerPrice in OrdersBuyPrices:
                    i = i + 1
                else:
                    noNewVal = False
            noNewVal = True 
            while noNewVal:
                print('Try to set new sell')
                nextSellOrderTrigerPrice = lastOrderPrice - GridSize * i
                if nextSellOrderTrigerPrice in OrdersSellPrices:
                    i = i + 1
                else:
                    noNewVal = False                   
        
        print(f'\r{time.asctime()}: NextBuy: {nextBuyOrderTrigerPrice}  NextSell: {nextSellOrderTrigerPrice}  Ask: {symbol.ask}  {OrdersBuyPrices}  {OrdersSellPrices}',end='')

    print('Program End..')