from scipy.signal import savgol_filter, medfilt, convolve, gaussian
import numpy as np
import pandas as pd

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
