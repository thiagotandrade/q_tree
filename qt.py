import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

# Simulation parameters
class params(): 
    SIMULATIONS = 100
    MAX_TAGS = 1000
    MIN_TAGS = 100
    STEP = 100
    TAG_LENGTH = 64


# Initializing variables
start = time.time()
params = params()
tag_count = params.MIN_TAGS
tags = []
'''
COMO INICIALIZAR A PILHA Q?
'''
Q = []
M = []

# Loop to generate the number of tags, with steps of 100. Then simulate for each amount
while tag_count <= params.MAX_TAGS:
    
    # Generate random tags IDs
    for _ in range(tag_count):
        tags.append(bin(random.getrandbits(params.TAG_LENGTH))[2:])

    for simulation in range(params.SIMULATIONS):
        # Query Tree algorithm
        # current_query = Q.pop()
        while true:

    
    tags = []
    tag_count = tag_count + params.STEP


end = time.time()

execution = end - start