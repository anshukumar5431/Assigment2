"""
Actual order placement. Takes an already-built client + already-validated
params and calls the Binance Futures API, then normalizes whatever goes
wrong into one OrderError so the CLI layer only has to catch one thing.
"""

from binance.exceptions import BinanceAPIException, BinanceRequestException
from requests.exceptions import RequestException

from .logging_config import setup_logger

logger = setup_logger()


class OrderError(Exception):
    """Raised when placing an order fails for any reason (API, network, etc)."""


def place_order(client, symbol: str, side: str, order_type: str, quantity: float, price=None) -> dict:
    """Places a MARKET or LIMIT order on Futures Testnet and returns the
    response dict Binance sends back (orderId, status, etc.)."""

    request_summary = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }
    if order_type == "LIMIT":
        request_summary["price"] = price
        request_summary["timeInForce"] = "GTC"  # assignment didn't say which TIF to use, GTC felt like the safe default

    logger.info("Order request: %s", request_summary)

    try:
        if order_type == "MARKET":
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity,
            )
        elif order_type == "LIMIT":
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC",
            )
        else:
            # shouldn't really happen since validators.py already checks this,
            # but keeping it here too in case place_order ever gets called
            # from somewhere else without going through validation first
            raise OrderError(f"Unsupported order type: {order_type}")

        logger.info("Order response: %s", response)
        return response

    except BinanceAPIException as exc:
        # Binance itself rejected the order - bad symbol, insufficient
        # margin, quantity below lot size, stuff like that
        logger.error("Binance API error placing order: %s", exc)
        raise OrderError(f"Binance API error: {exc.message} (code={exc.code})") from exc

    except (BinanceRequestException, RequestException) as exc:
        # this is more of a "couldn't even reach Binance" case - timeout,
        # DNS issue, connection refused
        logger.error("Network error placing order: %s", exc)
        raise OrderError(f"Network error while contacting Binance: {exc}") from exc

    except Exception as exc:
        # catch-all so a weird/unexpected error doesn't crash the whole
        # CLI with a raw traceback - still gets logged with full details
        logger.exception("Unexpected error placing order.")
        raise OrderError(f"Unexpected error: {exc}") from exc
