# coding=utf-8
'''
    TODO:
    Ver pra que serve a memória M;
    Ver o que fazer no caso de sucesso;
    Criar variáveis para guardar o que aconteceu com a query (s, c, e);
    Ver como armazenar os dados de cada simulação.
'''

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

# List of tags IDs
tags = []
# Stack of queries
Q = ['']
# Memory (stores successfuly read tags ids)
M = []
# Amount of successes, collisions and empty for each simulation
success = collision = empty = 0



while tag_count <= params.MAX_TAGS:
    
    # Generate random tags IDs
    for _ in range(tag_count):
        tags.append(bin(random.getrandbits(params.TAG_LENGTH))[2:])

    for simulation in range(1,params.SIMULATIONS+1):
        
        print("Simulation #: {}".format(simulation))

        # Query Tree algorithm
        while Q:
            current_query = Q.pop()

            # Find tags indexes that contain current prefix
            matched_indices = [i for i, tag in enumerate(tags) if tag.startswith(current_query)]
            
            # Success
            if len(matched_indices) == 1: 
                M.append(tags[matched_indices[0]])
                success += 1
                #print('Success', success)

            # Collision
            elif len(matched_indices) > 1:
                Q.append(current_query + '0')
                Q.append(current_query + '1')
                collision += 1
                #print('Collision', collision)

            # Empty            
            else: 
                empty += 1
                #print('Empty', empty)

        
        Q = ['']
        M = []
        success = collision = empty = 0
        
    
    tags = []
    tag_count += params.STEP


end = time.time()

execution = end - start