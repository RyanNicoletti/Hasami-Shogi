import pygame as pg
from .base_state import BaseState
from .hasamishogigame import Hasamishogigame
from constants import WHITE, BLACK, RED


class GameOver(BaseState):
    def __init__(self):
        super().__init__()
        self.title = self.font.render("", True, WHITE)
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.instructions = self.font.render("press space to start again, or enter to go to menu", True, WHITE)
        instructions_center = (self.screen_rect.center[0], self.screen_rect.center[1] + 50)
        self.instructions_rect = self.instructions.get_rect(center=instructions_center)

    def get_winner(self):
        self.title = self.font.render("Red wins!", True, WHITE) if self.persist['blackcaps'] >= 8 else self.font.render(
            "Black wins!", True, WHITE)
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                self.next_state = "MENU"
                self.done = True
            elif event.key == pg.K_SPACE:
                self.next_state = "GAMEPLAY"
                self.done = True
            elif event.key == pg.K_ESCAPE:
                self.quit = True

    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.instructions, self.instructions_rect)
