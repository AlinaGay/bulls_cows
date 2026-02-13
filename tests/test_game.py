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
