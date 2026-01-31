# tests/test_bulls_cows.py

from main import analyze_bulls, analyze_cows


class TestAnalyzeBulls:
    """Tests for bulls calculation."""

    def test_all_bulls(self):
        """Should return 4 when all digits match positions."""
        assert analyze_bulls("1234", "1234") == 4

    def test_no_bulls(self):
        """Should return 0 when no digits match positions."""
        assert analyze_bulls("1234", "4321") == 0

    def test_two_bulls(self):
        """Should return 2 when two digits match positions."""
        assert analyze_bulls("1234", "1243") == 2

    def test_one_bull(self):
        """Should return 1 when one digit matches position."""
        assert analyze_bulls("1234", "1567") == 1


class TestAnalyzeCows:
    """Tests for cows calculation."""

    def test_all_cows(self):
        """Should return 4 when all digits exist but in wrong positions."""
        bulls = analyze_bulls("1234", "4321")
        assert analyze_cows("1234", "4321", bulls) == 4

    def test_no_cows(self):
        """Should return 0 when no additional matches exist."""
        bulls = analyze_bulls("1234", "5678")
        assert analyze_cows("1234", "5678", bulls) == 0

    def test_two_cows(self):
        """Should return 2 cows for partial match."""
        bulls = analyze_bulls("1234", "1243")
        assert analyze_cows("1234", "1243", bulls) == 2

    def test_mixed_result(self):
        """Should correctly calculate cows with some bulls present."""
        bulls = analyze_bulls("1234", "1325")
        assert analyze_cows("1234", "1325", bulls) == 2


class TestBullsCowsCombined:
    """Integration tests for bulls and cows together."""

    def test_victory_condition(self):
        """Should return 4 bulls and 0 cows for exact match."""
        bulls = analyze_bulls("1234", "1234")
        cows = analyze_cows("1234", "1234", bulls)
        assert bulls == 4
        assert cows == 0

    def test_complete_miss(self):
        """Should return 0 bulls and 0 cows when nothing matches."""
        bulls = analyze_bulls("1234", "5678")
        cows = analyze_cows("1234", "5678", bulls)
        assert bulls == 0
        assert cows == 0
