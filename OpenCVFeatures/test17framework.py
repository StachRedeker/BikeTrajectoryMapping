import cv2
import numpy as np
import csv
import time

# Parameters
n = 100  # Maximum number of features to track
confidenceRegion = 60  # Size of the confidence region in pixels
video_path = 'video.mp4'
output_video_path = 'output.mp4'
csv_path = 'features.csv'
start_time_sec = 60  # Start time in seconds for clip analysis
end_time_sec = 80  # End time in seconds for clip analysis
trackDuration = 1  # Duration in seconds for which a feature needs to be tracked to be colored green
mask_path = 'mask.png'  # Path to the mask image

print(f"Loading video from {video_path}")

# Load video
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Video loaded: {frame_width}x{frame_height} at {fps} FPS, {total_frames} total frames")

# Load mask
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
if mask is None or mask.shape != (frame_height, frame_width):
    print("Mask image not found or dimensions do not match the video frame. Exiting.")
    cap.release()
    exit()
print(f"Mask loaded from {mask_path}")

# Calculate start and end frame based on the specified start and end time
start_frame = int(start_time_sec * fps)
end_frame = int(end_time_sec * fps)

if start_frame >= total_frames:
    print("Start time exceeds video length. Exiting.")
    cap.release()
    exit()
if end_frame > total_frames or end_time_sec == 0:
    end_frame = total_frames
print(f"Processing frames from {start_frame} to {end_frame} ({start_time_sec} to {end_time_sec} seconds)")

# Set the video to start at the start frame
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Parameters for ShiTomasi corner detection (without maxCorners)
feature_params = dict(qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Initialize tracking variables
old_gray = None
p0 = None
feature_num = 0
feature_dict = {}
feature_start_time = {}
feature_occurrence = {}

print("Starting feature tracking")

# Open CSV file for writing
with open(csv_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['frame number', 'feature number', 'pos x', 'pos y'])

    frame_num = start_frame
    start_time = time.time()
    while cap.isOpened() and frame_num < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if p0 is None:
            print(f"Frame {frame_num}: Detecting initial features")
            # Detect initial features
            p0 = cv2.goodFeaturesToTrack(frame_gray, mask=mask, maxCorners=n, **feature_params)
            if p0 is not None:
                current_time = time.time()
                for i in range(p0.shape[0]):
                    feature_dict[feature_num] = p0[i]
                    feature_start_time[feature_num] = current_time
                    feature_occurrence[feature_num] = 1
                    csvwriter.writerow([frame_num, feature_num, int(p0[i][0][0]), int(p0[i][0][1])])
                    feature_num += 1
                print(f"Detected {len(p0)} initial features")
            else:
                print("No initial features detected")
        else:
            # Calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            if p1 is not None:
                # Select good points
                good_new = p1[st == 1]
                good_old = p0[st == 1]

                print(f"Frame {frame_num}: Tracking {len(good_new)} features")

                # Draw the tracks
                for i, (new, old) in enumerate(zip(good_new, good_old)):
                    a, b = map(int, new.ravel())
                    c, d = map(int, old.ravel())
                    cv2.line(frame, (a, b), (c, d), (0, 255, 0), 2)

                # Update CSV file and feature dictionary
                new_feature_dict = {}
                current_time = time.time()
                for i, new in enumerate(good_new):
                    feature_id = None
                    min_dist = float('inf')
                    for key, value in feature_dict.items():
                        dist = np.linalg.norm(new - value)
                        if dist < min_dist:
                            min_dist = dist
                            feature_id = key

                    if feature_id is not None and min_dist < confidenceRegion:
                        csvwriter.writerow([frame_num, feature_id, int(new[0]), int(new[1])])
                        new_feature_dict[feature_id] = new
                        feature_occurrence[feature_id] += 1
                    else:
                        new_feature_dict[feature_num] = new
                        feature_start_time[feature_num] = current_time
                        feature_occurrence[feature_num] = 1
                        csvwriter.writerow([frame_num, feature_num, int(new[0]), int(new[1])])
                        feature_num += 1

                # Select new features if some went out of frame
                lost_features = n - len(new_feature_dict)
                if lost_features > 0:
                    mask_new = mask.copy()
                    for new in good_new:
                        x, y = map(int, new.ravel())
                        cv2.circle(mask_new, (x, y), confidenceRegion, 0, -1)
                    new_features = cv2.goodFeaturesToTrack(frame_gray, mask=mask_new, maxCorners=lost_features, **feature_params)
                    if new_features is not None:
                        for i in range(new_features.shape[0]):
                            new_feature_dict[feature_num] = new_features[i]
                            feature_start_time[feature_num] = time.time()
                            feature_occurrence[feature_num] = 1
                            csvwriter.writerow([frame_num, feature_num, int(new_features[i][0][0]), int(new_features[i][0][1])])
                            feature_num += 1
                        print(f"Detected {len(new_features)} new features")
                    else:
                        print("No new features detected")
                feature_dict = new_feature_dict

                # Draw the features
                for feature_id, new in new_feature_dict.items():
                    a, b = map(int, new.ravel())
                    color = (0, 0, 255)  # Red for new features
                    if current_time - feature_start_time[feature_id] > trackDuration:
                        color = (0, 255, 0)  # Green for features tracked for more than 1 second
                    cv2.circle(frame, (a, b), 5, color, -1)

                p0 = np.array([v.ravel() for v in new_feature_dict.values()]).reshape(-1, 1, 2)
            else:
                print(f"Frame {frame_num}: No features tracked")
                p0 = None

        # Write the frame to the output video
        out.write(frame)

        # Update the previous frame and previous points
        old_gray = frame_gray.copy()
        frame_num += 1

print("Releasing resources")

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Feature tracking complete. Results saved to {csv_path} and {output_video_path}")
