from RL_Agent_Lookup_Reduced.Agent import train_agent, test_agent, zeigen
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


def train_new_agent():
    file_path = 'lookup_new.json'
    try:
        with open(file_path, 'r') as f:
            lookup = json.load(f)
    except:
        print('Failed to load, making new lookup.')
        lookup = dict()
    train_agent(2010, lookup, random_player, random_mines, maze, file_path)
    with open(file_path, 'w') as f:
        json.dump(lookup, f)


def check_new_agent():
    file_path = 'lookup_new.json'
    with open(file_path, 'r') as f:
        lookup = json.load(f)

    wins = 0
    for _ in range(2):
        win, sol = test_agent(lookup, random_player, random_mines, maze)
        wins += win
        zeigen(pause=0.2)
    print('achieved', wins, 'wins')


def check_good_agent():
    file_path = 'lookup_trained.json'
    with open(file_path, 'r') as f:
        lookup = json.load(f)

    wins = 0
    for _ in range(20):
        win, sol = test_agent(lookup, random_player, random_mines, maze)
        wins += win
        zeigen(pause=0.5)
    print('achieved', wins, 'wins')




'''
Experimente - Beginn
'''

''' Schwierigkeit, 0, 1, 2 moeglich'''
difficulty = 2

random_player, random_mines, maze = set_difficulty(difficulty)

'''Trainiere deinen Agenten'''
#train_new_agent()

'''Teste deinen Agenten'''
# check_new_agent()


'''Teste guten Agenten'''
check_good_agent()


'''
Experimente - Ende
'''