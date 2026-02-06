# utils.py
"""Utility functions for Bulls and Cows game."""

import json
import random
import re

from config import DIGITS_OF_NUMBER


def is_valid_number(number: str) -> bool:
    """Validate that the number is correct."""
    if len(number) != DIGITS_OF_NUMBER:
        return False
    if not number.isdigit():
        return False
    if number[0] == '0':
        return False
    if len(set(number)) != DIGITS_OF_NUMBER:
        return False
    return True


def generate_number() -> str:
    """Generate four digit number with unique digits."""
    while True:
        number_list = random.sample(range(10), 4)
        if number_list[0] != 0:
            return ''.join(map(str, number_list))


def calculate_bulls_cows(secret: str, guess: str) -> tuple[int, int]:
    """Calculate the number of bulls and cows in guess number."""
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(g in secret for g in guess) - bulls
    return bulls, cows


def parse_response(response_text: str) -> dict:
    """Parse JSON-answer of agent."""
    text = response_text.strip()
    if "```" in text:
        match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            text = match.group(1)

    match = re.search(r'\{[^{}]*\}', text)
    if match:
        text = match.group(0)

    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        print(f"Ошибка парсинга JSON: {error}")
        print(f"   Ответ агента: {response_text[:100]}...")
        return {
            "action": "error",
            "number": "0000",
            "bulls": 0,
            "cows": 0
        }
