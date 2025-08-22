from binance.client import Client
import config
import pandas
import talib
import datetime
import time

sell = False
symbol = "BTCFDUSD"
number_of_candles = 200
rsi_size = 2
rsiMax = 99.5
quantity = 0.00010
usd = 0
candle_time = Client.KLINE_INTERVAL_15MINUTE
# candle_time = Client.KLINE_INTERVAL_1HOUR
# candle_time = Client.KLINE_INTERVAL_4HOUR
#########################
#sellPrice = 110500.23
#usd = sellPrice * quantity
#########################
if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')

    while not sell:

        try:

            candles = spot_client.get_historical_klines(
                symbol=symbol,
                interval=candle_time,
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

            minutes = datetime.datetime.now().minute
            hours = datetime.datetime.now().hour

            if candle_time == Client.KLINE_INTERVAL_15MINUTE:
                boolMinutes = minutes == 0 or minutes == 15 or minutes == 30 or minutes == 45

            if candle_time == Client.KLINE_INTERVAL_1HOUR:
                boolMinutes = minutes == 59

            if candle_time == Client.KLINE_INTERVAL_4HOUR:
                boolHours = hours == 0 or hours == 4 or hours == 8 or hours == 12 or hours == 16 or hours == 20
                boolMinutes = minutes == 59 and boolHours

            if not sell and rsi > rsiMax and boolMinutes:
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
                sell = True

            secs = datetime.datetime.now().second
            time.sleep(59.0 - secs)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(59.0)
            continue
    
    # while not sell ends here
    if sell:

        try:

            quantity = quantity + 0.00001
            buyPrice = round(usd/quantity, 2)
            # usd/actualPrice=quantity => usd=quantity*actualPrice => actualPrice=usd/quantity
            # quantity = round(usd / buyPrice, 5)
            print("************************************ buy price:", buyPrice)
            print("************************************ quantity:", quantity)
            print("************************************ USD:", usd)

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
                actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
                print(actualPrice, '\t', datetime.datetime.now())

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(10.0)
