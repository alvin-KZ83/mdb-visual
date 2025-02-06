D = {'joy': [[(0.0, 0.18181818181818182), (3.0, 0.13636363636363635), (5.0, 0.18181818181818182), (6.0, 0.2272727272727273), (9.0, 0.13636363636363635), (10.0, 0.13636363636363635)], [(0.01, 1.0)], [(0.1, 1.0)], [(5.0, 1.0)], [(15.0, 1.0)]], 'sad': [[(0.0, 0.4375), (1.0, 0.1875), (2.0, 0.375)], [(0.01, 0.7857142857142857), (0.1, 0.21428571428571427)], [(0.1, 1.0)], [(5.0, 1.0)], [(8.0, 0.33333333333333337), (15.0, 0.6666666666666667)]], 'anger': [[(0.0, 0.13636363636363635), (7.0, 0.18181818181818182), (8.0, 0.13636363636363635), (9.0, 0.18181818181818182), (10.0, 0.36363636363636365)], [(0.1, 1.0)], [(1.0, 1.0)], [(5.0, 1.0)], [(9.0, 0.19047619047619047), (15.0, 0.4761904761904762), (20.0, 0.3333333333333333)]], 'fear': [[(0.0, 0.2727272727272727), (1.0, 0.18181818181818182), (6.0, 0.13636363636363635), (7.0, 0.2272727272727273), (10.0, 0.18181818181818182)], [(0.01, 0.5714285714285714), (0.1, 0.42857142857142855)], [(1.0, 1.0)], [(5.0, 1.0)], [(6.0, 0.21428571428571427), (10.0, 0.21428571428571427), (15.0, 0.5714285714285714)]], 'disgust': [[(0.0, 0.3333333333333333), (2.0, 0.19047619047619047), (5.0, 0.14285714285714285), (6.0, 0.19047619047619047), (10.0, 0.14285714285714285)], [(0.01, 1.0)], [(1.0, 1.0)], [(5.0, 1.0)], [(7.0, 0.23529411764705882), (10.0, 0.29411764705882354), (15.0, 0.47058823529411764)]]}
from util import emotions as E
import random

def find_edge_value(joy, s, e):

    flat_list = [item for sublist in joy for item in sublist]
    return (s, e, flat_list[e - 1][1])

def create_node_and_edge(emotion_name):

    emotion = D[emotion_name]

    nodes = ['-']

    for feature in emotion:
        for datapoint in feature:
            nodes.append(str(datapoint[0]))

    L = []
    with open(f'./prob_tables/edge_information/{emotion_name}.txt', 'r') as the_file:
        L = the_file.readlines()
        L = [_.strip().split(',') for _ in L]
        L = [(int(x[0]), int(x[1])) for x in L]
    
    edges = [find_edge_value(emotion, a, b) for a, b in L]

    print(nodes, edges)

    return nodes, edges

# Function to find the next node based on the current node and its edges' probabilities
def find_next_node(current_node):
    # Find all the possible edges from the current node
    possible_edges = [edge for edge in edges if edge[0] == current_node]

    if len(possible_edges) == 0: return
    
    # Extract the nodes and probabilities for the next step
    next_nodes = [edge[1] for edge in possible_edges]
    probabilities = [edge[2] for edge in possible_edges]
    
    # Normalize the probabilities (they should already sum to 1, but just in case)
    total_prob = sum(probabilities)
    probabilities = [prob / total_prob for prob in probabilities]

    print(next_nodes)
    print(probabilities)
    
    # Select the next node based on the probabilities
    next_node = random.choices(next_nodes, probabilities)[0]
    
    return next_node

NN = {}

for emotion in E:

    nodes, edges = create_node_and_edge(emotion)

    paths = []

    with open(f'./samples/{emotion}.txt', 'a') as the_file:

        for i in range(20):
            curr_node = 0  # Define your starting node index here
            path = ''

            while (find_next_node(curr_node)):
                curr_node = find_next_node(curr_node)
                path += nodes[curr_node] + '+'
            path = path[:-1]

            paths.append(path)

            the_file.write(path + '\n')
    
    NN[emotion] = paths