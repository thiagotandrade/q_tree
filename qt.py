import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

# Simulation parameters
class simulationParameters(): 
    SIMULATIONS = 100
    MAX_TAGS = 1000
    MIN_TAGS = 100
    STEP = 100
    TAG_LENGTH = 64


# Initializing variables
start = time.time()
params = simulationParameters()
tag_count = params.MIN_TAGS
tags = []
Q = ['']
M = []

# Generate the number of tags, with steps of 100. Then simulate 100 times for each amount of tags
while tag_count <= params.MAX_TAGS:
    
    # Generate random tags IDs
    for _ in range(tag_count):
        tags.append(bin(random.getrandbits(params.TAG_LENGTH))[2:])

    for simulation in range(params.SIMULATIONS):
        # Query Tree algorithm
        while Q:
            current_query = Q.pop()
            '''
                Ver como singularizar a tag;
                Ver pra que serve a memória M;
                Ver como armazenar os dados de cada simulação; 
            '''


    
    tags = []
    tag_count += params.STEP


end = time.time()

execution = end - start