import numpy as np
from datetime import datetime
from utils import *

#parameters for TESTS

#================ players parameters =====================================================================================

num_players = 100
#----Simulation rounds
max_rounds = 100

prob_honest = 0.7
prob_opportunistic = 0.2
prob_malicious = 0.05
prob_random = 0.05
probabilities = (prob_honest, prob_opportunistic, prob_malicious, prob_random)

prob = 0.05 #probability that in that day a players wants an object in the showcase

n_token_init = 10

#================ associations parameters =====================================================================================
associations = {
    'Library': Person(name='Library', behavior_lending='honest',behavior_borrowing='', tokens=200),
    'Study help': Person(name='Study help', behavior_lending='honest', behavior_borrowing='', tokens = 100),
    'Transportation service': Person(name='Transportation service', behavior_lending='honest', behavior_borrowing='', tokens = 120)
}
num_books = 10000
num_study_helpers = 12000
num_vehicles = 8000
associations['Library'].createRandomObjects(num_books)
associations['Study help'].createRandomObjects(num_study_helpers)
associations['Transportation service'].createRandomObjects(num_vehicles)


#================ incentives parameters =======================================================================================
#TOKENS REWARD
payoffs_reward = {
    "lender": np.array([1, 0, 0]) , 
    "borrower": np.array([2, 0, 0])
}

