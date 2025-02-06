import csv

'''
Demographic
Young Adults (20–35)
Middle-aged Adults (36–55)
'''

emotions = ['joy', 'sad', 'anger', 'fear', 'disgust']
features = ['or', 'ir', 'pk', 'pc', 'no', 'bo', 'sp']

def read_data(file_path='./analyzer/raw_data.csv'):
    emotion_data = {emotion: [] for emotion in emotions}
    feature_data = {feature: [] for feature in features}

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip header row

        for row in reader:
            data_points = row[1:]  # Skip 'timestamp'
            for i, emotion in enumerate(emotions):
                emotion_data[emotion].append(data_points[i].split('+'))

        # Transpose the emotion data for each feature
        for feature_index, feature_name in enumerate(features):
            for emotion in emotions:
                feature_values = [data[feature_index] for data in emotion_data[emotion]]
                feature_data[feature_name].append(feature_values)

    return emotion_data, feature_data

EMOTION_DATA, FEATURE_DATA = read_data()