import re
import numpy as np

def load_trial_data(trial_id):
    """
    Load x and y coordinates as a numpy time series for a given trial_id.

    Parameters:
    - trial_id (str): ID of the trial. Should be in the format x_n where x is an integer and n is from 1 to 4.

    Returns:
    - numpy array: Time series data of x and y coordinates.
    """

    # Check if trial_id is a string
    if not isinstance(trial_id, str):
        raise ValueError("Input trial_id should be a string.")
    
    # Check if trial_id is in the format x_n
    if not re.match(r"^\d_[1-4]$", trial_id):
        raise ValueError("Input trial_id should be in the format x_n where x is an integer and n is a number from 1 to 4.")
    
    # Fetch data from the database for the given trial_id
    cursor_original.execute("SELECT x, y FROM tracking_raw_controls WHERE trial_id=?", (trial_id,))
    data = cursor_original.fetchall()
    
    # Check if data was retrieved
    if not data:
        raise ValueError(f"trial_id {trial_id} not found in the database.")
    
    # Convert data to numpy array
    time_series_data = np.array(data)
    
    # Log the successful loading
    log_message = f"trial {trial_id} successfully loaded with {len(data)} rows"
    
    return time_series_data, log_message

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, medfilt, convolve, gaussian
from scipy.ndimage import gaussian_filter1d
import numpy as np

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
    def __init__(self, data, log_message):
        self.data = data
        self.log_message = log_message
    
    def get_data(self):
        return self.data
    
    def show_plot(self):
        plt.show()
    
    def __repr__(self):
        return self.log_message


def smooth_data(raw_data, method, **kwargs):
    # Split the raw data into x and y coordinates
    x, y = raw_data[:, 0], raw_data[:, 1]
    
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
    
    log_message = f"Data smoothed using {method} method."
    
    return SmoothedData(smoothed_data, log_message)
