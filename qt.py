# coding=utf-8
'''
    TODO:
        Garantir que os tag IDs gerados sejam únicos;
        Como gerar os plots dos comparativos (ver e-mail professor);
        Implementar o QT-sc.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

# Values Store Classes
class SimulationParameters(): 
    SIMULATIONS = 100
    MAX_TAGS = 1000
    MIN_TAGS = 100
    STEP = 100
    TAG_LENGTH = 64

class Metrics():
    collision = 0
    empty = 0
    sent_bits = 0
    execution = 0
    tag_count = 0

def QT(tags):
    collision = empty = sent_bits = 0
    Q = ['']
    M = []

    # Query Tree algorithm
    while Q:
        # Current query will be the top of the stack of queries
        current_query = Q.pop()

        # Find tags indexes that contain current prefix
        matched_indices = [i for i, tag in enumerate(tags) if tag.startswith(current_query)]
        
        # Sum of Sent bits for each query
        sent_bits += sum([len(tags[i]) for i in matched_indices])

        # Success
        if len(matched_indices) == 1: 
            M.append(tags[matched_indices[0]])

        # Collision
        elif len(matched_indices) > 1:
            Q.append(current_query + '0')
            Q.append(current_query + '1')
            collision += 1

        # Empty            
        else: 
            empty += 1
    
    return collision, empty, sent_bits


def QTsc(tags):
    collision = empty = sent_bits = 0
    Qsc = ['']
    M = []

    # Query Tree Shortcut algorithm
    while Qsc:
        # Current query will be the top of the stack of queries
        current_query = Qsc.pop()

        # Find tags indexes that contain current prefix
        matched_indices = [i for i, tag in enumerate(tags) if tag.startswith(current_query)]
        
        # Sum of Sent bits for each query
        sent_bits += sum([len(tags[i]) for i in matched_indices])

        # Success
        if len(matched_indices) == 1: 
            M.append(tags[matched_indices[0]])

        # Collision
        elif len(matched_indices) > 1:
            Qsc.append(current_query + '0')
            Qsc.append(current_query + '1')
            collision += 1

        # Empty            
        else: 
            empty += 1
    
    return collision, empty, sent_bits

def main():
    # Initializing variables
    params = SimulationParameters()
    tag_count = params.MIN_TAGS

    # List of tags IDs
    tags = []

    # Objects to store simulation metrics
    qt = Metrics()
    qtsc = Metrics()
    
    # Initialize dataframes for plotting
    column_names = ['SIMULATION_NUMBER', 'TAG_COUNT', 'COLISION_SLOTS', 'EMPTY_SLOTS', 'SENT_BITS', 'SIMULATION_TIME']
    qt_df = pd.DataFrame(columns=column_names)
    qtsc_df = pd.DataFrame(columns=column_names)

    while tag_count <= params.MAX_TAGS:
        print("Tag count: {}".format(tag_count))

        for simulation in range(1,params.SIMULATIONS+1): 
            print("Simulation #: {}".format(simulation))

            # Generate random tags IDs
            for _ in range(tag_count):
                tags.append(bin(random.getrandbits(params.TAG_LENGTH))[2:].zfill(params.TAG_LENGTH))
            
            # Query Tree Simulation
            start = time.time()
            qt.collision, qt.empty, qt.sent_bits = QT(tags)
            end = time.time()
            # Calculate QT execution time in seconds
            qt.execution = end - start

            # Query Tree Shortcut Simulation
            start = time.time()
            qtsc.collision, qtsc.empty, qtsc.sent_bits = QTsc(tags)
            end = time.time()
            # Calculate QTsc execution time in seconds
            qtsc.execution = end - start

            qt_df = qt_df.append(pd.Series([simulation, tag_count, qt.collision, qt.empty, qt.sent_bits, qt.execution], index=column_names), ignore_index=True)
            qtsc_df = qtsc_df.append(pd.Series([simulation, tag_count, qtsc.collision, qtsc.empty, qtsc.sent_bits, qtsc.execution], index=column_names), ignore_index=True)


        tags = []
        tag_count += params.STEP
    

    qt_df.to_csv('qt.csv', index=False)
    qtsc_df.to_csv('qt_sc_df.csv', index=False)



if __name__ == '__main__':
    main()