# coding=utf-8

import pandas as pd
import random
import time
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row


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
    df['COLLISION_SLOTS'] = collision
    df['EMPTY_SLOTS'] = empty
    df['SENT_BITS'] = sent_bits
    df['SIMULATION_TIME'] = execution

def saveMetricsToObject(obj, simulation, tag_count, collision, empty, sent_bits, execution):
    obj.simulation.append(simulation)
    obj.tag_count.append(tag_count)
    obj.collision.append(collision)
    obj.empty.append(empty)
    obj.sent_bits.append(sent_bits)
    obj.execution.append(execution)

def plotResults(qt, qtsc):
    TOOLS='pan,wheel_zoom,box_zoom,reset,hover'
    output_file('plots.html')

    # Colisões
    p1 = figure(title='Média de Colisões por # Tags', width=400, height=400, 
                tools=TOOLS, toolbar_location='below')
    p1.yaxis.axis_label = '# Colisões médias'
    p1.xaxis.axis_label = '# Tags'

    p1.circle(qt.index, qt['COLLISION_SLOTS'], legend="QT",
                line_color="red", fill_color='red', size=5)
    p1.line(qt.index, qt['COLLISION_SLOTS'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10)

    p1.circle(qtsc.index, qtsc['COLLISION_SLOTS'], legend="QTsc",
            line_color="green", fill_color='green', size=5)
    p1.line(qtsc.index, qtsc['COLLISION_SLOTS'], legend="QTsc",
            line_color="green", line_width=2, line_dash='dotted')

    # Vazios
    p2 = figure(title='Média de Slots Vazios por # Tags', width=400, height=400, 
                tools=TOOLS, toolbar_location='below')
    p2.yaxis.axis_label = '# Slots Vazios Médios'
    p2.xaxis.axis_label = '# Tags'

    p2.circle(qt.index, qt['EMPTY_SLOTS'], legend="QT",
                line_color="red", fill_color='red', size=6, fill_alpha=0.6)
    p2.line(qt.index, qt['EMPTY_SLOTS'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10, alpha=0.6)

    p2.circle(qtsc.index, qtsc['EMPTY_SLOTS'], legend="QTsc",
            line_color="green", fill_color='green', size=5, fill_alpha=0.3)
    p2.line(qtsc.index, qtsc['EMPTY_SLOTS'], legend="QTsc",
            line_color="green", line_width=2, line_dash='solid', alpha=0.3)

    # Bits
    p3 = figure(title='Média de Bits Enviados por # Tags', width=400, height=400, 
                tools=TOOLS, toolbar_location='below')
    p3.yaxis.axis_label = '# Bits Enviados Médios'
    p3.xaxis.axis_label = '# Tags'

    p3.circle(qt.index, qt['SENT_BITS'], legend="QT",
                line_color="red", fill_color='red', size=5)
    p3.line(qt.index, qt['SENT_BITS'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10)

    p3.circle(qtsc.index, qtsc['SENT_BITS'], legend="QTsc",
            line_color="green", fill_color='green', size=5)
    p3.line(qtsc.index, qtsc['SENT_BITS'], legend="QTsc",
            line_color="green", line_width=2, line_dash='dotted')

    show(row(p1,p2, p3))



def main():
    # Simulation Parameters
    params_index = ['SIMULATIONS', 'MAX_TAGS', 'MIN_TAGS', 'STEP', 'TAG_LENGTH']
    params = pd.Series([100, 1000, 100, 100, 64], index=params_index)
    # Initializing simulation variables
    tag_count = params.MIN_TAGS
    collision = empty = sent_bits = 0
    # List of tags IDs
    tags = []
        
    # Objects to store simulations metrics
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
            collision, empty, sent_bits, execution = QT(tags)
            saveMetricsToObject(qt, simulation, tag_count, collision, empty, sent_bits, execution)

            '''
                QT-sc Algorithm
            '''            
            collision, empty, sent_bits, execution = QTsc(tags)
            saveMetricsToObject(qtsc, simulation, tag_count, collision, empty, sent_bits, execution)

            # Clear tags list for next simulation
            tags = []

        # Increase number of tags based on step value
        tag_count += params.STEP
    

    # Save results into Dataframes for plotting
    column_names = ['SIMULATION_NUMBER', 'TAG_COUNT', 'COLLISION_SLOTS', 'EMPTY_SLOTS', 'SENT_BITS', 'SIMULATION_TIME']
    qt_df = pd.DataFrame(columns=column_names)
    qtsc_df = pd.DataFrame(columns=column_names)
    saveMetricsToDf(qt_df, qt.tag_count, qt.simulation, qt.collision, qt.empty, qt.sent_bits, qt.execution)
    saveMetricsToDf(qtsc_df, qtsc.tag_count, qtsc.simulation, qtsc.collision, qtsc.empty, qtsc.sent_bits, qtsc.execution)

    qt_df.to_csv('qt.csv', index=False)
    qtsc_df.to_csv('qtsc.csv', index=False)

    # Plotting results accordingly
    qt_per_tag_count = (qt_df.drop(['SIMULATION_NUMBER'], axis=1).groupby(['TAG_COUNT']).sum()) / params.SIMULATIONS
    qtsc_per_tag_count = (qtsc_df.drop(['SIMULATION_NUMBER'], axis=1).groupby(['TAG_COUNT']).sum()) / params.SIMULATIONS
    plotResults(qt_per_tag_count, qtsc_per_tag_count)


if __name__ == '__main__':
    main()