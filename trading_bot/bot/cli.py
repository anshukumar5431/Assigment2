"""
CLI entry point.

Examples:
    python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
    python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
"""

import argparse
import sys

from dotenv import load_dotenv

from .client import get_futures_client, BotClientError
from .orders import place_order, OrderError
from .validators import validate_order_params, ValidationError
from .logging_config import setup_logger

logger = setup_logger()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading-bot",
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M).",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side")
    parser.add_argument(
        "--type", required=True, dest="order_type",
        choices=["MARKET", "LIMIT", "market", "limit"], help="Order type",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, default=None, help="Price (required for LIMIT orders)")
    return parser


def main(argv=None) -> int:
    load_dotenv()  # grabs BINANCE_API_KEY / BINANCE_API_SECRET from .env if it exists

    parser = build_parser()
    args = parser.parse_args(argv)

    # validate everything before we even think about hitting the API
    try:
        params = validate_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as exc:
        print(f"[VALIDATION ERROR] {exc}")
        logger.warning("Validation failed: %s", exc)
        return 1

    print("\n--- Order Request ---")
    for key, value in params.items():
        if value is not None:
            print(f"{key:>10}: {value}")

    try:
        client = get_futures_client()
        response = place_order(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        )
    except (BotClientError, OrderError) as exc:
        print(f"\n[FAILURE] {exc}")
        return 1

    print("\n--- Order Response ---")
    print(f"   orderId: {response.get('orderId')}")
    print(f"    status: {response.get('status')}")
    print(f"executedQty: {response.get('executedQty')}")
    if response.get("avgPrice") is not None:
        print(f"  avgPrice: {response.get('avgPrice')}")

    print("\n[SUCCESS] Order placed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
