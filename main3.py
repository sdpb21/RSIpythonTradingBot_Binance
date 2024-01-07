from binance.client import Client
import config
import pandas
import talib
import datetime
import time

symbol = "BTCFDUSD"
usd = 100
number_of_candles = 200
rsi_size = 2
buy = False
buyPrice = 100000
quantity = 0
sumProfit = 0

if __name__ == '__main__':
    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')
    while True:

        candles = spot_client.get_historical_klines(
            symbol=symbol,
            # interval=Client.KLINE_INTERVAL_1HOUR,
            interval=Client.KLINE_INTERVAL_15MINUTE,
            # interval=Client.KLINE_INTERVAL_1MINUTE,
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

        print(round(rsi, 3), datetime.datetime.now())

        # time.sleep(0.3)

        if not buy and rsi < 25.0:
            buy = True
            buyPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
            print("************************************ buy price:", buyPrice)
            quantity = usd / buyPrice
            # comprar

        actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
        minutes = datetime.datetime.now().minute
        boolMinutes = minutes == 0 or minutes == 15 or minutes == 30 or minutes == 45
        # time.sleep(60.0)

        if buy and buyPrice < actualPrice and boolMinutes:
            # vender
            print("************************************ sell price:", actualPrice)
            usdAfterSell = quantity * actualPrice
            profit = usdAfterSell - usd
            sumProfit += profit
            print("profit:", profit, "sumProfit: ", sumProfit)
            if rsi <= 75.0:
                buyPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
                print("************************************ buy price:", buyPrice)
                # comprar otra vez
            if rsi > 75.0:
                buy = False

        time.sleep(59.0)
