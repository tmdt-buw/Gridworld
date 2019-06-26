import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import json

from Agent import q_values_aus_lookup

# print(plt.style.available)
# plt.style.use('seaborn-dark')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

show_qvals = False
lookup = None
neural_network = None
a_type = None


def toggle_qvals(agent, agent_type):
    global show_qvals, lookup, neural_network, a_type

    if agent_type=="lookup":
        lookup = agent
        show_qvals = True
        a_type = agent_type
    elif agent_type=="net":
        neural_network = agent
        show_qvals = True
        a_type = agent_type

def visualize(states):
    grid_states = []
    positions = []
    deaths = []
    state_mines = []
    state_walls = []
    state_qvals = []
    goal = [5, 0]
    dead = False

    for state in states:
        # state = np.flip(state, axis=0)
        grid = []
        mines = []
        walls = []
        qvals = []
        for id_y, state_y in enumerate(state):
            grid_y = []
            for id_x, state_x in enumerate(state_y):
                if state_x == 'P' or (state_x == np.array([0, 0, 0, 1])).all():
                    grid_x = [0.5, 0.5, 1.0]
                    pos = [id_x, id_y]
                    if show_qvals:
                        if a_type=="lookup":
                            qv = q_values_aus_lookup(lookup, state, [id_x, id_y])
                        elif a_type=="net":
                            qv = q_values_aus_netz(neural_network, state, [id_x, id_y])
                        qvals.append([id_x, id_y, qv, np.argmax(qv)])
                elif state_x == 'X' or (state_x == np.array([0, 1, 0, 0])).all():
                    grid_x = [0.5, 0.5, 0.0]
                    mines.append([id_x, id_y])
                elif state_x == 'W' or (state_x == np.array([0, 0, 1, 0])).all():
                    grid_x = [0.0, 0.5, 0.5]
                    walls.append([id_x, id_y])
                elif state_x == 'G'or (state_x == np.array([1, 0, 0, 0])).all() or (state_x == np.array([1, 0, 0, 1])).all():
                    grid_x = [0.5, 0.0, 0.5]
                elif state_x == 'D'or (state_x == np.array([0, 1, 0, 1])).all():
                    grid_x = [1.0, 0.0, 0.0]
                    pos = [id_x, id_y]
                    dead = True
                else:
                    grid_x = [0.0, 1.0, 0.0]
                    if show_qvals:
                        if a_type=="lookup":
                            qv = q_values_aus_lookup(lookup, state, [id_x, id_y])
                        elif a_type=="net":
                            qv = q_values_aus_netz(neural_network, state, [id_x, id_y])
                        qvals.append([id_x, id_y, qv, np.argmax(qv)])
                grid_y.append(grid_x)
            grid.append(grid_y)
        grid_states.append(grid)
        positions.append(pos)
        deaths.append(dead)
        state_mines.append(mines)
        state_walls.append(walls)
        state_qvals.append(qvals)

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    sm = 0
    sw = 0
    sq = 0
    for state, pos, dead in zip(grid_states, positions, deaths):
        ax.cla()
        state = np.flip(state, axis=0)
        ax.imshow(state)
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-0.5, 4.5)
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(-.5, 5.5, 1))
        ax.xaxis.tick_top()
        ax.set_yticks(np.flip(np.arange(-.5, 4.5, 1), axis=0))
        ax.set_xticklabels(np.arange(0, 7, 1))
        ax.set_yticklabels(np.arange(0, 6, 1))
        ax.grid()
        ax.text(goal[0], goal[1], 'Z', va='center', ha='center', fontsize=25, color='w')
        for mine in state_mines[sm]:
            ax.text(mine[0], 4-mine[1], 'M', va='center', ha='center', fontsize=25, color='w')
        for wall in state_walls[sw]:
            ax.text(wall[0], 4-wall[1], 'W', va='center', ha='center', fontsize=25, color='w')
        for qvals in state_qvals[sq]:
            if qvals[3] == 0:
                ax.arrow(qvals[0], 4-qvals[1], 0.0, 0.5, length_includes_head=True,
          head_width=0.2, head_length=0.2)
                # ax.text(qvals[0], 9-qvals[1]+0.4, '{}'.format(round(qvals[2][0], 1)), va='top', ha='center', fontsize=15, color='black')
            elif qvals[3] == 1:
                ax.arrow(qvals[0], 4-qvals[1], 0.0, -0.5, length_includes_head=True,
          head_width=0.2, head_length=0.2)
                # ax.text(qvals[0], 9-qvals[1]-0.4, '{}'.format(round(qvals[2][1], 1)), va='bottom', ha='center', fontsize=15, color='black')
            elif qvals[3] == 2:
                ax.arrow(qvals[0], 4-qvals[1], -0.5, 0.0, length_includes_head=True,
          head_width=0.2, head_length=0.2)
                # ax.text(qvals[0]-0.4, 9-qvals[1], '{}'.format(round(qvals[2][2], 1)), va='center', ha='left', fontsize=15, color='black')
            elif qvals[3] == 3:
                ax.arrow(qvals[0], 4-qvals[1], 0.5, 0.0, length_includes_head=True,
          head_width=0.2, head_length=0.2)
                # ax.text(qvals[0]+0.4, 9-qvals[1], '{}'.format(round(qvals[2][3], 1)), va='center', ha='right', fontsize=15, color='black')
        if dead:
            ax.text(pos[0], 4-pos[1], 'T', va='center', ha='center', fontsize=25, color='w')
        else:
            ax.text(pos[0], 4-pos[1], 'S', va='center', ha='center', fontsize=15, color='w')

        plt.pause(0.05)
        sm += 1
        sw += 1
        sq += 1

    plt.close()
