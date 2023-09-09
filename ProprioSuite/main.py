from preprocessing import *
# Load the data for trial_id "1_1"
data, log = load_trial_data("1_1")
print(log)

# Smooth the data using the moving average method with window size of 100
smoothed_data = smooth_data(data, "moving_average", window_size=100)
