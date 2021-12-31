import pygame as pg
from constants import WIDTH, HEIGHT, SQUARE_SIZE


class GameRunner(object):

    # initialize a new game with a starting state (menu screen)
    def __init__(self, WIN, states, start_state):
        self.done = False
        self.WIN = WIN
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):

        def get_row_col_from_mouse(pos):
            x, y = pos
            row = y // SQUARE_SIZE  # invert, SQUARE_SIZE = WIDTH//COLS, width=800, cols = 9
            col = x // SQUARE_SIZE
            return row, col

        for event in pg.event.get():
            self.state.get_event(event)
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                self.state.select_move(row, col)

    def change_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.change_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.WIN)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()