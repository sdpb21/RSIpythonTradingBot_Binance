from binance.client import Client
import config
import pandas
import talib
import time
import datetime

symbol = "BTCFDUSD"
number_of_candles = 200
ema_size = 3
ema1 = 0.0
ema2 = 0.0
mPast = 0.0
buy = False
usd = 100.0
buyPrice = 100000.0
quantity = 0.0
sumProfit = 0.0
i = 0

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')
    while True:

        try:

            seconds = datetime.datetime.now().second
            i += 1
            print(seconds, i)

            if seconds == 0:

                candles = spot_client.get_historical_klines(
                    symbol=symbol,
                    # interval=Client.KLINE_INTERVAL_1HOUR,
                    # interval=Client.KLINE_INTERVAL_15MINUTE,
                    interval=Client.KLINE_INTERVAL_1MINUTE,
                    limit=number_of_candles
                )

                candles_dataframe = pandas.DataFrame(candles)

                candles_dataframe.columns = ["time", "open", "high", "low", "close", "volume", "close Time",
                                             "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                             "Taker Buy Quote Asset Volume", "Ignore"]

                candles_dataframe['human_time'] = pandas.to_datetime(candles_dataframe['time'], unit='ms')

                candles_dataframe[["open", "high", "low", "close", "volume"]] = candles_dataframe[
                    ["open", "high", "low", "close", "volume"]].astype(float)

                # ema = int(talib.EMA(candles_dataframe['close'], timeperiod=ema_size).iloc[-1])
                ema2 = talib.EMA(candles_dataframe['close'], timeperiod=ema_size).iloc[-1]
                # ema2 = talib.EMA(candles_dataframe['open'], timeperiod=ema_size).iloc[-1]

                # print(round(ema2, 3), '\t', datetime.datetime.now())

                m = ema2 - ema1

                ema1 = ema2

                if not buy and (mPast < 0.0) and (m > 0.0):
                    buyPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
                    print("************************************ buy price:", buyPrice)
                    buy = True
                    quantity = usd / buyPrice

                actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
                print(actualPrice, '\t', round(m, 3), '\t', datetime.datetime.now())

                if buy and actualPrice > buyPrice and (mPast > 0.0) and (m < 0.0):
                    print("************************************ sell price:", actualPrice)
                    usdAfterSell = quantity * actualPrice
                    profit = usdAfterSell - usd
                    sumProfit += profit
                    print("profit:", profit, "sumProfit: ", sumProfit)
                    buy = False

                mPast = m

                time.sleep(58.0)

            else:

                time.sleep(60 - seconds)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(59.0)
            continue
            