# game.py
import openai

from config import BASE_URL, MODEL, YANDEX_API_KEY, YANDEX_FOLDER_ID
from prompts import PLAYER_SYSTEM_PROMPT
from utils import parse_response


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
