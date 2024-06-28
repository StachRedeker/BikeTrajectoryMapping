% MATLAB script to convert ROS bag file to MATLAB format
bag = rosbag('trajectory4.bag');

% Display all topics in the bag file
bag.AvailableTopics

% Select the topic you are interested in
odom_topic = select(bag, 'Topic', '/qxc_robot/system/odom');

% Read messages from the topic
odom_msgs = readMessages(odom_topic);

% Initialize arrays to store data
times = zeros(length(odom_msgs), 1);
x_coords = zeros(length(odom_msgs), 1);
y_coords = zeros(length(odom_msgs), 1);
z_coords = zeros(length(odom_msgs), 1);

% Extract data from the messages
for i = 1:length(odom_msgs)
    times(i) = odom_topic.MessageList.Time(i);
    x_coords(i) = odom_msgs{i}.Pose.Pose.Position.X;
    y_coords(i) = odom_msgs{i}.Pose.Pose.Position.Y;
    z_coords(i) = odom_msgs{i}.Pose.Pose.Position.Z;
end

% Create a table and save it to a CSV file
data = table(times, x_coords, y_coords, z_coords, 'VariableNames', {'Time', 'X', 'Y', 'Z'});
writetable(data, 'trajectory.csv');

disp('Trajectory data saved to trajectory.csv');
