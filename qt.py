'''
    TODO:

    Ver pra que serve a memória M;
    Ver o que fazer no caso de sucesso;
    Criar variáveis para guardar o que aconteceu com a query (s, c, v);
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
tags = []
Q = ['']
M = []



while tag_count <= params.MAX_TAGS:
    
    # Generate random tags IDs
    for _ in range(tag_count):
        tags.append(bin(random.getrandbits(params.TAG_LENGTH))[2:])

    for simulation in range(params.SIMULATIONS):
        # Query Tree algorithm
        matched_indices = []
        while Q:
            current_query = Q.pop()

            # Find tags indexes that contain current prefix
            matched_indices = [i for i, tag in enumerate(tags) if tag.startswith(current_query)]
            
            if len(matched_indices) == 1:
                # Sucess
                ''' Talvez retirar a tag da lista de tags? '''

            else if len(matched_indices) > 1:
                # Collision
                Q.append(current_query + '0')
                Q.append(current_query + '1')

            else:
                #Empty, does nothing
    
    tags = []
    tag_count += params.STEP


end = time.time()

execution = end - start