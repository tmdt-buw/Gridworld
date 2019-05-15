import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

import numpy as np
from matplotlib import pyplot as plt
import time
import threading
from kivy.interactive import InteractiveLauncher
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
import warnings

Window.size = (890, 620)
warnings.simplefilter(action='ignore', category=FutureWarning)

state_i = 1

class GameVisualizer(Widget):
    def __init__(self, states):
        super(GameVisualizer, self).__init__()

        self.states = states
        self.game = Game(self.states[0])
        self.add_widget(self.game)
        pass

    def vis_states(self, *args):
        global state_i
        if state_i != len(self.states):
            self.remove_widget(self.game)
            self.game = Game(self.states[state_i])
            self.add_widget(self.game)
            state_i += 1

        return True


class Game(Widget):
    def __init__(self, state, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.player = Player((15, 325))
        self.grid = Grid(state)
        self.add_widget(self.grid)


class Player(Image):
    def __init__(self, position, dead=False, goal=False, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.keep_ratio = False
        self.allow_stretch = True
        self.keep_data = True
        self.source = 'Artwork/Player.zip'
        if dead:
            self.source = 'Artwork/Dead.zip'
        if goal:
            self.source = 'Artwork/Flag.zip'
        self.pos = position  # (15, 325)
        self.size = (60, 60)

    def move_to(self, position):
        self.source = 'Artwork/Player.zip'
        self.pos = (15 + 44.25*position[0], 325 + 25*position[1])


class Grid(Widget):
    def __init__(self, state, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.add_widget(Image(source='Artwork/Background.png', pos=(0, 0), size=(890, 620), keep_ratio=False, allow_stretch=True))
        for y in reversed(range(0, 10)):
            for x in range(0, 10):

                new_tile = Tile(type=state[y][x][0], position=[state[y][x][1][0], state[y][x][1][1], np.random.randint(0, 2)])

                self.add_widget(new_tile)
                if state[y][x][2]:
                    if state[y][x][0] == 7:
                        self.add_widget(Player((new_tile.pos[0] + 15+5, new_tile.pos[1] + 70), dead=True))
                    elif state[y][x][0] == 6:
                        self.add_widget(Player((new_tile.pos[0] + 15, new_tile.pos[1] + 70), goal=True))
                    else:
                        self.add_widget(Player((new_tile.pos[0] + 15, new_tile.pos[1] + 70)))


class Tile(Image):
    def __init__(self, type, position, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.size = (100, 100)
        if type == 1:
            self.pos = ((self.size[0] / 2 - 6) * position[0] + (self.size[0] / 2 - 6) * position[1],
                        300 - self.size[1] / 2 - 25 * position[0] + 25 * position[1] + 5 * position[2])
            self.source = 'Artwork/isometric_0056.png'
        elif type == 2:
            self.pos = ((self.size[0] / 2 - 6) * position[0] + (self.size[0] / 2 - 6) * position[1],
                        300 - self.size[1] / 2 - 25 * position[0] + 25 * position[1] + 5 * position[2])
            self.source = 'Artwork/isometric_0057.png'
        elif type == 3:
            self.pos = ((self.size[0] / 2 - 6) * position[0] + (self.size[0] / 2 - 6) * position[1],
                        300 - self.size[1] / 2 - 25 * position[0] + 25 * position[1] + 5 * position[2])
            self.source = 'Artwork/isometric_0058.png'
        elif type == 4:
            self.pos = ((self.size[0] / 2 - 6)*position[0]+(self.size[0] / 2 - 6)*position[1], 300 - self.size[1] / 2 - 25*position[0]+25*position[1]+5*position[2])
            self.source = 'Artwork/isometric_0036.png'
        elif type == 5:
            self.pos = ((self.size[0] / 2 - 6) * position[0] + (self.size[0] / 2 - 6) * position[1],
                        300 - self.size[1] / 2 - 25 * position[0] + 25 * position[1] + 30)
            self.source = 'Artwork/isometric_0055.png'
        elif type == 6:
            self.pos = ((self.size[0] / 2 - 6) * position[0] + (self.size[0] / 2 - 6) * position[1],
                        300 - self.size[1] / 2 - 25 * position[0] + 25 * position[1] + 5 * position[2])
            self.source = 'Artwork/isometric_0023.png'
        elif type == 7:
            self.pos = ((self.size[0] / 2 - 6) * position[0] + (self.size[0] / 2 - 6) * position[1],
                        300 - self.size[1] / 2 - 25 * position[0] + 25 * position[1] + 5 * position[2])
            self.source = 'Artwork/isometric_0036.png'


class VisualizerApp(App):
    def __init__(self, states, actions, **kwargs):
        super(VisualizerApp, self).__init__(**kwargs)
        self.game_visualizer = None
        self.states = states
        self.actions = actions

    def build(self):
        self.game_visualizer = GameVisualizer(self.states)
        Clock.schedule_interval(self.game_visualizer.vis_states, 0.8)
        return self.game_visualizer


def visualize(states):
    grids = []

    for state in states:
        if len(state.shape) > 2:
            state = np.transpose(state, axes=(1, 0, 2))
        grid = []
        for id_y, state_y in enumerate(state):
            grid_y = []
            for id_x, state_x in enumerate(state_y):
                if state_x == 'P' or (state_x == np.array([0, 0, 0, 1])).all():
                    grid_x = [1, [id_x, id_y], True]
                elif state_x == 'X' or (state_x == np.array([0, 1, 0, 0])).all():
                    grid_x = [4, [id_x, id_y], False]
                elif state_x == 'W' or (state_x == np.array([0, 0, 1, 0])).all():
                    grid_x = [5, [id_x, id_y], False]
                elif state_x == 'G'or (state_x == np.array([1, 0, 0, 0])).all():
                    grid_x = [6, [id_x, id_y], True]
                elif state_x == 'D'or (state_x == np.array([0, 1, 0, 1])).all():
                    grid_x = [7, [id_x, id_y], True]
                else:
                    grid_x = [1, [id_x, id_y], False]
                grid_y.append(grid_x)
            grid.append(grid_y)
        grids.append(grid)

    app = VisualizerApp(grids, 'b')
    app.run()
