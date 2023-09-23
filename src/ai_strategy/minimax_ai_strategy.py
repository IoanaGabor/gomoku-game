import random

from src.ai_strategy.general_ai_strategy import GeneralAIStrategy
from src.board.board_utils import BoardUtils

from src.board.board import Board


class MinimaxAIStrategy(GeneralAIStrategy):

    def get_move(self, player):
        """Computes computer's move

        :param player: computer player index (int)
        :return: move (tuple)
        """
        move = BoardUtils.find_winning_move(self._board.copy_of(), player)
        if move is not None:
            return move
        move = BoardUtils.find_winning_move(self._board.copy_of(), 3 - player)
        if move is not None:
            return move
        if self._board.empty_board():
            rand_x = random.randrange(0, self._board.height)
            rand_y = random.randrange(0, self._board.width)
            return rand_x, rand_y
        # minimax here
        _, x, y = MinimaxAIStrategy.__minimax(self._board.copy_of(), 3, player, player, -100000000, 10000000000)
        return x, y

    @staticmethod
    def __compute_board_value_for_computer_player(board, player_in_turn, computer_player_index):
        """Computes the board value as (computer_player_board_value / human_player_board_value)

        :param board: Board
        :param player_in_turn:int
        :param computer_player_index:int
        :return: float
        """
        first_score = MinimaxAIStrategy.__get_score(board, computer_player_index, player_in_turn)
        second_score = MinimaxAIStrategy.__get_score(board, 3 - computer_player_index, player_in_turn)
        if second_score == 0:
            second_score = 1
        return first_score / second_score

    @staticmethod
    def __minimax(board: Board, depth: int, current_player, computer_player_index, alpha, beta):
        """Minimax algorithm for getting computer's move

        :param board: Board
        :param depth: int
        :param current_player:int
        :param computer_player_index:int
        :param alpha: float
        :param beta: float
        :return: move (tuple - move_value, x, y)
        """
        if depth == 0:
            val = MinimaxAIStrategy.__compute_board_value_for_computer_player(board, current_player,
                                                                            computer_player_index)
            return val, None, None
        all_moves = BoardUtils.get_empty_neighbouring_cells(board)
        if len(all_moves) == 0:
            return MinimaxAIStrategy.__compute_board_value_for_computer_player(board, current_player,
                                                                             computer_player_index), None, None
        if current_player == computer_player_index:  # maximizing player
            best_value = -100000000
            best_x = None
            best_y = None
            for move in all_moves:
                new_board = board.copy_of()
                new_board.add_stone(move[0], move[1], current_player)
                value, _, _ = MinimaxAIStrategy.__minimax(new_board, depth - 1, 3 - current_player, computer_player_index,
                                                        alpha,
                                                        beta)
                if value > alpha:
                    alpha = value
                if value >= beta:
                    return value, None, None
                if value > best_value:
                    best_value = value
                    best_x = move[0]
                    best_y = move[1]
        else:  # minimizing player
            best_value = 10000000000
            best_x = None
            best_y = None
            for move in all_moves:
                new_board = board.copy_of()
                new_board.add_stone(move[0], move[1], current_player)
                value, _, _ = MinimaxAIStrategy.__minimax(new_board, depth - 1, 3 - current_player, computer_player_index,
                                                        alpha,
                                                        beta)
                if value < beta:
                    beta = value
                if value <= alpha:
                    return value, None, None
                if value < best_value:
                    best_value = value
                    best_x = move[0]
                    best_y = move[1]
        return best_value, best_x, best_y

    @staticmethod
    def __get_score(board, player, player_in_turn):
        """Gets a player's score on the board, considering the horizontal, vertical and diagonal score.

        :param board: Board
        :param player: int
        :param player_in_turn:int
        :return: float
        """
        return MinimaxAIStrategy.__compute_horizontal_value(board, player, player_in_turn) \
            + MinimaxAIStrategy.__compute_vertical_value(board, player, player_in_turn) \
            + MinimaxAIStrategy.__compute_diagonal_value(board, player, player_in_turn)

    @staticmethod
    def __compute_horizontal_value(board, player, player_in_turn):
        """Computes the horizontal value of a player's stones, by grouping consecutive ocupied cells
        in intervals, taking into account if those intervals can be extended further and the player that is in turn.

        :param board: Board
        :param player: int
        :param player_in_turn:int
        :return: float
        """
        score = 0
        for i in range(board.height):
            count = 0
            interval_beginning = -1
            for j in range(board.width):
                if board.configuration[i][j] == player:
                    count += 1
                    if interval_beginning == -1:
                        interval_beginning = j
                else:
                    if count > 0:
                        blocked_cells = 0
                        if interval_beginning == 0 or (interval_beginning != 0
                                                       and board.configuration[i][
                                                           interval_beginning - 1] != 0):
                            blocked_cells += 1

                        if board.configuration[i][j] != 0:
                            blocked_cells += 1
                        # call to the calculate value function
                        score += MinimaxAIStrategy.__get_value_of_interval_of_stones(count, blocked_cells,
                                                                                   (player == player_in_turn))
                        interval_beginning = -1
                        count = 0
            if count > 0:
                blocked_cells = 1
                if interval_beginning == 0 or (interval_beginning != 0
                                               and board.configuration[i][interval_beginning - 1] != 0):
                    blocked_cells += 1
        return score

    @staticmethod
    def __compute_vertical_value(board, player, player_in_turn):
        """Computes the vertical value of a player's stones, by grouping consecutive ocupied cells
        in intervals, taking into account if those intervals can be extended further and the player that is in turn.

        :param board: Board
        :param player: int
        :param player_in_turn:int
        :return: float
        """
        score = 0
        for j in range(board.width):
            count = 0
            interval_beginning = -1
            for i in range(board.height):
                if board.configuration[i][j] == player:
                    count += 1
                    if interval_beginning == -1:
                        interval_beginning = i
                else:
                    if count > 0:
                        blocked_cells = 0
                        if interval_beginning == 0 or (interval_beginning != 0
                                                       and board.configuration[interval_beginning - 1][
                                                           j] != 0):
                            blocked_cells += 1

                        if board.configuration[i][j] != 0:
                            blocked_cells += 1
                        # call to the calculate value function
                        score += MinimaxAIStrategy.__get_value_of_interval_of_stones(count, blocked_cells,
                                                                                   (player == player_in_turn))
                        interval_beginning = -1
                        count = 0
            if count > 0:
                blocked_cells = 1
                if interval_beginning == 0 or (interval_beginning != 0
                                               and board.configuration[interval_beginning - 1][j] != 0):
                    blocked_cells += 1
        return score

    @staticmethod
    def __compute_diagonal_value(board, player, player_in_turn):
        """Computes the diagonal value of a player's stones, by grouping consecutive ocupied cells
        in intervals, taking into account if those intervals can be extended further and the player that is in turn.

        :param board: Board
        :param player: int
        :param player_in_turn:int
        :return: float
        """
        # "principal" diagonals
        score = 0
        for i in range(board.height):
            count = 0
            interval_beginning_x = -1
            interval_beginning_y = -1
            x = i
            y = 0
            while x < board.height and y < board.width:
                if board.configuration[x][y] == player:
                    count += 1
                    if interval_beginning_x == -1:
                        interval_beginning_x = x
                        interval_beginning_y = y
                else:
                    if count > 0:
                        blocked_cells = 0
                        if interval_beginning_y == 0 or (interval_beginning_y != 0
                                                         and board.configuration[interval_beginning_x - 1][
                                                             interval_beginning_y - 1] != 0):
                            blocked_cells += 1

                        if board.configuration[x][y] != 0:
                            blocked_cells += 1
                        # call to the calculate value function
                        score += MinimaxAIStrategy.__get_value_of_interval_of_stones(count, blocked_cells,
                                                                                   (player == player_in_turn))
                        interval_beginning_x = -1
                        interval_beginning_y = -1
                        count = 0
                x += 1
                y += 1
            if count > 0:
                blocked_cells = 1
                if interval_beginning_y == 0 or (interval_beginning_y != 0
                                                 and board.configuration[interval_beginning_x - 1][
                                                     interval_beginning_y - 1] != 0):
                    blocked_cells += 1
        for i in range(board.width):
            count = 0
            interval_beginning_x = -1
            interval_beginning_y = -1
            x = 0
            y = i
            while x < board.height and y < board.width:
                if board.configuration[x][y] == player:
                    count += 1
                    if interval_beginning_x == -1:
                        interval_beginning_x = x
                        interval_beginning_y = y
                else:
                    if count > 0:
                        blocked_cells = 0
                        if interval_beginning_x == 0 or (interval_beginning_x != 0
                                                         and board.configuration[interval_beginning_x - 1][
                                                             interval_beginning_y - 1] != 0):
                            blocked_cells += 1

                        if board.configuration[x][y] != 0:
                            blocked_cells += 1
                        # call to the calculate value function
                        score += MinimaxAIStrategy.__get_value_of_interval_of_stones(count, blocked_cells,
                                                                                   (player == player_in_turn))
                        interval_beginning_x = -1
                        interval_beginning_y = -1
                        count = 0
                x += 1
                y += 1
            if count > 0:
                blocked_cells = 1
                if interval_beginning_x == 0 or (interval_beginning_x != 0
                                                 and board.configuration[interval_beginning_x - 1][
                                                     interval_beginning_y - 1] != 0):
                    blocked_cells += 1

        # "secondary" diagonals
        for i in range(board.height):
            count = 0
            interval_beginning_x = -1
            interval_beginning_y = -1
            x = i
            y = board.width - 1
            while x < board.height and y >= 0:
                if board.configuration[x][y] == player:
                    count += 1
                    if interval_beginning_x == -1:
                        interval_beginning_x = x
                        interval_beginning_y = y
                else:
                    if count > 0:
                        blocked_cells = 0
                        if interval_beginning_y == board.width - 1 or (
                                interval_beginning_y != board.width - 1
                                and board.configuration[interval_beginning_x - 1][
                                    interval_beginning_y + 1] != 0):
                            blocked_cells += 1

                        if board.configuration[x][y] != 0:
                            blocked_cells += 1
                        # call to the calculate value function
                        score += MinimaxAIStrategy.__get_value_of_interval_of_stones(count, blocked_cells,
                                                                                   (player == player_in_turn))
                        interval_beginning_x = -1
                        interval_beginning_y = -1
                        count = 0
                x += 1
                y -= 1
            if count > 0:
                blocked_cells = 1
                if interval_beginning_y == board.width - 1 or (interval_beginning_y != board.width - 1
                                                               and board.configuration[
                                                                   interval_beginning_x - 1][
                                                                   interval_beginning_y + 1] != 0):
                    blocked_cells += 1
        for i in range(board.width):
            count = 0
            interval_beginning_x = -1
            interval_beginning_y = -1
            x = 0
            y = i
            while x < board.height and y >= 0:
                if board.configuration[x][y] == player:
                    count += 1
                    if interval_beginning_x == -1:
                        interval_beginning_x = x
                        interval_beginning_y = y
                else:
                    if count > 0:
                        blocked_cells = 0
                        if interval_beginning_x == 0 or (interval_beginning_x != 0
                                                         and board.configuration[interval_beginning_x - 1][
                                                             interval_beginning_y + 1] != 0):
                            blocked_cells += 1

                        if board.configuration[x][y] != 0:
                            blocked_cells += 1
                        # call to the calculate value function
                        score += MinimaxAIStrategy.__get_value_of_interval_of_stones(count, blocked_cells,
                                                                                   (player == player_in_turn))
                        interval_beginning_x = -1
                        interval_beginning_y = -1
                        count = 0
                x += 1
                y -= 1
            if count > 0:
                blocked_cells = 1
                if interval_beginning_x == 0 or (interval_beginning_x != 0
                                                 and board.configuration[interval_beginning_x - 1][
                                                     interval_beginning_y + 1] != 0):
                    blocked_cells += 1

        return score

    @staticmethod
    def __get_value_of_interval_of_stones(interval_length, blocked_cells, turn):
        """Gets the value of an interval of stones, given its length, the number of cells that block it from extending
        and the player's turn.

        :param interval_length: int
        :param blocked_cells: int
        :param turn: int
        :return: float
        """
        if blocked_cells == 2 and interval_length < 5:
            return 0
        if interval_length >= 5:
            return 1000000000
        if interval_length == 4:
            if turn:
                return 1000000
            else:
                if blocked_cells == 0:
                    return 200000
                return 500
        if interval_length == 3:
            if blocked_cells == 0:
                if turn:
                    return 5000
                return 200
            else:
                if turn:
                    return 20
                else:
                    return 15
        if interval_length == 2:
            if blocked_cells == 0:
                if turn:
                    return 10
                return 8
            else:
                return 4
        if interval_length == 1:
            return 1
