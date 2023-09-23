from unittest import TestCase

from src.ai_strategy.minimax_ai_strategy import MinimaxAIStrategy
from src.board.board import Board


class TestMiniMaxAI(TestCase):
    def setUp(self):
        self.__board = Board(7, 7)
        self.__ai_strategy = MinimaxAIStrategy(self.__board)

    def test_place_winning_move(self):
        self.__board.add_stone(1, 1, 1)
        self.__board.add_stone(1, 3, 2)
        self.__board.add_stone(2, 1, 1)
        self.__board.add_stone(2, 4, 2)
        self.__board.add_stone(3, 1, 1)
        self.__board.add_stone(3, 2, 2)
        self.__board.add_stone(5, 1, 1)
        self.__board.add_stone(4, 2, 2)
        self.assertEqual(self.__ai_strategy.get_move(2), (4, 1))

    def test_place_best_move(self):
        self.__board.add_stone(1, 1, 1)
        self.__board.add_stone(1, 3, 2)
        self.__board.add_stone(2, 1, 1)
        self.__board.add_stone(5, 5, 2)
        self.__board.add_stone(4, 1, 1)
        self.__board.add_stone(2, 4, 2)
        self.assertEqual(self.__ai_strategy.get_move(2), (3, 1))

    def test_block_winning_move(self):
        self.__board.add_stone(1, 1, 1)
        self.__board.add_stone(1, 3, 2)
        self.__board.add_stone(2, 1, 1)
        self.__board.add_stone(2, 4, 2)
        self.__board.add_stone(3, 1, 1)
        self.__board.add_stone(3, 2, 2)
        self.__board.add_stone(5, 1, 1)
        self.__board.add_stone(4, 2, 2)
        self.assertEqual(self.__ai_strategy.get_move(1), (4, 1))