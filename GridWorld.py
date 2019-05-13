import numpy as np
from Visualizer import visualize


class GridWorld():
    def __init__(self, random_player=False, random_mines=False, maze=False):
        self.grid_x = 10
        self.grid_y = 10

        self.states = list()
        self.states.append(self.initGrid(random_player, random_mines, maze))

    def randPair(s, e):
        return np.random.randint(s, e), np.random.randint(s, e)


    # finds an array in the "depth" dimension of the grid
    def findLoc(self, state, obj):
        locs = []
        for i in range(0, self.grid_x):
            for j in range(0, self.grid_y):
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
    def initGrid(self, random_player=False, random_mines=False, maze=False):
        state = np.zeros((self.grid_x, self.grid_y, 4))
        # place player
        if random_player:
            state[np.random.randint(0, self.grid_x), np.random.randint(0, self.grid_y)] = np.array([0, 0, 0, 1])
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
            state[np.random.randint(1, self.grid_x, 6), np.random.randint(1, 6, 6)] = np.array([0, 1, 0, 0])
        else:
            state[[2, 4, 6, 1, 1, 2], [1, 2, 3, 5, 3, 4]] = np.array([0, 1, 0, 0])
        # place goal
        state[self.grid_x-1, self.grid_y-1] = np.array([1, 0, 0, 0])

        p = self.findLoc(state, np.array([0, 0, 0, 1]))
        if not p:
            return self.initGrid(random_player, random_mines, maze)

        return state



    def make_move(self, state, action):
        # need to locate player in grid
        # need to determine what object (if any) is in the new grid spot the player is moving to
        player_loc = self.findLoc(state, np.array([0, 0, 0, 1]))
        death_loc = self.findLoc(state, np.array([0, 1, 0, 1]))
        walls = self.findLoc(state, np.array([0, 0, 1, 0]))
        goal = self.findLoc(state, np.array([1, 0, 0, 0]))
        mines = self.findLoc(state, np.array([0, 1, 0, 0]))
        death_flag = False
        if len(player_loc) == 0:
            player_loc = death_loc
            death_flag = True

        if not death_flag:
            state = np.zeros((self.grid_x, self.grid_y, 4))
            # up (row - 1)
            if action == 0:
                # make move
                new_loc = (player_loc[0] - 1, player_loc[1])
                # force movement within the grid world
                if (new_loc not in walls):
                    if ((np.array(new_loc) <= (self.grid_x-1, self.grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                        state[new_loc][3] = 1

            # down (row + 1)
            elif action == 1:
                new_loc = (player_loc[0] + 1, player_loc[1])
                if (new_loc not in walls):
                    if ((np.array(new_loc) <= (self.grid_x-1, self.grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                        state[new_loc][3] = 1

            # left (column - 1)
            elif action == 2:
                new_loc = (player_loc[0], player_loc[1] - 1)
                if (new_loc not in walls):
                    if ((np.array(new_loc) <= (self.grid_x-1, self.grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                        state[new_loc][3] = 1

            # right (column + 1)
            elif action == 3:
                new_loc = (player_loc[0], player_loc[1] + 1)
                if (new_loc not in walls):
                    if ((np.array(new_loc) <= (self.grid_x-1, self.grid_y-1)).all() and (np.array(new_loc) >= (0, 0)).all()):
                        state[new_loc][3] = 1

            new_player_loc = self.findLoc(state, np.array([0, 0, 0, 1]))
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
    def getLoc(self, state, level):
        locs = []
        for i in range(0, self.grid_x):
            for j in range(0, self.grid_y):
                if (state[i,j][level] == 1):
                    locs.append((i, j))
        if len(locs) == 1:
            return locs[0]
        else:
            return locs


    def getReward(self, state):
        player_loc = self.getLoc(state, 3)
        mines = self.getLoc(state, 1)
        goal = self.getLoc(state, 0)
        if (player_loc in mines):
            return -10
        elif (player_loc == goal):
            return 10
        else:
            return -1


    # display GridWorld
    def dispGrid(self, state):
        grid = np.zeros((self.grid_x, self.grid_y), dtype=np.unicode_)
        player_loc = self.findLoc(state, np.array([0, 0, 0, 1]))
        walls = self.findLoc(state, np.array([0, 0, 1, 0]))
        goal = self.findLoc(state, np.array([1, 0, 0, 0]))
        mines = self.findLoc(state, np.array([0, 1, 0, 0]))
        death = self.findLoc(state, np.array([0, 1, 0, 1]))
        for i in range(0, self.grid_x):
            for j in range(0, self.grid_y):
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
        if death:
            grid[goal] = 'D' # goal

        return grid


    def zeigen(self):
        visualize(self.states)
