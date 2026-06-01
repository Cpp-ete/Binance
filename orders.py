from typing import Any, Dict

from .client import BinanceFuturesClient
from .validators import OrderInput
from .logging_config import setup_logger

logger = setup_logger("orders", "orders.log")


class OrderService:
    def __init__(self, client: BinanceFuturesClient) -> None:
        self.client = client

    def place_order(self, order_input: OrderInput) -> Dict[str, Any]:
        logger.info("Received order_input: %s", order_input)

        if order_input.order_type == "MARKET":
            response = self.client.place_market_order(
                symbol=order_input.symbol,
                side=order_input.side,
                quantity=order_input.quantity,
            )
        elif order_input.order_type == "LIMIT":
            if order_input.price is None:
                raise ValueError("Price must be provided for LIMIT orders.")
            response = self.client.place_limit_order(
                symbol=order_input.symbol,
                side=order_input.side,
                quantity=order_input.quantity,
                price=order_input.price,
            )
        else:
            raise ValueError(f"Unsupported order type: {order_input.order_type}")

        logger.info("Order placed successfully. Response: %s", response)
        return response

    @staticmethod
    def format_order_summary(order_input: OrderInput) -> str:
        base = (
            f"Order Request:\n"
            f"  Symbol: {order_input.symbol}\n"
            f"  Side: {order_input.side}\n"
            f"  Type: {order_input.order_type}\n"
            f"  Quantity: {order_input.quantity}\n"
        )
        if order_input.order_type == "LIMIT":
            base += f"  Price: {order_input.price}\n"
        return base

    @staticmethod
    def format_order_response(response: Dict[str, Any]) -> str:
        # Futures response fields: orderId, status, executedQty, avgPrice, etc.
        order_id = response.get("orderId")
        status = response.get("status")
        executed_qty = response.get("executedQty")
        avg_price = response.get("avgPrice")

        lines = [
            "Order Response:",
            f"  orderId: {order_id}",
            f"  status: {status}",
            f"  executedQty: {executed_qty}",
            f"  avgPrice: {avg_price}",
        ]
        return "\n".join(lines)