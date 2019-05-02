import json
import hashlib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

grid_x = 10
grid_y = 10


def randPair(s, e):
    return np.random.randint(s, e), np.random.randint(s, e)


# finds an array in the "depth" dimension of the grid
def findLoc(state, obj):
    locs = []
    for i in range(0, grid_x):
        for j in range(0, grid_y):
            if (state[i, j] == obj).all():
                locs.append((i, j))
    if len(locs) == 1:
        return locs[0]
    else:
        return locs


# Initialize stationary grid, all items are placed deterministically.
# state is a XxYx4 Matrix; The first two entries correspond to the grid coordinates.
# the last entry corresponds to whether the grid position contains the player, a wall, a mine or the goal.
# Initialize player in random location, but keep wall, goal and mine stationary
def initGrid(random_player=False, random_mines=False, maze=False):
    state = np.zeros((grid_x, grid_y, 4))
    # place player
    if random_player:
        state[np.random.randint(0, grid_x), np.random.randint(0, grid_y)] = np.array([0, 0, 0, 1])
    else:
        state[0, 0] = np.array([0, 0, 0, 1])
    # place walls
    if maze:
        state[[0, 2, 3, 4, 5, 6, 7, 8, 9], [8, 8, 8, 8, 8, 8, 8, 8, 8]] = np.array([0, 0, 1, 0])
        state[[0, 1, 2, 3, 4, 5, 6, 7, 9], [6, 6, 6, 6, 6, 6, 6, 6, 6]] = np.array([0, 0, 1, 0])
    else:
        state[[8, 8, 7], [7, 8, 8]] = np.array([0, 0, 1, 0])
    # place mines
    if random_mines:
        state[np.random.randint(1, grid_x, 6), np.random.randint(1, 6, 6)] = np.array([0, 1, 0, 0])
    else:
        state[[2, 4, 6, 1, 1, 2], [1, 2, 3, 5, 3, 4]] = np.array([0, 1, 0, 0])
    # place goal
    state[grid_x-1, grid_y-1] = np.array([1, 0, 0, 0])

    p = findLoc(state, np.array([0, 0, 0, 1]))
    if not p:
        return initGrid(random_player, random_mines, maze)

    return state


def make_move(state, action):
    # need to locate player in grid
    # need to determine what object (if any) is in the new grid spot the player is moving to
    player_loc = findLoc(state, np.array([0, 0, 0, 1]))
    walls = findLoc(state, np.array([0, 0, 1, 0]))
    goal = findLoc(state, np.array([1, 0, 0, 0]))
    mines = findLoc(state, np.array([0, 1, 0, 0]))
    state = np.zeros((grid_x, grid_y, 4))

    # up (row - 1)
    if action == 0:
        # make move
        new_loc = (player_loc[0] - 1, player_loc[1])
        # force movement within the grid world
        if (new_loc not in walls):
            if ((np.array(new_loc) <= (grid_x-1, grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                state[new_loc][3] = 1

    # down (row + 1)
    elif action == 1:
        new_loc = (player_loc[0] + 1, player_loc[1])
        if (new_loc not in walls):
            if ((np.array(new_loc) <= (grid_x-1, grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                state[new_loc][3] = 1

    # left (column - 1)
    elif action == 2:
        new_loc = (player_loc[0], player_loc[1] - 1)
        if (new_loc not in walls):
            if ((np.array(new_loc) <= (grid_x-1, grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                state[new_loc][3] = 1

    # right (column + 1)
    elif action == 3:
        new_loc = (player_loc[0], player_loc[1] + 1)
        if (new_loc not in walls):
            if ((np.array(new_loc) <= (grid_x-1, grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                state[new_loc][3] = 1

    new_player_loc = findLoc(state, np.array([0, 0, 0, 1]))
    if (not new_player_loc):
        state[player_loc] = np.array([0, 0, 0, 1])

    # re-place mine
    for i_mine in mines:
        state[i_mine][1] = 1
    # re-place wall
    for i_wall in walls:
        state[i_wall][2] = 1
    # re-place goal
    state[goal][0] = 1

    return state


# this function finds superpositions of objects
def getLoc(state, level):
    locs = []
    for i in range(0, grid_x):
        for j in range(0, grid_y):
            if (state[i,j][level] == 1):
                locs.append((i, j))
    if len(locs) == 1:
        return locs[0]
    else:
        return locs


def getReward(state):
    player_loc = getLoc(state, 3)
    mines = getLoc(state, 1)
    goal = getLoc(state, 0)
    if (player_loc in mines):
        return -10
    elif (player_loc == goal):
        return 10
    else:
        return -1


# display GridWorld
def dispGrid(state):
    grid = np.zeros((grid_x, grid_y), dtype=np.unicode_)
    player_loc = findLoc(state, np.array([0, 0, 0, 1]))
    walls = findLoc(state, np.array([0, 0, 1, 0]))
    goal = findLoc(state, np.array([1, 0, 0, 0]))
    mines = findLoc(state, np.array([0, 1, 0, 0]))
    for i in range(0, grid_x):
        for j in range(0, grid_y):
            grid[i, j] = ' '

    if player_loc:
        grid[player_loc] = 'P' # player
    if walls:
        for i_wall in walls:
            grid[i_wall] = 'W' # wall
    if goal:
        grid[goal] = 'G' # goal
    if mines:
        for i_mine in mines:
            grid[i_mine] = 'X' # mine

    return grid


def train_agent(epochs, lookup, random_player, random_mines, maze):
    gamma = 0.975
    epsilon = 1
    for i in range(epochs):
        state = initGrid(random_player, random_mines, maze)
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
            new_state = make_move(state, action)
            new_state.flags.writeable = False
            new_state_hash = str(hashlib.md5(bytes(new_state)).hexdigest())
            new_state.flags.writeable = True
            if new_state_hash not in lookup.keys():
                lookup[new_state_hash] = [0, 0, 0, 0]
            newQ = lookup[new_state_hash]
            maxQ = np.max(newQ)
            # Observe reward
            reward = getReward(new_state)
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
            if reward in [10, -10] or step > 50:
                status = 0
        if epsilon > 0.1:
            epsilon -= (1/epochs)


def test_agent(lookup, random_player, random_mines, maze):
    win = False
    solution = []
    step = 0
    state = initGrid(random_player, random_mines, maze)
    print(dispGrid(state))
    status = 1
    while status == 1:
        state.flags.writeable = False
        state_hash = str(hashlib.md5(bytes(state)).hexdigest())
        state.flags.writeable = True
        if state_hash not in lookup.keys():
            print('taking random action...')
            action = np.random.randint(0, 4)
        else:
            qval = lookup[state_hash]
            action = np.argmax(qval)
        print('Move %s; Taking action: %s' % (step+1, action))
        new_state = make_move(state, action)
        reward = getReward(new_state)
        print(dispGrid(new_state))
        solution.append(action)
        print("Reward: %s" % (reward,))
        if reward in [10, -10,]:
            status = 0
            if reward == 10:
                win = True
        state = np.copy(new_state)
        step += 1
        if step > 50:
            print("Game lost; too many moves.")
            break
    return win, solution


if __name__ == '__main__':

    flag_train_agent = False
    flag_test_agent = True

    # difficulty
    random_player = False
    random_mines = True
    maze=True

    if flag_train_agent:
        lookup = dict()
        train_agent(5000, lookup, random_player, random_mines, maze)
        with open('lookup.json', 'w') as f:
            json.dump(lookup, f)

    if flag_test_agent:
        with open('lookup.json', 'r') as f:
            lookup = json.load(f)

        wins = 0
        for _ in range(1):
            win, sol = test_agent(lookup, random_player, random_mines, maze)
            wins += win
        print('achieved', wins, 'wins')