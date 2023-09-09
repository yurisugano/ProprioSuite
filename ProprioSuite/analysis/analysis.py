from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import euclidean
from scipy.stats import circmean
import numpy as np

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
    
    return round_values(summaries)

def round_values(d):
    """Rounds all values in a dictionary to 2 decimal places."""
    return {k: round(v, 2) for k, v in d.items()}