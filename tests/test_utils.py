# tests/test_utils.py
"""Unit tests for utility functions."""

import pytest

from utils import (
    calculate_bulls_cows,
    generate_number,
    is_valid_number,
    parse_response
)


class TestIsValidNumber:
    """Tests for is_valid_number function."""

    def test_valid_numver(self):
        """Valid numbers should return True."""
        assert is_valid_number("1234") is True
        assert is_valid_number("5678") is True
        assert is_valid_number("9012") is True
        assert is_valid_number("1023") is True

    def test_invalid_length_short(self):
        """Numbers with less than 4 digits should be invalid."""
        assert is_valid_number("123") is False
        assert is_valid_number("6") is False
        assert is_valid_number("") is False

    def test_invalid_length_long(self):
        """Numbers with more than 4 digits should be invalid."""
        assert is_valid_number("81736401923") is False
        assert is_valid_number("123") is False

    def test_leading_zero(self):
        """Numbers starting with 0 should be invalid."""
        assert is_valid_number("0123") is False
        assert is_valid_number("0789") is False

    def test_repeating_digits(self):
        """Numbers with repeating digits should be invalid."""
        assert is_valid_number("1123") is False
        assert is_valid_number("1223") is False
        assert is_valid_number("1233") is False
        assert is_valid_number("1111") is False

    def test_non_digits(self):
        """Non-digit strings should be invalid."""
        assert is_valid_number("abcd") is False
        assert is_valid_number("12ab") is False
        assert is_valid_number("12.4") is False
        assert is_valid_number("12 4") is False


class TestCalculateBullsCows:
    """Tests for calculate_bulls_cows function."""

    def test_bulls_cows(self):
        """Exact match should return 4 bulls, 0 cows."""
        assert calculate_bulls_cows("1234", "1234") == (4, 0)
        assert calculate_bulls_cows("5678", "5678") == (4, 0)

    def test_no_match(self):
        """No matching digits should return 0 bulls, 0 cows."""
        assert calculate_bulls_cows("1234", "5678") == (0, 0)
        assert calculate_bulls_cows("1234", "9876") == (0, 0)

    def test_all_cows(self):
        """All digits present but wrong positions."""
        assert calculate_bulls_cows("1234", "4321") == (0, 4)
        assert calculate_bulls_cows("1234", "2143") == (0, 4)

    def test_mixed_bulls_cows(self):
        """Mix of bulls and cows."""
        assert calculate_bulls_cows("1234", "1243") == (2, 2)
        assert calculate_bulls_cows("1234", "1325") == (1, 2)
        assert calculate_bulls_cows("1234", "1567") == (1, 0)

    def test_one_bull(self):
        """One digit in correct position."""
        assert calculate_bulls_cows("1234", "1567") == (1, 0)
        assert calculate_bulls_cows("1234", "5234") == (3, 0)

    def test_one_cow(self):
        """One digit present but wrong position."""
        assert calculate_bulls_cows("1234", "5617") == (0, 1)

    def test_edge_case(self):
        """Edge cases with zeros."""
        assert calculate_bulls_cows("1023", "3210") == (0, 4)
        assert calculate_bulls_cows("9012", "2109") == (0, 4)


class TestGenerateNumber:
    """Tests for generate_number function."""

    def test_returns_valid_number(self):
        """Generated number should be valid."""
        for _ in range(100):
            number = generate_number()
            assert is_valid_number(number), f"Invalid umber generate: {number}"

    def test_returnstring(self):
        """Generated number should be a string."""
        number = generate_number()
        assert isinstance(number, str)

    def test_correct_length(self):
        """Generated number should have 4 digits."""
        number = generate_number()
        assert len(number) == 4

    def test_no_leading_zero(self):
        """Generated number should not start with 0."""
        for _ in range(100):
            number = generate_number()
            assert number[0] != "0"

    def test_unique_digits(self):
        """Generated number should have unique digits."""
        for _ in range(100):
            number = generate_number()
            assert len(set(number)) == 4


class TestParseResponse:
    """Tests for parse_response function."""

    def test_valid_json(self):
        """Valid JSON should be parsed correctly."""
        response = ('{"action": "guess", '
                    '"number": "1234", "bulls": 0, "cows": 0}')
        result = parse_response(response)
        assert result["action"] == "guess"
        assert result["number"] == "1234"

    def test_json_in_markdown(self):
        """JSON wrapped in markdown code blocks."""
        response = ('```json\n{"action": "guess", '
                    '"number": "5678", "bulls": 1, "cows": 2}\n```')
        result = parse_response(response)
        assert result["number"] == "5678"
        assert result["bulls"] == 1
        assert result["cows"] == 2

    def test_json_in_markdown_no_language(self):
        """JSON in markdown without language specification."""
        response = ('```\n{"action": "make", '
                    '"number": "9012", "bulls": 0, "cows": 0}\n```')
        result = parse_response(response)
        assert result["number"] == "9012"

    def test_json_with_extra_text(self):
        """JSON with surrounding text."""
        response = ('Here is my guess: {"action": "guess", '
                    '"number": "1234", "bulls": 0, "cows": 0} Good luck!')
        result = parse_response(response)
        assert result["number"] == "1234"

    def test_invalid_json_returns_default(self):
        """Invalid JSON should return default values."""
        response = "This is not JSON at all"
        result = parse_response(response)
        assert result["action"] == "error"
        assert result["number"] == "0000"

    def test_empty_response(self):
        """Empty response should return default values."""
        result = parse_response("")
        assert result["action"] == "error"

    def test_whitespace_handling(self):
        """JSON with extra whitespace."""
        response = ('  \n  {"action": "guess", '
                    '"number": "1234", "bulls": 0, "cows": 0}  \n  ')
        result = parse_response(response)
        assert result["number"] == "1234"
