# coding=utf-8

import numpy as np
import pandas as pd
import random
import time
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, row


# Lists to store all simulations data
class Metrics:
    def __init__(self):
        self.collision = []
        self.empty = []
        self.sent_bits = []
        self.execution = []
        self.tag_count = []
        self.simulation = []
        self.total = []

        
def QT(tags):
    success = collision = empty = sent_bits = 0
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
            success += 1
            M.append(tags[matched_indices[0]])

        # Collision
        elif len(matched_indices) > 1:
            Q.extend([current_query + '0', current_query + '1'])
            collision += 1

        # Empty            
        else: 
            empty += 1
    
    end = time.time()
    
    return collision, empty, sent_bits, (end - start)*1000, (collision + empty + success)


def QTsc(tags):
    success = collision = empty = sent_bits = 0
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
            success += 1
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
    return collision, empty, sent_bits, (end - start)*1000, (collision + empty + success)

def saveMetricsToDf(df, tag_count, simulation, collision, empty, sent_bits, execution, total):
    df['TAG_COUNT'] = tag_count
    df['SIMULATION_NUMBER'] = simulation
    df['COLLISION_SLOTS'] = collision
    df['EMPTY_SLOTS'] = empty
    df['SENT_BITS'] = sent_bits
    df['SIMULATION_TIME'] = execution
    df['TOTAL_SLOTS'] = total

def saveMetricsToObject(obj, simulation, tag_count, collision, empty, sent_bits, execution, total):
    obj.simulation.append(simulation)
    obj.tag_count.append(tag_count)
    obj.collision.append(collision)
    obj.empty.append(empty)
    obj.sent_bits.append(sent_bits)
    obj.execution.append(execution)
    obj.total.append(total)

def generateRandomTag(length):
   return bin(random.getrandbits(length))[2:].zfill(length)

def plotResults(qt, qtsc):
    TOOLS='pan,wheel_zoom,box_zoom,reset,hover'
    output_file('plots.html')

    # Collisions
    p1 = figure(title='Média de Colisões por # Tags', 
                tools=TOOLS, toolbar_location='below')
    p1.yaxis.axis_label = 'Média de Colisões '
    p1.xaxis.axis_label = '# Tags'

    p1.circle(qt.index, qt['COLLISION_SLOTS'], legend="QT",
                line_color="red", fill_color='red', size=5)
    p1.line(qt.index, qt['COLLISION_SLOTS'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10)

    p1.circle(qtsc.index, qtsc['COLLISION_SLOTS'], legend="QTsc",
            line_color="green", fill_color='green', size=5)
    p1.line(qtsc.index, qtsc['COLLISION_SLOTS'], legend="QTsc",
            line_color="green", line_width=2, line_dash='dotted')

    p1.legend.location = "top_left"
    p1.legend.click_policy="hide"


    # Empty
    p2 = figure(title='Média de Slots Vazios por # Tags', 
                tools=TOOLS, toolbar_location='below')
    p2.yaxis.axis_label = 'Média de Slots Vazios'
    p2.xaxis.axis_label = '# Tags'

    p2.circle(qt.index, qt['EMPTY_SLOTS'], legend="QT",
                line_color="red", fill_color='red', size=6, fill_alpha=0.6)
    p2.line(qt.index, qt['EMPTY_SLOTS'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10, alpha=0.6)

    p2.circle(qtsc.index, qtsc['EMPTY_SLOTS'], legend="QTsc",
            line_color="green", fill_color='green', size=5, fill_alpha=0.3)
    p2.line(qtsc.index, qtsc['EMPTY_SLOTS'], legend="QTsc",
            line_color="green", line_width=2, line_dash='solid', alpha=0.3)

    p2.legend.location = "top_left"
    p2.legend.click_policy="hide"


    # Bits
    p3 = figure(title='Média de Bits Enviados por # Tags', 
                tools=TOOLS, toolbar_location='below')
    p3.yaxis.axis_label = 'Média de Bits Enviados'
    p3.xaxis.axis_label = '# Tags'

    p3.circle(qt.index, qt['SENT_BITS'], legend="QT",
                line_color="red", fill_color='red', size=5)
    p3.line(qt.index, qt['SENT_BITS'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10)

    p3.circle(qtsc.index, qtsc['SENT_BITS'], legend="QTsc",
            line_color="green", fill_color='green', size=5)
    p3.line(qtsc.index, qtsc['SENT_BITS'], legend="QTsc",
            line_color="green", line_width=2, line_dash='dotted')

    p3.legend.location = "top_left"
    p3.legend.click_policy="hide"


    # Simulation Time
    p4 = figure(title='Média de Tempo de Simulação (ms) por # Tags', 
        tools=TOOLS, toolbar_location='below')
    p4.yaxis.axis_label = 'Média de Tempo de Simulação (ms)'
    p4.xaxis.axis_label = '# Tags'
    
    p4.circle(qt.index, qt['SIMULATION_TIME'], legend="QT",
                line_color="red", fill_color='red', size=5)
    p4.line(qt.index, qt['SIMULATION_TIME'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10)

    p4.circle(qtsc.index, qtsc['SIMULATION_TIME'], legend="QTsc",
            line_color="green", fill_color='green', size=5)
    p4.line(qtsc.index, qtsc['SIMULATION_TIME'], legend="QTsc",
            line_color="green", line_width=2, line_dash='dotted')

    p4.legend.location = "top_left"
    p4.legend.click_policy="hide"    


    # Total Slots
    p5 = figure(title='Total de Slots Médio por # Tags', 
                tools=TOOLS, toolbar_location='below')
    p5.yaxis.axis_label = 'Média de Total de Slots'
    p5.xaxis.axis_label = '# Tags'

    p5.circle(qt.index, qt['TOTAL_SLOTS'], legend="QT",
                line_color="red", fill_color='red', size=5)
    p5.line(qt.index, qt['TOTAL_SLOTS'], legend="QT",
                line_color="red", line_width=2, line_dash='dashed', line_dash_offset=10)

    p5.circle(qtsc.index, qtsc['TOTAL_SLOTS'], legend="QTsc",
            line_color="green", fill_color='green', size=5)
    p5.line(qtsc.index, qtsc['TOTAL_SLOTS'], legend="QTsc",
            line_color="green", line_width=2, line_dash='dotted')

    p5.legend.location = "top_left"
    p5.legend.click_policy="hide"    

    show(row(p1, p2, p3, p4, p5))



def main():
    # Simulation Parameters
    params_index = ['SIMULATIONS', 'MAX_TAGS', 'MIN_TAGS', 'STEP', 'TAG_LENGTH']
    params = pd.Series([100, 1000, 100, 100, 64], index=params_index)
    # Initializing simulation variables
    tag_count = params.MIN_TAGS
    total = collision = empty = sent_bits = 0
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

            # Generate unique random tags IDs
            while len(tags) < tag_count:
                tag = generateRandomTag(params.TAG_LENGTH)
                while tag in tags:
                    tag = generateRandomTag(params.TAG_LENGTH)
                tags.append(tag)

            '''
                QT Algorithm
            '''           
            collision, empty, sent_bits, execution, total = QT(tags)
            saveMetricsToObject(qt, simulation, tag_count, collision, empty, sent_bits, execution, total)

            '''
                QT-sc Algorithm
            '''            
            collision, empty, sent_bits, execution, total = QTsc(tags)
            saveMetricsToObject(qtsc, simulation, tag_count, collision, empty, sent_bits, execution, total)

            # Clear tags list for next simulation
            tags = []

        # Increase number of tags based on step value
        tag_count += params.STEP
    

    # Save results into Dataframes for plotting
    column_names = ['SIMULATION_NUMBER', 'TAG_COUNT', 'COLLISION_SLOTS', 'EMPTY_SLOTS', 'SENT_BITS', 'SIMULATION_TIME', 'TOTAL_SLOTS']
    qt_df = pd.DataFrame(columns=column_names)
    qtsc_df = pd.DataFrame(columns=column_names)
    saveMetricsToDf(qt_df, qt.tag_count, qt.simulation, qt.collision, qt.empty, qt.sent_bits, qt.execution, qt.total)
    saveMetricsToDf(qtsc_df, qtsc.tag_count, qtsc.simulation, qtsc.collision, qtsc.empty, qtsc.sent_bits, qtsc.execution, qtsc.total)

    qt_df.to_csv('qt.csv', index=False)
    qtsc_df.to_csv('qtsc.csv', index=False)

    # Plotting results accordingly
    qt_per_tag_count = (qt_df.drop(['SIMULATION_NUMBER'], axis=1).groupby(['TAG_COUNT']).sum()) / params.SIMULATIONS
    qtsc_per_tag_count = (qtsc_df.drop(['SIMULATION_NUMBER'], axis=1).groupby(['TAG_COUNT']).sum()) / params.SIMULATIONS
    plotResults(qt_per_tag_count, qtsc_per_tag_count)


if __name__ == '__main__':
    main()