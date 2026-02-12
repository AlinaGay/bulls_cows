# player.py
"""Player class for Bulls and Cows game."""

from config import MODEL, YANDEX_FOLDER_ID
from client import client
from loguru import logger
from prompts import COUNT_BULLS_COWS
from utils import parse_response


class Player:
    """Player of Bulls and cows game."""

    def __init__(self, name: str, system_prompt: str):
        """Initialize the Player."""
        self.name = name
        self.system_prompt = system_prompt

    def send_message(self, message: str) -> str | None:
        """Send message to agent."""
        response = client.chat.completions.create(
            model=f"gpt://{YANDEX_FOLDER_ID}/{MODEL}",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.5,
            max_tokens=100
        )

        return response.choices[0].message.content or ""

    def make_secret(self) -> str:
        """Generate secret number."""
        response = self.send_message(
            "Роль: ЗАГАДЫВАЮЩИЙ — ЗАГАДАТЬ ЧИСЛО\n\nЗагадай 4-значное число."
        )
        if not response:
            raise ValueError("Empty response from agent")
        data = parse_response(response)
        return data["number"]

    def make_guess(self, history: list | None = None) -> str:
        """Generate guess number."""
        if not history:
            history_text = "Это твоя первая попытка."
        else:
            lines = [
                f"Ход {h['attempt']}: {h['guess']} -> "
                f"{h['bulls']}быков {h['cows']}коров"
                for h in history
            ]
            history_text = "История: \n" + "\n".join(lines)

        response = self.send_message(
            f"Роль: ОТГАДЫВАЮЩИЙ\n\n{history_text}\n\nСделай попытку."
        )
        if not response:
            raise ValueError("Empty response from agent")
        data = parse_response(response)
        return data["number"]

    def count_bulls_cows(self, secret: str, guess: str) -> tuple[int, int]:
        """Count bulls and cows for guess number."""
        response = self.send_message(
            "Роль: ЗАГАДЫВАЮЩИЙ — ОЦЕНИТЬ ПОПЫТКУ\n\n"
            f"Твоё загаданное число: {secret}\n"
            f"Попытка соперника: {guess}\n\n"
            + COUNT_BULLS_COWS)
        if not response:
            raise ValueError("Empty response from agent")
        data = parse_response(response)
        return data["bulls"], data['cows']
