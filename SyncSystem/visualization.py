import matplotlib.pyplot as plt
import os
from concurrent.futures import ProcessPoolExecutor
import cv2
import numpy as np


def plot_imu_data(imu_data, save_path):
    print("Plotting IMU data...")
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(imu_data['timestamp'], imu_data['ax'], label='Ax', color='r')
    plt.plot(imu_data['timestamp'], imu_data['ay'], label='Ay', color='g')
    plt.plot(imu_data['timestamp'], imu_data['az'], label='Az', color='b')
    plt.title('Accelerometer Data')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s^2]')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(imu_data['timestamp'], imu_data['magnitude'], label='Magnitude', color='m')
    plt.title('Magnitude of the Acceleration')
    plt.xlabel('Time [s]')
    plt.ylabel('Magnitude [m/s^2]')
    plt.legend()

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_imu_frame(data, current_time, plot_path):
    plt.figure(figsize=(10, 6))
    plt.plot(data['timestamp'], data['ax'], label='Ax', color='r')
    plt.plot(data['timestamp'], data['ay'], label='Ay', color='g')
    plt.plot(data['timestamp'], data['az'], label='Az', color='b')
    # Add a vertical line at the current time
    plt.axvline(x=current_time, color='k', linestyle='--')
    plt.legend()
    plt.title('Accelerometer Data')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s^2]')
    plt.savefig(plot_path)
    plt.close()

def create_combined_video(video_path, imu_data, output_path, fps):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Prepare the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width * 2, frame_height))

    plot_path = 'temp_plot.png'
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate the corresponding IMU timestamp
        current_time = frame_number / fps
        plot_imu_frame(imu_data, current_time, plot_path)

        # Read the plot image and resize to match the video frame height
        plot_img = cv2.imread(plot_path)
        plot_img_resized = cv2.resize(plot_img, (frame_width, frame_height))

        # Combine video frame and IMU plot
        combined_frame = np.hstack((frame, plot_img_resized))
        out.write(combined_frame)

        frame_number += 1

    cap.release()
    out.release()
    os.remove(plot_path)
    print("Combined video created at:", output_path)

