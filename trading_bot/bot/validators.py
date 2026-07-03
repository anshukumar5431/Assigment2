"""
Validation for whatever the user types in on the CLI.

I kept this separate from cli.py on purpose - didn't want argparse mixed
up with the actual "is this a real order" logic. Makes it easier to test
too (I ran a few of these manually in a python shell while building it).
"""

import re

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}

# Binance symbols are stuff like BTCUSDT, ETHUSDT etc - all caps, no
# spaces/symbols. 5-15 chars covers pretty much every USDT-M pair.
SYMBOL_RE = re.compile(r"^[A-Z0-9]{5,15}$")


class ValidationError(Exception):
    """Custom exception so the CLI can catch just validation problems
    and not accidentally swallow real bugs."""


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not SYMBOL_RE.match(symbol):
        raise ValidationError(
            f"'{symbol}' doesn't look like a valid symbol. Expected something like 'BTCUSDT'."
        )
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Side must be BUY or SELL, got '{side}'.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Order type must be MARKET or LIMIT, got '{order_type}'.")
    return order_type


def validate_quantity(quantity) -> float:
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity has to be a number, got '{quantity}'.")
    if quantity <= 0:
        raise ValidationError(f"Quantity has to be greater than 0, got {quantity}.")
    return quantity


def validate_price(price, order_type: str):
    """Only LIMIT orders need a price. For MARKET we just ignore whatever
    was passed (even if the user typed something by mistake)."""
    if order_type != "LIMIT":
        return None

    if price is None:
        raise ValidationError("Price is required for LIMIT orders.")
    try:
        price = float(price)
    except (TypeError, ValueError):
        raise ValidationError(f"Price has to be a number, got '{price}'.")
    if price <= 0:
        raise ValidationError(f"Price has to be greater than 0, got {price}.")
    return price


def validate_order_params(symbol, side, order_type, quantity, price=None):
    """Runs everything above and hands back a clean dict, or raises on
    the first thing that's wrong."""
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_type = validate_order_type(order_type)
    clean_qty = validate_quantity(quantity)
    clean_price = validate_price(price, clean_type)

    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "order_type": clean_type,
        "quantity": clean_qty,
        "price": clean_price,
    }
