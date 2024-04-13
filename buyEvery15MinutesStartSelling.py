import config
from binance.client import Client
import datetime
import time

buy = True
symbol = "BTCFDUSD"
buyPrice = 70717.74
usd = 382
quantity = 0.00540
sumProfit = 0

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')

    while True:

        try:

            minuteNow = datetime.datetime.now().minute

            actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
            print(actualPrice, '\t', datetime.datetime.now())

            boolMinutes = minuteNow == 0 or minuteNow == 15 or minuteNow == 30 or minuteNow == 45

            # boolMinutesSELL = minuteNow == 59 or minuteNow == 14 or minuteNow == 29 or minuteNow == 44

            if buy and boolMinutes and actualPrice > buyPrice:
                buy = False
                
                params = {
                        "symbol": symbol,
                        "side": 'SELL',
                        "type": "LIMIT",
                        "timeInForce": "GTC",
                        "quantity": quantity,
                        "price": actualPrice
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
                
                print("************************************ sell price:", actualPrice)
                usdAfterSell = quantity * actualPrice
                profit = usdAfterSell - usd
                sumProfit += profit
                print("profit:", profit, "sumProfit: ", sumProfit)
            
            if not buy and boolMinutes:
                # buyPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
                buyPrice = actualPrice
                buy = True
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
                
            time.sleep(59.0)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(59.0)
            continue
