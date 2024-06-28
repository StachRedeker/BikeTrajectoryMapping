% Load the CSV file
data = readtable('trajectory.csv');

% Extract time and coordinates
time = data.Time;
x = data.X;
y = data.Y;
z = data.Z;

% Plot the trajectory
figure;
plot3(x, y, z, 'b');
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Trajectory');
grid on;
