import random

from src.board.board import Board

from src.ai_strategy.general_ai_strategy import GeneralAIStrategy


class RandomizedAIStrategy(GeneralAIStrategy):
    def __init__(self, board: Board):
        super().__init__(board)

    def get_move(self, player):
        """Gets the move of the computer player with a randomized strategy

        :param player: int
        :return:
        """
        width = self._board.width
        height = self._board.height
        while True:
            rand_x = random.randrange(0, height)
            rand_y = random.randrange(0, width)
            if self._board.validate_added_stone(rand_x, rand_y)[0]:
                break
        return rand_x, rand_y
