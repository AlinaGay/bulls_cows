# main.py
"""Entry point for Bulls and Cows AI game."""

import logging_config

from game import Game
from loguru import logger
from player import Player
from prompts import PLAYER_1_PROMPT, PLAYER_2_PROMPT


def main():
    """Run the Bulls and Cows game between two AI agents."""
    logger.info("=" * 50)
    logger.info("БЫКИ И КОРОВЫ: AI vs AI")
    logger.info("=" * 50)

    player_1 = Player("Player_1", PLAYER_1_PROMPT)
    player_2 = Player("Player_2", PLAYER_2_PROMPT)

    logger.info("")
    logger.info("\n РАУНД 1: Player_1 загадывает, Player_2 угадывает")
    game_1 = Game(codemaker=player_1, codebreaker=player_2)
    result_1 = game_1.play()

    logger.info("")
    logger.info("\n РАУНД 2: Player_2 загадывает, Player_1 угадывает")
    game_2 = Game(codemaker=player_2, codebreaker=player_1)
    result_2 = game_2.play()

    logger.info("")
    logger.info("=" * 40)
    logger.info("ИТОГИ")
    logger.info("=" * 40)
    logger.info(f"Раунд 1: {result_1['attempts']} ходов")
    logger.info(f"Раунд 2: {result_2['attempts']} ходов")

    if result_1['winner'] and result_2['winner']:
        if result_1['attempts'] < result_2['attempts']:
            logger.info("Победитель: Player_2")
        elif result_2['attempts'] < result_1['attempts']:
            logger.info("Победитель: Player_1")
        else:
            logger.info("Ничья!")
    elif result_1['winner']:
        logger.info("Победитель: Player_2")
    elif result_2['winner']:
        logger.info("Победитель: Player_1")
    else:
        logger.info("Никто не угадал!")

    logger.info("Игра завершена")


if __name__ == "__main__":
    main()
