import pygame

from src.exceptions.service_exceptions import InvalidMoveException
from src.gui.colors import BLACK, BUTTON, WHITE, BOARD

from src.services.game_service import GameService


class GUI:
    def __init__(self, game_service: GameService):
        self.__game_service = game_service
        self.size = 675
        self.screen = pygame.display.set_mode((900, self.size + 45))
        pygame.display.set_caption("Gomoku game")
        self.game_type = None

    def draw_text(self, text, x_pos, y_pos, font_color, font_size):
        font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x_pos, y_pos)
        self.screen.blit(text_surface, text_rect)

    def draw_main(self, x=45 * 16, y=45, w=125, h=45):
        self.screen.fill(BOARD)
        pygame.draw.rect(self.screen, BUTTON, (x, y, w, h))
        pygame.draw.rect(self.screen, BUTTON, (x, y + 70, w, h))
        pygame.draw.rect(self.screen, BUTTON, (x, y + 140, w, h))
        self.draw_text("2 players", x + 59, y + 25, BLACK, 20)
        self.draw_text("1 player", x + 59, y + 95, BLACK, 20)
        self.draw_text("exit", x + 59, y + 165, BLACK, 20)
        for i in range(1, 16):
            pygame.draw.line(self.screen, BLACK,
                             [45 * i, 45], [45 * i, self.size], 2)
            pygame.draw.line(self.screen, BLACK,
                             [45, 45 * i], [self.size, 45 * i], 2)

    def play_draw_stone(self, current_player, stone_color, x_mouse, y_mouse):
        if x_mouse % 45 > 20:
            x_mouse += 45
        if y_mouse % 45 > 20:
            y_mouse += 45
        x_mouse = (x_mouse // 45) * 45
        y_mouse = (y_mouse // 45) * 45
        try:
            self.__game_service.add_stone(x_mouse // 45 - 1, y_mouse // 45 - 1, current_player)
        except InvalidMoveException:
            return
        pygame.draw.circle(self.screen, stone_color,
                           (x_mouse, y_mouse), 30 // 2)
        return x_mouse // 45 - 1, y_mouse // 45 - 1

    def game_over(self):
        draw = self.__game_service.check_for_draw()
        if draw:
            self.draw_text("DRAW", self.size // 2, 30, BLACK, 35)
            self.game_type = None
            self.__game_service.reset()
        winner = self.__game_service.check_for_win()
        if winner is not None:
            if winner == 1:
                self.draw_text("white is the winner", self.size // 2, 30, BLACK, 35)
            else:
                self.draw_text("black is the winner", self.size // 2, 30, BLACK, 35)
            self.game_type = None
            self.__game_service.reset()

    def run(self):
        pygame.init()
        pygame.font.init()
        self.draw_main()
        player_turn = 1
        self.game_type = None
        while True:
            event = pygame.event.poll()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if (125 + 45 * 16) > x_mouse > 45 * 16 and 90 > y_mouse > 45:
                    self.game_type = 1
                    self.__game_service.reset()
                    player_turn = 1
                    self.draw_main()
                    self.draw_text("2 players", 45 * 16 + 60, 300, BLACK, 35)
                if (125 + 45 * 16) > x_mouse > 45 * 16 and 160 > y_mouse > 115:
                    self.game_type = 2
                    self.__game_service.reset()
                    player_turn = 1
                    self.draw_main()
                    self.draw_text("1 player", 45 * 16 + 60, 300, BLACK, 35)
                if (125 + 45 * 16) > x_mouse > 45 * 16 and 230 > y_mouse > 185:
                    pygame.quit()
                    quit()
                if self.game_type == 1:
                    if 45 <= x_mouse <= self.size \
                            and 45 <= y_mouse <= self.size:
                        if player_turn == 1:
                            self.play_draw_stone(1, WHITE, x_mouse, y_mouse)
                        elif player_turn == 2:
                            self.play_draw_stone(2, BLACK, x_mouse, y_mouse)
                        self.game_over()

                        player_turn = 3 - player_turn
                elif self.game_type == 2:
                    if 45 <= x_mouse <= self.size \
                            and 45 <= y_mouse <= self.size:
                        if player_turn == 1:
                            position = self.play_draw_stone(1, WHITE, x_mouse, y_mouse)
                            if position is not None:
                                self.game_over()
                                pygame.display.update()
                                player_turn = 2
                                x, y = self.__game_service.place_computer_move(player_turn)
                                pygame.draw.circle(self.screen, BLACK,
                                                   ((x + 1) * 45, (y + 1) * 45), 30 // 2)
                                self.game_over()
                                player_turn = 1
            pygame.display.update()
