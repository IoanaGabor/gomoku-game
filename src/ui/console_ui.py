from src.exceptions.service_exceptions import InvalidMoveException
from src.services.game_service import GameService
import texttable


class ConsoleUI:
    def __init__(self, game_service: GameService):
        self.__game_service = game_service

    def print_board(self):
        t = texttable.Texttable()
        board = self.__game_service.get_board()
        header = ['X']
        for i in range(board.width):
            header.append(i)

        t.header(header)
        for i in range(board.height):
            row = [i]
            for j in range(board.width):
                if board.configuration[i][j] == 1:
                    row.append('x')
                elif board.configuration[i][j] == 2:
                    row.append('o')
                else:
                    row.append(' ')
            t.add_row(row)
        print(t.draw())

    def __human_player_move(self, current_player):
        while True:
            print("Please enter your move")
            try:
                line = int(input("Enter the line:\n"))
                column = int(input("Enter the column:\n"))
                self.__game_service.add_stone(line, column, current_player)
                break
            except ValueError as ve:
                print("The line and column should be integers")
            except InvalidMoveException as ie:
                print(ie)

    def display_the_potential_winner(self):
        winner = self.__game_service.check_for_win()
        if winner is not None:
            print("#{0} is the winner".format(winner))

    def run_game_vs_human_player(self):
        current_player = 1
        while True:
            self.print_board()
            print("Player #{0}".format(current_player))
            self.__human_player_move(current_player)
            current_player = 3 - current_player
            draw = self.__game_service.check_for_draw()
            if draw:
                print("Draw")
                break
            winner = self.__game_service.check_for_win()
            if winner is not None:
                print("#{0} is the winner".format(winner))
                break

    @staticmethod
    def __read_starting_player():
        while True:
            starting_player = input("Who shall start the game? 1 - you, 2 - computer\n")
            if starting_player == '1' or starting_player == '2':
                return int(starting_player)
            else:
                print("Invalid choice")

    def run_game_vs_ai_player(self):
        current_player = self.__read_starting_player()
        while True:
            if current_player == 1:
                self.__human_player_move(current_player)
            else:
                self.__game_service.place_computer_move(current_player)
                self.print_board()
            current_player = 3 - current_player
            winner = self.__game_service.check_for_win()
            if winner is not None:
                self.print_board()
                if winner == 1:
                    print("you are the winner")
                else:
                    print("you lost")
                break

    @staticmethod
    def print_menu():
        print("Options: ")
        print("1. Start a new game vs human player: ")
        print("2. Start a new game vs AI")
        print("0. Quit")

    def start(self):
        while True:
            self.__game_service.reset()
            ConsoleUI.print_menu()
            option = input()
            if option == '0':
                break
            elif option == '1':
                self.run_game_vs_human_player()
            elif option == '2':
                self.run_game_vs_ai_player()
            else:
                print("Invalid command")
