# logging_config.py
"""Logging configuration for Bulls and Cows game."""

import sys
from loguru import logger


logger.remove()

logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{message}</level>",
    level="INFO",
    colorize=True,
)

logger.add(
    "logs/game_{time:YYYY-MM-DD}.txt",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    level="INFO",
    rotation="1 game",
)
