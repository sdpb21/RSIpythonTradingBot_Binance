import config
from binance.client import Client
import datetime
import time

symbol = "BTCFDUSD"
price = 69225
sell = False
buy = True      # Start selling

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')

    while True:

        try:

            actualPrice = float(spot_client.get_symbol_ticker(symbol=symbol).get('price'))

            print(actualPrice, '\t', datetime.datetime.now())

            if (actualPrice < price) and not sell:
                # sell
                print("************************************ sell price:", actualPrice)
                sell = True
                buy = False

            if actualPrice >= price and not buy:
                # buy
                print("************************************ buy price:", actualPrice)
                buy = True
                sell = False

            time.sleep(2.0)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            time.sleep(59.0)
            continue
