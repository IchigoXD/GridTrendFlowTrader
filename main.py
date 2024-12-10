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
    Volume = float(config['Volume'])
    SymbolName = str(config['symbol'])
    pipdelay = float(config['pipdelay'])

    print(f"Username: {username}, Server: {server} GridSize: {GridSize}")

    mt5.initialize()
    mt5.login(username, password, server)

    OrdersBuyPrices = []
    OrdersSellPrices = []
    
    nextSellOrderTrigerPrice = 0.00
    nextBuyOrderTrigerPrice = 0.00
    symbol = mt5.symbol_info(SymbolName)

    lastOrderPrice = symbol.ask
    nextBuyOrderTrigerPrice = symbol.ask
    nextSellOrderTrigerPrice = symbol.ask

    while True:
        print(mt5.last_error())
        symbol = mt5.symbol_info(SymbolName)
        if nextBuyOrderTrigerPrice - pipdelay <= symbol.ask:
            print(f'\n{time.asctime()}: Buy Order on {nextBuyOrderTrigerPrice} with delay {nextBuyOrderTrigerPrice - pipdelay} trggired. delta: {nextBuyOrderTrigerPrice - pipdelay - symbol.ask}')
            market_order(symbol.name,Volume,'buy')
            lastOrderPrice = nextBuyOrderTrigerPrice
            if nextBuyOrderTrigerPrice not in OrdersBuyPrices:
                OrdersBuyPrices.append(nextBuyOrderTrigerPrice)
            i = 1
            noNewVal = True
            while noNewVal:
                nextBuyOrderTrigerPrice = lastOrderPrice + GridSize * i 
                print(f'{time.asctime()}: Trying to set new buy on {nextBuyOrderTrigerPrice}')
                if nextBuyOrderTrigerPrice in OrdersBuyPrices:
                    print(f'{time.asctime()}: Allready buy trade on {nextBuyOrderTrigerPrice}')
                    i = i + 1
                else:
                    noNewVal = False
            i = 1
            noNewVal = True
            while noNewVal:
                nextSellOrderTrigerPrice = lastOrderPrice - GridSize * i
                print(f'{time.asctime()}: Try to set new sell on {nextBuyOrderTrigerPrice}')
                if nextSellOrderTrigerPrice in OrdersSellPrices:
                    i = i + 1
                    print(f'{time.asctime()}: Allready sell trade on {nextBuyOrderTrigerPrice}')
                else:
                    noNewVal = False                    

        if nextSellOrderTrigerPrice + pipdelay >= symbol.bid :
            print(f'\n{time.asctime()}: Sell Order on {nextSellOrderTrigerPrice} with delay {nextSellOrderTrigerPrice + pipdelay} trigged. delta: {nextSellOrderTrigerPrice + pipdelay - symbol.bid}')
            market_order(symbol.name,Volume,'sell')
            lastOrderPrice = nextSellOrderTrigerPrice
            if nextSellOrderTrigerPrice not in OrdersSellPrices:
                OrdersSellPrices.append(nextSellOrderTrigerPrice)
            i = 1
            noNewVal = True
            while noNewVal:
                nextBuyOrderTrigerPrice = lastOrderPrice + GridSize * i
                print(f'{time.asctime()}: Trying to set new buy on {nextBuyOrderTrigerPrice}')
                if nextBuyOrderTrigerPrice in OrdersBuyPrices:
                    print(f'{time.asctime()}: Allready buy trade on {nextBuyOrderTrigerPrice}')
                    i = i + 1
                else:
                    noNewVal = False
            i = 1
            noNewVal = True
            while noNewVal:
                nextSellOrderTrigerPrice = lastOrderPrice - GridSize * i
                print(f'{time.asctime()}: Try to set new sell on {nextBuyOrderTrigerPrice}')
                if nextSellOrderTrigerPrice in OrdersSellPrices:
                    i = i + 1
                    print(f'{time.asctime()}: Allready sell trade on {nextBuyOrderTrigerPrice}')
                else:
                    noNewVal = False                    

    print('Program End..')