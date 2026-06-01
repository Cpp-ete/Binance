import os
from typing import Any, Dict, Optional

from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL
from dotenv import load_dotenv

from .logging_config import setup_logger

logger = setup_logger("binance_client", "binance_client.log")

load_dotenv()


class BinanceFuturesClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = base_url or os.getenv(
            "BINANCE_FUTURES_TESTNET_URL",
            "https://testnet.binancefuture.com",
        )

        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret must be set (env or arguments).")

        logger.info("Initializing Binance Futures client with base_url=%s", self.base_url)

        # Note: python-binance testnet uses `futures_testnet=True`, but they gave a custom base URL.
        # We'll respect their URL by setting `tld` and `futures_testnet=True`.
        self.client = Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=True,
        )
        # Override base futures URL to match the assignment requirement
        self.client.FUTURES_URL = self.base_url + "/fapi"

    def _translate_side(self, side: str) -> str:
        side_upper = side.upper()
        if side_upper == "BUY":
            return SIDE_BUY
        elif side_upper == "SELL":
            return SIDE_SELL
        raise ValueError("side must be BUY or SELL")

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
    ) -> Dict[str, Any]:
        order_side = self._translate_side(side)
        logger.info(
            "Placing MARKET order: symbol=%s side=%s qty=%s",
            symbol,
            order_side,
            quantity,
        )
        response = self.client.futures_create_order(
            symbol=symbol,
            side=order_side,
            type="MARKET",
            quantity=quantity,
        )
        logger.info("MARKET order response: %s", response)
        return response

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        order_side = self._translate_side(side)
        logger.info(
            "Placing LIMIT order: symbol=%s side=%s qty=%s price=%s tif=%s",
            symbol,
            order_side,
            quantity,
            price,
            time_in_force,
        )
        response = self.client.futures_create_order(
            symbol=symbol,
            side=order_side,
            type="LIMIT",
            timeInForce=time_in_force,
            quantity=quantity,
            price=str(price),
        )
        logger.info("LIMIT order response: %s", response)
        return response