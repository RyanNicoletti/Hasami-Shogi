from constants import RED, WHITE, BLACK, SQUARE_SIZE
import pygame as pg

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.calc_pos()

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pg.draw.circle(win, BLACK, (self.x, self.y), radius + self.OUTLINE)
        pg.draw.circle(win, self.color, (self.x, self.y), radius)

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
