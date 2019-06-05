from RL_Agent_Lookup_Big.Agent import train_agent, test_agent, zeigen
import json

def set_difficulty(dif):
    if dif == 0:
        return False, False, False
    elif dif == 1:
        return True, False, False
    elif dif == 2:
        return True, True, False
    elif dif == 3:
        return True, True, True
    else:
        return False, False, False


flag_train_agent = False
flag_test_agent = True

difficulty = 1
random_player, random_mines, maze = set_difficulty(difficulty)


file_path = f'lookup_difficulty_{difficulty}.json'

for x in range(5):
    if flag_train_agent:
        try:
            with open(file_path, 'r') as f:
                lookup = json.load(f)
        except:
            print('Failed to load, making new lookup.')
            lookup = dict()
        train_agent(3000, lookup, random_player, random_mines, maze)
        with open(file_path, 'w') as f:
            json.dump(lookup, f)

    if flag_test_agent:
        with open(file_path, 'r') as f:
            lookup = json.load(f)

        wins = 0
        for _ in range(10):
            win, sol = test_agent(lookup, random_player, random_mines, maze)
            wins += win
            zeigen()
        print('achieved', wins, 'wins')
