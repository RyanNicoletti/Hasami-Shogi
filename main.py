import pygame as pg
from constants import WIDTH, HEIGHT, SQUARE_SIZE
from game_states.hasamishogigame import Hasamishogigame
from game_states.menu import Menu
from game_states.game_over import GameOver
from game import GameRunner

pg.display.set_caption('Hasami Shogi')

pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
states = {
    'MENU': Menu(),
    'GAMEPLAY': Hasamishogigame(WIN),
    'GAME_OVER': GameOver()
}
game = GameRunner(WIN, states, 'MENU')
game.run()
pg.quit()