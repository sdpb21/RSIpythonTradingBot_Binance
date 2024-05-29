import config
from binance.client import Client
import datetime
import time

symbol = "BTCFDUSD"
price = 69000.0
sellLimit = price + 15.0
startPrice = sellLimit + 10.0
# buyLimit = price + 10.0
sell = False
buy = True      # Start selling
quantity = 0.00605

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
                        params = {
                                "symbol": symbol,
                                "side": 'SELL',
                                "type": "LIMIT",
                                "timeInForce": "GTC",
                                "quantity": quantity,
                                "price": (price + 8)
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
                        sell = True
                        buy = False
                        time.sleep(59.0)
                        print("1")
                        time.sleep(59.0)
                        print("2")
                        time.sleep(59.0)
                        print("3")
                        time.sleep(59.0)
                        print("4")
                        time.sleep(59.0)
                        print("5")
                        time.sleep(59.0)
                        print("6")
                        time.sleep(59.0)
                        print("7")
                        time.sleep(59.0)
                        print("8")
                        time.sleep(59.0)
                        print("9")
                        time.sleep(59.0)
                        print("10")
                        time.sleep(59.0)
                        print("11")
                        time.sleep(59.0)
                        print("12")
                        time.sleep(59.0)
                        print("13")
                        time.sleep(59.0)
                        print("14")
                        time.sleep(59.0)
                        print("15")

                    actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

                    if actualPrice > price and not buy:
                        # buy
                        params = {
                                "symbol": symbol,
                                "side": 'BUY',
                                "type": "LIMIT",
                                "timeInForce": "GTC",
                                "quantity": quantity,
                                "price": (sellLimit - 8)
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
                        buy = True
                        sell = False
                        print("break")
                        break
                        # time.sleep(59.0)
                    
                    time.sleep(0.5)

                except Exception as e:
                    print("EXCEPTION 1: ", e)
                    time.sleep(59.0)
                    continue
        
        time.sleep(1.0)
