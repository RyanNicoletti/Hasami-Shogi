import pygame as pg
from .base_state import BaseState
from board import Board

from constants import RED, WHITE, BLACK


class Menu(BaseState):
    def __init__(self):
        super(Menu, self).__init__()
        self.active_index = 0
        self.options = ["Start Game", "Quit Game"]
        self.next_state = "GAMEPLAY"

    def render_text(self, index):
        color = RED if index == self.active_index else WHITE
        return self.font.render(self.options[index], True, color)

    def get_text_positions(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index*50))
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.done = True
        if self.active_index == 1:
            self.quit = True

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.active_index = 1 if self.active_index <= 0 else 0
            elif event.key == pg.K_DOWN:
                self.active_index = 0 if self.active_index >= 1 else 1
            elif event.key == pg.K_RETURN:
                self.handle_action()

    def draw(self, surface):
        surface.fill(BLACK)
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_positions(text_render, index))
