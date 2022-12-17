import ccxt 
import pandas as pd
from datetime import datetime

#reliance['EWMA30'] = reliance['Close'].ewm(span=30).mean()
def get_lists():
    exchange = ccxt.binance({
                'enableRateLimit': True, # required https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
                    'options': {
                        'defaultType': 'future',
                            },
                        })
    spot_exchange = ccxt.binance({
                'enableRateLimit': True, # required https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
                    'options': {
                        'defaultType': 'spot',
                            },
                        })
    futures = exchange.fetch_markets()
    spot = spot_exchange.fetch_markets()

    spot_list = []
    for x in range(len(spot)):
        id = spot[x]['id']
        spot_list.append(id)
    

    #remove plus busd market from futures
    futures_list = []
    for x in range(len(futures)):
        id = futures[x]['id']
        baseId = futures[x]['baseId']
        quoteId = futures[x]['quoteId']
        usdtpair = baseId+'USDT'
        if quoteId == 'BUSD' and usdtpair in spot:
            pair = usdtpair
        else:
            pair = id
        if pair in spot_list:
            futures_list.append(pair)
            
    #futures_list = ['ETHUSDT','ADAUSDT']
    #50/200 h4 h1 m15 vwap vol 5/21 vol
    #50/200 h1 m15 vwap vol 5/21
    #50/200 h1 m15 vwap
    bullish_list = []
    for x in range(len(futures_list)):
        id = futures_list[x]
        data = spot_exchange.fetch_ohlcv(symbol=id,timeframe='15m',limit=2401)
        df = pd.DataFrame(data[:-1],columns=['time','open','high','low','close','volume'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        v = df['volume'].values
        tp = (df['low'] + df['close'] + df['high']).div(3).values
        df['vwap'] = ((tp * v).cumsum() / v.cumsum())
        df['SMA5'] = df['close'].rolling(5).mean()
        df['SMA50'] = df['close'].rolling(20).mean()
        df['SMA200'] = df['close'].rolling(200).mean()
        df['SMA800'] = df['close'].rolling(800).mean()

        df['VOLMA5'] = df['volume'].rolling(20).mean()
        df['VOLMA13'] = df['volume'].rolling(52).mean()

        
        bearish_list = ['ADAUSDT']
        buy_cond = df['SMA5'].iloc[-1] > df['SMA50'].iloc[-1] and df['SMA50'].iloc[-1] > df['SMA200'].iloc[-1] and df['SMA200'].iloc[-1] > df['SMA800'].iloc[-1] and df['VOLMA5'].iloc[-1] > df['VOLMA13'].iloc[-1] and df['VOLMA13'].iloc[-1] > df['VOLMA34'].iloc[-1]
        if buy_cond:
            bullish_list.append(id)


    return(bullish_list,bearish_list)

print(get_lists())



