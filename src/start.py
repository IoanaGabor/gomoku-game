from src.ai_strategy.minimax_ai_strategy import MinimaxAIStrategy
from src.ai_strategy.randomized_ai_strategy import RandomizedAIStrategy
from src.board.board import Board
from src.gui.gui import GUI

from src.services.game_service import GameService
from src.settings import SettingsLoader
from src.ui.console_ui import ConsoleUI


def start():
    board = Board(15, 15)
    ai_strategy = MinimaxAIStrategy(board)
    game_service = GameService(board, ai_strategy)
    settings = SettingsLoader()
    if settings.get_type() == "cli":
        console_ui = ConsoleUI(game_service)
        console_ui.start()
    elif settings.get_type() == "gui":
        gui = GUI(game_service)
        gui.run()


if __name__ == "__main__":
    start()
