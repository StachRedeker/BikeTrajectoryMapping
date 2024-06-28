import rosbag
import pandas as pd

# Path to the bag file
bag_file = 'trajectory.bag'

# Topic to extract
topic_name = '/qxc_robot/system/odom'  # Replace with the identified topic name

# Open the bag file
bag = rosbag.Bag(bag_file)

# Lists to hold the data
times = []
x_coords = []
y_coords = []
z_coords = []

# Extract data from the bag file
for topic, msg, t in bag.read_messages(topics=[topic_name]):
    times.append(t.to_sec())
    x_coords.append(msg.pose.pose.position.x)
    y_coords.append(msg.pose.pose.position.y)
    z_coords.append(msg.pose.pose.position.z)

# Create a DataFrame
data = {'Time': times, 'X': x_coords, 'Y': y_coords, 'Z': z_coords}
df = pd.DataFrame(data)

# Save DataFrame to CSV
csv_file = 'trajectory.csv'
df.to_csv(csv_file, index=False)

print(f'Trajectory data saved to {csv_file}')

