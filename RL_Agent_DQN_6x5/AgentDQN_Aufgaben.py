import hashlib
import json
from GridWorld import GridWorld
import numpy as np
import copy

from matplotlib import pyplot as plt

import torch
from torch.nn.modules.loss import SmoothL1Loss
import torch.nn as nn
from torch.optim import Adam
import random

grid_world = GridWorld()

rewards_to_plot = []
stats_ax = None
rewards_ax = None
model = None


def init_gridworld(random_player=False, random_mines=False, maze=False):
    global grid_world
    grid_world = GridWorld(random_player, random_mines, maze)


class NeuralNetwork(nn.Module):

    def __init__(self, iterations=500):
        super(NeuralNetwork, self).__init__()

        self.number_of_actions = 4
        self.gamma = 0.99
        self.final_epsilon = 0.001
        self.initial_epsilon = 0.5
        self.number_of_iterations = iterations
        self.replay_memory_size = 30000
        self.minibatch_size = 100

        self.fc1 = nn.Linear(120, 64)
        self.relu1 = nn.ReLU(inplace=True)
        self.fc2 = nn.Linear(64, 16)
        self.relu2 = nn.ReLU(inplace=True)
        self.fc3 = nn.Linear(16, 4)

    def forward(self, x):
        x = x.contiguous()
        x = x.view(x.size()[0], -1)

        out = self.fc1(x)
        out = self.relu1(out)
        out = self.fc2(out)
        out = self.relu2(out)
        out = self.fc3(out)

        return out


def state_to_tensor(state):
    state_tensor = torch.Tensor(state).unsqueeze(0)
    state_tensor_t = torch.transpose(state_tensor, 1, 2)
    state_tensor_t = torch.transpose(state_tensor_t, 1, 3)
    return state_tensor_t


def frame_step(action, iteration):
    action_index = torch.argmax(action)
    state_data = grid_world.make_move(grid_world.states[-1], action_index)
    reward = grid_world.getReward(state_data, iteration)

    if reward in [10, -10]:
        terminal = True
    else:
        terminal = False

    add_reward_to_plot(reward)
    state = state_to_tensor(state_data)

    action = action.unsqueeze(0)
    reward = torch.from_numpy(np.array([reward], dtype=np.float32)).unsqueeze(0)

    return state, action, reward, terminal


def init_plotting():
    global stats_ax, rewards_ax
    fig, ax = plt.subplots(1, 2)
    stats_ax = ax[0]
    rewards_ax = ax[1]


def add_reward_to_plot(reward):
    global rewards_to_plot
    rewards_to_plot.append(reward)


def plot_stats():
    global rewards_to_plot

    stats_ax.cla()
    rewards_ax.cla()

    len_rewards = len(rewards_to_plot)
    if len_rewards > 100:
        rewards_ax.plot(rewards_to_plot[len_rewards - 100:len_rewards])
    else:
        rewards_ax.plot(rewards_to_plot)

    unique, counts = np.unique(rewards_to_plot, return_counts=True)

    statistics_to_plot = dict(zip(unique, counts))

    stats_ax.bar(range(len(statistics_to_plot)), list(statistics_to_plot.values()), align='center')
    stats_ax.set_xticks(range(len(list(statistics_to_plot.keys()))))
    stats_ax.set_xticklabels(list(statistics_to_plot.keys()))

    if -0.25 not in statistics_to_plot.keys():
        statistics_to_plot[-0.25] = 0
    if -10 not in statistics_to_plot.keys():
        statistics_to_plot[-10] = 0
    if 10 not in statistics_to_plot.keys():
        statistics_to_plot[10] = 0

    stats_ax.set_title('Stats -0.25: {} -10: {} 10: {}'.format(statistics_to_plot[-0.25],
                                                               statistics_to_plot[-10],
                                                               statistics_to_plot[10]))
    rewards_ax.set_title('Rewards')

    plt.pause(0.00005)


def q_values_aus_netz(model, state, pos):
    state_copy = copy.deepcopy(state)
    player_loc = grid_world.getLoc(state_copy, 3)
    state_copy[player_loc][3] = 0
    state_copy[pos[1], pos[0]][3] = 1

    state_copy = state_to_tensor(state_copy)

    qval = model(state_copy)[0]

    return qval.detach().numpy()


def zeigen():
    global model
    if model is not None:
        vis_net = copy.deepcopy(model)
        grid_world.zeigen(agent=vis_net, agent_type='net')


def initialization(model):
    action = torch.zeros([model.number_of_actions], dtype=torch.float32)
    action[1] = 1
    state, action, reward, terminal = frame_step(action, 0)
    epsilon = model.initial_epsilon

    return action, state, epsilon


def generate_batch_and_update_memory(replay_memory, state, action, reward, state_next, terminal):
    replay_memory.append((state, action, reward, state_next, terminal))

    if len(replay_memory) > model.replay_memory_size:
        replay_memory.pop(0)

    minibatch = random.sample(replay_memory, min(len(replay_memory), model.minibatch_size))

    state_batch = torch.cat(tuple(d[0] for d in minibatch))
    action_batch = torch.cat(tuple(d[1] for d in minibatch))
    reward_batch = torch.cat(tuple(d[2] for d in minibatch))
    state_next_batch = torch.cat(tuple(d[3] for d in minibatch))

    if torch.cuda.is_available():
        state_batch = state_batch.cuda()
        action_batch = action_batch.cuda()
        reward_batch = reward_batch.cuda()
        state_next_batch = state_next_batch.cuda()

    return state_batch, action_batch, reward_batch, state_next_batch, minibatch


def agent(random_player, random_mines, maze, train=False, load_model=None, save_model=None):
    global model

    init_plotting()

    if train:
        if model is None:
            model = NeuralNetwork()
    else:
        if model is None:
            model = NeuralNetwork(iterations=20)
        else:
            model.number_of_iterations = 10

    if load_model is not None:
        model.load_state_dict(torch.load(load_model))

    init_gridworld(random_player, random_mines, maze)

    optimizer = Adam(model.parameters(), lr=0.001)
    criterion = SmoothL1Loss()

    replay_memory = []

    action, state, epsilon = initialization(model)

    iteration = 1
    steps = 1

    while iteration < model.number_of_iterations:
        print('------------------ Iteration: {} ------------------'.format(iteration))

        if torch.cuda.is_available():
            action_index = action_index.cuda()

        output = model(state)[0]

        # Aufgabe: Get Action Index
        # -----------------------Musterloesung----------------------------









        # -----------------------------------------------------------------

        action[action_index] = 1

        state_next, action, reward, terminal = frame_step(action, steps)

        if train:
            state_batch, action_batch, reward_batch, state_next_batch, minibatch = generate_batch_and_update_memory(
                replay_memory,
                state,
                action,
                reward,
                state_next,
                terminal)

            if epsilon > 0.1:
                epsilon -= (1 / model.number_of_iterations)

            # Aufgabe: ANN training
            # -----------------------Musterloesung----------------------------









            # -----------------------------------------------------------------

        state = state_next

        print('step: {}\naction: {}\nreward: {}\n'.format(steps, action_index.detach().cpu().numpy().item(), reward))
        steps += 1

        if terminal:
            if train:
                interval_achieved = iteration % 10 == 0
            else:
                interval_achieved = iteration % 1 == 0
            if interval_achieved:
                zeigen()
                plot_stats()
            init_gridworld(random_player, random_mines, maze)
            iteration += 1
            steps = 0

    if save_model is not None:
        torch.save(model.state_dict(), save_model)


if __name__ == "__main__":
    random_player = True
    random_mines = True
    maze = True

    agent(random_player, random_mines, maze, train=True, load_model='dqn_model.torch')
    agent(random_player, random_mines, maze, load_model='dqn_model.torch')
