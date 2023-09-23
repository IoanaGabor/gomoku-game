from src.board.board import Board


class GeneralAIStrategy:
    def __init__(self, board: Board):
        self._board = board

    def get_move(self, player):
        """Gets the move of the AI Strategy. Abstract method.

        :param player: int
        :return: move (tuple)
        """
        raise NotImplementedError("This method is not implemented here")
