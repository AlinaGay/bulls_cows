# player.py
"""Player class for Bulls and Cows game."""

from client import client
from loguru import logger
from config import MODEL, YANDEX_FOLDER_ID
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
            "Когда тебе дают попытку соперника для оценки:\n"
            "1. Сравни попытку с твоим загаданным числом\n"
            "2. Посчитай быков (цифра на правильном месте)\n"
            "3. Посчитай коров (цифра есть, но на другом месте)\n\n"

            "Как считать:\n"
            "- Сначала найди все точные совпадения (позиция И цифра) = быки\n"
            "- Затем среди оставшихся найди цифры, "
            "которые есть в числе = коровы\n"
            "- Одна цифра не может быть одновременно быком и коровой\n\n"
            "Пример:\n"
            "Загадано: 1234, Попытка: 1325\n"
            "- Позиция 1: 1=1 → БЫК\n"
            "- Позиция 2: 2≠3, но 3 есть в 1234 → КОРОВА\n"
            "- Позиция 3: 3≠2, но 2 есть в 1234 → КОРОВА\n"
            "- Позиция 4: 4≠5, и 5 нет в 1234 → ничего\n"
            "Результат: 1 бык, 2 коровы\n\n"
            "Теперь посчитай для своих чисел."
        )
        if not response:
            raise ValueError("Empty response from agent")
        data = parse_response(response)
        return data["bulls"], data['cows']
