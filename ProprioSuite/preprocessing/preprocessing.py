from . import smoothing_methods
import numpy as np
import sqlite3
import re
import matplotlib.pyplot as plt



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
