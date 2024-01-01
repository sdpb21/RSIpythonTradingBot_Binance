from binance.client import Client
import config
import datetime
import time

if __name__ == '__main__':
    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')
    while True:
        minute = datetime.datetime.now().minute
        print(minute)
        time.sleep(0.75)
