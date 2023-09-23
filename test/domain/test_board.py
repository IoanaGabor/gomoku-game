from unittest import TestCase

from src.board.board import Board


class TestBoard(TestCase):
    def setUp(self):
        self.__board = Board(5, 5)

    def test_height(self):
        self.assertEqual(self.__board.height, 5)

    def test_width(self):
        self.assertEqual(self.__board.width, 5)

    def test_validate_added_stone_ok(self):
        valid, messages = self.__board.validate_added_stone(3, 4)
        self.assertEqual(valid, True)
        self.assertEqual(messages, "")

    def test_validate_added_stone_outside(self):
        valid, messages = self.__board.validate_added_stone(10, -1)
        self.assertEqual(valid, False)
        self.assertEqual(messages, "x is not in range.y is not in range.\n")

    def test_validate_added_stone_already_taken_place(self):
        self.__board.add_stone(2, 3, 1)
        valid, messages = self.__board.validate_added_stone(2, 3)
        self.assertEqual(valid, False)
        self.assertEqual(messages, "Can't place stone here. The place is not empty\n")
