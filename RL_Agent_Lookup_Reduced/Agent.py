import hashlib
import json
from RL_Agent_Lookup_Reduced.GridWorld import GridWorld
import numpy as np
import RL_Agent_Lookup_Reduced.Aktionen as act

grid_world = GridWorld()

def init_gridworld(random_player=False, random_mines=False, maze=False):
    global grid_world
    grid_world = GridWorld(random_player, random_mines, maze)
    act.grid_world = grid_world

agent = False
def zeigen(pause):
    grid_world.zeigen(agent=agent, pause=pause)

def reduce(pos = None):
    if pos==None:
        pos = act.spieler_position()
    reduced = [[act.inhalt_oben(pos), act.inhalt_unten(pos), act.inhalt_links(pos), act.inhalt_rechts(pos)]]
    new_reduced = [[]]
    for cell in reduced[0]:
        if cell == 'Frei':
            new_reduced[0].append([0, 0, 0, 0])
        elif cell == 'Mine':
            new_reduced[0].append([0, 1, 0, 0])
        elif cell == 'Wand':
            new_reduced[0].append([0, 0, 1, 0])
        elif cell == 'Spieler':
            new_reduced[0].append([0, 0, 0, 0])
        elif cell == 'Ziel':
            new_reduced[0].append([1, 0, 0, 0])
        elif cell == 'A':
            new_reduced[0].append([0, 0, 1, 0])

    # new_reduced[0].append([0, 0, pos[0], pos[1]])
    return np.array(new_reduced)

def train_agent(epochs, lookup, random_player, random_mines, maze, file_path):
    global agent

    agent = lookup

    gamma = 0.975
    epsilon = 1

    for i in range(epochs):
        init_gridworld(random_player, random_mines, maze)
        state = grid_world.states[0]
        state_reduced = reduce()
        status = 1
        step = 0
        print(f'Spiel: {i}')
        # while game still in progress
        while(status == 1):
            state_reduced.flags.writeable = False
            state_hash = str(hashlib.md5(bytes(state_reduced)).hexdigest())
            state_reduced.flags.writeable = True
            if state_hash not in lookup.keys():
                lookup[state_hash] = [0, 0, 0, 0]
            qval = lookup[state_hash]
            if (np.random.random(1) < epsilon): # choose random action
                action = np.random.randint(0, 4)
            else: # choose best action from Q(s,a) values
                action = (np.argmax(qval))
            # Take action, observe new state S'
            new_state = grid_world.make_move(state, action)
            new_state_reduced = reduce()
            new_state_reduced.flags.writeable = False
            new_state_hash = str(hashlib.md5(bytes(new_state_reduced)).hexdigest())
            new_state_reduced.flags.writeable = True
            if new_state_hash not in lookup.keys():
                lookup[new_state_hash] = [0, 0, 0, 0]
            newQ = lookup[new_state_hash]
            maxQ = np.max(newQ)
            # Observe reward
            reward = grid_world.getReward(new_state, step)
            if reward not in [10, -100]:  # non-terminal state
                update = reward + gamma * maxQ
            else:  # terminal state
                update = reward
            y = qval[:]
            y[action] = update
            # if i % 100 == 0:
            #     print('Game {0}, action {1}, reward {2}'.format(i, action, reward))
            lookup[str(state_hash)] = y[:]
            state = np.copy(new_state)
            state_reduced = reduce()
            if reward in [10, -100]:
                status = 0
            if i % 100 == 0:
                if reward in [10, -100]:
                    status = 0
                    with open(file_path, 'w') as f:
                        json.dump(lookup, f)
                    print('*'*30)
                    print(f'Zeige Spiel{i}')
                    print('*'*30)
                    zeigen(0.05)
            step += 1
        if epsilon > 0.1:
            epsilon -= (1/epochs)


def test_agent(lookup, random_player, random_mines, maze):
    global agent

    agent = lookup

    win = False
    solution = []
    step = 0
    init_gridworld(random_player, random_mines, maze)
    state = grid_world.states[0]
    state_reduced = reduce()
    status = 1
    while status == 1:
        state_reduced.flags.writeable = False
        state_hash = str(hashlib.md5(bytes(state_reduced)).hexdigest())
        state_reduced.flags.writeable = True
        if state_hash not in lookup.keys():
            #print('taking random action...')
            action = np.random.randint(0, 4)
        else:
            qval = lookup[state_hash]
           #print('taking lookup action with qvals: {}'.format(qval))
            action = np.argmax(qval)
        #print('Move %s; Taking action: %s' % (step+1, action))
        new_state = grid_world.make_move(state, action)
        new_state_reduced = reduce()
        reward = grid_world.getReward(new_state, step)
        solution.append(action)
        #print("Reward: %s" % (reward,))
        if reward in [10, -100]:
            status = 0
            if reward == 10:
                win = True
        state = np.copy(new_state)
        state_reduced = reduce()
        step += 1
        if step > 50:
            print("Game lost; too many moves.")
            break
    return win, solution

def q_values_aus_lookup(lookup, state, pos):
    state_reduced = reduce(pos)
    state_reduced.flags.writeable = False
    state_hash = str(hashlib.md5(bytes(state_reduced)).hexdigest())
    state_reduced.flags.writeable = True
    if state_hash not in lookup.keys():
        lookup[state_hash] = [0, 0, 0, 0]
    qval = lookup[state_hash]

    return qval
