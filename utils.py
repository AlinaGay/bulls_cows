# utils.py
"""Utility functions for Bulls and Cows game."""

import json
import random
import re

from config import DIGITS_OF_NUMBER
from loguru import logger


def is_valid_number(number: str) -> bool:
    """Validate that the number is correct."""
    if len(number) != DIGITS_OF_NUMBER:
        logger.debug(f"Неверная длина: {number}")
        return False
    if not number.isdigit():
        logger.debug(f"Не цифры: {number}")
        return False
    if number[0] == '0':
        logger.debug(f"Начинается с 0: {number}")
        return False
    if len(set(number)) != DIGITS_OF_NUMBER:
        logger.debug(f"Повторяющиеся цифры: {number}")
        return False
    return True


def generate_number() -> str:
    """Generate four digit number with unique digits."""
    while True:
        number_list = random.sample(range(10), 4)
        if number_list[0] != 0:
            number = ''.join(map(str, number_list))
            logger.debug(f"Сгенерировано число: {number}")
            return number


def calculate_bulls_cows(secret: str, guess: str) -> tuple[int, int]:
    """Calculate the number of bulls and cows in guess number."""
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(g in secret for g in guess) - bulls
    logger.debug(f"Расчёт: {secret} vs {guess} → {bulls}Б {cows}К")
    return bulls, cows


def parse_response(response_text: str) -> dict:
    """Parse JSON-answer of agent."""
    text = response_text.strip()
    logger.debug(f"Парсинг ответа: {text[:100]}...")

    if "```" in text:
        match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            text = match.group(1)
            logger.debug("Извлечён JSON из markdown")

    match = re.search(r'\{[^{}]*\}', text)
    if match:
        text = match.group(0)

    try:
        result = json.loads(text)
        logger.debug(f"Парсинг JSON успешно завершен: {result}")
        return result
    except json.JSONDecodeError as error:
        logger.error(f"Ошибка парсинга JSON: {error}")
        logger.error(f"Ответ агента: {response_text}")
        return {
            "action": "error",
            "number": "0000",
            "bulls": 0,
            "cows": 0
        }
