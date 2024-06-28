import pandas as pd
import datetime
from moviepy.editor import VideoFileClip
from synchronisation.data_processing import reset_timestamps
from params import CAMERA_TIME, CAMERA_FPS

def output_sync_files(VIDEO_PATH, IMU_PATH, TRUTH_PATH, time_offset, imu_point_zero, video_point_zero):
    # Load video
    video_clip = VideoFileClip(VIDEO_PATH)
    
    # Load IMU data
    imu_data = pd.read_csv(IMU_PATH, usecols=['timestamp', 'ax', 'ay', 'az'])

    # Reset timestamps
    reset_timestamps(imu_data)

    # Shift timestamps
    imu_data['timestamp'] += time_offset

    # Load ground truth data
    truth_data = pd.read_csv(TRUTH_PATH, usecols=['timestamp', 'latitude', 'longitude'], parse_dates=['timestamp'],
                             date_parser=lambda x: pd.to_datetime(x, format='%a %b %d %H:%M:%S GMT+02:00 %Y'))

    # Convert CAMERA_TIME to datetime
    camera_start_time = pd.to_datetime(CAMERA_TIME, format='%Y-%m-%d %H:%M:%S')

    # Convert ground truth timestamps to relative seconds
    truth_data['timestamp'] = (truth_data['timestamp'] - camera_start_time).dt.total_seconds()

    # Convert video start time to relative seconds
    video_start_seconds = (video_point_zero - camera_start_time).total_seconds()

    # Align the three zero points and calculate the overall start and end times
    overall_start_time = max(imu_data['timestamp'].min(), video_start_seconds, truth_data['timestamp'].min())
    overall_end_time = min(imu_data['timestamp'].max(), truth_data['timestamp'].max())

    # Filter IMU data based on the overall start and end times
    imu_data = imu_data[(imu_data['timestamp'] >= overall_start_time) & (imu_data['timestamp'] <= overall_end_time)]

    # Filter ground truth data based on the overall start and end times
    truth_data = truth_data[(truth_data['timestamp'] >= overall_start_time) & (truth_data['timestamp'] <= overall_end_time)]

    # Check if the data is empty after filtering
    if imu_data.empty:
        raise ValueError("Filtered IMU data is empty. Please check the input data and parameters.")
    if truth_data.empty:
        raise ValueError("Filtered Ground Truth data is empty. Please check the input data and parameters.")

    # Reset IMU timestamps
    reset_timestamps(imu_data)

    # Calculate subclip times for the video
    video_subclip_start = overall_start_time - video_start_seconds
    video_subclip_end = overall_end_time - video_start_seconds

    # Output synchronized video
    output_video_path = "video_s.mp4"
    output_data_path = "data_s.csv"
    output_truth_path = "truth_s.csv"

    video_clip.subclip(video_subclip_start, video_subclip_end).write_videofile(output_video_path, fps=CAMERA_FPS)

    # Output synchronized IMU data
    imu_data.to_csv(output_data_path, index=False)

    # Output synchronized ground truth data
    truth_data.to_csv(output_truth_path, index=False)

    print(f"Synchronized data saved to {output_video_path}, {output_data_path}, and {output_truth_path}")
