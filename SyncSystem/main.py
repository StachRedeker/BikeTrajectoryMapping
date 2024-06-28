from data_processing import load_imu_data, compute_magnitude, detect_movement_from_accel, reset_timestamps
from video_processing import trim_video, detect_movement_in_video
from visualization import plot_imu_data, create_combined_video
from params import VIDEO_START, VIDEO_END, IMU_START, IMU_END, MANUAL

def main():
    # File paths
    video_path = 'input_video.mp4'
    trimmed_video_path = 'trimmed_video.mp4'
    plot_video_path = 'plot_video.mp4'  # For the moving plot video
    imu_plot_path = 'imu_data_plot.png'  # Static plot of the synchronised IMU data
    combined_video_path = 'combined_video.mp4'

    # Step 1: Load IMU data and trim according to the user-defined parameters
    imu_data = load_imu_data('data.csv')
    compute_magnitude(imu_data)
    reset_timestamps(imu_data)  # Reset timestamps after trimming

    # Step 2: Trim the video according to the user-defined parameters
    trim_video(video_path, trimmed_video_path, VIDEO_START, VIDEO_END)

    # Step 3: Detect synchronisation points (i.e. the start of the calibration)
    video_movement_time = detect_movement_in_video(trimmed_video_path)
    imu_movement_time = detect_movement_from_accel(imu_data)

    if video_movement_time is not None and imu_movement_time is not None:
        # Step 4: Calculate time offset for synchronisation
        time_offset = video_movement_time - imu_movement_time + MANUAL
        print(f"Synchronisation Offset: {time_offset} [s]")
        # Adjust IMU data timestamps based on the detected synchronisation
        imu_data['timestamp'] += time_offset

        # Step 5: Plot and save the synchronized IMU data (static plot)
        plot_imu_data(imu_data, imu_plot_path)

        # Step 6: Create a combined video of the synchronised video and IMU plot
        create_combined_video(trimmed_video_path, imu_data, combined_video_path, 30)

        print("Process completed. Combined video is saved at:", combined_video_path)
    else:
        print("Failed to detect initial movements accurately in either video or IMU data. Change tresholds or add more non-moving shots.")

if __name__ == "__main__":
    main()
