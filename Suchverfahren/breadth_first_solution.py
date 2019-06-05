from Aktionen import bewege_links, bewege_oben, bewege_rechts, bewege_unten
from Aktionen import inhalt, init_gridworld, spieler_position
import numpy as np
from matplotlib import pyplot as plt
import copy
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Bewege dich in alle Richtungen von x/y, falls moeglich
# Wenn Ziel erreicht sein sollte, gib True zurueck
def fortschritt(x, y):
    global punkte, welten
    umgebung = []
    aktuelle_welt = copy.deepcopy(welten[len(welten) - 1])
    for rg in richtungen:
        umgebung.append(inhalt( x+rg[0], y+rg[1]))

    for rg, inh in zip(richtungen, umgebung):
        new_x, new_y = x+rg[0], y+rg[1]
        if inh == 'Frei' and [new_x, new_y] not in punkte:
            punkte.append([new_x, new_y])
            aktuelle_welt[new_y][new_x] = np.array([0, 1, 1, 0])
        if inh == 'Ziel':
            punkte.append([new_x, new_y])
            return True
    welten.append(aktuelle_welt)
    return False



def verbunden(punkt_1, punkt_2):
    delta_x = abs(punkt_1[0] - punkt_2[0])
    delta_y = abs(punkt_1[1] - punkt_2[1])

    if delta_x > 1 or delta_y > 1:
        return False
    elif delta_x == delta_y:
        return False
    else:
        return True

def welche_bewegung(p1, p2):
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]

    bewegung = richtungen.index([delta_x, delta_y])
    return bewegung

def zeigen(states):

    grid_states = []
    positions = []
    alle_besuchte = []
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
        besuchte = []
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
                elif state_x == 'B' or (state_x == np.array([0, 1, 1, 0])).all():
                    grid_x = [0.0, 0.75, 0.5]
                    besuchte.append([id_x, id_y])
                else:
                    grid_x = [0.0, 1.0, 0.0]
                grid_y.append(grid_x)
            grid.append(grid_y)
        grid_states.append(grid)
        positions.append(pos)
        deaths.append(dead)
        state_mines.append(mines)
        state_walls.append(walls)
        alle_besuchte.append(besuchte)

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    sm = 0
    sw = 0
    sb = 0
    movement = 0
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
        for besucht in alle_besuchte[sb]:
            ax.text(besucht[0], besucht[1], 'B', va='center', ha='center', fontsize=30, color='w')
        if dead:
            ax.text(pos[0], pos[1], 'T', va='center', ha='center', fontsize=30, color='w')
        else:
            ax.text(pos[0], pos[1], 'S', va='center', ha='center', fontsize=30, color='w')

        if movement == 0:
            plt.pause(3) # Erste Position lange anzeigen
            movement = 1
        else:
            plt.pause(0.1)
        sm += 1
        sw += 1
        sb += 1

    plt.close()


if __name__ == '__main__':
    random_player = True
    random_mines = True
    maze = True

    grid_world = init_gridworld(random_player, random_mines, maze)
    welt = grid_world.states[0]
    welten = [welt]

    sx, sy = spieler_position()

    punkte = []
    punkte.append([sx, sy])

    richtungen = [[0, -1], [0, 1], [-1, 0], [1, 0]]

    # Breitensuche
    fertig = False
    while not fertig:
        for x, y in punkte:
            fertig = fortschritt(x, y)
            if fertig:
                break

    # Suche den Pfad, angefangen vom Ziel aus
    punkte.reverse()
    pfad = []
    pfad_bewegungen = []

    pfad.append(punkte[0])

    punkt_checkpoint = punkte[0]
    for i in range(len(punkte)-1):
        if verbunden(punkt_checkpoint, punkte[i+1]):
            pfad.append(punkte[i+1])
            punkt_checkpoint = punkte[i+1]

    pfad.reverse()


    # Bewege Spieler entlang des Pfades und zeige Spielwelt an
    for i in range(len(pfad)-1):
        pfad_bewegungen.append(welche_bewegung(pfad[i], pfad[i+1]))

    for bew in pfad_bewegungen:
        if bew == 0:
            bewege_oben()
        if bew == 1:
            bewege_unten()
        if bew == 2:
            bewege_links()
        if bew == 3:
            bewege_rechts()

    alle_welte = np.concatenate([np.asarray(welten), grid_world.states])
    zeigen(alle_welte)
