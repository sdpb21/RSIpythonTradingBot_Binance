import config
from binance.client import Client
import datetime
import time

symbol = "BTCFDUSD"
price = 68300.0
sellLimit = price + 10.0
startPrice = sellLimit + 40.0
# buyLimit = price + 10.0
sell = False
buy = True      # Start selling
quantity = 0.00554

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')

    while True:

        actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

        print(actualPrice, '\t', datetime.datetime.now())

        if actualPrice > startPrice:

            print("start buy and sell")

            while True:

                try:

                    actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

                    print(actualPrice, '\t', datetime.datetime.now())

                    if (actualPrice < sellLimit) and not sell:
                        # sell
                        sell = True
                        buy = False
                        params = {
                                "symbol": symbol,
                                "side": 'SELL',
                                "type": "LIMIT",
                                "timeInForce": "GTC",
                                "quantity": quantity,
                                "price": (price + 6)
                            }
                        orderID = spot_client.create_order(**params).get('orderId')
                        print("orderId:", orderID)
                        
                        orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                        print(orderStatus)
                        while orderStatus != "FILLED":
                            print("waitin' to get FILLED")
                            time.sleep(59.0)
                            orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                            print(orderStatus)
                        print("************************************ sell price:", actualPrice)
                        time.sleep(59.0)

                    actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

                    if actualPrice > price and not buy:
                        # buy
                        buy = True
                        sell = False
                        params = {
                                "symbol": symbol,
                                "side": 'BUY',
                                "type": "LIMIT",
                                "timeInForce": "GTC",
                                "quantity": quantity,
                                "price": (sellLimit - 6)
                            }
                        orderID = spot_client.create_order(**params).get('orderId')
                        print("orderId:", orderID)
                        
                        orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                        print(orderStatus)
                        while orderStatus != "FILLED":
                            print("waitin' to get FILLED")
                            time.sleep(59.0)
                            orderStatus = spot_client.get_order(symbol=symbol, orderId=orderID).get('status')
                            print(orderStatus)
                        print("************************************ buy price:", actualPrice)
                        print("break")
                        break
                        # time.sleep(59.0)
                    
                    time.sleep(2.0)

                except Exception as e:
                    print("EXCEPTION 1: ", e)
                    time.sleep(59.0)
                    continue
        
        time.sleep(59.0)
