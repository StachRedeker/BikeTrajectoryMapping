import imageio
import os
from moviepy.editor import VideoFileClip

# Check if frames are already extracted
def check_frame_availability(data, output_folder, video_path):
    if not os.path.exists(output_folder) or not os.listdir(output_folder):
        # If the folder doesn't exist or is empty, extract frames
        data = extract_frames(data, video_path, output_folder)
    else:
        # If frames exist, assign paths to DataFrame
        for index in range(len(data)):
            frame_path = f'{output_folder}/frame_{index}.jpg'
            if os.path.exists(frame_path):
                data.at[index, 'frame_path'] = frame_path
    return data

# Extract video frames for corresponding timestamps
def extract_frames(data, video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    clip = VideoFileClip(video_path)
    for index, row in data.iterrows():
        frame_time = row['time_offset']
        if frame_time >= 0 and frame_time <= clip.duration:
            frame_path = f'{output_folder}/frame_{index}.jpg'
            if not os.path.exists(frame_path):  # Only save if the frame does not already exist
                frame = clip.get_frame(frame_time)
                imageio.imwrite(frame_path, frame)
            data.at[index, 'frame_path'] = frame_path
    clip.close()
    return data
