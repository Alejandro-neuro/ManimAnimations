import copy
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def draw_glow_nodes(G,pos, max_size=500, min_size=200, alpha=0.02):

    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    

    max_size = 500
    min_size = 200
    alpha = 0.02
    #nx.draw_networkx_nodes(G, pos, node_color='white', node_size=max_size, alpha=0.3, cmap=plt.cm.cool )
    for i in range(50):
        Pos = copy.deepcopy(pos)

        if i > 30:
            for key, value in Pos.items():
                
                # Add the random number to the first dimension of the array
                value[0] += random.uniform(-1, 1)/10
                value[1] += random.uniform(-1, 1)/10

        nx.draw_networkx_nodes(G, Pos, node_color='white', node_size=min_size+5*(i+1), alpha=alpha, cmap=plt.cm.gray_r )
    nx.draw_networkx_nodes(G, pos, node_color='white', node_size=150, alpha=1, cmap=plt.cm.gray_r )
    plt.grid(False)

    ax.set_facecolor('black')
    fig.set_facecolor('black')
    #mplcyberpunk.add_glow_effects()
    plt.show()

def propagation_step(A, x):
    w = np.sum(A,axis=0)
    w[w==0] = 1
    xA = np.matmul(x,A)/w
    xA[np.isnan(xA)] = 0
    x1 = xA - x
    x1[x1<0.8] = 0
    return x1


def extend_time_series(timeseries, samples, n_nodes):
    for i in range(samples):
        timeseries.append(np.zeros(n_nodes))

    return timeseries