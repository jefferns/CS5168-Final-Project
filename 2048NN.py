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

##env is the game environment
##This will be changed to 2048
env = gym.make("2048-v0")
env.reset()

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
        score = 0
        game_memory = []
        prev_observation = []

        for _ in range(goal_score):
            action = random.randrange(0,4) #will need to be (0,4) for 2048?
            game_data, reward, done, info = env.step(action) #controls the game

            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])

            prev_observation = game_data
            score += reward
            
            if done:
                break

        if score >= score_required:
            accepted_scores.append(score)

            for data in game_memory:
                if data[1] == 1:
                    output = [0,1,0,0]
                elif data[1] == 0:
                    output = [1,0,0,0]
                elif data[1] == 2:
                    output = [0,0,1,0]
                elif data[1] == 3:
                    output = [0,0,0,1]

                training_data.append([data[0], output])
        env.reset() #reset the game
        scores.append(score)

    training_data_save = np.array(training_data) ### current error
    np.save('saved.npy', training_data_save)

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

    for _ in range(goal_score):
        env.render() #show the game
        if len(prev_obs) == 0:
            action = random.randrange(0,4) #4
        else:
            action = np.argmax(model.predict(prev_obs.reshape(-1, len(prev_obs), 1))[0])

        choices.append(action)

        newObs, reward, done, info = env.step(action) #this is what gets the game info, will need to be chaged to fit 2048
        prev_obs = newObs
        game_memory.append([newObs, action])
        score += reward

        if done:
            break

    scores.append(score)

print("average score: ", sum(scores)/len(scores))
print("Choice 1: {}, Choice 2: {}".format(choices.count(1)/len(choices), choices.count(0)/len(choices)))
