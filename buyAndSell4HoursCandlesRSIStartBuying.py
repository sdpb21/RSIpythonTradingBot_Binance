from binance.client import Client
import config
import pandas
import talib
import datetime
import time

symbol = "BTCFDUSD"
usd = 179
number_of_candles = 200
rsi_size = 2
buy = False
buyPrice = 0
sellPrice = 1000000
# quantity = 0.00725
rsiMin = 99.01
rsiMax = 99.99

if __name__ == '__main__':
    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')
    while True:

        try:

            candles = spot_client.get_historical_klines(
                symbol=symbol,
                # interval=Client.KLINE_INTERVAL_1HOUR,
                # interval=Client.KLINE_INTERVAL_15MINUTE,
                interval=Client.KLINE_INTERVAL_4HOUR,
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

            actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
            print(actualPrice, '\t', round(rsi, 3), '\t', datetime.datetime.now())

            # time.sleep(0.3)
            minutes = datetime.datetime.now().minute
            hours = datetime.datetime.now().hour
            boolHours = hours == 2 or hours == 4 or hours == 8 or hours == 12 or hours == 16 or hours == 20
            boolMinutes = minutes == 30 and boolHours

            if not buy and actualPrice < sellPrice and rsi < rsiMin and boolMinutes:
                buyPrice = actualPrice
                quantity = round(usd / buyPrice, 5)
                params = {
                        "symbol": symbol,
                        "side": 'BUY',
                        "type": "LIMIT",
                        "timeInForce": "GTC",
                        "quantity": quantity,
                        "price": buyPrice
                    }
                orderID = spot_client.create_order(**params).get('orderId')
                print("orderId:", orderID)
                
                orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                print(orderStatus)
                while orderStatus != "FILLED":
                    time.sleep(2.0)
                    print("waitin' to get FILLED")
                    orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                    print(orderStatus)
                print("************************************ buy price:", buyPrice)
                print("************************************ quantity:", quantity)
                print("************************************ USD:", usd)
                buy = True
                buyPrice = 0
                # comprar

            if buy and buyPrice < actualPrice and rsi > rsiMax and boolMinutes:
                # vender
                sellPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

                params = {
                        "symbol": symbol,
                        "side": 'SELL',
                        "type": "LIMIT",
                        "timeInForce": "GTC",
                        "quantity": quantity,
                        "price": sellPrice
                    }
                orderID = spot_client.create_order(**params).get('orderId')
                print("orderId:", orderID)
                
                orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                print(orderStatus)
                while orderStatus != "FILLED":
                    time.sleep(2.0)
                    print("waitin' to get FILLED")
                    orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                    print(orderStatus)
                
                print("************************************ sell price:", sellPrice)
                usd = sellPrice * quantity
                print("************************************ quantity:", quantity)
                print("************************************ USD:", usd)
                buy = False

            secs = datetime.datetime.now().second
            time.sleep(60.0 - secs)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(59.0)
            continue
