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


class SimulationParameters: 
    SIMULATIONS = 100
    MAX_TAGS = 1000
    MIN_TAGS = 100
    STEP = 100
    TAG_LENGTH = 64

# Lists to store all simulations data
class Metrics:
    def __init__(self):
        self.collision = []
        self.empty = []
        self.sent_bits = []
        self.execution = []
        self.tag_count = []
        self.simulation = []

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

def saveToDf(df, tag_count, simulation, collision, empty, sent_bits, execution):
    df['TAG_COUNT'] = tag_count
    df['SIMULATION_NUMBER'] = simulation
    df['COLISION_SLOTS'] = collision
    df['EMPTY_SLOTS'] = empty
    df['SENT_BITS'] = sent_bits
    df['SIMULATION_TIME'] = execution

    return df

def main():
    # Initializing variables
    params = SimulationParameters()
    tag_count = params.MIN_TAGS
    collision = empty = sent_bits = 0
    # List of tags IDs
    tags = []
    # Objects to store simulation metrics
    qt = Metrics()
    qtsc = Metrics()

    while tag_count <= params.MAX_TAGS:
        print("\nTag count: {}".format(tag_count))
        print("Simulation #: ", end='')

        for simulation in range(1,params.SIMULATIONS+1): 
            print("{} ".format(simulation), end='')

            #Store current simulation number and tags amount for later plotting
            qt.tag_count.append(tag_count)
            qtsc.tag_count.append(tag_count)
            qt.simulation.append(simulation)
            qtsc.simulation.append(simulation)

            # Generate random tags IDs
            for _ in range(tag_count):
                tags.append(bin(random.getrandbits(params.TAG_LENGTH))[2:].zfill(params.TAG_LENGTH))
            
            '''
                QT Algorithm
            '''           
            start = time.time()
            
            # Query Tree Simulation
            collision, empty, sent_bits = QT(tags)
            
            qt.collision.append(collision)
            qt.empty.append(empty)
            qt.sent_bits.append(sent_bits)
            end = time.time()
            # Calculate QT execution time in seconds
            qt.execution.append(end - start)

            '''
                QT-sc Algorithm
            '''
            start = time.time()
            
            # Query Tree Shortcut Simulation            
            collision, empty, sent_bits = QTsc(tags)
            
            qtsc.collision.append(collision)
            qtsc.empty.append(empty)
            qtsc.sent_bits.append(sent_bits)
            end = time.time()
            # Calculate QTsc execution time in seconds
            qtsc.execution.append(end - start)

            # Clear tags list for next simulation
            tags = []

        
        tag_count += params.STEP
    

    # Save results into Dataframes for plotting
    column_names = ['SIMULATION_NUMBER', 'TAG_COUNT', 'COLISION_SLOTS', 'EMPTY_SLOTS', 'SENT_BITS', 'SIMULATION_TIME']
    qt_df = pd.DataFrame(columns=column_names)
    qtsc_df = pd.DataFrame(columns=column_names)
    qt_df = saveToDf(qt_df, qt.tag_count, qt.simulation, qt.collision, qt.empty, qt.sent_bits, qt.execution)
    qtsc_df = saveToDf(qtsc_df, qtsc.tag_count, qtsc.simulation, qtsc.collision, qtsc.empty, qtsc.sent_bits, qtsc.execution)

    qt_df.to_csv('qt.csv', index=False)
    qtsc_df.to_csv('qtsc.csv', index=False)



if __name__ == '__main__':
    main()