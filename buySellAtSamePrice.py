import config
from binance.client import Client

if __name__ == '__main__':

    spot_client = Client(api_key=config.APY_KEY, api_secret=config.APY_SECRET_KEY, tld='com')

    while True:

        try:


            # time.sleep(59.0)

        except Exception as e:
            print("EXCEPTION 1: ", e)
            # time.sleep(59.0)
            continue
