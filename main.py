# main.py
"""Entry point for Bulls and Cows AI game."""

from game import Game
from player import Player
from prompts import PLAYER_1_PROMPT, PLAYER_2_PROMPT


def main():
    """Run the Bulls and Cows game between two AI agents."""
    player_1 = Player("Player_1", PLAYER_1_PROMPT)
    player_2 = Player("Player_2", PLAYER_2_PROMPT)

    print("=" * 50)
    print("        БЫКИ И КОРОВЫ: AI vs AI")
    print("=" * 50)

    print("\n РАУНД 1: Player_1 загадывает, Player_2 угадывает")
    game_1 = Game(codemaker=player_1, codebreaker=player_2)
    result_1 = game_1.play()

    print("\n РАУНД 2: Player_2 загадывает, Player_1 угадывает")
    game_2 = Game(codemaker=player_2, codebreaker=player_1)
    result_2 = game_2.play()

    print("\n" + "=" * 50)
    print("                 ИТОГИ")
    print("=" * 50)
    print(f"Раунд 1: {result_1['attempts']} ходов")
    print(f"Раунд 2: {result_2['attempts']} ходов")


if __name__ == "__main__":
    main()
