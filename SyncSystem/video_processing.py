import cv2
import numpy as np

def trim_video(video_path, output_path, start_time, end_time):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError("Cannot open video file")
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(fps * start_time)
    end_frame = int(fps * end_time)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while cap.get(cv2.CAP_PROP_POS_FRAMES) < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

def detect_movement_in_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError("Cannot open video file")

    ret, prev_frame = cap.read()
    if not ret:
        raise ValueError("No frames to read from video")

    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_diffs = []
    movement_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frame_gray, prev_frame_gray)
        diff_sum = np.sum(diff)  # Sum of pixel differences

        frame_diffs.append(diff_sum)

        if len(frame_diffs) > 1:
            # Calculate the standard deviation of the differences
            std_diff = np.std(frame_diffs[-10:])  # Use last 10 frames to calculate std deviation

            # Define a threshold for significant movement
            # This threshold may need to be adjusted based on the video quality and expected movement size
            threshold = np.mean(frame_diffs[-10:]) + 2 * std_diff
            if diff_sum > threshold:
                movement_frame = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert [ms] to [s]
                break

        prev_frame_gray = frame_gray

    cap.release()

    return movement_frame
