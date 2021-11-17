import numpy as np
import gym
import gym_2048
import random
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter

learningRate = 1e-3


#Will need to change these for 2048
goal_score = 500
score_required = 50
initial_games = 10

#get initial random data
def initial_population():
    training_data = []
    scores = []
    accepted_scores = []

    for _ in range(initial_games):
        env = gym.make('2048-v0')
        env.reset()
        env.render()
        done = False
        moves = 0
        while not done:
            action = env.np_random.choice(range(4), 1).item()
            next_state, reward, done, info = env.step(action)
            moves += 1

            print('Next Action: "{}"\n\nReward: {}'.format(
            gym_2048.Base2048Env.ACTION_STRING[action], reward))
            env.render()

        print('\nTotal Moves: {}'.format(moves))

    #training_data_save = np.array(training_data) ### current error
    #np.save('saved.npy', training_data_save)

    print('Average Accepted Score: ', mean(accepted_scores))
    print('Median Accepted Score: ', median(accepted_scores))
    print(Counter(accepted_scores))

    return training_data


#Create a NN model using tensorflow and tflearn
def neuralNetworkModel(input_size):
    #input layer
    network = input_data(shape=[None, input_size, 1], name='input')

    #5 layers
    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    #change 2 to 4 for 2048?
    network = fully_connected(network, 2, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=learningRate,
                         loss='categorical_crossentropy', name='targets')
    
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model

def train_model(trainingData, model=False):
    X = np.array([i[0] for i in trainingData]).reshape(-1, len(trainingData[0][0]), 1)
    Y = [i[1] for i in trainingData]

    if not model:
        model = neuralNetworkModel(input_size = len(X[0]))

    model.fit({'input':X}, {'targets':Y}, n_epoch=5, snapshot_step=500, show_metric=True, run_id='openaistuff')

    return model

trainingData = initial_population()
model = train_model(trainingData)

scores = []
choices = []

for eachGame in range(10):
    score = 0
    game_memory = []
    prev_obs = []
    env.reset() #reset the game
    env.render()
    done = False
    moves = 0

    while not done:
        action = env.np_random.choice(range(4), 1).item()
        next_state, reward, done, info = env.step(action)
        moves += 1

        print('Next Action: "{}"\n\nReward: {}'.format(
        gym_2048.Base2048Env.ACTION_STRING[action], reward))
        env.render()

   #print('\nTotal Moves: {}'.format(moves))

#print("average score: ", sum(scores)/len(scores))
#print("Choice 1: {}, Choice 2: {}".format(choices.count(1)/len(choices), choices.count(0)/len(choices)))
