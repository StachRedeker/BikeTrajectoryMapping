import pandas as pd
import numpy as np

def load_imu_data(filepath, IMU_START, IMU_END):
    print("Loading IMU data...")
    data = pd.read_csv(filepath, usecols=['timestamp', 'ax', 'ay', 'az'])
    data = data[(data['timestamp'] >= IMU_START) & (data['timestamp'] <= IMU_END)]
    return data

def compute_magnitude(accel_data):
    accel_data['magnitude'] = np.sqrt(accel_data['ax']**2 + accel_data['ay']**2 + accel_data['az']**2)
    accel_data['magnitude'] = accel_data['magnitude'].rolling(window=10, center=True).mean().fillna(method='bfill').fillna(method='ffill')

def reset_timestamps(accel_data):
    accel_data['timestamp'] -= accel_data['timestamp'].min()

def detect_movement_from_accel(accel_data):
    print("Detecting movements from accelerometer data...")
    threshold = accel_data['magnitude'].mean() + 1.5 * accel_data['magnitude'].std()
    movement_times = accel_data['timestamp'][accel_data['magnitude'] > threshold]
    return movement_times.iloc[0] if not movement_times.empty else None
