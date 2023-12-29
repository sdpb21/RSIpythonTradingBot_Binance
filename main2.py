import datetime
import time

from playsound import playsound
# from binance.client import Client
from binance.spot import Spot
import pandas
import talib

symbol = "BTCFDUSD"
timeframe = "1m"
number_of_candles = 200
rsi_size = 2
ema_size = 7
ema_size2 = 15

if __name__ == '__main__':
    # Psuedocode
    # 1. Set the query timeframe, so it is consistent with the timeframe used for other exchanges
    # 2. Ensure that no more than 1000 candles retrieved (hard limit from Binance)
    # 3. Retrieve the candles
    # 4. Format the candles into a dataframe, and label columns accordingly

    # Step 1: Convert the timeframe into a Binance friendly format
    # timeframe = set_query_timeframe(timeframe=timeframe)
    # Step 2: Make sure that no more than 1000 candles are being retrieved as this is a hard limit from Binance
    if number_of_candles > 1000:
        raise ValueError("Number of candles cannot be greater than 1000")
    # Step 3: Retrieve the candles
    # Instantiate the Spot Client
    spot_client = Spot()  # <- No API keys needed for this request

    # to show all columns when printing to screen:
    pandas.set_option('display.max_columns', None)

    # candles_dataframe['rsi'] = talib.RSI(candles_dataframe['close'], timeperiod=rsi_size)
    # print(candles_dataframe)

    # candles_dataframe[ema_name] = talib.EMA(candles_dataframe['close'], timeperiod=ema_size)
    # print(candles_dataframe)
    buy = False

    while True:

        try:
            # Retrieve the candles / OHLC data
            candles = spot_client.klines(
                symbol=symbol,
                interval=timeframe,
                limit=number_of_candles
            )
            # print(candles)
        except Exception as e:
            print("exception 1:", e)

        try:
            # Convert to a dataframe
            candles_dataframe = pandas.DataFrame(candles)
            # print(candles_dataframe)
        except Exception as e:
            print("Exception 2:", e)

        try:
            # Step 4: Format the columns of the Dataframe.
            # Documentation: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
            candles_dataframe.columns = ["time", "open", "high", "low", "close", "volume", "close Time",
                                         "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                         "Taker Buy Quote Asset Volume", "Ignore"]
            # print("candles_dataframe.columns = [")
        except Exception as e:
            print("Exception 3:", e)

        try:
            # Add a human time column which is based on a DateTime fo the 'time' column
            candles_dataframe['human_time'] = pandas.to_datetime(candles_dataframe['time'], unit='ms')
            # print("candles_dataframe['human_time'] = pandas.t")
        except Exception as e:
            print("Exception 4:", e)

        try:
            # Make sure that the "open", "high", "low", "close", "volume" columns are floats
            candles_dataframe[["open", "high", "low", "close", "volume"]] = candles_dataframe[
                ["open", "high", "low", "close", "volume"]].astype(float)
            # print('["open", "high", "low", "close", "volume"]].astype(float)')
        except Exception as e:
            print("Exception 5:", e)

        try:
            rsi = talib.RSI(candles_dataframe['close'], timeperiod=rsi_size).iloc[-1]
            # print("rsi = talib.RSI(candles_dataframe['close'], timeperiod=rsi_size).iloc[-1]")
        except Exception as e:
            print("Exception 6:", e)

        try:
            print(rsi, datetime.datetime.now())
        except Exception as e:
            print("Exception 7:", e)

        try:
            if rsi <= 0.1 and not buy:
                buyPrice = float(spot_client.ticker_price(symbol).get('price'))
                print("buy price:", buyPrice)
                buy = True
                # while True:
                #     playsound("/home/asdf/Downloads/beep-04.wav")
                #     time.sleep(1.0)
            if buy and rsi >= 99.9:
                priceNow = float(spot_client.ticker_price(symbol).get('price'))

            # noinspection PyUnboundLocalVariable
            if buy and rsi >= 99.9 and priceNow > buyPrice:
                print("sell price:", priceNow)
                buy = False
                # print("bought at: ", buyPrice)
                playsound("/home/asdf/Downloads/beep-04.wav")
                # break
        except Exception as e:
            print("Exception 8:", e)

        try:
            # print("time.sleep(1.0)")
            time.sleep(2.0)
        except Exception as e:
            print("Exception 9:", e)

        # ema = int(talib.EMA(candles_dataframe['close'], timeperiod=ema_size).iloc[-1])
        # ema2 = int(talib.EMA(candles_dataframe['close'], timeperiod=ema_size2).iloc[-1])
        # print("ema_", ema_size, ema, " ema_", ema_size2, ema2)
        # time.sleep(1.0)
