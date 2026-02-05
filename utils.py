# utils.py
import json
import random

from constants import DIGITS_OF_NUMBER


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
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text)
