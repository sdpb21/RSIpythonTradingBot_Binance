from binance.client import Client
import config
import pandas
import talib
import datetime
import time

symbol = "BTCFDUSD"
usd = 200
number_of_candles = 200
rsi_size = 4

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

        time.sleep(0.3)
