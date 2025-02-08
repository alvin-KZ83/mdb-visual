import matplotlib.pyplot as plt
import networkx as nx

def parse_graph_file(file_path):
    # Initialize graph
    G = nx.DiGraph()

    with open(file_path, 'r') as file:
        layers = file.read().split('+')  # Split by '+' to separate layers
        print("Layers found:", len(layers))  # Check how many layers are found
        
        # Process each layer
        start_node = None  # Initialize start_node outside the loop
        for layer in layers:
            lines = layer.strip().splitlines()
            
            if not lines:
                continue

            print("Processing layer with", len(lines), "lines")
            
            for line in lines:
                # Extract node and weight from the line
                node, weight = map(float, line.split(','))
                node = int(node)  # Assuming node is an integer

                if start_node is None:
                    start_node = node  # Set the first node as the start node
                    continue  # Skip adding edges for the first node, just set it
                
                # Add edge from previous node (start_node) to current node with weight
                G.add_edge(start_node, node, weight=weight)
                start_node = node  # Move to the next node for the next edge

    print("Graph created with", len(G.nodes), "nodes and", len(G.edges), "edges.")
    return G

def visualize_graph(G):
    if len(G.nodes) == 0:
        print("The graph is empty! No nodes to display.")
        return

    # Use circular layout for better node positioning
    pos = nx.circular_layout(G)  # Layout for positioning nodes
    
    # Get edge weights
    weights = nx.get_edge_attributes(G, 'weight')
    
    # Plot the graph
    plt.figure(figsize=(12, 12))  # Increase figure size for clarity
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_weight='bold', font_color='black')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, font_size=10)
    
    # Title and show the plot
    plt.title("Graph Visualization")
    plt.show()

# Parse the graph from the file
file_path = 'joy_prob.txt'  # Change to the path of your file
G = parse_graph_file(file_path)

# Visualize the graph
visualize_graph(G)
