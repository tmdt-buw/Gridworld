from GridWorld import GridWorld

grid_world = GridWorld()

def init_gridworld(random_player=False, random_mines=False, maze=False):
    global grid_world, zeigen
    grid_world = GridWorld(random_player, random_mines, maze)

def zeigen():
    grid_world.zeigen()

def bewege_oben():
    grid_world.states.append(grid_world.make_move(grid_world.states[len(grid_world.states)-1], 0))

def bewege_unten():
    grid_world.states.append(grid_world.make_move(grid_world.states[len(grid_world.states)-1], 1))

def bewege_links():
    grid_world.states.append(grid_world.make_move(grid_world.states[len(grid_world.states)-1], 2))

def bewege_rechts():
    grid_world.states.append(grid_world.make_move(grid_world.states[len(grid_world.states)-1], 3))

def inhalt(x, y):
    last_state = grid_world.states[len(grid_world.states)-1]
    type = last_state[y, x]

    if type == 'P' or (type == [0, 0, 0, 1]).all():
        return 'Spieler'
    elif type == 'X' or (type == [0, 1, 0, 0]).all():
        return 'Mine'
    elif type == 'W' or (type == [0, 0, 1, 0]).all():
        return 'Wand'
    elif type == 'G' or (type == [1, 0, 0, 0]).all():
        return 'Ziel'
    elif type == 'D' or (type == [0, 1, 0, 1]).all():
        return 'Tot'
    else:
        return 'Frei'

def spieler_position():
    last_state = grid_world.states[len(grid_world.states) - 1]
    loc = grid_world.getLoc(last_state, 3)
    return loc[1] , loc[0]

def inhalt_oben():
    position = spieler_position()
    x = position[0]
    y = position[1] - 1

    if x>=0 and y>=0 and x<=grid_world.grid_x-1 and y<=grid_world.grid_y-1:
        inh = inhalt(x, y)
        return inh
    else:
        return 'A'

def inhalt_unten():
    position = spieler_position()
    x = position[0]
    y = position[1] + 1

    if x >= 0 and y >= 0 and x <= grid_world.grid_x-1 and y <= grid_world.grid_y-1:
        inh = inhalt(x, y)
        return inh
    else:
        return 'A'

def inhalt_links():
    position = spieler_position()
    x = position[0] - 1
    y = position[1]

    if x >= 0 and y >= 0 and x <= grid_world.grid_x-1 and y <= grid_world.grid_y-1:
        inh = inhalt(x, y)
        return inh
    else:
        return 'A'

def inhalt_rechts():
    position = spieler_position()
    x = position[0] + 1
    y = position[1]

    if x >= 0 and y >= 0 and x <= grid_world.grid_x-1 and y <= grid_world.grid_y-1:
        inh = inhalt(x, y)
        return inh
    else:
        return 'A'

def ist_oben_frei():
    inh = inhalt_oben()
    if inh == 'Frei':
        return True
    else:
        return False

def ist_unten_frei():
    inh = inhalt_unten()
    if inh == 'Frei':
        return True
    else:
        return False

def ist_links_frei():
    inh = inhalt_links()
    if inh == 'Frei':
        return True
    else:
        return False

def ist_rechts_frei():
    inh = inhalt_rechts()
    if inh == 'Frei':
        return True
    else:
        return False

def wenn_dann(bedingung, action):
    if bedingung():
        action()
        return True
    else:
        return False