import matplotlib.pyplot as plt
import os

box_plot_data = [
    # emotion = {'pk': [min, q1, med, q3, max, mean, mode],...}
    {
        'pk': [0,3,7,10,10,6.32,10], 
        'pc': [0.01,0.028,0.042,0.089,0.1,0.05356,0.1], 
        'n': [0.1,0.14,0.3,0.41,1,0.3804,0.1], 
        'b': [1.93,2.98,3.89,4.89,5,3.804,5], 
        's': [3,13,16,18,20,14.88,20]
    },
    {
        'pk': [0,0,3,5,10,3.56,0], 
        'pc': [0.01,0.01,0.015,0.025,0.1,0.02444,0.01], 
        'n': [0.1,0.1,0.19,0.48,1,0.3388,0.1], 
        'b': [1,1,1.58,2.67,5,2.0844,1], 
        's': [1,5,10,15,20,10.52,20]
    },
    {
        'pk': [0,5,9,10,10,6.96,10], 
        'pc': [0.016,0.064,0.095,0.1,0.1,0.07704,0.1], 
        'n': [0.1,0.61,0.98,1,1,0.8216,1], 
        'b': [2.34,3.4,4.81,5,5,4.2352,5], 
        's': [1,8,11,20,20,12.16,20]
    },
    {
        'pk': [0,3,5,10,10,5.84,10], 
        'pc': [0.01,0.03,0.067,0.1,0.1,0.062,0.1], 
        'n': [0.1,0.54,0.68,0.97,1,0.6668,1], 
        'b': [1,1.51,2.34,3.33,5,2.5464,1], 
        's': [1,3,8,12,20,7.88,3]
    },
    {
        'pk': [0,2,3,6,10,4.16,10], 
        'pc': [0.01,0.018,0.028,0.05,0.1,0.03776,0.01], 
        'n': [0.1,0.52,0.65,0.96,1,0.6764,1], 
        'b': [1,2.23,3.44,4.55,5,3.3824,5], 
        's': [3,6,11,14,20,10.36,14]
    },
]

for emotion in box_plot_data:
    for key, list_value in emotion.items():
        if (key == 'pk'): 
            scale = 1
        elif (key == 'pc'):
            scale = 100
        elif (key == 'n'):
            scale = 10
        elif (key == 'b'):
            scale = 2
        elif (key == 's'):
            scale = 0.5
        for i in range(len(list_value)):
            list_value[i] *= scale

# Assert all lists have exactly 6 elements
for emotion_data in box_plot_data:
    for feature_values in emotion_data.values():
        try:
            assert len(feature_values) == 7, "Each feature list must contain exactly 6 values."
        except AssertionError as e:
            print(feature_values)
# Feature keys
features = ['pk', 'pc', 'n', 'b', 's']

emotions_list = ['joy', 'sad', 'anger', 'fear', 'disgust']
features_dict = {'pk' : 'Peaks', 'pc': 'Pace', 'n': 'Noise', 'b': 'Bold', 's': 'Space'}

# Create boxplots for each feature
for feature in features:
    plt.figure(figsize=(8, 5))

    # Extract data for the current feature across all emotions
    feature_data = [emotion_data[feature][:5] for emotion_data in box_plot_data]  # Exclude the mean
    mean_values = [emotion_data[feature][5] for emotion_data in box_plot_data]  # Extract the mean
    mode_values = [emotion_data[feature][6] for emotion_data in box_plot_data]  # Extract the mode


    # Create boxplot
    plt.boxplot(feature_data, vert=True, patch_artist=True)

    # Overlay mean markers
    for i, mean in enumerate(mean_values):
        plt.plot(i + 1, mean, 'ro')  # Use a red circle for the mean

    # Overlay mean markers
    for j, mode in enumerate(mode_values):
        plt.plot(j + 1, mode, 'rx')  # Use a red cross for the mode

    # Set plot labels and title
    plt.xticks(range(1, len(feature_data) + 1), [f'{emotions_list[i]}' for i in range(len(feature_data))])
    plt.title(f"Boxplot for {features_dict[feature]}")
    plt.xlabel("Emotions")
    plt.ylabel(f"Values of {features_dict[feature]}")
    
    # Show legend
    plt.legend()

    # Show plot
    plt.savefig(os.path.join('analyzer//graphs',f'{feature}_boxplot.png'))