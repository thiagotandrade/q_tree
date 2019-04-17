# coding=utf-8
'''
    TODO:
    Ver como armazenar os dados de cada simulação.
    Como gerar os plots dos comparativos (ver e-mail professor)
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
        tags.append(bin(random.getrandbits(params.TAG_LENGTH))[2:].zfill(params.TAG_LENGTH))

    for simulation in range(1,params.SIMULATIONS+1):
        
        print("Simulation #: {}".format(simulation))
        # Clearing previous simulation data
        Q = ['']
        M = []
        success = collision = empty = sent_bits = 0

        # Query Tree algorithm
        while Q:
            # Current query will be the top of the stack of queries
            current_query = Q.pop()

            # Find tags indexes that contain current prefix
            matched_indices = [i for i, tag in enumerate(tags) if tag.startswith(current_query)]
            
            # Sent bits in each query for both collisions and successes
            sent_bits += sum([len(tags[i]) for i in matched_indices])

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
        
        '''
            Armazenar dados num dataframe da seguinte forma:
            +------------------------------------------------------------------------------+
            | SIMULATION_NUMBER | TAG_COUNT | EMPTY_SLOTS | COLISION_SLOTS | SUCCESS_SLOTS |
            +------------------------------------------------------------------------------+
            |       ...         |    ...    |     ...     |      ...       |      ...      |
            |       ...         |    ...    |     ...     |      ...       |      ...      |
            |                                                                              |
            |                                      .                                       |
            |                                      .                                       |
            |                                      .                                       |
            
            Referência sobre como inserir linha em um dataframe:
            https://thispointer.com/python-pandas-how-to-add-rows-in-a-dataframe-using-dataframe-append-loc-iloc/

        '''
    
    tags = []
    tag_count += params.STEP


end = time.time()

execution = end - start