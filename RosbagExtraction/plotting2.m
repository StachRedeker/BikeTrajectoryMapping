% Load the CSV files
trajectory_data = readtable('trajectory.csv');
p_data = readtable('data.csv');

% Extract time and coordinates for trajectory data
time_trajectory = trajectory_data.Time;
x_trajectory = trajectory_data.X;
y_trajectory = trajectory_data.Y;
z_trajectory = trajectory_data.Z;

% Extract time and coordinates for p data
time_p = p_data{:,1}; % Assuming the first column is the timestamp
x_p = p_data{:,2}; % Column for p_RS_R_x [m]
y_p = p_data{:,3}; % Column for p_RS_R_y [m]
z_p = p_data{:,4}; % Column for p_RS_R_z [m]

% Plot the trajectory
figure;
plot3(x_trajectory, y_trajectory, z_trajectory, 'b');
hold on;
plot3(x_p, y_p, z_p, 'r');
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Trajectory');
legend('Trajectory', 'P data');
grid on;
hold off;

% Compute the RMSE
rmse_x = sqrt(mean((x_trajectory - x_p).^2));
rmse_y = sqrt(mean((y_trajectory - y_p).^2));
rmse_z = sqrt(mean((z_trajectory - z_p).^2));

% Display RMSE
fprintf('RMSE X: %.4f\n', rmse_x);
fprintf('RMSE Y: %.4f\n', rmse_y);
fprintf('RMSE Z: %.4f\n', rmse_z);

% Compute errors
x_error = x_trajectory - x_p;
y_error = y_trajectory - y_p;
z_error = z_trajectory - z_p;

% Plot X error
figure;
plot(time_trajectory, x_error, 'r');
xlabel('Time');
ylabel('X Error');
title('X Error');
grid on;

% Plot Y error
figure;
plot(time_trajectory, y_error, 'g');
xlabel('Time');
ylabel('Y Error');
title('Y Error');
grid on;

% Plot Z error
figure;
plot(time_trajectory, z_error, 'b');
xlabel('Time');
ylabel('Z Error');
title('Z Error');
grid on;
