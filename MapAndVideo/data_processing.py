import pandas as pd
import geopy.distance
from datetime import datetime

# Load CSV data and convert timestamps
def load_data(csv_path):
    data = pd.read_csv(csv_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='Wed %b %d %H:%M:%S GMT+02:00 %Y')
    return data

# Synchronize timestamps and calculate time offset
def calculate_offsets(data, video_start_time_str):
    video_start_time = datetime.strptime(video_start_time_str, '%Y-%m-%d %H:%M:%S')
    data['time_offset'] = (data['timestamp'] - video_start_time).dt.total_seconds()
    return data

# Calculate distance between two points
def calculate_distance(coord1, coord2):
    return geopy.distance.distance(coord1, coord2).meters

# Filter points by distance or time
def filter_points(data):
    filtered_indices = [0]
    for i in range(1, len(data)):
        time_diff = abs(data.loc[i, 'time_offset'] - data.loc[filtered_indices[-1], 'time_offset'])
        coord1 = (data.loc[filtered_indices[-1], 'latitude'], data.loc[filtered_indices[-1], 'longitude'])
        coord2 = (data.loc[i, 'latitude'], data.loc[i, 'longitude'])
        distance = calculate_distance(coord1, coord2)
        if time_diff >= 10 or distance >= 10:
            filtered_indices.append(i)
    return data.iloc[filtered_indices]

