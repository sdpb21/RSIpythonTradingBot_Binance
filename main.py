import time

import playsound
from binance.spot import Spot as Client
import pandas
import talib

symbol = "BTCFDUSD"
timeframe = "1m"
number_of_candles = 200
rsi_size = 2
ema_size = 7
ema_size2 = 15

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
spot_client = Client()  # <- No API keys needed for this request

# to show all columns when printing to screen:
pandas.set_option('display.max_columns', None)

# candles_dataframe['rsi'] = talib.RSI(candles_dataframe['close'], timeperiod=rsi_size)
# print(candles_dataframe)

# candles_dataframe[ema_name] = talib.EMA(candles_dataframe['close'], timeperiod=ema_size)
# print(candles_dataframe)

while True:
    # Retrieve the candles / OHLC data
    candles = spot_client.klines(
        symbol=symbol,
        interval=timeframe,
        limit=number_of_candles
    )
    # Convert to a dataframe
    candles_dataframe = pandas.DataFrame(candles)
    # Step 4: Format the columns of the Dataframe.
    # Documentation: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
    candles_dataframe.columns = ["time", "open", "high", "low", "close", "volume", "close Time", "Quote Asset Volume",
                                 "Number of Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume",
                                 "Ignore"]
    # Add a human time column which is based on a DateTime fo the 'time' column
    candles_dataframe['human_time'] = pandas.to_datetime(candles_dataframe['time'], unit='ms')
    # Make sure that the "open", "high", "low", "close", "volume" columns are floats
    candles_dataframe[["open", "high", "low", "close", "volume"]] = candles_dataframe[
        ["open", "high", "low", "close", "volume"]].astype(float)

    rsi = talib.RSI(candles_dataframe['close'], timeperiod=rsi_size).iloc[-1]
    print(rsi)
    if rsi <= 1:
        price = float(spot_client.ticker_price(symbol).get('price'))
        print("buy price:", price)
        while True:
            playsound("/home/asdf/Downloads/beep-04.wav")
            time.sleep(1.0)
    time.sleep(1.0)

    # ema = int(talib.EMA(candles_dataframe['close'], timeperiod=ema_size).iloc[-1])
    # ema2 = int(talib.EMA(candles_dataframe['close'], timeperiod=ema_size2).iloc[-1])
    # print("ema_", ema_size, ema, " ema_", ema_size2, ema2)
    # time.sleep(1.0)
