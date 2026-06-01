from dataclasses import dataclass
from typing import Optional


class ValidationError(Exception):
    pass


@dataclass
class OrderInput:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in {"BUY", "SELL"}:
        raise ValidationError("Side must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in {"MARKET", "LIMIT"}:
        raise ValidationError("order_type must be MARKET or LIMIT.")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except ValueError:
        raise ValidationError("Quantity must be a number.")
    if q <= 0:
        raise ValidationError("Quantity must be positive.")
    return q


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            p = float(price)
        except ValueError:
            raise ValidationError("Price must be a number.")
        if p <= 0:
            raise ValidationError("Price must be positive.")
        return p
    else:
        return None


def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str],
) -> OrderInput:
    v_symbol = validate_symbol(symbol)
    v_side = validate_side(side)
    v_type = validate_order_type(order_type)
    v_qty = validate_quantity(quantity)
    v_price = validate_price(price, v_type)

    return OrderInput(
        symbol=v_symbol,
        side=v_side,
        order_type=v_type,
        quantity=v_qty,
        price=v_price,
    )