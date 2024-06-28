import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def compare_results(truth_preprocess_path, prediction_path):
    # Compare truth and prediction data
    print("Comparing results...")
    # Plot results in 3D or 2D space
    # Example placeholder code for plotting:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Load data and plot
    # truth_data = ...
    # prediction_data = ...

    # ax.plot(truth_data_x, truth_data_y, truth_data_z, label='Truth')
    # ax.plot(prediction_data_x, prediction_data_y, prediction_data_z, label='Prediction')

    plt.legend()
    plt.show()
    pass

