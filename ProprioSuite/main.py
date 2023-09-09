from preprocessing import *
from analysis import *

# Load the data for trial_id "1_1"
try:
    db_path = "../data/proprio.db"  # Replace with the actual path
    trial_id = "1_1"
    temp_data = load_trial_data(trial_id, db_path)
    if temp_data:
        print("Data loaded successfully." )
    else:
        print("Failed to load data.")
except Exception as e:
    print("An error occurred:", e)

# Smooth the data using the moving average method with window size of 100
smooth_object = smooth_data(temp_data, MovingAverage, window_size=100)

smooth_data = smooth_object.get_data()

smooth_object.show_plot()

results = xy_summaries(smooth_data)

print(results)