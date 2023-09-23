class BoardUtils:
    @staticmethod
    def __check_principal_diagonal_win(board, x, y, player):
        """Checks if a player has a winning line of stones, with the line starting at (x,y)
        and being parallel to the principal diagonal

        :param board: Board
        :param x: int
        :param y: int
        :param player:int
        :return: True if win, False otherwise
        """
        for i in range(5):
            if not (x + i < board.height and y + i < board.width and
                    board.configuration[x + i][y + i] == player):
                return False
        return True

    @staticmethod
    def __check_secondary_diagonal_win(board, x, y, player):
        """Checks if a player has a winning line of stones, with the line starting at (x,y)
        and being parallel to the secondary diagonal

        :param board: Board
        :param x: int
        :param y: int
        :param player:int
        :return: True if win, False otherwise
        """
        for i in range(5):
            if not (x + i < board.height and y + i >= 0 and
                    board.configuration[x + i][y - i] == player):
                return False
        return True

    @staticmethod
    def __check_horizontal_win(board, x, y, player):
        """Checks if a player has a winning line of stones, with the horizontal line starting at (x,y)

        :param board: Board
        :param x: int
        :param y: int
        :param player:int
        :return: True if win, False otherwise
        """
        for i in range(5):
            if not (x + i < board.height and board.configuration[x + i][y] == player):
                return False
        return True

    @staticmethod
    def __check_vertical_win(board, x, y, player):
        """Checks if a player has a winning line of stones, with the vertical line starting at (x,y)

        :param board: Board
        :param x: int
        :param y: int
        :param player:int
        :return: True if win, False otherwise
        """
        for i in range(5):
            if not (y + i < board.width and board.configuration[x][y + i] == player):
                return False
        return True

    @staticmethod
    def check_for_win(board):
        """Checks for a winner.

        :param board: Board
        :return: int or None
        """
        width = board.width
        height = board.height
        for i in range(height):
            for j in range(width):
                for player in [1, 2]:
                    if BoardUtils.__check_principal_diagonal_win(board, i, j, player) or \
                            BoardUtils.__check_vertical_win(board, i, j, player) or \
                            BoardUtils.__check_horizontal_win(board, i, j, player) or\
                            BoardUtils.__check_secondary_diagonal_win(board, i, j, player):
                        return player
        return None

    @staticmethod
    def get_empty_neighbouring_cells(board):
        """Get the empty cells that are neighbours to an occupied cell.

        :return: list of tuples
        """
        dx = [-1, 0, 1, 0, -1, 1, -1, 1]
        dy = [0, -1, 0, 1, -1, -1, 1, 1]
        cells = []
        for i in range(board.height):
            for j in range(board.width):
                if board.configuration[i][j] == 0:
                    for d in range(8):
                        nx = i + dx[d]
                        ny = j + dy[d]
                        if 0 <= nx < board.height and 0 <= ny < board.width:
                            if board.configuration[nx][ny] != 0:
                                cells.append((i, j))
                                break
        return cells

    @staticmethod
    def find_winning_move(board, player):
        """Finds a winning move, assuming that the given player is in turn.

        :param board: Board
        :param player: int
        :return: tuple or None
        """
        possible_moves = BoardUtils.get_empty_neighbouring_cells(board)
        for move in possible_moves:
            x = move[0]
            y = move[1]
            board.configuration[x][y] = player
            if BoardUtils.check_for_win(board) == player:
                return move
            board.configuration[x][y] = 0
        return None
