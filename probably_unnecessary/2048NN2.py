import gym_2048
import gym
import numpy as np
from actor_critic import Agent
from gym import wrappers

if __name__ == '__main__':
    env = gym.make('2048-v0')
    agent = Agent(alpha=1e-5, n_actions=env.action_space.n)
    n_games = 1800

    best_score = env.reward_range[0]
    score_history = []

    for i in range(n_games):
        observation = env.reset()
        done = False
        score = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            observation = observation_
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score

        print('episode ', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score)





