D = {'joy': [[(0.0, 0.13636363636363635), (3.0, 0.0909090909090909), (5.0, 0.11363636363636363), (6.0, 0.1818181818181818), (7.0, 0.11363636363636363), (9.0, 0.1818181818181818), (10.0, 0.1818181818181818)], [(0.01, 1.0)], [(0.1, 1.0)], [(5.0, 1.0)], [(13.0, 0.10256410256410257), (15.0, 0.46153846153846156), (16.0, 0.15384615384615385), (18.0, 0.12820512820512822), (20.0, 0.15384615384615385)]], 'sad': [[(0.0, 0.36111111111111105), (1.0, 0.22222222222222218), (2.0, 0.2777777777777778), (6.0, 0.1388888888888889)], [(0.01, 0.8461538461538461), (0.1, 0.15384615384615383)], [(0.1, 0.5454545454545454), (1.0, 0.45454545454545453)], [(1.0, 0.6363636363636364), (5.0, 0.3636363636363636)], [(8.0, 0.18181818181818182), (10.0, 0.18181818181818182), (13.0, 0.12121212121212122), (15.0, 0.36363636363636365), (20.0, 0.15151515151515152)]], 'anger': [[(0.0, 0.14285714285714288), (7.0, 0.1904761904761905), (8.0, 0.09523809523809525), (9.0, 0.16666666666666669), (10.0, 0.40476190476190477)], [(0.1, 1.0)], [(1.0, 1.0)], [(5.0, 1.0)], [(9.0, 0.13513513513513514), (11.0, 0.10810810810810811), (15.0, 0.35135135135135137), (20.0, 0.40540540540540543)]], 'fear': [[(0.0, 0.3333333333333333), (1.0, 0.09523809523809523), (2.0, 0.09523809523809523), (6.0, 0.09523809523809523), (7.0, 0.14285714285714285), (10.0, 0.2380952380952381)], [(0.01, 0.37499999999999994), (0.1, 0.625)], [(0.55, 0.25), (1.0, 0.75)], [(1.0, 0.5), (5.0, 0.5)], [(3.0, 0.22727272727272727), (10.0, 0.1818181818181818), (15.0, 0.40909090909090906), (20.0, 0.1818181818181818)]], 'disgust': [[(0.0, 0.2682926829268293), (1.0, 0.09756097560975609), (2.0, 0.12195121951219512), (5.0, 0.14634146341463414), (6.0, 0.14634146341463414), (10.0, 0.2195121951219512)], [(0.01, 1.0)], [(1.0, 1.0)], [(1.0, 0.3636363636363636), (5.0, 0.6363636363636364)], [(7.0, 0.15625000000000003), (9.0, 0.125), (10.0, 0.28125), (15.0, 0.31250000000000006), (20.0, 0.125)]]}
from util import emotions as E
import random

def find_edge_value(joy, s, e):

    flat_list = [item for sublist in joy for item in sublist]
    print(flat_list)
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

        for i in range(10):
            curr_node = 0  # Define your starting node index here
            path = ''

            while (find_next_node(curr_node)):
                curr_node = find_next_node(curr_node)
                path += nodes[curr_node] + '+'
            path = path[:-1]

            paths.append(path)

            the_file.write(path + '\n')
    
    NN[emotion] = paths