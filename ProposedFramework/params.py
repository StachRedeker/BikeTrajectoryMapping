# FILE PATHS
VIDEO_PATH = 'inputs/video.mp4'
IMU_PATH = 'inputs/data.csv'
TRUTH_PATH = 'inputs/truth.csv'

VIDEO_SYNC_PATH = 'path/to/video_s.mp4'
IMU_SYNC_PATH = 'path/to/imu_s.csv'
TRUTH_SYNC_PATH = 'path/to/truth_s.csv'

IMU_PREPROCESS_PATH = 'path/to/imu_p.csv'
VIDEO_PREPROCESS_PATH = 'path/to/video_p.csv'
TRUTH_PREPROCESS_PATH = 'path/to/truth_p.csv'

PREDICTION_PATH = 'path/to/prediction.csv'

# FRAMEWORK OPTIONS
## Synchronisation
SYNC_NEEDED = True # synchronise ground truth, camera, and IMU before further processing
VISUALISE_SYNC = True # visualise the result of the sync process from the camera and IMU
SYNC_FILES_NEEDED = False # if we need to create sync files

EXTRACT_FRAMES = True
EXTRACT_FEATURES = True
ESTIMATE_TRAJECTORY = True
MASKING = True

# User-configurable parameters for calibration movement timing
TIME_OFFSET = -10.747892352784548         # if one already knows the time ofset of the IMU and camera (in [s])
VIDEO_START = 12        # Start time of calibration movements in the video (in [s])
VIDEO_END = 23          # End time of calibration movements in the video (in [s])
IMU_START = 5 + 4296    # Start time of calibration movements in the IMU data (in [s])
IMU_END = 40 + 4296     # End time of calibration movements in the IMU data (in [s])
MANUAL = 0.6            # If some manual correction (in [s]) is required, input it here. Usually, this can be 0 for videos with few objects.

# User-configurable parameters for outputting sync files
CAMERA_FPS = 30.02
IMU_F = 200
CAMERA_TIME = '2024-04-10 14:32:45'