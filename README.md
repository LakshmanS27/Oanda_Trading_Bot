# OANDA Opening Range Breakout (ORB) Trading Bot

This project implements an automated trading bot using the **Opening Range Breakout (ORB) Strategy** on the OANDA trading platform. The bot fetches live prices, determines breakout signals, and places market orders accordingly.

---

## 📌 Features
- **Live Market Data Fetching**: Retrieves live Last Traded Prices (LTP) using OANDA API.
- **Opening Range Calculation**: Determines the high and low from the first 15-minute candle.
- **ORB Signal Generation**: Identifies breakout conditions and generates BUY/SELL signals.
- **Automated Order Placement**: Places market orders based on generated signals.
- **Multithreading Support**: Handles orders concurrently for multiple instruments.
- **Logging System**: Maintains order logs in `order_log.txt` for tracking.

---

## 📂 Project Structure

```
📁 OANDA_ORB_Bot/
├── config.py               # Stores API credentials
├── oanda_orb.py            # Handles data retrieval & ORB strategy
├── oanda_manager.py        # Manages order execution and logging
├── order_log.txt           # Logs order transactions
├── README.md               # Project documentation
```

---

## 🚀 Installation & Setup

### 1️⃣ Prerequisites
- Python 3.x
- OANDA Practice Account ([Sign up here](https://www.oanda.com))
- API Key & Account ID from OANDA

### 2️⃣ Install Dependencies
```bash
pip install oandapyV20
```

### 3️⃣ Configure API Credentials
Edit `config.py` and add your OANDA credentials:
```python
API_KEY = "your_oanda_api_key"
ACCOUNT_ID = "your_oanda_account_id"
```

### 4️⃣ Run the Bot
```bash
python oanda_manager.py
```

---

## ⚙️ How It Works
1. The bot collects price data for the first 15 minutes.
2. It determines the highest and lowest price within this period.
3. If the price breaks above the high → **BUY Signal**.
4. If the price breaks below the low → **SELL Signal**.
5. Orders are placed automatically using OANDA's API.
6. Logs are stored in `order_log.txt`.

---

## 🛠️ Code Overview
### `oanda_orb.py`
- `OandaAPIHandler`: Fetches real-time price data.
- `ORBStrategy`: Implements the Opening Range Breakout logic.

### `oanda_manager.py`
- `OrderManager`: Places orders based on breakout signals.
- Uses **multithreading** to handle multiple orders simultaneously.
- Implements **thread-safe logging** to track order execution.

---

## 📜 Example Output
```bash
Collecting data for the first 15 minutes...
Placing orders based on ORB signals...
[SUCCESS] Order placed for EUR_USD: BUY. Response: {...}
[SUCCESS] Order placed for USD_JPY: SELL. Response: {...}
All orders processed. Check order_log.txt for details.
```

---

## 📝 Notes
- This bot is for educational purposes and should be tested on **demo accounts** before live trading.
- Modify the order size in `oanda_manager.py` before real trading.

---

## 🏗️ Future Improvements
- Add **stop-loss and take-profit** mechanisms.
- Implement **trailing stop orders**.
- Support **multiple timeframes** for strategy customization.

---

## 📧 Contact
For questions or improvements, feel free to contribute or reach out!
