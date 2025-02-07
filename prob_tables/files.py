def parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().strip().split("\n")
    
    levels = []
    current_level = []

    for line in lines:
        if line.startswith('+'):
            # Save the current level and reset for the next
            levels.append(current_level)
            current_level = []
        else:
            current_level.append(line.strip())

    # Append the last level
    if current_level:
        levels.append(current_level)

    return levels


def generate_edges(levels):
    edges = []
    node_index = 0
    node_indices = []  # Store the index mapping for each level

    for level in levels:
        current_level_indices = list(range(node_index, node_index + len(level)))
        node_indices.append(current_level_indices)
        node_index += len(level)

    # Generate edges between consecutive levels
    for i in range(len(node_indices) - 1):
        for start_node in node_indices[i]:
            for end_node in node_indices[i + 1]:
                edges.append(f"{start_node},{end_node}")

    return edges


def write_edges_to_file(edges, output_file):
    with open(output_file, 'w') as f:
        for edge in edges:
            f.write(edge + '\n')

emotion = 'disgust'
# Paths
input_file = f'./prob_tables/{emotion}_prob.txt'  # Replace with your actual file path
output_file = f'./prob_tables/edge_information/{emotion}.txt'

# Process
levels = parse_file(input_file)
edges = generate_edges(levels)
write_edges_to_file(edges, output_file)

print(f"Edges written to {output_file}")
