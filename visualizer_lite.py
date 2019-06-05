import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

# print(plt.style.available)
# plt.style.use('seaborn-dark')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def visualize(states):

    grid_states = []
    positions = []
    deaths = []
    state_mines = []
    state_walls = []
    goal = [9, 0]
    dead = False

    for state in states:
        state = np.flip(state, axis=0)
        grid = []
        mines = []
        walls = []
        for id_y, state_y in enumerate(state):
            grid_y = []
            for id_x, state_x in enumerate(state_y):
                if state_x == 'P' or (state_x == np.array([0, 0, 0, 1])).all():
                    grid_x = [0.0, 0.0, 1.0]
                    pos = [id_x, id_y]
                elif state_x == 'X' or (state_x == np.array([0, 1, 0, 0])).all():
                    grid_x = [0.5, 0.5, 0.0]
                    mines.append([id_x, id_y])
                elif state_x == 'W' or (state_x == np.array([0, 0, 1, 0])).all():
                    grid_x = [0.0, 0.5, 0.5]
                    walls.append([id_x, id_y])
                elif state_x == 'G'or (state_x == np.array([1, 0, 0, 0])).all():
                    grid_x = [0.5, 0.0, 0.5]
                elif state_x == 'D'or (state_x == np.array([0, 1, 0, 1])).all():
                    grid_x = [1.0, 0.0, 0.0]
                    pos = [id_x, id_y]
                    dead = True
                else:
                    grid_x = [0.0, 1.0, 0.0]
                grid_y.append(grid_x)
            grid.append(grid_y)
        grid_states.append(grid)
        positions.append(pos)
        deaths.append(dead)
        state_mines.append(mines)
        state_walls.append(walls)

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    sm = 0
    sw = 0
    for state, pos, dead in zip(grid_states, positions, deaths):
        ax.cla()
        ax.imshow(state)
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.5, 9.5)
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(-.5, 10.5, 1))
        ax.xaxis.tick_top()
        ax.set_yticks(np.flip(np.arange(-.5, 10.5, 1), axis=0))
        ax.set_xticklabels(np.arange(0, 11, 1))
        ax.set_yticklabels(np.arange(0, 11, 1))
        ax.grid()
        ax.text(goal[0], goal[1], 'Z', va='center', ha='center', fontsize=30, color='w')
        for mine in state_mines[sm]:
            ax.text(mine[0], mine[1], 'M', va='center', ha='center', fontsize=30, color='w')
        for wall in state_walls[sw]:
            ax.text(wall[0], wall[1], 'W', va='center', ha='center', fontsize=30, color='w')
        if dead:
            ax.text(pos[0], pos[1], 'T', va='center', ha='center', fontsize=30, color='w')
        else:
            ax.text(pos[0], pos[1], 'S', va='center', ha='center', fontsize=30, color='w')

        plt.pause(0.5)
        sm += 1
        sw += 1
        # plt.savefig('bilder/{}.png'.format(sm))

    plt.close()