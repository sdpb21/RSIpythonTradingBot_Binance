import config
from binance.client import Client
import datetime
import time

symbol = "BTCFDUSD"
price = 70220.0
sellLimit = price - 10.0
buyLimit = price + 10.0
sell = False
buy = True      # Start selling
quantity = 0.005

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')

    while True:

        try:

            actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

            print(actualPrice, '\t', datetime.datetime.now())

            if (actualPrice < price) and actualPrice >= sellLimit and not sell:
                # sell
                print("************************************ sell price:", actualPrice)
                sell = True
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

            actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

            if actualPrice >= price and actualPrice <= buyLimit and not buy:
                # buy
                print("************************************ buy price:", actualPrice)
                buy = True
                sell = False
            
            time.sleep(2.0)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(59.0)
            continue
