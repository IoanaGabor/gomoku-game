import copy

from src.exceptions.board_exceptions import BoardException


class Board:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__configuration = []
        for line in range(height):
            self.__configuration.append([])
            for column in range(width):
                self.__configuration[line].append(0)

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def configuration(self):
        return self.__configuration

    def validate_added_stone(self, x, y):
        """Validates an added stone.

        :param x: int
        :param y: int
        :return: tuple (bool - True if valid, string - error messages)
        """
        valid = True
        messages = ""
        if x >= self.__height or x < 0:
            valid = False
            messages += "x is not in range."
        if y >= self.__width or y < 0:
            valid = False
            messages += "y is not in range.\n"
        if valid and self.__configuration[x][y] != 0:
            valid = False
            messages += "Can't place stone here. The place is not empty\n"
        return valid, messages

    def add_stone(self, x, y, player):
        """Adds a stone to the board.

        :param x: int
        :param y: int
        :param player:int
        :return: -
        """
        valid, message = self.validate_added_stone(x, y)
        if valid is False:
            raise BoardException(message)
        self.__configuration[x][y] = player

    def copy_of(self):
        """Returns a copy of the board

        :return: Board
        """
        return copy.deepcopy(self)

    def reset(self):
        """Clears the board.

        :return: -
        """
        for line in range(self.height):
            for column in range(self.width):
                self.__configuration[line][column] = 0

    def empty_board(self):
        """Checks if the board is empty.

        :return: True if empty, False otherwise.
        """
        for line in range(self.height):
            for column in range(self.width):
                if self.__configuration[line][column] != 0:
                    return False
        return True

    def full_board(self):
        """Checks if the board is full.

        :return: True if full, False otherwise.
        """
        for line in range(self.height):
            for column in range(self.width):
                if self.__configuration[line][column] == 0:
                    return False
        return True
