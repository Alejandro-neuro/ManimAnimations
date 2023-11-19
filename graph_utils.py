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

def get_group_nodes(G, node_positions):

    # Split the space into 9 quadrants with 3 rows and 3 columns
    quadrant_size_x = 1 / 3
    quadrant_size_y = 1 / 3
    quadrants = [
        (
            int(pos[0] // quadrant_size_x) + int(pos[1] // quadrant_size_y)*3,
        )
        for node, pos in node_positions.items()
    ]
    
    # Assign a group to each node based on the probability distribution
    node_groups = {}
    for node, quadrant in zip(G.nodes(), quadrants):
        probability = random.random()  # Probability between 0 and 1

        # Assign the node to its group with a probability of 80%, otherwise to one of the other eight groups
        if probability < 2:
            node_groups[node] = quadrant[0] % 9  # Assign to the same group as the quadrant's x-coordinate
        else:
            other_groups = [i for i in range(9) if i != quadrant[0] % 9]
            node_groups[node] = random.choice(other_groups)
    return node_groups

def generateFrameGraph(G,node_positions, node_sizes,node_groups,  values, name):
    
    # Generate random positions for each node
    #node_positions = {node: (random.uniform(0, 1), random.uniform(0, 1)) for node in G.nodes()}

    # Assign a random value between 0 and 1 to each node
    node_values = {node: random.uniform(0.2, 1) for node in G.nodes()}
    

    #node_values = {node: values[i] for node,i in G.nodes()}

    # Draw the graph with node colors based on values

    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    

    

    # Create a colormap based on the number of groups
    cmap = plt.cm.get_cmap('tab10', 9)

    # Define different sizes for each node
    

    # Map the number between 0 and 8 to a value between 0 and 1 for each group
    #node_signal = np.array(values, dtype=float)
    node_signal = values
    node_signal[node_signal <0.20] = 0.3

  

    group_values = {group: node_signal[group] for group in range(9)}  

    # Assign the same value between 0 and 1 to all nodes in the same group
    node_values = {node: group_values[node_groups[node]] for node in G.nodes()}

   

    

    #nx.draw(
    #    G,
    #    pos=node_positions,
    #    with_labels=False,
    #    node_size=[node_sizes[node] for node in G.nodes()],
    #    #node_color=[cmap(group) for group in node_groups.values()],
    #    node_color=[node_values[node] for node in G.nodes()],
    #    cmap=plt.cm.get_cmap('gray'),
    #    alpha=1,
    #    vmin=0,
    #    vmax=1,
    #    edge_color='gray',
    #)

    # Draw the graph with node colors based on groups
    nx.draw_networkx_nodes(G, node_positions, node_color=[node_values[node] for node in G.nodes()], node_size=[node_sizes[node]*2 for node in G.nodes()], alpha=0.3,vmin=0,vmax=1, cmap=plt.cm.get_cmap('gray') )
    nx.draw_networkx_nodes(G, node_positions, node_color=[node_values[node] for node in G.nodes()], node_size=[node_sizes[node] for node in G.nodes()], alpha=1,vmin=0,vmax=1, cmap=plt.cm.get_cmap('gray') )

    

    # Add a colorbar to show the mapping

    ax.set_facecolor('black')
    fig.set_facecolor('black')
    #fig.patch.set_visible(True)
    # Show the plot
    
    
    plt.savefig('./imgs2vid/'+str(name)+'.png', transparent=False, dpi=fig.dpi)
    plt.close()
