# logger.py
"""Logging configuration for Bulls and Cows game."""

import sys
from loguru import logger


logger.remove()

logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
           "<velev>{message}</level>",
    level="INFO",
    colorize=True,
)

logger.add(
    "logs/game_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH-mm-ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="DEBAG",
    rotation="1 day",
    retention="7 days",
    compression="zip",
)
