import config
from binance.client import Client
import datetime
import time

buy = False
symbol = "SXTUSDT"
buyPrice = 0
usd = 1289
quantity = 0
minutes = 0
hours = 0
buyMinute = 0
sellMinute = 15
startHour = 10
boolBuy = False
boolSell = False

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')

    while True:

        try:

            minutes = datetime.datetime.now().minute
            hours = datetime.datetime.now().hour

            if hours == startHour or buy:
                actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))
                print(actualPrice, '\t', datetime.datetime.now())
            else:
                print(datetime.datetime.now())

            boolBuy = minutes == buyMinute and hours == startHour
            boolSell = minutes == sellMinute and hours == startHour

            if not buy and boolBuy:

                buyPrice = actualPrice
                quantity = round(usd / buyPrice, 0)
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

                buy = True

            if buy and boolSell and actualPrice > buyPrice:

                sellPrice = actualPrice

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
                break

            time.sleep(59.0)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(59.0)
            continue
