import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv

video_path = '01eerstekleinerondje.mp4'
start_time_sec = 350  # Start time in seconds
end_time_sec = 450    # End time in seconds
mask_path = 'mask-own.png'  # Path to the mask image (optional)
csv_file_path = 'results.csv'

def feature_tracking(prev_img, curr_img, prev_points):
    lk_params = dict(winSize=(21, 21), maxLevel=3,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    
    curr_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_img, curr_img, prev_points, None, **lk_params)
    
    good_old = prev_points[status == 1]
    good_new = curr_points[status == 1]
    
    return good_old, good_new

def detect_features(image, mask):
    feature_params = dict(maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=7)
    points = cv2.goodFeaturesToTrack(image, mask=mask, **feature_params)
    return points

def main():
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Set start and end time in milliseconds
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time_sec * 1000)
    end_time = end_time_sec * 1000

    # Read the first frame to get dimensions
    ret, prev_frame = cap.read()
    if not ret:
        print("Cannot read video file")
        return
    frame_height, frame_width = prev_frame.shape[:2]
    
    # Load mask
    if mask_path:
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None or mask.shape != (frame_height, frame_width):
            print("Mask image not found or dimensions do not match the video frame. Exiting.")
            cap.release()
            return
        print(f"Mask loaded from {mask_path}")
    else:
        mask = None
    
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_points = detect_features(prev_frame_gray, mask)
    
    # Create mask for drawing the trajectory
    mask_draw = np.zeros_like(prev_frame)
    
    # Initialize transformation matrix
    trajectory = np.zeros((3, 1))
    poses = [trajectory]

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['frame_num', 'x', 'y', 'z'])

        frame_num = 0

        while cap.isOpened():
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC)
            if current_time > end_time:
                break
            
            ret, frame = cap.read()
            if not ret:
                break
            
            curr_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            prev_points, curr_points = feature_tracking(prev_frame_gray, curr_frame_gray, prev_points)
            
            # If not enough points are tracked, detect new points
            if prev_points.shape[0] < 8 or curr_points.shape[0] < 8:
                print("Not enough points to compute the essential matrix, detecting new points")
                prev_points = detect_features(prev_frame_gray, mask)
                curr_points = detect_features(curr_frame_gray, mask)
                if prev_points is None or curr_points is None or prev_points.shape[0] < 8 or curr_points.shape[0] < 8:
                    print("Not enough points detected, exiting")
                    break
            
            # Ensure the points are in the correct shape and type
            if prev_points is not None and curr_points is not None:
                prev_points = prev_points.reshape(-1, 2)
                curr_points = curr_points.reshape(-1, 2)
                prev_points = prev_points.astype(np.float32)
                curr_points = curr_points.astype(np.float32)
            
            # Find the essential matrix
            E, mask_e = cv2.findEssentialMat(curr_points, prev_points, focal=1.0, pp=(0.0, 0.0), method=cv2.RANSAC, prob=0.999, threshold=1.0)
            
            if E is None or E.shape != (3, 3):
                print("Invalid essential matrix")
                continue
            
            # Decompose the essential matrix to get the rotation and translation
            _, R, t, _ = cv2.recoverPose(E, curr_points, prev_points, focal=1.0, pp=(0.0, 0.0))
            
            # Update the trajectory
            trajectory = trajectory + R @ t
            poses.append(trajectory)
            
            # Write the current frame number and trajectory to the CSV file
            x, y, z = trajectory.flatten()
            writer.writerow([frame_num, x, y, z])
            
            # Draw the trajectory on the mask
            cv2.circle(mask_draw, (int(x) + 300, int(y) + 300), 1, (0, 0, 255), 2)
            
            # Ensure mask is the same size as the frame
            if mask_draw.shape != frame.shape:
                mask_draw = np.zeros_like(frame)
            
            img = cv2.add(frame, mask_draw)
            
            cv2.imshow('Trajectory', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            prev_frame_gray = curr_frame_gray.copy()
            prev_points = curr_points.reshape(-1, 1, 2)
            
            frame_num += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Plot the 3D trajectory
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    poses = np.array(poses)
    ax.plot(poses[:, 0], poses[:, 1], poses[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

if __name__ == "__main__":
    main()
