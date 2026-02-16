# tests/test_game.py
"""Tests for Game class."""

import pytest
from unittest.mock import MagicMock, patch

from game import Game
from player import Player


class TestGameInit:
    """Tests for Game initialization."""

    def test_game_init(self):
        """Game should initialize with correct attributes."""
        codemaker = MagicMock(spec=Player)
        codebreaker = MagicMock(spec=Player)

        game = Game(codemaker, codebreaker)

        assert game.codemaker == codemaker
        assert game.codebreaker == codebreaker
        assert game.max_attempts == 10
        assert game.history == []
        assert game.secret is None

    def test_game_custom_attempts(self):
        """Game should accept custom max_attempts."""
        codemaker = MagicMock(spec=Player)
        codebreaker = MagicMock(spec=Player)

        game = Game(codemaker, codebreaker, max_attempts=5)

        assert game.max_attempts == 5


class TestGamePlay:
    """Tests for Game.play method."""

    def test_immediate_win(self):
        """Codebreaker guesses correctly on first try."""
        codemaker = MagicMock(spec=Player)
        codemaker.name = "Maker"
        codemaker.make_secret.return_value = "1234"
        codemaker.count_bulls_cows.return_value = (4, 0)

        codebreaker = MagicMock(spec=Player)
        codebreaker.name = "Breaker"
        codebreaker.make_guess.return_value = "1234"

        game = Game(codemaker, codebreaker)
        result = game.play()

        assert result["winner"] == "Breaker"
        assert result["attempts"] == 1
        assert result["secret"] == "1234"

    def test_win_after_several_attempts(self):
        """Codebreaker wins after multiple guesses."""
        codemaker = MagicMock(spec=Player)
        codemaker.name = "Maker"
        codemaker.make_secret.return_value = "1234"
        codemaker.count_bulls_cows.side_effect = [(0, 2), (1, 2), (4, 0)]

        codebreaker = MagicMock(spec=Player)
        codebreaker.name = "Breaker"
        codebreaker.make_guess.side_effect = ["5678", "1324", "1234"]

        game = Game(codemaker, codebreaker)
        result = game.play()

        assert result["winner"] == "Breaker"
        assert result["attempts"] == 3

    def test_no_winner(self):
        """Codebreaker fails to guess within max attempts."""
        codemaker = MagicMock(spec=Player)
        codemaker.name = "Maker"
        codemaker.make_secret.return_value = "1234"
        codemaker.count_bulls_cows.return_value = (0, 0)

        codebreaker = MagicMock(spec=Player)
        codebreaker.name = "Breaker"
        codebreaker.make_guess.return_value = "5678"

        game = Game(codemaker, codebreaker, max_attempts=3)
        result = game.play()

        assert result["winner"] is None
        assert result["attempts"] == 3

    def test_invalid_secret_replaced(self):
        """Invalid secret should be replaced with generated number."""
        codemaker = MagicMock(spec=Player)
        codemaker.name = "Maker"
        codemaker.make_secret.return_value = "1123"
        codemaker.count_bulls_cows.return_value = (4, 0)

        codebreaker = MagicMock(spec=Player)
        codebreaker.name = "Breaker"
        codebreaker.make_guess.return_value = "1234"

        game = Game(codemaker, codebreaker)

        with patch("game.generate_number", return_value="5678"):
            result = game.play()

        assert result["secret"] == "5678"

    def test_invalid_guess_skipped(self):
        """Invalid guesses should be skipped."""
        codemaker = MagicMock(spec=Player)
        codemaker.name = "Maker"
        codemaker.make_secret.return_value = "1234"
        codemaker.count_bulls_cows.return_value = (4, 0)

        codebreaker = MagicMock(spec=Player)
        codebreaker.name = "Breaker"
        codebreaker.make_guess.side_effect = ["1123", "0123", "1234"]
        game = Game(codemaker, codebreaker)
        result = game.play()

        assert result["winner"] == "Breaker"
        assert len(result["history"]) == 1

    def test_history_recorded(self):
        """History should record all valid attempts."""
        codemaker = MagicMock(spec=Player)
        codemaker.name = "Maker"
        codemaker.make_secret.return_value = "1234"
        codemaker.count_bulls_cows.side_effect = [(0, 2), (4, 0)]

        codebreaker = MagicMock(spec=Player)
        codebreaker.name = "Breaker"
        codebreaker.make_guess.side_effect = ["5621", "1234"]

        game = Game(codemaker, codebreaker)
        result = game.play()

        assert len(result["history"]) == 2
        assert result["history"][0]["guess"] == "5621"
        assert result["history"][0]["bulls"] == 0
        assert result["history"][0]["cows"] == 2

    def test_engine_overrides_agent_calculation(self):
        """Engine calculation should override agent's wrong calculation."""
        codemaker = MagicMock(spec=Player)
        codemaker.name = "Maker"
        codemaker.make_secret.return_value = "1234"
        codemaker.count_bulls_cows.return_value = (1, 1)

        codebreaker = MagicMock(spec=Player)
        codebreaker.name = "Breaker"
        codebreaker.make_guess.side_effect = ["5678", "1234"]

        game = Game(codemaker, codebreaker)
        result = game.play()

        assert result["history"][0]["bulls"] == 0
        assert result["history"][0]["cows"] == 0
