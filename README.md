# Real-Time Binance Crypto Dashboard

This is a Python desktop application that demonstrates real-time cryptocurrency monitoring using the Binance API. The dashboard displays live prices, candlestick charts, order books, and recent trades for Bitcoin, Ethereum, Solana, Binance Coin, and Ripple.

---

## Features

The dashboard supports the following operations:

* **Live Price Tracking:** Display real-time prices for 5 cryptocurrencies with 24-hour change percentages
* **Candlestick Charts:** Visualize price movements with historical data and volume bars
* **Order Book Display:** View top 10 bids and asks in real-time via popup window
* **Recent Trades Feed:** Monitor the last 5 trades as they happen
* **Preferences:** Automatically save and restore your selected cryptocurrency which you chose before you closed.
* **Full Chart Popup:** Open a larger view of the candlestick chart for detailed analysis
***Toggle Switches:** Modern sliding switches to control chart and order book popups

---

## Files

* **`main.py`**: Contains the main application entry point and `FinalIntegratedDashboard` class
* **`config.py`**: Configuration file with cryptocurrency symbols, API endpoints, and color themes
* **`toggle_switch.py`**: Custom toggle switch widget for modern UI controls
* **`requirements.txt`**: List of required Python packages

### Utils Directory (`utils/`)
* **`__init__.py`**: Package initialization and exports
* **`binance_api.py`**: API call wrapper with retry logic and error handling
* **`preferences.py`**: Functions to save and load user preferences (`save_preferences`, `load_preferences`)

### Components Directory (`components/`)
* **`__init__.py`**: Component exports
* **`ticker.py`**: `PriceTickerCard` class for displaying live cryptocurrency prices
* **`chart.py`**: `CandlestickChart` and `ChartPopup` classes for chart visualization
* **`orderbook.py`**: `OrderBookPanel` and `OrderBookPopup` classes for order book display
* **`trades.py`**: `RecentTradesPanel` class for showing live trades
* **`spread.py`**: `BidAskSpreadPanel` class for bid/ask spread analysis
---

## Additional Notes

- This application uses Binance's **public API** (no account or API key required)
- All data is **read-only** (cannot place trades)
- Your preferences are saved in `dashboard_preferences.json` when you close the app

---

```
crypto_dashboard/
│
├── main.py                      # Main application
├── config.py                    # Configuration
├── toggle_switch.py             # Toggle switch widget
├── requirements.txt             # Dependencies
├── dashboard_preferences.json   # Saved preferences (auto-created after the first run)
│
├── utils/                       # Helper functions
│   ├── __init__.py
│   ├── binance_api.py          # API wrapper
│   └── preferences.py          # Save/load preferences
│
└── components/                  # UI Components
    ├── __init__.py
    ├── ticker.py               # Price tickers
    ├── chart.py                # Charts
    ├── orderbook.py            # Order book
    ├── trades.py               # Trades feed
    └── spread.py               # Spread panel
```


---
## Requirements

* Python 3.7 or higher
* Internet connection (for Binance API access)
* Pip in 'requirment.txt'


