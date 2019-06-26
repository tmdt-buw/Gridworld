# from Regler import ist_rechts_frei, ist_links_frei, ist_unten_frei, ist_oben_frei
# from Regler import inhalt_rechts, inhalt_links, inhalt_unten, inhalt_oben
# from Regler import bewege_links, bewege_oben, bewege_rechts, bewege_unten
# from Regler import inhalt, init_gridworld, zeigen, wenn_dann

from Agent import train_agent, test_agent, zeigen
import json


flag_train_agent = False
flag_test_agent = True

# difficulty
random_player = True
random_mines = False
maze = False

file_path = 'lookup_6x5.json'

if flag_train_agent:
    try:
        with open(file_path, 'r') as f:
            lookup = json.load(f)
    except:
        print('Failed to load, making new lookup.')
        lookup = dict()
    train_agent(10000, lookup, random_player, random_mines, maze, file_path)
    with open(file_path, 'w') as f:
        json.dump(lookup, f)

if flag_test_agent:
    with open(file_path, 'r') as f:
        lookup = json.load(f)

    wins = 0
    for _ in range(20):
        win, sol = test_agent(lookup, random_player, random_mines, maze)
        wins += win
        zeigen()
    print('achieved', wins, 'wins')
