import os
import openai
from dotenv import load_dotenv

load_dotenv()

YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
BASE_URL = os.getenv("API_BASE_URL")
MODEL = os.getenv("MODEL")

# Prompt from AI Studio
PLAYER_SYSTEM_PROMPT = """Ты играешь в игру "Быки и коровы".
В каждом сообщении тебе будет указана твоя текущая роль.

ПРАВИЛА ИГРЫ:
Один игрок загадывает 4-значное число, другой пытается его отгадать.
- Число состоит из 4 разных цифр (цифры не повторяются)
- Первая цифра не может быть 0 (число от 1000 до 9999)
- Примеры валидных чисел: 1234, 5678, 9012, 3847
- Примеры НЕвалидных: 1123 (повтор), 0123 (ноль в начале)

Подсказки после каждой попытки:
- Бык — цифра угадана И стоит на правильной позиции
- Корова — цифра есть в числе, но стоит на другой позиции
- Победа — 4 быка (число полностью угадано)

---

РОЛЬ: ЗАГАДЫВАЮЩИЙ — ЗАГАДАТЬ ЧИСЛО
Когда тебе говорят загадать число — придумай случайное 4-значное число по правилам.

Ответ: {"action": "make", "number": "XXXX", "bulls": 0, "cows": 0}

---

РОЛЬ: ЗАГАДЫВАЮЩИЙ — ОЦЕНИТЬ ПОПЫТКУ
Когда тебе дают попытку соперника для оценки:
1. Сравни попытку с твоим загаданным числом
2. Посчитай быков (цифра на правильном месте)
3. Посчитай коров (цифра есть, но на другом месте)

Как считать:
- Сначала найди все точные совпадения (позиция И цифра) = быки
- Затем среди оставшихся найди цифры, которые есть в числе = коровы
- Одна цифра не может быть одновременно быком и коровой

Пример:
Загадано: 1234, Попытка: 1432
- Позиция 1: 1=1 → БЫК
- Позиция 2: 2≠4, но 4 есть → КОРОВА  
- Позиция 3: 3=3 → БЫК
- Позиция 4: 4≠2, но 2 есть → КОРОВА
Результат: 2 быка, 2 коровы

Ответ: {"action": "evaluate", "number": "", "bulls": X, "cows": Y}

---

РОЛЬ: ОТГАДЫВАЮЩИЙ
Когда тебе говорят сделать попытку, проанализируй историю и сделай логичный ход.

СТРАТЕГИЯ ОТГАДЫВАНИЯ:

1. ПЕРВАЯ ПОПЫТКА (нет истории):
   Выбери число с разными цифрами, например: 1234, 5678, 1256, 3847

2. АНАЛИЗ РЕЗУЛЬТАТОВ:
   - 0 быков, 0 коров → этих 4 цифр НЕТ в числе, исключи их
   - 0 быков, N коров → N цифр есть, но ВСЕ не на своих местах
   - N быков, 0 коров → N цифр угаданы с позицией, остальных нет
   - N быков, M коров → N на местах + M есть, но не на местах

3. ЛОГИКА ИСКЛЮЧЕНИЯ:
   - Попытка 1234 → 0Б 0К: цифры 1,2,3,4 исключены навсегда
   - Попытка 5678 → 1Б 1К: две из 5,6,7,8 верные
   - Комбинируй информацию из ВСЕХ попыток

4. ЛОГИКА ПОЗИЦИОНИРОВАНИЯ:
   - Корова → пробуй эту цифру на других позициях
   - Бык → сохраняй цифру на этой позиции
   - Не было быка → меняй цифру на этой позиции

5. ПРИМЕР РАССУЖДЕНИЯ:
   Попытка 1: 1234 → 1Б 1К
   Попытка 2: 1567 → 1Б 0К
   Анализ:
   - Бык в обоих на позиции 1 → цифра 1 верна
   - Корова из попытки 1: одна из 2,3,4 есть, но не на месте
   - Цифры 5,6,7 исключены
   Следующая: 1342 (1 на месте, пробуем 3,4,2 в других позициях)

6. ПРАВИЛА:
   - Не повторяй сделанные попытки
   - Учитывай ВСЮ историю
   - 4 разные цифры, первая не 0

Ответ: {"action": "guess", "number": "XXXX", "bulls": 0, "cows": 0}

---

ВАЖНО:
- Отвечай ТОЛЬКО JSON без лишнего текста
- ВСЕГДА возвращай все 4 поля: action, number, bulls, cows
- Внимательно читай свою роль в каждом сообщении
- При подсчёте быков и коров будь точен"""


client = openai.OpenAI(
    api_key=YANDEX_API_KEY,
    base_url=BASE_URL,
    project=YANDEX_FOLDER_ID,
)


class Player:
    """Player of 'Bulls and cows' is agent from AI Studio."""

    def __init__(self, name: str):
        """Init method for class Player."""
        self.name = name

    def send_message(self, message: str) -> str:
        """Send message (analogy of agent calling)."""
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
        return self.send_message(
            "Роль: ЗАГАДЫВАЮЩИЙ — ЗАГАДАТЬ ЧИСЛО\n\nЗагадай 4-значное число.")

    def evaluate_guess(self, secret: str, guess: str) -> str:
        """Evaluate the guess number."""
        return self.send_message(f"""Роль: ЗАГАДЫВАЮЩИЙ — ОЦЕНИТЬ ПОПЫТКУ

        Твоё загаданное число: {secret}
        Попытка соперника: {guess}

        Посчитай быков и коров.""")

    def make_guess(self, history: list = None) -> str:
        """Generate guess number."""
        if not history:
            history_text = "Это твоя первая попытка."
        else:
            lines = [f"Ход {m['attempt']}: {m['guess']} → {m['bulls']}Б {m['cows']}К" for m in history]
            history_text = "История:\n" + "\n".join(lines)

        return self.send_message(
            f"Роль: ОТГАДЫВАЮЩИЙ\n\n{history_text}\n\nСделай попытку.")


# Two players (Player_1 и Player_2 from AI Studio)
player_1 = Player("Player_1")
player_2 = Player("Player_2")

# Test
print("=== Player_1: загадывает ===")
print(player_1.make_secret())

print("\n=== Player_2: угадывает ===")
print(player_2.make_guess())
