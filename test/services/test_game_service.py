from unittest import TestCase

from src.ai_strategy.minimax_ai_strategy import MinimaxAIStrategy
from src.board.board import Board
from src.exceptions.service_exceptions import InvalidMoveException
from src.services.game_service import GameService


class TestGameService(TestCase):
    def setUp(self):
        self.__board = Board(7, 7)
        self.__ai_strategy = MinimaxAIStrategy(self.__board)
        self.__service = GameService(self.__board, self.__ai_strategy)
        self.__board.add_stone(1, 1, 1)
        self.__board.add_stone(1, 3, 2)
        self.__board.add_stone(2, 1, 1)
        self.__board.add_stone(2, 4, 2)
        self.__board.add_stone(3, 1, 1)
        self.__board.add_stone(3, 2, 2)
        self.__board.add_stone(5, 1, 1)
        self.__board.add_stone(4, 2, 2)

    def test_validate_move(self):
        self.assertEqual(self.__service.validate_move(3, 3), (True, ""))
        self.assertEqual(self.__service.validate_move(5, 1),
                         (False, "Can't place stone here. The place is not empty\n"))

    def test_add_stone(self):
        self.__service.add_stone(3, 3, 1)
        self.assertRaises(InvalidMoveException, self.__service.add_stone, 3, 3, 2)

    def test_height(self):
        self.assertEqual(self.__service.get_height(), 7)

    def test_width(self):
        self.assertEqual(self.__service.get_width(), 7)

    def test_check_for_win(self):
        self.__service.add_stone(4, 1, 1)
        self.assertEqual(self.__service.check_for_win(), 1)

    def test_check_for_win_none(self):
        self.assertEqual(self.__service.check_for_win(), None)

    def test_place_computer_move(self):
        self.__service.place_computer_move(2)
        self.assertEqual(self.__board.configuration[4][1], 2)
