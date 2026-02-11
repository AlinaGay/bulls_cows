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