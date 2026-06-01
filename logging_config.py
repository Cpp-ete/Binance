import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name: str, filename: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    log_file = LOG_DIR / filename
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger