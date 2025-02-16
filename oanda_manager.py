import oandapyV20
import oandapyV20.endpoints.orders as orders
import threading
import time
import logging
import os
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from config import API_KEY, ACCOUNT_ID
from oanda_orb import OandaAPIHandler, ORBStrategy

#order_log.txt file check
if not os.path.exists("order_log.txt"):
    with open("order_log.txt", "w") as f:
        f.write("")

# Set up thread-safe logging with QueueHandler and QueueListener
log_queue = Queue()
queue_handler = QueueHandler(log_queue)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("order_log.txt")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(queue_handler)

listener = QueueListener(log_queue, file_handler, console_handler)
listener.start()


class OrderManager:
    def __init__(self, api_key, account_id):
        self.api_key = api_key
        self.account_id = account_id
        self.client = oandapyV20.API(access_token=api_key)

    def place_order(self, symbol, signal):
        """Places a market order based on the signal (BUY or SELL)."""
        units = "100" if signal == "BUY" else "-100"
        order_data = {
            "order": {
                "instrument": symbol,
                "units": units,
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        try:
            r = orders.OrderCreate(accountID=self.account_id, data=order_data)
            response = self.client.request(r)
            logging.info(f"Order placed for {symbol}: {signal}. Response: {response}")
            print(f"[SUCCESS] Order placed for {symbol}: {signal}. Response: {response}")
        except Exception as e:
            logging.error(f"Failed to place order for {symbol}: {e}")
            print(f"[ERROR] Failed to place order for {symbol}: {e}")


def order_thread(symbol, signal, order_manager):
    """Thread target function to place orders."""
    try:
        order_manager.place_order(symbol, signal)
    except Exception as e:
        logging.error(f"Error in order_thread for {symbol}: {e}")


if __name__ == "__main__":
    api_handler = OandaAPIHandler(API_KEY, ACCOUNT_ID)
    orb = ORBStrategy()
    order_manager = OrderManager(API_KEY, ACCOUNT_ID)
    symbols = ["EUR_USD", "USD_JPY", "GBP_USD"]

    try:
        print("Collecting data for the first 15 minutes...")
        for _ in range(15):
            ltp = api_handler.get_ltp(symbols)
            for symbol in symbols:
                orb.collect_candle_data(symbol, ltp[symbol])
                logging.info(f"Collected candle data for {symbol}: {ltp[symbol]}")
            time.sleep(1) #1-minute interval

        print("Placing orders based on ORB signals...")
        threads = []
        for symbol in symbols:
            current_price = api_handler.get_ltp([symbol])[symbol]
            signal = orb.generate_signal(symbol, current_price)
            if signal:
                t = threading.Thread(target=order_thread, args=(symbol, signal, order_manager))
                threads.append(t)
                t.start()
                logging.info(f"Started thread for {symbol} with signal {signal}")

        for t in threads:
            t.join()

        print("All orders processed. Check order_log.txt for details.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"[ERROR] An unexpected error occurred: {e}")
    finally:
        listener.stop()
