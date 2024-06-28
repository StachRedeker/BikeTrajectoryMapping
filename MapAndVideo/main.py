from data_processing import load_data, calculate_offsets, filter_points
from video_processing import check_frame_availability
from map_creation import create_map

CSV_FILE_PATH = '73_location_data_round1.csv'
VIDEO_FILE_PATH = 'video.mp4'
VIDEO_START_TIME_STR = '2024-04-10 14:32:45'
MAP_CENTER = (52.238956, 6.855655)
FRAME_OUTPUT_FOLDER = 'frames'

def main():
    print("Loading timestamps.")
    data = load_data(CSV_FILE_PATH)
    print("Calculating offsets.")
    data = calculate_offsets(data, VIDEO_START_TIME_STR)
    print("Connecting video to GPS data.")
    data = check_frame_availability(data, FRAME_OUTPUT_FOLDER, VIDEO_FILE_PATH)
    print("Filter relevant points.")
    data = filter_points(data)
    print("Create map.")
    map = create_map(data, MAP_CENTER)
    map.save('interactive_map.html')
    print("Map has been created and saved as interactive_map.html")

if __name__ == "__main__":
    main()
