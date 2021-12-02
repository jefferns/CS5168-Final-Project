import os
import gym_2048
import gym
import numpy as np
from actor_critic import Agent
from gym import wrappers
import matplotlib.pyplot as plt


CHILD_COUNT = 10
GAME_COUNT = 1000


def plot_learning_curve(x, scores, figure_file):
    running_avg = np.zeros(len(scores))
    for i in range(len(running_avg)):
        running_avg[i] = np.mean(scores[max(0, i-100):(i+1)])
    plt.plot(x, running_avg)
    plt.title('Running average of previous 100 scores')
    plt.savefig(figure_file)

pid_list = []
pid = 0
for _ in range(CHILD_COUNT):
    if pid == 0:
        n = os.fork()
        pid = os.getpid()
        pid_list += [pid]
    else:
        break

if pid > 0:
    # ONLY CHILDREN RUN HERE
    print(f"Child #{pid} starting...")
    env = gym.make('2048-v0')
    agent = Agent(alpha=1e-5, n_actions=env.action_space.n)
    n_games = GAME_COUNT
    filename = '2048_plot_'+str(pid)+'.png'
    figure_file = './plots/'+filename

    best_score = env.reward_range[0]
    score_history = []

    for i in range(n_games // CHILD_COUNT):
        observation = env.reset()
        done = False
        score = 0
        while not done:
            action = agent.choose_action(observation)            
            observation_, reward, done, info = env.step(sum(action)%4)
            score += reward
            observation = observation_
            output = open('./outputs/'+str(pid)+'.txt', 'w')
            output.write(score)
            output.close()

        # print('episode ', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score)

    x = [i+1 for i in range(n_games)]
    plot_learning_curve(x, score_history, figure_file)
    
    print(f"Child #{pid} stopping...")
    exit(1)


else:
    os.wait()
    #ONLY PARENT RUNS HERE
    score_history = []
    for pid in pid_list:
        file = open('./outputs/'+str(pid)+'.txt', 'r')
        for line in file:
            score_history.append(line)

    best_score = 0
    avg_score = np.mean(score_history[-100:])
    if avg_score > best_score:
        best_score = avg_score

    print("\nBest score was ", best_score)
