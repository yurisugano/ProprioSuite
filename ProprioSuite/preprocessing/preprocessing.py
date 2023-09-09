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
    
class SmoothingMethod:
    def __init__(self, data):
        self.time = data[:, 0]
        self.x = data[:, 1]
        self.y = data[:, 2]

    def smooth(self):
        raise NotImplementedError("Each smoothing method should implement this method.")

    def adjust_time(self):
        raise NotImplementedError("Each smoothing method should adjust the time accordingly.")


class MovingAverage(SmoothingMethod):
    def __init__(self, data, window_size):
        super().__init__(data)
        self.window_size = window_size

    def smooth(self):
        kernel = np.ones(self.window_size) / self.window_size
        smoothed_x = convolve(self.x, kernel, mode='valid')
        smoothed_y = convolve(self.y, kernel, mode='valid')
        return smoothed_x, smoothed_y

    def adjust_time(self):
        adjusted_length = len(self.x) - self.window_size + 1
        return self.time[-adjusted_length:]


class WeightedMovingAverage(SmoothingMethod):
    def __init__(self, data, window_size):
        super().__init__(data)
        self.window_size = window_size

    def smooth(self):
        weights = np.arange(1, self.window_size + 1)
        smoothed_x = convolve(self.x, weights / weights.sum(), mode='valid')
        smoothed_y = convolve(self.y, weights / weights.sum(), mode='valid')
        return smoothed_x, smoothed_y

    def adjust_time(self):
        adjusted_length = len(self.x) - self.window_size + 1
        return self.time[-adjusted_length:]


class ExponentialMovingAverage(SmoothingMethod):
    def __init__(self, data, alpha=0.3):
        super().__init__(data)
        self.alpha = alpha

    def smooth(self):
        smoothed_x = pd.Series(self.x).ewm(alpha=self.alpha).mean().values
        smoothed_y = pd.Series(self.y).ewm(alpha=self.alpha).mean().values
        return smoothed_x, smoothed_y

    def adjust_time(self):
        return self.time


class GaussianSmoothing(SmoothingMethod):
    def __init__(self, data, window_size):
        super().__init__(data)
        self.window_size = window_size

    def smooth(self):
        window = gaussian(self.window_size, self.window_size / 3)
        smoothed_x = convolve(self.x, window / window.sum(), mode='valid')
        smoothed_y = convolve(self.y, window / window.sum(), mode='valid')
        return smoothed_x, smoothed_y

    def adjust_time(self):
        adjusted_length = len(self.x) - self.window_size + 1
        return self.time[-adjusted_length:]


class SavitzkyGolay(SmoothingMethod):
    def __init__(self, data, window_size, polynomial_order=2):
        super().__init__(data)
        self.window_size = window_size
        self.polynomial_order = polynomial_order

    def smooth(self):
        smoothed_x = savgol_filter(self.x, self.window_size, self.polynomial_order)
        smoothed_y = savgol_filter(self.y, self.window_size, self.polynomial_order)
        return smoothed_x, smoothed_y

    def adjust_time(self):
        return self.time


class MedianFilter(SmoothingMethod):
    def __init__(self, data, window_size):
        super().__init__(data)
        self.window_size = window_size

    def smooth(self):
        smoothed_x = medfilt(self.x, self.window_size)
        smoothed_y = medfilt(self.y, self.window_size)
        return smoothed_x, smoothed_y

    def adjust_time(self):
        return self.time


class SmoothedData:
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def show_plot(self):
        plt.show()


def smooth_data(raw_data, method_class, **kwargs):
    method_instance = method_class(raw_data, **kwargs)
    smoothed_x, smoothed_y = method_instance.smooth()
    adjusted_time = method_instance.adjust_time()

    smoothed_data = np.column_stack((adjusted_time, smoothed_x, smoothed_y))

    # ... [Plotting code]
    plt.figure(figsize=(10, 6))
    plt.plot(adjusted_time, smoothed_x, 'r-', label="Smoothed X")
    plt.plot(adjusted_time, smoothed_y, 'b-', label="Smoothed Y")
    plt.title("Smoothed Data")
    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.legend()

    return SmoothedData(smoothed_data)
