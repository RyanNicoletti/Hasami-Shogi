import pygame as pg
from constants import WIDTH, HEIGHT, SQUARE_SIZE
from hasamishogigame import Hasamishogigame

FPS = 60

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Hasami Shogi')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE #invert
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pg.time.Clock()
    game = Hasamishogigame(WIN)
    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select_move(row, col)

        game.update()
    pg.quit()
main()