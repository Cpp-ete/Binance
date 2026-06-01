import sys
import traceback

import click
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.validators import ValidationError, validate_order_input
from bot.logging_config import setup_logger

logger = setup_logger("cli", "cli.log")


@click.command()
@click.option("--symbol", required=True, help="Trading pair symbol, e.g., BTCUSDT.")
@click.option("--side", required=True, type=click.Choice(["BUY", "SELL"], case_sensitive=False))
@click.option(
    "--order-type",
    "order_type",
    required=True,
    type=click.Choice(["MARKET", "LIMIT"], case_sensitive=False),
)
@click.option("--quantity", required=True, help="Order quantity.")
@click.option(
    "--price",
    required=False,
    help="Price (required for LIMIT orders).",
)
def main(symbol: str, side: str, order_type: str, quantity: str, price: str | None) -> None:
    """
    Simple Binance USDT-M Futures testnet trading bot.
    """
    try:
        order_input = validate_order_input(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
    except ValidationError as e:
        click.echo(f"Input validation error: {e}")
        logger.error("Validation error: %s", e)
        sys.exit(1)

    client = None
    try:
        client = BinanceFuturesClient()
    except Exception as e:
        click.echo(f"Failed to initialize Binance client: {e}")
        logger.error("Client initialization error: %s", e)
        sys.exit(1)

    service = OrderService(client)

    click.echo(service.format_order_summary(order_input))

    try:
        response = service.place_order(order_input)
        click.echo(service.format_order_response(response))
        click.echo("Order placement SUCCESS.")
    except BinanceAPIException as e:
        click.echo(f"Binance API error: {e.message}")
        logger.error("Binance API error: %s", e, exc_info=True)
        sys.exit(1)
    except BinanceRequestException as e:
        click.echo("Network error while making request to Binance.")
        logger.error("Binance request error: %s", e, exc_info=True)
        sys.exit(1)
    except Exception as e:
        click.echo("Unexpected error occurred. See logs for details.")
        logger.error("Unexpected error: %s", e)
        logger.error("Traceback: %s", traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()