import numpy as np
import sqlite3
import re
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, medfilt, convolve, gaussian
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import euclidean
from scipy.stats import circmean


def load_trial_data(trial_id, db_path):
    """
    Load x and y coordinates as a numpy time series for a given trial_id.

    Parameters:
    - trial_id (str): ID of the trial. Should be in the format x_n where x is an integer and n is from 1 to 4.

    Returns:
    - numpy array: Time series data of x and y coordinates.
    """

    try:
        # Establish a connection to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch data from the database for the given trial_id
        all_data_query = "SELECT trial_id, time, x, y FROM pointing_rawdata WHERE trial_id = ?;"
        all_data = cursor.execute(all_data_query, (trial_id,)).fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # 3. Calculate % missing frames
        missing_frames = [row for row in all_data if row[2] in ("-", None) or row[3] in ("-", None)]
        n_missing = len(missing_frames)
        n_data = len(all_data)
        percent_missing = (len(missing_frames) / len(all_data)) * 100
    
        # Check if data was retrieved
        if n_data > 0:
            # 4. Filter out missing frames and return x, y as numpy array
            valid_data = [row for row in all_data if row not in missing_frames]
            numpy_data = np.array(valid_data, dtype=float)[:, 1:]  # Exclude trial_id from the numpy array
            return(numpy_data)

        else:
            print(f"No data found for trial_id: {trial_id}")
            return None

    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return None
    
# Helper functions for smoothing methods

def moving_average(data, window_size):
    kernel = np.ones(window_size) / window_size
    return convolve(data, kernel, mode='valid')

def weighted_moving_average(data, window_size):
    weights = np.arange(1, window_size + 1)
    return convolve(data, weights/weights.sum(), mode='valid')

def exponential_moving_average(data, alpha=0.3):
    return pd.Series(data).ewm(alpha=alpha).mean().values

def gaussian_smoothing(data, window_size):
    window = gaussian(window_size, window_size/3)
    return convolve(data, window/window.sum(), mode='valid')

def savitzky_golay(data, window_size, polynomial_order=2):
    return savgol_filter(data, window_size, polynomial_order)

def median_filter(data, window_size):
    return medfilt(data, window_size)

class SmoothedData:
    def __init__(self, data):
        self.data = data
    
    def get_data(self):
        return self.data
    
    def show_plot(self):
        plt.show()
    

def smooth_data(raw_data, method, **kwargs):
    # Split the raw data into x and y coordinates
    x, y = raw_data[:, 1], raw_data[:, 2]
    
    # Map method names to functions
    methods = {
        "moving_average": moving_average,
        "weighted_moving_average": weighted_moving_average,
        "exponential_moving_average": exponential_moving_average,
        "gaussian_smoothing": gaussian_smoothing,
        "savitzky_golay": savitzky_golay,
        "median_filter": median_filter
    }
    
    # Check if the method exists
    if method not in methods:
        raise ValueError(f"Method {method} not recognized.")
    
    # Apply the selected method to smooth the data
    smoothed_x = methods[method](x, **kwargs)
    smoothed_y = methods[method](y, **kwargs)
    
    # Combine smoothed x and y into a numpy array
    smoothed_data = np.column_stack((smoothed_x, smoothed_y))
    
    # Plotting the raw and smoothed data
    time = np.arange(len(x))
    plt.figure(figsize=(10, 6))
    plt.plot(time, x, 'r--', label="Raw X")
    plt.plot(time, y, 'b--', label="Raw Y")
    plt.plot(time[len(time) - len(smoothed_x):], smoothed_x, 'r-', label="Smoothed X")
    plt.plot(time[len(time) - len(smoothed_y):], smoothed_y, 'b-', label="Smoothed Y")
    
    plt.title("Raw vs Smoothed Data")
    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.legend()
    
    print(f"Data smoothed using {method} method.")
    
    return SmoothedData(smoothed_data)

def xy_summaries(data):
    # 1. Center the first frame at 0,0
    centered_data = data.copy()
    centered_data[:, 1] -= data[0, 1]
    centered_data[:, 2] -= data[0, 2]
    
    # Compute distances between consecutive points for total_excursion and velocities
    distances = [euclidean(centered_data[i, 1:], centered_data[i+1, 1:]) for i in range(len(centered_data)-1)]
    total_excursion = sum(distances)
    
    # Compute time differences for velocity calculations
    time_diffs = np.diff(centered_data[:, 0])
    velocities = np.array(distances) / time_diffs
    vel_mean = np.mean(velocities)
    vel_max = np.max(velocities)
    
    # final_length and final_angle
    final_point = centered_data[-1, 1:]
    final_length = euclidean(final_point, [0, 0])
    final_angle = np.degrees(np.arctan2(final_point[1], final_point[0]))
    
    # mean_angle
    angles = np.arctan2(centered_data[:, 2], centered_data[:, 1])
    mean_angle = np.degrees(circmean(angles))
    
    # x and y statistics
    x_variance = np.var(centered_data[:, 1])
    y_variance = np.var(centered_data[:, 2])
    x_range = np.ptp(centered_data[:, 1])
    y_range = np.ptp(centered_data[:, 2])
    
    # Quadrant percentages
    q1 = len(centered_data[(centered_data[:, 1] >= 0) & (centered_data[:, 2] >= 0)]) / len(centered_data)
    q2 = len(centered_data[(centered_data[:, 1] < 0) & (centered_data[:, 2] >= 0)]) / len(centered_data)
    q3 = len(centered_data[(centered_data[:, 1] < 0) & (centered_data[:, 2] < 0)]) / len(centered_data)
    q4 = len(centered_data[(centered_data[:, 1] >= 0) & (centered_data[:, 2] < 0)]) / len(centered_data)
    
    summaries = {
        "total_excursion": total_excursion,
        "vel_mean": vel_mean,
        "vel_max": vel_max,
        "final_length": final_length,
        "final_angle": final_angle,
        "mean_angle": mean_angle,
        "x_variance": x_variance,
        "y_variance": y_variance,
        "x_range": x_range,
        "y_range": y_range,
        "pct_1q": q1 * 100,
        "pct_2q": q2 * 100,
        "pct_3q": q3 * 100,
        "pct_4q": q4 * 100,
    }
    
    return summaries
