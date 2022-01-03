import pygame as pg
from constants import WIDTH, HEIGHT, SQUARE_SIZE


class GameRunner():

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
        for event in pg.event.get():
            self.state.get_event(event)

    def change_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

        # determine winner if game is over
        if self.state == self.states["GAME_OVER"]:
            self.states["GAME_OVER"].get_winner()

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
