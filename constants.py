# constants.py

import os
from dotenv import load_dotenv

load_dotenv()

YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
BASE_URL = os.getenv("API_BASE_URL")
MODEL = os.getenv("MODEL")
MAX_ATTEMPTS = 10
