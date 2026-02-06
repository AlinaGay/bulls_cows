# game.py
"""Game module for Bulls and Cows game."""

from config import MAX_ATTEMPTS
from player import Player
from utils import calculate_bulls_cows, generate_number, is_valid_number


class Game:
    """One round of the game: one makes a secret, the other guesses."""

    def __init__(
        self,
        codemaker: Player,
        codebreaker: Player,
        max_attempts: int = MAX_ATTEMPTS
    ):
        """Initialize the Game."""
        self.codemaker = codemaker
        self.codebreaker = codebreaker
        self.max_attempts = max_attempts
        self.history: list[dict] = []
        self.secret: str | None = None

    def play(self) -> dict:
        """Play a round of the game."""
        self.secret = self.codemaker.make_secret()

        if not is_valid_number(self.secret):
            print(f"Агент загадал невалидное число: {self.secret}")
            self.secret = generate_number()
            print(f"   Заменено на: {self.secret}")

        print(f"\n {self.codemaker.name} загадал число (скрыто)")

        for attempt in range(1, self.max_attempts + 1):
            guess = self.codebreaker.make_guess(self.history)

            if not is_valid_number(guess):
                print(f"Ход {attempt}: невалидная попытка {guess}, пропуск")
                continue

            bulls, cows = self.codemaker.count_bulls_cows(self.secret, guess)
            engine_bulls, engine_cows = calculate_bulls_cows(
                self.secret, guess)
            if bulls != engine_bulls or cows != engine_cows:
                print(f"Агент ошибся: {bulls} Б {cows} К")
                print(f"Правильно: {engine_bulls} Б {engine_cows} К")
                bulls, cows = engine_bulls, engine_cows

            self.history.append({
                "attempt": attempt,
                "guess": guess,
                "bulls": bulls,
                "cows": cows
            })

            print(f"Ход {attempt}: {guess} → {bulls} Б {cows} К)")

            if bulls == 4:
                print(f"\n{self.codebreaker.name} угадал за {attempt} ходов!")
                return {
                    "winner": self.codebreaker.name,
                    "attempts": attempt,
                    "secret": self.secret,
                    "history": self.history
                }

        print(f"\n{self.codebreaker.name} не угадал."
              f"Число было: {self.secret}")

        return {
                "winner": None,
                "attempts": self.max_attempts,
                "secret": self.secret,
                "history": self.history
            }
