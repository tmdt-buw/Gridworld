import hashlib
import json
from GridWorld import GridWorld
import numpy as np
import copy

grid_world = GridWorld()

def init_gridworld(random_player=False, random_mines=False, maze=False):
    global grid_world
    grid_world = GridWorld(random_player, random_mines, maze)

agent = False

def zeigen():
    grid_world.zeigen(agent=agent, agent_type='lookup')

def get_state_hash_string(state):
    state.flags.writeable = False
    state_hash = str(hashlib.md5(bytes(state)).hexdigest())
    state.flags.writeable = True

    return state_hash

def train_agent(epochs, lookup, random_player, random_mines, maze, file_path):
    global agent

    agent = lookup

    gamma = 0.975
    epsilon = 1

    for i in range(epochs):
        init_gridworld(random_player, random_mines, maze)
        state = grid_world.states[0]
        status = 1
        step = 0
        # while game still in progress
        while(status == 1):
            # State Hash Berechnung in eine Methode get_state_hash_string(state)
            state_hash = get_state_hash_string(state)

            if state_hash not in lookup.keys():
                lookup[state_hash] = [0, 0, 0, 0]
            qval = lookup[state_hash]
            if (np.random.random(1) < epsilon): # choose random action
                action = np.random.randint(0, 4)
            else: # choose best action from Q(s,a) values
                action = (np.argmax(qval))
            # Take action, observe new state S'
            new_state = grid_world.make_move(state, action)
            new_state_hash = get_state_hash_string(new_state)
            if new_state_hash not in lookup.keys():
                lookup[new_state_hash] = [0, 0, 0, 0]
            newQ = lookup[new_state_hash]
            maxQ = np.max(newQ)
            # Observe reward
            reward = grid_world.getReward(new_state, step)
            if reward not in [10, -10]:  # non-terminal state
                update = (reward + (gamma * maxQ))
            else:  # terminal state
                update = reward
            y = qval[:]
            y[action] = update
            if i % 100 == 0:
                print('Game {0}, action {1}, reward {2}'.format(i, action, reward))
            lookup[str(state_hash)] = y[:]
            state = np.copy(new_state)
            if reward in [10, -10]:
                status = 0
                if i%100==0:
                    with open(file_path, 'w') as f:
                        json.dump(lookup, f)
                    zeigen()
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
    status = 1
    while status == 1:
        state_hash = get_state_hash_string(state)
        if state_hash not in lookup.keys():
            print('taking random action...')
            action = np.random.randint(0, 4)
        else:
            qval = lookup[state_hash]
            print('taking lookup action...')
            action = np.argmax(qval)
        print('Move %s; Taking action: %s' % (step+1, action))
        new_state = grid_world.make_move(state, action)
        reward = grid_world.getReward(new_state, step)
        solution.append(action)
        print("Reward: %s" % (reward,))
        if reward in [10, -10]:
            status = 0
            if reward == 10:
                win = True
        state = np.copy(new_state)
        step += 1
        if step > 50:
            print("Game lost; too many moves.")
            break
    return win, solution


def get_q_values_from_lookup(lookup, state, pos):
    '''
    Used for visualization of vector field.
    '''
    state_copy = copy.deepcopy(state)
    player_loc = grid_world.getLoc(state_copy, 3)
    state_copy[player_loc][3] = 0
    state_copy[pos[1], pos[0]][3] = 1

    state_hash = get_state_hash_string(state_copy)
    if state_hash not in lookup.keys():
        lookup[state_hash] = [0, 0, 0, 0]
    qval = lookup[state_hash]

    return qval
