import config
from binance.client import Client
import time
import datetime
import pandas
import talib

symbol = "BTCFDUSD"
usd = 100
buy = False
number_of_candles = 200
rsi_size = 2

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')
    buyPrice = 0
    quantity = 0
    sumProfit = 0

    while True:

        try:

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

            rsi = talib.RSI(candles_dataframe['close'], timeperiod=rsi_size).iloc[-1]

            if not buy and rsi < 20.0:
                buyPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
                quantity = usd / buyPrice
                buy = True
                print("************************************ buy price:", buyPrice)

            priceNow = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
            print(priceNow, round(rsi, 3), datetime.datetime.now())

            if buy and priceNow > buyPrice and rsi > 80.0:
                buy = False
                usdAfterSell = quantity * priceNow
                profit = usdAfterSell - usd
                sumProfit += profit
                print("************************************ sell price:", priceNow)
                print("profit:", profit, "sumProfit: ", sumProfit)

            time.sleep(59.0)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            continue
