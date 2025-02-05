from analyze import D
from util import emotions as E
import random

def find_edge_value(joy, s, e):
    
    out_idx = int((e - 1) / 3)
    in_idx = int(((e - 1)  % 3))
    return (s, e, joy[out_idx][in_idx][1])

def create_node_and_edge(emotion_name):

    emotion = D[emotion_name]

    nodes = ['-']

    for feature in emotion:
        for datapoint in feature:
            nodes.append(str(datapoint[0]))

    edges = [
        find_edge_value(emotion, 0, 1),
        find_edge_value(emotion, 0, 2),
        find_edge_value(emotion, 0, 3),

        find_edge_value(emotion, 1, 4),
        find_edge_value(emotion, 1, 5),
        find_edge_value(emotion, 1, 6),

        find_edge_value(emotion, 2, 4),
        find_edge_value(emotion, 2, 5),
        find_edge_value(emotion, 2, 6),

        find_edge_value(emotion, 3, 4),
        find_edge_value(emotion, 3, 5),
        find_edge_value(emotion, 3, 6),
        
        find_edge_value(emotion, 4, 7),
        find_edge_value(emotion, 4, 8),
        find_edge_value(emotion, 4, 9),

        find_edge_value(emotion, 5, 7),
        find_edge_value(emotion, 5, 8),
        find_edge_value(emotion, 5, 9),

        find_edge_value(emotion, 6, 7),
        find_edge_value(emotion, 6, 8),
        find_edge_value(emotion, 6, 9),

        find_edge_value(emotion, 7, 10),
        find_edge_value(emotion, 7, 11),
        find_edge_value(emotion, 7, 12),

        find_edge_value(emotion, 8, 10),
        find_edge_value(emotion, 8, 11),
        find_edge_value(emotion, 8, 12),

        find_edge_value(emotion, 9, 10),
        find_edge_value(emotion, 9, 11),
        find_edge_value(emotion, 9, 12),

        find_edge_value(emotion, 10, 13),
        find_edge_value(emotion, 10, 14),
        find_edge_value(emotion, 10, 15),

        find_edge_value(emotion, 11, 13),
        find_edge_value(emotion, 11, 14),
        find_edge_value(emotion, 11, 15),

        find_edge_value(emotion, 12, 13),
        find_edge_value(emotion, 12, 14),
        find_edge_value(emotion, 12, 15),
    ]

    return nodes, edges

# Function to find the next node based on the current node and its edges' probabilities
def find_next_node(current_node):
    # Find all the possible edges from the current node
    possible_edges = [edge for edge in edges if edge[0] == current_node]
    
    # Extract the nodes and probabilities for the next step
    next_nodes = [edge[1] for edge in possible_edges]
    probabilities = [edge[2] for edge in possible_edges]
    
    # Normalize the probabilities (they should already sum to 1, but just in case)
    total_prob = sum(probabilities)
    probabilities = [prob / total_prob for prob in probabilities]
    
    # Select the next node based on the probabilities
    next_node = random.choices(next_nodes, probabilities)[0]
    
    return next_node

NN = {}

for emotion in E:

    nodes, edges = create_node_and_edge(emotion)

    paths = []

    with open(f'{emotion}.txt', 'a') as the_file:

        for i in range(5):
            curr_node = 0  # Define your starting node index here
            path = ''

            while (curr_node < 13):
                curr_node = find_next_node(curr_node)
                path += nodes[curr_node] + '+'
            path = path[:-1]

            paths.append(path)

            the_file.write(path + '\n')
    
    NN[emotion] = paths

print(NN)