# Bulls and Cows: AI vs AI

Implementation of the classic "Bulls and Cows" game where two AI agents powered by YandexGPT play against each other.

## Description

The program runs a two-round tournament between AI agents:

- ** Round 1: Player_1 picks a number, Player_2 guesses
- ** Round 2: Player_2 picks a number, Player_1 guesses

Each agent uses its own guessing strategy. The winner is the one who guesses the number in fewer attempts.

## Game Rules

- A 4-digit number with unique digits is chosen (1023-9876)
- First digit cannot be 0
- **Bull** — digit is guessed and in the correct position
- **Cow** — digit exists in the number but in a different position
- **Win** — 4 bulls (number fully guessed)
- Maximum 10 attempts per round

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/username/bulls_cows.git
cd bulls_cows
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:
```env
YANDEX_FOLDER_ID=ваш_folder_id
YANDEX_API_KEY=ваш_api_key
API_BASE_URL=https://llm.api.cloud.yandex.net/v1
MODEL=yandexgpt-lite/rc
```

## Running
```bash
python main.py
```

## Project Structure
```
bulls_cows/
├── main.py              # Entry point
├── game.py              # Game and round logic
├── player.py            # Player class (API interaction)
├── prompts.py           # System prompts and strategies
├── utils.py             # Helper functions
├── config.py            # Configuration
├── client.py            # OpenAI client for Yandex API
├── logging_config.py    # Logging configuration
├── requirements.txt     # Dependencies
├── .env                 # Environment variables (not in git)
├── logs/                # Game logs
└── README.md
```

## Agent Strategies

### Player_1: Fast Scanning

1. **Scanning phase:** first moves — 1234, then 5678
2. **Identification phase:** determines "active" digits by sum of bulls and cows
3. **Permutation phase:** rearranges found digits until victory

### Player_2: Logical Deduction

1. **Result analysis:** eliminates impossible digits
2. **Positioning logic:** locks bulls, moves cows
3. **Combining:** uses information from ALL previous attempts

## Architecture

### Separation of Concerns

| Component | Responsibility |
|-----------|----------------|
| `Game` | Round management, validation, result calculation |
| `Player` | API interaction, move generation |
| `utils` | Number validation, bulls/cows calculation, JSON parsing |
| `prompts` | System prompts and strategies |

### Validation and Reliability

- **Double-check:** agent calculates bulls/cows, engine verifies
- **Fallback:** generates random number if invalid
- **Parsing:** handles markdown blocks and malformed JSON

## Logging

Logs are saved to the `logs/` folder with the name `game_YYYY-MM-DD_HH-mm-ss.txt`.

### Log Example
```
2026-02-10 12:30:45 | ==================================================
2026-02-10 12:30:45 | BULLS AND COWS: AI vs AI
2026-02-10 12:30:45 | ==================================================
2026-02-10 12:30:45 | 
2026-02-10 12:30:45 | ROUND 1: Player_1 picks, Player_2 guesses
2026-02-10 12:30:46 | Player_1 picked number: 3814
2026-02-10 12:30:47 | Move 1: 1234 → 1B 2C
2026-02-10 12:30:48 | Move 2: 4312 → 1B 2C
2026-02-10 12:30:49 | Move 3: 3142 → 1B 2C
2026-02-10 12:30:50 | Move 4: 3814 → 4B 0C
2026-02-10 12:30:50 | Player_2 guessed in 4 moves!
2026-02-10 12:30:50 | 
2026-02-10 12:30:50 | ROUND 2: Player_2 picks, Player_1 guesses
2026-02-10 12:30:51 | Player_2 picked number: 5672
2026-02-10 12:30:52 | Move 1: 1234 → 0B 1C
2026-02-10 12:30:53 | Move 2: 5678 → 2B 1C
2026-02-10 12:30:54 | Move 3: 5672 → 4B 0C
2026-02-10 12:30:54 | Player_1 guessed in 3 moves!
2026-02-10 12:30:54 | 
2026-02-10 12:30:54 | ========================================
2026-02-10 12:30:54 | RESULTS
2026-02-10 12:30:54 | ========================================
2026-02-10 12:30:54 | Round 1: 4 moves
2026-02-10 12:30:54 | Round 2: 3 moves
2026-02-10 12:30:54 | Winner: Player_1
2026-02-10 12:30:54 | Game finished
```

## Tech Stack

- **Python** 3.12+
- **OpenAI SDK** — Yandex AI Studio API interaction
- **Loguru** —  logging
- **python-dotenv** — environment variables

## Известные особенности

1. **Agent miscounting**: LLM sometimes miscalculates bulls/cows — engine always verifies and corrects
2. **Repeated moves**: agent may repeat attempts despite prompt instructions
3. **Temperature 0.5:** balance between creativity and stability

## License

MIT
