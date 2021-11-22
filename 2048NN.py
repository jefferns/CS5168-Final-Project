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
    # list of lists
    #   [data[0], output]
    #        data[0] is [previous_observation, action]
    #           previous observation is list of lists (game board)
    #               [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    scores = []
    accepted_scores = []
    options = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

    for _ in range(initial_games):
        count=0
        score = 0
        game_memory = []
        prev_observation = []

        for _ in range(goal_score):
            action = options[random.randrange(0,4)] #will need to be (0,4) for 2048?
            print("Action: ", action)
            game_data, reward, done, info = env.step(action) #controls the game
            count+=1
            print(env.get_board())

            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])

            prev_observation = env.get_board()
            score += reward
            
            if done:
                #print("Game Over")
                #print(count)
                break

        if score >= score_required:
            accepted_scores.append(score)

            for data in game_memory:
                if data[1] == options[0]:
                    output = [1,0,0,0]
                elif data[1] == options[1]:
                    output = [0,1,0,0]
                elif data[1] == options[2]:
                    output = [0,0,1,0]
                elif data[1] == options[3]:
                    output = [0,0,0,1]
                # print('********')
                # print([data[0], output])
                training_data.append([data[0], output])
        env.reset() #reset the game
        scores.append(score)


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


    network = fully_connected(network, 4, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=learningRate,
                         loss='categorical_crossentropy', name='targets')
    
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model


# def condense_board(data):
#     tmp = []
#     for move in data:  # Get a move
#         tmp2 = []
#         board = move[0]  # Board
#         print(board)
#         for row in board:
#             tmp2.append(row)
#         tmp.append(tmp2)
        
#     return tmp

def train_model(trainingData, model=False):

    # for x in trainingData:
    #     print('******')
    #     print(condense_board(x[0]))
#   X = np.array([i[0] for i in training_data]).reshape(-1,len(training_data[0][0]),1)
    X = np.array([i[0] for i in trainingData]).reshape(len(trainingData),4,4)
    #print("Type: " ,type(X[0]))
    print("X Shape: ", X.shape)
    #print(Y)
    Y = [i[1] for i in trainingData] #[1,0,0,0] [0,1,0,0] 
    #print(Y)
    #Y = np.array([i[1] for i in trainingData]).reshape(-1)
   # Y.reshape(len(trainingData), 1)
    #print("Y Shape: ", Y.shape)
    #print(X)

    if not model:
        print(len(X))
        model = neuralNetworkModel(input_size = 4)

    model.fit({'input':X}, {'targets':Y}, batch_size=len(trainingData),n_epoch=5, snapshot_step=500, show_metric=True, run_id='openaistuff')

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
