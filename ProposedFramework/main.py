import params
from synchronisation.synchronisation import synchronize_IMUVIDEO
from synchronisation.output_files import output_sync_files
from preprocessing.imu_preprocessing import preprocess_imu
from preprocessing.video_preprocessing import preprocess_video
from preprocessing.truth_preprocessing import preprocess_truth
from processing import process_data
from comparing import compare_results

def main():
    # Synchronize data
    time_offset = params.TIME_OFFSET
    if (params.SYNC_NEEDED):
        time_offset, imu_point_zero, video_point_zero = synchronize_IMUVIDEO(params.VIDEO_PATH, params.IMU_PATH)
    if (params.SYNC_FILES_NEEDED):
        output_sync_files('input_video.mp4', 'imu_data.csv', 'ground_truth.csv', time_offset, imu_point_zero, video_point_zero)

    # Preprocess IMU data
    preprocess_imu(params.IMU_SYNC_PATH)

    # Preprocess video data
    preprocess_video(params.VIDEO_SYNC_PATH, 
                     extract_frames=params.EXTRACT_FRAMES, 
                     extract_features=params.EXTRACT_FEATURES, 
                     estimate_trajectory=params.ESTIMATE_TRAJECTORY, 
                     masking=params.MASKING)

    # Preprocess truth data
    preprocess_truth(params.TRUTH_SYNC_PATH)

    # Process data
    process_data(params.IMU_PREPROCESS_PATH, params.VIDEO_PREPROCESS_PATH)

    # Compare results
    compare_results(params.TRUTH_PREPROCESS_PATH, params.PREDICTION_PATH)

if __name__ == "__main__":
    main()
