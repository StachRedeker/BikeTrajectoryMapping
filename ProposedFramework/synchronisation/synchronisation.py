import os
import pandas as pd
from synchronisation.data_processing import load_imu_data, compute_magnitude, detect_movement_from_accel, reset_timestamps
from synchronisation.video_processing import trim_video, detect_movement_in_video
from synchronisation.visualization import plot_imu_data, create_combined_video
from params import VIDEO_START, VIDEO_END, IMU_START, IMU_END, MANUAL, VISUALISE_SYNC

def reset_timestamps(accel_data, store_original=False):
    if store_original:
        accel_data['original_timestamp'] = accel_data['timestamp']
    accel_data['timestamp'] -= accel_data['timestamp'].min()

def synchronize_IMUVIDEO(video_path, imu_path):
    # File paths
    trimmed_video_path = 'trimmed_video.mp4'
    imu_plot_path = 'imu_data_plot.png'
    combined_video_path = 'combined_video.mp4'

    # Ensure VIDEO_START is a datetime object
    #video_start_datetime = pd.to_datetime(VIDEO_START, format='%Y-%m-%d %H:%M:%S')

    # Step 1: Load IMU data
    imu_data = pd.read_csv(imu_path, usecols=['timestamp', 'ax', 'ay', 'az'])

    # Step 2: Reset timestamps
    reset_timestamps(imu_data, store_original=True)

    # Step 3: Cut to size & compute magnitude
    imu_data = imu_data[(imu_data['original_timestamp'] >= IMU_START) & (imu_data['original_timestamp'] <= IMU_END)]
    compute_magnitude(imu_data)

    # Step 4: Synchronize
    trim_video(video_path, trimmed_video_path, VIDEO_START, VIDEO_END)
    video_movement_time = detect_movement_in_video(trimmed_video_path)
    imu_movement_time = detect_movement_from_accel(imu_data)
    if video_movement_time is not None and imu_movement_time is not None:
        time_offset = video_movement_time - imu_movement_time + MANUAL
        imu_data['timestamp'] += time_offset

        # Step 5: Obtain zero point
        imu_point_zero = imu_data['timestamp'].min() + IMU_START
        #video_point_zero = video_start_datetime + pd.to_timedelta(video_movement_time, unit='s')

        plot_imu_data(imu_data, imu_plot_path)
        if VISUALISE_SYNC:
            create_combined_video(trimmed_video_path, imu_data, combined_video_path, 30)
        return time_offset, imu_point_zero, video_point_zero
    else:
        print("Failed to detect initial movements accurately in either video or IMU data.")
        return -1, None, None
