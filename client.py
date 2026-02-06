# client.py
"""OpenAI client configured for Yandex AI Studio API."""

import openai

from config import (
    BASE_URL,
    YANDEX_API_KEY,
    YANDEX_FOLDER_ID
)


client = openai.OpenAI(
    api_key=YANDEX_API_KEY,
    base_url=BASE_URL,
    project=YANDEX_FOLDER_ID,
)
