# Trading Bot — Binance Futures Testnet (USDT-M)

Simple CLI tool that places MARKET and LIMIT orders (BUY/SELL) on Binance
Futures Testnet. Built for the "simplified trading bot" assignment.

I went with `python-binance` instead of raw REST calls since it already
handles the request signing/timestamp stuff, and that let me spend more
time on the validation + logging + error handling parts, which is what's
actually being graded.

## Structure

```
trading_bot/
  bot/
    __init__.py
    client.py           # builds the Binance client (Futures Testnet)
    orders.py           # actually places the order, wraps errors
    validators.py        # checks CLI input before it ever hits the API
    logging_config.py    # one shared logger config
    cli.py               # argparse entry point, ties everything together
  logs/
    trading_bot.log       # gets created the first time you run it
  README.md
  requirements.txt
  .env.example
```

I split it this way mainly so `cli.py` doesn't get bloated - it's just
parsing args and calling the other modules, and each module has one job.

## Setup

1. Make a Binance Futures Testnet account at https://testnet.binancefuture.com
   and generate an API key + secret from the dashboard there.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and paste your testnet keys in:

   ```bash
   cp .env.example .env
   ```

   ```
   BINANCE_API_KEY=your_testnet_api_key_here
   BINANCE_API_SECRET=your_testnet_api_secret_here
   ```

   (`.env` is git-ignored, so keys never end up committed by accident.)

## How to run it

Run these from the `trading_bot/` folder.

**Market order**

```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**Limit order**

```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

Each run prints out:
- the order request (what's about to be sent)
- the order response (orderId, status, executedQty, avgPrice if there is one)
- a success or failure line at the end

Everything also gets written to `logs/trading_bot.log` - both the request
and response, plus any errors, so there's a record even if you weren't
watching the terminal.

## Assumptions I made

- Only USDT-M Futures, not Spot or Coin-M — that's what the assignment asked for.
- Only MARKET and LIMIT, since those were the core requirement (bonus order
  types weren't done, ran out of time before the deadline).
- LIMIT orders always use `timeInForce=GTC` since the assignment didn't
  specify a TIF and GTC seemed like the sensible default.
- I'm assuming quantity/price precision is valid for whatever symbol is
  passed — Binance will reject it with a proper error if it violates the
  exchange's lot size/tick size filters, and that gets caught and logged
  same as any other API error, so it's not a silent failure.
- API keys only ever come from `.env` / environment variables, never
  hardcoded, never logged.

## Error handling

- **Bad input** (wrong symbol format, invalid side/type, quantity or price
  that isn't a positive number, missing price on a LIMIT order) is caught
  in `validators.py` before any API call happens, printed as
  `[VALIDATION ERROR]`.
- **API-level errors** (invalid symbol, insufficient margin, etc.) come
  back from Binance as a `BinanceAPIException` and get printed as
  `[FAILURE]` along with Binance's own error code and message.
- **Network errors** (timeouts, DNS failure, connection refused) are
  caught separately from API errors so it's obvious from the log whether
  the order actually reached Binance or not.
- Anything else unexpected falls into a last catch-all that logs the full
  traceback instead of just crashing.

## What I'd add if I had more time

- One of the bonus order types (probably Stop-Limit, seemed the most
  useful one)
- A couple of actual unit tests for `validators.py` since that logic is
  the easiest to test without hitting the real API
