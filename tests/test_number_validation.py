# tests/test_number_validation.py

class TestNumberValidation:
    """Validation of four-digit number."""

    def test_valid_number_1234(self):
        """Should accept a standard four-digit number with unique digits."""
        assert is_valid_number("1234") == True

    def test_valid_number_with_zero_inside(self):
        """Should accept a number containing zero in non-leading position."""
        assert is_valid_number("1023") == True

    def test_valid_number_9876(self):
        """Should accept a valid number with high digits."""
        assert is_valid_number("9876") == True

    def test_invalid_too_short(self):
        """Should reject a number with fewer than four digits."""
        assert is_valid_number("123") == False

    def test_invalid_too_long(self):
        """Should reject a number with more than four digits."""
        assert is_valid_number("12345") == False

    def test_invalid_empty(self):
        """Should reject an empty string."""
        assert is_valid_number("") == False

    def test_invalid_repeating_digits(self):
        """Should reject a number with repeating digits at the beginning."""
        assert is_valid_number("1123") == False

    def test_invalid_all_same_digits(self):
        """Should reject a number where all digits are identical."""
        assert is_valid_number("1111") == False

    def test_invalid_repeating_at_end(self):
        """Should reject a number with repeating digits at the end."""
        assert is_valid_number("1233") == False

    def test_invalid_contains_letters(self):
        """Should reject input containing alphabetic characters."""
        assert is_valid_number("12ab") == False

    def test_invalid_contains_special_chars(self):
        """Should reject input containing special characters."""
        assert is_valid_number("12-4") == False

    def test_invalid_contains_spaces(self):
        """Should reject input containing whitespace."""
        assert is_valid_number("1 34") == False

    def test_invalid_leading_zero(self):
        """Should reject a number starting with zero."""
        assert is_valid_number("0123") == False

    def test_none_input(self):
        """Should handle None input gracefully and return False."""
        assert is_valid_number(None) == False

    def test_integer_input(self):
        """Should accept integer input and validate it correctly."""
        assert is_valid_number(1234) == True 
