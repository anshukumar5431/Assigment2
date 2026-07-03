# Trading Bot — Binance Futures Testnet (USDT-M)

A simple Python CLI trading bot that places **MARKET** and **LIMIT** orders on **Binance Futures Testnet (USDT-M)**.
This project is built with a modular structure and focuses on **input validation, error handling, logging, and clean CLI-based order execution**.

---

## Features

* Place **MARKET** and **LIMIT** orders from the terminal
* Supports **BUY** and **SELL** order sides
* Uses **Binance Futures Testnet** for safe testing
* Validates order parameters before hitting the API
* Logs order requests, responses, and errors to a log file
* Loads API credentials securely from a `.env` file
* Clean modular code structure for maintainability

---

## Project Structure

```bash
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── client.py           # Binance Futures Testnet client setup
│   ├── orders.py           # Order placement logic
│   ├── validators.py       # Input validation
│   └── logging_config.py   # Logging setup
│
├── logs/
│   └── .gitkeep
│
├── .env.example            # Example environment variables
├── .gitignore
├── requirements.txt        # Project dependencies
└── README.md
```

---

## Tech Stack

* **Python**
* **python-binance**
* **python-dotenv**
* **requests**

---

## Requirements

* Python **3.9+** recommended
* A **Binance Futures Testnet** account
* Binance **Testnet API Key** and **Secret Key**

---

## Setup Instructions

### 1) Clone or download the project

If you already have the project folder, move into it:

```bash
cd trading_bot
```

---

### 2) Create and activate a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4) Create your `.env` file

Copy the example file:

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

#### CMD

```cmd
copy .env.example .env
```

#### Mac/Linux

```bash
cp .env.example .env
```

Then open `.env` and add your Binance Futures Testnet credentials:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

---

## Binance Testnet Setup

1. Go to **Binance Futures Testnet**
2. Create/login to your testnet account
3. Generate an **API Key** and **Secret Key**
4. Paste them into your `.env` file

> Important: This bot is configured for **Binance Futures Testnet**, not live trading.

---

## How to Run the Bot

Run commands from the root project folder:

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

---

## Example Commands

### 1) Place a MARKET BUY order

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2) Place a MARKET SELL order

```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type MARKET --quantity 0.01
```

### 3) Place a LIMIT BUY order

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000
```

### 4) Place a LIMIT SELL order

```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

---

## CLI Arguments

| Argument     |       Required | Description                     | Example   |
| ------------ | -------------: | ------------------------------- | --------- |
| `--symbol`   |            Yes | Trading pair symbol             | `BTCUSDT` |
| `--side`     |            Yes | Order side: `BUY` or `SELL`     | `BUY`     |
| `--type`     |            Yes | Order type: `MARKET` or `LIMIT` | `MARKET`  |
| `--quantity` |            Yes | Quantity to trade               | `0.01`    |
| `--price`    | Only for LIMIT | Price for LIMIT orders          | `60000`   |

---

## Example Output

### Order Request

```bash
--- Order Request ---
    symbol: BTCUSDT
      side: BUY
order_type: MARKET
  quantity: 0.01
```

### Order Response

```bash
--- Order Response ---
   orderId: 123456789
    status: NEW
executedQty: 0.01
  avgPrice: 0.0
```

### Success Message

```bash
[SUCCESS] Order placed successfully.
```

---

## Logging

All order activity and errors are logged automatically.

### Log file location

```bash
logs/trading_bot.log
```

### What gets logged

* Order request details
* Binance API responses
* Validation errors
* API errors
* Network-related failures
* Unexpected exceptions

This makes it easier to debug issues and keep a history of trading actions during testing.

---

## Validation Rules

Before sending any request to Binance, the bot validates the input:

* **Symbol** must look like a valid trading pair (example: `BTCUSDT`)
* **Side** must be either `BUY` or `SELL`
* **Order type** must be `MARKET` or `LIMIT`
* **Quantity** must be a positive number
* **Price** is required for LIMIT orders and must be positive

---

## Error Handling

The bot handles three main types of errors:

### 1) Validation Errors

These happen when the input is invalid before any API call is made.

Example:

```bash
[VALIDATION ERROR] Price is required for LIMIT orders.
```

---

### 2) Binance API Errors

These happen when Binance rejects the order.

Possible reasons:

* Invalid symbol
* Insufficient margin
* Quantity below minimum lot size
* Invalid price precision

Example:

```bash
[FAILURE] Binance API error: Invalid symbol. (code=-1121)
```

---

### 3) Network / Request Errors

These happen when the request cannot reach Binance.

Possible reasons:

* No internet connection
* DNS issues
* Timeout
* Connection refused

Example:

```bash
[FAILURE] Network error while contacting Binance: ...
```

---

## Internal Working Flow

The bot follows this flow:

1. **Load environment variables** from `.env`
2. **Parse CLI arguments**
3. **Validate inputs** using `validators.py`
4. **Create Binance Futures Testnet client**
5. **Build order request**
6. **Send order to Binance**
7. **Print response**
8. **Log everything** to the log file

---

## Module Overview

### `cli.py`

Handles command-line input and connects the full workflow together.

### `client.py`

Creates and returns a Binance client configured for **Futures Testnet**.

### `validators.py`

Checks user inputs such as symbol, side, quantity, price, and order type before placing the order.

### `orders.py`

Contains the logic to place **MARKET** and **LIMIT** orders through Binance Futures API.

### `logging_config.py`

Creates a shared logger configuration for console output and file logging.

---

## Dependencies

From `requirements.txt`:

```txt
python-binance>=1.0.19
python-dotenv>=1.0.0
requests>=2.31.0
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## Limitations

Current version supports:

* **USDT-M Futures Testnet only**
* **MARKET** and **LIMIT** orders only
* **CLI-based execution only**

Not included in this version:

* Stop-Loss / Take-Profit orders
* OCO / advanced order types
* Web dashboard / GUI
* Real-time market data monitoring
* Strategy automation
* Unit tests

---

## Future Improvements

Possible next upgrades for the project:

* Add **Stop-Limit**, **Stop-Market**, or **Take-Profit** orders
* Add **unit tests** for validators and order flow
* Add **symbol precision / lot size checks** before placing orders
* Add **account balance / open positions display**
* Add **strategy-based auto trading**
* Add a **Streamlit or Flask dashboard**
* Add **trade history export**

---

## Security Notes

* API keys are loaded from a `.env` file
* `.env` should never be committed to GitHub
* This project is intended for **Testnet usage**
* Do **not** use production keys unless you intentionally modify the bot for live trading

---

## Sample `.env` File

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

---

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env and add keys
copy .env.example .env

# 5. Run a sample market order
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

---

## Conclusion

This project is a **minimal Binance Futures Testnet trading bot** built with a strong focus on **clean structure, validation, error handling, and logging**. It is a good foundation for extending into a more advanced automated trading system in the future.

If you want, I can also turn this into a **better GitHub-level README** with:

* badges
* project screenshot section
* “how it works” architecture diagram section
* cleaner professional formatting for internship/project submission

and make it look much stronger than a normal student README.
