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

# Test the function with trial_id = "1_1"
load_trial_data("1_1")
