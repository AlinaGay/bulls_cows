# game.py
import openai

from config import (
    BASE_URL,
    MAX_ATTEMPTS,
    MODEL,
    YANDEX_API_KEY,
    YANDEX_FOLDER_ID
)
from prompts import PLAYER_SYSTEM_PROMPT
from utils import (
    calculate_bulls_cows,
    generate_number,
    is_valid_number,
    parse_response
)


client = openai.OpenAI(
    api_key=YANDEX_API_KEY,
    base_url=BASE_URL,
    project=YANDEX_FOLDER_ID,
)


class Player:
    """Player of Bulls and cows game."""

    def __init__(self, name: str):
        """Initialize the Player."""
        self.name = name

    def send_message(self, message: str) -> str:
        """Send message to agent."""
        response = client.chat.completions.create(
            model=f"gpt://{YANDEX_FOLDER_ID}/{MODEL}",
            messages=[
                {"role": "system", "content": PLAYER_SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].message.content

    def make_secret(self) -> str:
        """Generate secret number."""
        response = self.send_message(
            "Роль: ЗАГАДЫВАЮЩИЙ — ЗАГАДАТЬ ЧИСЛО\n\nЗагадай 4-значное число."
        )
        data = parse_response(response)
        return data["number"]

    def make_guess(self, history: list = None) -> str:
        """Generate guess number."""
        if not history:
            history_text = "Это твоя первая попытка."
        else:
            lines = [
                f"Ход {h['attempt']}: {h['guess']} -> {h['bulls']}быков {h['cows']}коров"
                for h in history
            ]
            history_text = "История: \n" + "\n".join(lines)

        response = self.send_message(
            f"Роль: ОТГАДЫВАЮЩИЙ\n\n{history_text}\n\nСделай попытку."
        )
        data = parse_response(response)
        return data["number"]

    def count_bulls_cows(self, secret: str, guess: str) -> tuple[int, int]:
        """Count bulls and cows for guess number."""
        response = self.send_message(
            "Роль: ЗАГАДЫВАЮЩИЙ — ОЦЕНИТЬ ПОПЫТКУ\n\n"
            f"Сравни {secret} и {guess}."
            "Посчитай быков и коров."
        )
        data = parse_response(response)
        return data["bulls"], data['cows']


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
        self.history = []
        self.secret = None

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
        engine_bulls, engine_cows = calculate_bulls_cows(self.secret, guess)
        if bulls != engine_bulls or cows != engine_cows:
            print(f"Агент ошибся: {bulls}Б {cows}К")
            print(f"   Правильно:    {engine_bulls}Б {engine_cows}К")
            bulls, cows = engine_bulls, engine_cows

        self.history.append({
            "attempt": attempt,
            "guess": guess,
            "bulls": bulls,
            "cows": cows
        })

        print(f"   Ход {attempt}: {guess} → {bulls}Б {cows}К")

        if bulls == 4:
            print(f"\n{self.codebreaker.name} угадал за {attempt} ходов!")
            return {
                "winner": self.codebreaker.name,
                "attempts": attempt,
                "secret": self.secret,
                "history": self.history
            }

        print(f"\n😞 {self.codebreaker.name} не угадал."
              f"Число было: {self.secret}")

        return {
                "winner": None,
                "attempts": self.max_attempts,
                "secret": self.secret,
                "history": self.history
            }
