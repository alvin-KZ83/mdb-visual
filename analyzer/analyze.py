import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from util import read_data
from scipy import stats
import os

# L = [joy, sad, anger, fear, dsgst]
# OUTER RING, INNER RING, PEAKS, PACE, NOISE, BOLD, SPACE
# or, ir, pk, pc, n, b, s

data = read_data()

joy, sad, anger, fear, disgust = data

emotions = {'joy': joy, 'sad':sad, 'anger':anger, 'fear': fear, 'disgust': disgust}
features = {'pk' : 'Peaks', 'pc': 'Pace', 'n': 'Noise', 'b': 'Bold', 's': 'Space'}

def tally_data(emotion, feature):
    # type is either or, ir, pk, pc, n, b, s
    values = emotion[feature]
    tally = Counter(values)
    sorted_tally = dict(sorted(tally.items()))
    return sorted_tally

def tally_emotion(emotion):
    tallied_emotion = {}
    for key, value in emotion.items():
        if (key == 'or' or key == 'ir'): continue
        tallied_emotion[key] = tally_data(emotion, key)
    return tallied_emotion
        
def graph_emotion_type(emotion, feature, ax):
    emotion_data = emotions[emotion]
    tallied_emotion = tally_emotion(emotion_data)
    data = tallied_emotion.get(feature, {})
    keys = list(data.keys())
    values = list(data.values())

    if (feature == 'pk'): 
        scale = 10
    elif (feature == 'pc'):
        scale = 1000
    elif (feature == 'n'):
        scale = 100
    elif (feature == 'b'):
        scale = 20
    elif (feature == 's'):
        scale = 5

    scaled_keys = [key * scale for key in keys]

    # Create a bar plot of the distribution
    ax.bar(scaled_keys, values, color='black', width=1)

    # Plot a line that connects the bars
    ax.plot(scaled_keys, values, color='red', marker='o', linestyle='-', linewidth=2, markersize=5, label='Trend Line')

    # Adding titles and labels
    ax.set_title(f'Distribution of {features[feature]} for {emotion.capitalize()}', fontsize=12)
    ax.set_xlabel(features[feature], fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    
    # Format x-axis labels to show only a few decimal places
    ax.tick_params(axis='x', rotation=45)

def plot_all_emotion_types(emotion):
    fig, axes = plt.subplots(len(features), 1, figsize=(10, 6 * len(features)))  # Create a figure with multiple subplots

    # If there is only one subplot, `axes` is not an array, so we need to handle that case
    if len(features) == 1:
        axes = [axes]

    for i, feature in enumerate(features):
        graph_emotion_type(emotion, feature, axes[i])  # Plot each emotion type on a separate subplot

    # Adjust layout to avoid overlap
    plt.tight_layout()

    # Show the final stacked plot
    plt.savefig(os.path.join('analyzer//graphs',f'{emotion}.png'))

for key in emotions.keys():
    plot_all_emotion_types(key)