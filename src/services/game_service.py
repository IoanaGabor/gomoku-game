import copy

from src.board.board import Board

from src.ai_strategy.general_ai_strategy import GeneralAIStrategy
from src.exceptions.service_exceptions import InvalidMoveException
from src.board.board_utils import BoardUtils


class GameService:
    def __init__(self, board: Board, ai_strategy: GeneralAIStrategy):
        self.__board = board
        self.__ai_strategy = ai_strategy

    def validate_move(self, x, y):
        return self.__board.validate_added_stone(x, y)

    def add_stone(self, x, y, player):
        """Adds a stone to the board.

        :param x: int
        :param y: int
        :param player:int
        """
        valid, messages = self.validate_move(x, y)
        if not valid:
            raise InvalidMoveException(messages)
        self.__board.add_stone(x, y, player)

    def check_for_win(self):
        """Checks for a winner

        :return: int or None
        """
        return BoardUtils.check_for_win(self.__board)

    def check_for_draw(self):
        """Checks for a draw

        :return: True if draw, False otherwise
        """
        return self.__board.full_board()

    def place_computer_move(self, current_player):
        """Places and returns a computer move, by using an AI strategy.

        :param current_player: int
        :return:
        """
        x, y = self.__ai_strategy.get_move(current_player)
        self.add_stone(x, y, current_player)
        return x, y

    def get_board(self):
        return copy.deepcopy(self.__board)

    def get_width(self):
        return self.__board.width

    def get_height(self):
        return self.__board.height

    def reset(self):
        self.__board.reset()
