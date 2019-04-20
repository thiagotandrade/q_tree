# coding=utf-8
'''
    TODO:
        Garantir que os tag IDs gerados sejam únicos;
        Como gerar os plots dos comparativos (ver e-mail professor);
        Verificar se o QT e o QT-sc estão funcionando corretamente.
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
    start = time.time()

    # Query Tree algorithm
    while Q:
        # Current query will be the top of the stack of queries
        current_query = Q.pop()

        # Find tags indexes that contain current prefix
        matched_indices = [i for i, tag in enumerate(tags) if tag.startswith(current_query)]
        
        # Sum of each query sent bits 
        sent_bits += sum([len(tags[i]) for i in matched_indices])

        # Success
        if len(matched_indices) == 1: 
            M.append(tags[matched_indices[0]])

        # Collision
        elif len(matched_indices) > 1:
            Q.extend([current_query + '0', current_query + '1'])
            collision += 1

        # Empty            
        else: 
            empty += 1
    
    end = time.time()
    
    return collision, empty, sent_bits, end-start


def QTsc(tags):
    collision = empty = sent_bits = 0
    last_bit_collided = ' '
    Qsc = ['']
    M = []
    start = time.time()
    
    # Query Tree Shortcut algorithm
    while Qsc:
        # Current query will be the top of the stack of queries
        current_query = Qsc.pop()

        # Find tags indexes that contain current prefix
        matched_indices = [i for i, tag in enumerate(tags) if tag.startswith(current_query)]
        
        # Sum of each query sent bits
        sent_bits += sum([len(tags[i]) for i in matched_indices])

        # Success
        if len(matched_indices) == 1: 
            M.append(tags[matched_indices[0]])

        # Collision
        elif len(matched_indices) > 1:
            collision += 1
            Qsc.extend([current_query + '0', current_query + '1'])
            last_collision = current_query

        # Empty            
        else: 
            empty += 1
            if current_query[:-1] == last_collision:
                # The prefix to be skipped will be on the top of the queue
                Qsc.pop()
                # Skip prefix q0
                if current_query[-1:] == '1':
                    Qsc.extend([current_query[:-1] + '00', current_query[:-1] + '01'])
                # Skip prefix q1
                elif current_query[-1:] == '0':
                    Qsc.extend([current_query[:-1] + '10', current_query[:-1] + '11'])
              
    
    end = time.time()
    return collision, empty, sent_bits, end-start

def saveMetricsToDf(df, tag_count, simulation, collision, empty, sent_bits, execution):
    df['TAG_COUNT'] = tag_count
    df['SIMULATION_NUMBER'] = simulation
    df['COLISION_SLOTS'] = collision
    df['EMPTY_SLOTS'] = empty
    df['SENT_BITS'] = sent_bits
    df['SIMULATION_TIME'] = execution

    return df

def saveMetricsToObject(obj, simulation, tag_count, collision, empty, sent_bits, execution):
    obj.simulation.append(simulation)
    obj.tag_count.append(tag_count)
    obj.collision.append(collision)
    obj.empty.append(empty)
    obj.sent_bits.append(sent_bits)
    obj.execution.append(execution)

    return obj



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

            # Generate random tags IDs
            tags.extend([bin(random.getrandbits(params.TAG_LENGTH))[2:].zfill(params.TAG_LENGTH) for _ in range(tag_count)])
            
            '''
                QT Algorithm
            '''           
            start = time.time()
            # Query Tree Simulation
            collision, empty, sent_bits, execution = QT(tags)
            end = time.time()
            qt = saveMetricsToObject(qt, simulation, tag_count, collision, empty, sent_bits, execution)

            '''
                QT-sc Algorithm
            '''
            start = time.time()
            # Query Tree Shortcut Simulation            
            collision, empty, sent_bits, execution = QTsc(tags)
            end = time.time()
            qtsc = saveMetricsToObject(qtsc, simulation, tag_count, collision, empty, sent_bits, execution)

            # Clear tags list for next simulation
            tags = []

        
        tag_count += params.STEP
    

    # Save results into Dataframes for plotting
    column_names = ['SIMULATION_NUMBER', 'TAG_COUNT', 'COLISION_SLOTS', 'EMPTY_SLOTS', 'SENT_BITS', 'SIMULATION_TIME']
    qt_df = pd.DataFrame(columns=column_names)
    qtsc_df = pd.DataFrame(columns=column_names)
    qt_df = saveMetricsToDf(qt_df, qt.tag_count, qt.simulation, qt.collision, qt.empty, qt.sent_bits, qt.execution)
    qtsc_df = saveMetricsToDf(qtsc_df, qtsc.tag_count, qtsc.simulation, qtsc.collision, qtsc.empty, qtsc.sent_bits, qtsc.execution)

    qt_df.to_csv('qt.csv', index=False)
    qtsc_df.to_csv('qtsc.csv', index=False)



if __name__ == '__main__':
    main()