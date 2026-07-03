"""
Small wrapper that builds the python-binance Client for Futures Testnet.

Keeping this in its own file so orders.py / cli.py never have to touch
API keys directly - they just call get_futures_client() and get back a
ready-to-use client.
"""

import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from .logging_config import setup_logger

logger = setup_logger()

FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"


class BotClientError(Exception):
    """Raised when the Binance client can't be created."""


def get_futures_client() -> Client:
    """Builds a python-binance Client pointed at Futures Testnet.

    Reads BINANCE_API_KEY / BINANCE_API_SECRET from the environment
    (cli.py loads these from a .env file before calling this).
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Missing BINANCE_API_KEY / BINANCE_API_SECRET environment variables.")
        raise BotClientError(
            "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET "
            "(e.g. in a .env file) before running the bot."
        )

    try:
        # Passing testnet=True is actually enough on its own - python-binance
        # already routes futures_create_order() etc. to
        # https://testnet.binancefuture.com internally once this flag is set.
        # (I initially tried manually overwriting client.FUTURES_URL here too,
        # thinking it was needed, but that was pointless - checked the
        # library source and testnet routing is handled separately from
        # that attribute. Leaving this note so I remember why it's gone.)
        client = Client(api_key, api_secret, testnet=True)
        logger.debug("Binance Futures Testnet client initialized (base_url=%s).", FUTURES_TESTNET_URL)
        return client
    except (BinanceAPIException, BinanceRequestException) as exc:
        logger.error("Failed to initialize Binance client: %s", exc)
        raise BotClientError(f"Could not initialize Binance client: {exc}") from exc
