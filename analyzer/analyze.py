from util import FEATURE_DATA as RAW_DATA
from util import emotions as E
from util import features as F

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgb
import colorsys
import random

from collections import Counter

feature_titles = ['Outer Ring Color', 'Inner Ring Color', 'Peak (Polygon Edges)', 'Pace (Speed)', 'Noise (Distortion / Disturbance)', 'Boldness / Thickness', 'Space (Airyness)']

def generate():
    for i in range(len(F)):

        if (i < 2): continue # skip the colors

        data = RAW_DATA[F[i]]

        data = [[float(__) for __ in _] for _ in data] # conversion to floats

        x = [set(_) for _ in data]
        x = sorted(list(set.union(*x)))

        # Initialize the plot
        plt.figure(figsize=(12, 6))

        # Colors for each list line
        colors = ['blue', 'orange', 'green', 'red', 'purple']

        for idx, dataset in enumerate(data):
            # Count occurrences of each value
            counter = Counter(dataset)
            
            # Extract the value-frequency pairs sorted by value
            y = [counter[value] for value in x]
            
            # Plot each line
            plt.plot(x, y, marker='o', color=colors[idx], label=f'{E[idx].capitalize()}')


            with open(f'analyzer/plots/tables/{E[idx]}_{F[i]}.csv', 'w') as f:
                for j in range(len(x)):
                    f.write(str(x[j]) + ',' + str(y[j]) + '\n')


        # Labeling
        plt.title(f'Frequency Data of {feature_titles[i]}')
        plt.xlabel(f'Values of {feature_titles[i]}')
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)
        
        # Save the plot to a specific path
        save_path = f'analyzer/plots/frequency_{F[i]}.svg'
        plt.savefig(save_path, format='svg', dpi=300, bbox_inches='tight')

def sort_colors_by_hsl(color_list):
    """
    Sorts colors by a combination of Hue, Saturation, and Lightness.
    Sorting order:
    1. Hue (Primary)
    2. Saturation (Secondary)
    3. Lightness (Tertiary)
    """
    # Convert hex colors to RGB, then to HSL for sorting
    colors_hsl = [(color, colorsys.rgb_to_hls(*to_rgb(color))) for color in color_list]
    
    # Sort by hue, saturation, then lightness
    sorted_colors = sorted(colors_hsl, key=lambda x: (x[1][0], x[1][2], x[1][1]))  # Sort by H, then L, then S
    return [color[0] for color in sorted_colors]

def visualize_colors(color_data, filetype):
    num_datasets = len(RAW_DATA[F[color_data]])
    
    # Create a single figure with subplots
    fig, axes = plt.subplots(num_datasets, 1, figsize=(12, 2 * num_datasets))
    
    if num_datasets == 1:  # Handle single dataset case for consistent indexing
        axes = [axes]

    for idx, (ax, color_list) in enumerate(zip(axes, RAW_DATA[F[color_data]])):
        # Sort colors by hue before plotting
        sorted_colors = sort_colors_by_hsl(color_list)

        # Remove axis for a cleaner look
        ax.axis('off')

        # Plot color patches for the current dataset
        for i, color in enumerate(sorted_colors):
            rect = patches.Rectangle((i, 0), 1, 1, facecolor=color)
            ax.add_patch(rect)

        # Set plot limits
        ax.set_xlim(0, len(sorted_colors))
        ax.set_ylim(0, 1)
        ax.set_title(f"Dataset for {E[idx].capitalize()}", loc='left')

    # Labeling
    plt.suptitle(f'Color Grid of {feature_titles[color_data]}')
    plt.tight_layout()
    save_path = f'analyzer/plots/colors_grid_{F[color_data]}.{filetype}'
    plt.savefig(save_path, format=f'{filetype}', dpi=300, bbox_inches='tight')

# def visualize_colors(color_data, filetype):
#     num_datasets = len(RAW_DATA[F[color_data]])
    
#     # Create a single figure with subplots
#     fig, axes = plt.subplots(num_datasets, 1, figsize=(12, 2 * num_datasets))
    
#     if num_datasets == 1:  # Handle single dataset case for consistent indexing
#         axes = [axes]

#     for idx, (ax, color_list) in enumerate(zip(axes, RAW_DATA[F[color_data]])):
#         # Sort colors by hue before plotting
#         sorted_colors = sort_colors_by_hsl(color_list)

#         # Remove axis for a cleaner look
#         ax.axis('off')

#         # Plot color patches for the current dataset
#         for i, color in enumerate(sorted_colors):
#             rect = patches.Rectangle((i, 0), 1, 1, facecolor=color)
#             ax.add_patch(rect)

#         # Set plot limits
#         ax.set_xlim(0, len(sorted_colors))
#         ax.set_ylim(0, 1)
#         ax.set_title(f"Dataset for {E[idx].capitalize()}", loc='left')

#     # Labeling
#     plt.suptitle(f'Color Grid of {feature_titles[color_data]}')
#     plt.tight_layout()
#     save_path = f'analyzer/plots/colors_grid_{F[color_data]}.{filetype}'
#     plt.savefig(save_path, format=f'{filetype}', dpi=300, bbox_inches='tight')

def visualize_color(color_data, f_type):

    for idx, color_list in enumerate(color_data):
        sorted_colors = sort_colors_by_hsl(color_list)

        fig, ax = plt.subplots(figsize=(12, 2))
        
        # Remove axis for a cleaner look
        ax.axis('off')

        # Plot color patches
        for i, color in enumerate(sorted_colors):
            rect = patches.Rectangle((i, 0), 1, 1, facecolor=color)
            ax.add_patch(rect)
        
        # Set plot limits
        ax.set_xlim(0, len(sorted_colors))
        ax.set_ylim(0, 1)
        
        # Save the figure
        save_path = f'analyzer/plots/colors/{F[f_type]}_{E[idx]}.png'
        plt.savefig(save_path, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
        plt.show()

def generate_freq_table():
    D = {key : [] for key in E}
    for i in range(len(F)):

        if (i < 2): continue # skip the colors

        data = RAW_DATA[F[i]]

        data = [[float(__) for __ in _] for _ in data] # conversion to floats

        x = [set(_) for _ in data]
        x = sorted(list(set.union(*x)))

        for idx, dataset in enumerate(data):
            # Count occurrences of each value
            counter = Counter(dataset)
            
            # Extract the value-frequency pairs sorted by value
            y = [counter[value] for value in x]
            
            assert len(x) == len(y)

            ftable = []

            for e_idx, a in enumerate(x):
                ftable.append((a, y[e_idx]))

            sorted_ftable = [(a , b / sum(b for _, b in ftable)) for a, b in ftable]

            # sorted_ftable = sorted(ftable, key=lambda x: x[1], reverse=True)[:3]
            sorted_ftable = [x for x in sorted_ftable if x[1] > 2/28]

            D[E[idx]].append(sorted_ftable)
        
    for emotion, value in D.items():
        result = [
            [(a, b / sum(b for _, b in group)) for a, b in group]
            for group in value
        ]
        D[emotion] = result
    
    return D

generate()
# visualize_colors(0, 'svg')
# visualize_colors(1, 'svg')
# D = generate_freq_table()
# print(D)

