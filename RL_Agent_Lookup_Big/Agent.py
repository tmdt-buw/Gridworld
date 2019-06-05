import hashlib
from GridWorld import GridWorld
import numpy as np

grid_world = GridWorld()

def init_gridworld(random_player=False, random_mines=False, maze=False):
    global grid_world
    grid_world = GridWorld(random_player, random_mines, maze)

def zeigen():
    grid_world.zeigen()

def train_agent(epochs, lookup, random_player, random_mines, maze):
    gamma = 0.975
    epsilon = 1

    for i in range(epochs):
        init_gridworld(random_player, random_mines, maze)
        state = grid_world.states[0]
        status = 1
        step = 0
        # while game still in progress
        while(status == 1):
            state.flags.writeable = False
            state_hash = str(hashlib.md5(bytes(state)).hexdigest())
            state.flags.writeable = True
            if state_hash not in lookup.keys():
                lookup[state_hash] = [0, 0, 0, 0]
            qval = lookup[state_hash]
            if (np.random.random(1) < epsilon): # choose random action
                action = np.random.randint(0, 4)
            else: # choose best action from Q(s,a) values
                action = (np.argmax(qval))
            # Take action, observe new state S'
            new_state = grid_world.make_move(state, action)
            new_state.flags.writeable = False
            new_state_hash = str(hashlib.md5(bytes(new_state)).hexdigest())
            new_state.flags.writeable = True
            if new_state_hash not in lookup.keys():
                lookup[new_state_hash] = [0, 0, 0, 0]
            newQ = lookup[new_state_hash]
            maxQ = np.max(newQ)
            # Observe reward
            reward = grid_world.getReward(new_state)
            if reward not in [100, -50]:  # non-terminal state
                update = (reward + (gamma * maxQ))
            else:  # terminal state
                update = reward
            y = qval[:]
            y[action] = update
            if i % 100 == 0:
                print('Game {0}, action {1}, reward {2}'.format(i, action, reward))
            lookup[str(state_hash)] = y[:]
            state = np.copy(new_state)
            if reward in [100, -50] or step > 50:
                status = 0
                # if i % 500 == 0:
                #     zeigen()
        if epsilon > 0.1:
            epsilon -= (1/epochs)


def test_agent(lookup, random_player, random_mines, maze):
    win = False
    solution = []
    step = 0
    init_gridworld(random_player, random_mines, maze)
    state = grid_world.states[0]
    status = 1
    while status == 1:
        state.flags.writeable = False
        state_hash = str(hashlib.md5(bytes(state)).hexdigest())
        state.flags.writeable = True
        if state_hash not in lookup.keys():
            print('taking random action...')
            action = np.random.randint(0, 4)
        else:
            print('taking lookup action...')
            qval = lookup[state_hash]
            action = np.argmax(qval)
        print('Move %s; Taking action: %s' % (step+1, action))
        new_state = grid_world.make_move(state, action)
        reward = grid_world.getReward(new_state)
        print(len(grid_world.states))
        solution.append(action)
        print("Reward: %s" % (reward,))
        if reward in [100, -50]:
            status = 0
            if reward == 100:
                win = True
        state = np.copy(new_state)
        step += 1
        if step > 50:
            print("Game lost; too many moves.")
            break
    return win, solution
