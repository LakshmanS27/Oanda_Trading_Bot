import oandapyV20
import oandapyV20.endpoints.pricing as pricing
import logging

logging.basicConfig(level=logging.INFO)

class OandaAPIHandler:
    def __init__(self, api_key, account_id):
        self.api_key = api_key
        self.account_id = account_id
        self.client = oandapyV20.API(access_token=api_key)

    def get_ltp(self, instruments):
        """Fetches the live LTP for given instruments."""
        params = {"instruments": ",".join(instruments)}
        r = pricing.PricingInfo(accountID=self.account_id, params=params)
        response = self.client.request(r)
        ltp_data = {}
        for price in response['prices']:
            ltp_data[price['instrument']] = float(price['bids'][0]['price'])
        return ltp_data


class ORBStrategy:
    def __init__(self):
        self.candle_data = {symbol: [] for symbol in ["EUR_USD", "USD_JPY", "GBP_USD"]}

    def collect_candle_data(self, symbol, price):
        """Collects and stores candle data (simulating every 1 minute)."""
        self.candle_data[symbol].append(price)
        if len(self.candle_data[symbol]) > 15:  #First 15-minute prices
            self.candle_data[symbol] = self.candle_data[symbol][:15]

    def calculate_opening_range(self, symbol):
        """Calculates the high and low for the first 15-minute candle."""
        prices = self.candle_data[symbol]
        if len(prices) < 15:
            return None, None
        return max(prices), min(prices)

    def generate_signal(self, symbol, price):
        """Generates a buy or sell signal based on the ORB strategy."""
        high, low = self.calculate_opening_range(symbol)
        if high is None or low is None:
            return None
        if price > high:
            return "BUY"
        elif price < low:
            return "SELL"
        return None