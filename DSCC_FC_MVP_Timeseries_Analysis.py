import DSCC_FP_MVP_Configuration as config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error


class TimeSeriesAnalysis:
    def __init__(self, dataframe, col_name) -> None:
        self.dataframe = dataframe
        self.col_name = col_name
        self.series = dataframe[col_name]

    def plotMovingAverage(self, col_to_plot: str, window: int, plot_upperlowerbound=False, scale=1.96, plot_anomalies=False):
        """To plot the moving average, lower and upper bound and find anomaly in data

        Args:
            col_to_plot (str): The selected column to plot
            window (int): Time-period length
            plot_upperlowerbound (bool, optional): Defaults to False.
            scale (float, optional): Defaults to 1.96.
            plot_anomalies (bool, optional): Defaults to False.
        """
        # To select the dataframe and convert from series to frame
        series = self.dataframe[col_to_plot].to_frame()
        # Calculate the mean for a window size
        # Skips the first n window size
        # If window size is 3, then will start shoing values from 3rd row
        rolling_mean = series.rolling(window).mean()
        plt.figure(figsize=(12, 7))
        plt.title('Moving average')
        plt.plot(rolling_mean, 'g', label='Rolling Mean Trend')

        # To plot the upper and lower bound
        # The formula is from https://www.kaggle.com/code/kashnitsky/topic-9-part-1-time-series-analysis-in-python/notebook#Move,-smoothe,-evaluate
        if plot_upperlowerbound:
            mae = mean_absolute_error(series[window:], rolling_mean[window:])
            std_dev = np.std(series[window:]-rolling_mean[window:])
            upper_bound = rolling_mean + (mae + std_dev * scale)
            lower_bound = rolling_mean - (mae + std_dev * scale)
            plt.plot(upper_bound, 'b--', label='Upper Bound')
            plt.plot(lower_bound, 'c--', label='Lower Bound')

        # To find anomalies and plot
        if plot_anomalies:
            # Create a new empty df for anomalies same as the main df
            anomalies = pd.DataFrame(
                index=series.index, columns=series.columns)
            # Fill in the empty df with anomalies from lower and upper bound
            anomalies[series > upper_bound] = series[series > upper_bound]
            anomalies[series < lower_bound] = series[series < lower_bound]
            # Plot the values
            plt.plot(anomalies, 'ro', markersize=10, label='Anomaly')

        # To plot the actual values
        plt.plot(series[window:], label='Actual Values')
        plt.legend(loc='upper left')
        plt.grid(True)

    @staticmethod
    def expotential_smoothing(series, alpha):
        # Takes an series data
        # Alpha values - weight
        # result is a list which is used to store value at previous timestep
        result = [series[0]]
        for i in range(1, len(series)):
            result.append((alpha*series[i])+((1-alpha)*result[i-1]))
        return result

    def plot_expotential_smoothing(self, alphas):
        # For different values of alphas
        plt.figure(figsize=(12, 7))
        plt.title('Expotential Smoothing')
        for i in alphas:
            plt.plot(TimeSeriesAnalysis.expotential_smoothing(
                self.series, i), label=f'Alpha={i}')
        plt.plot(self.series.values, label='Actual')
        plt.legend()

    @staticmethod
    def double_expotential_smoothing(series, alpha, beta):
        level_average = [series[0]]
        slope_trend = [series[1]-series[0]]
        result = [series[0]]
        for i in range(len(series)-1):
            # print(f'y_x is {series[i+1]}, l_x-1 is {level_average[i]}, b_x-1 is {slope_trend[i]}')
            # print(f'Result is {(alpha*series[i+1])+((1-alpha)*(level_average[i]+slope_trend[i]))}')
            level_average.append(
                (alpha*series[i+1])+((1-alpha)*(level_average[i]+slope_trend[i])))
            slope_trend.append(
                (beta*(level_average[i+1]-level_average[i]))+((1-beta)*slope_trend[i]))
            result.append(level_average[i+1]+slope_trend[i+1])
        return result

    def plot_double_expotential_smoothing(self, alphas, betas):
        plt.figure(figsize=(10, 7))
        for alpha in alphas:
            for beta in betas:
                plt.plot(TimeSeriesAnalysis.double_expotential_smoothing(
                    self.series, alpha, beta), label=f'Alpha={alpha} & Beta={beta}')
        plt.plot(self.series, label='Actual Data')
        plt.legend()
        plt.grid(True)


if __name__ == '__main__':
    df = pd.read_csv(
        r'C:\My_Files\LambtonCollege\WIL_Term\code\fetched_data.csv')
    time_analysis = TimeSeriesAnalysis(df, 'Close')
    time_analysis.plotMovingAverage(
        'Close', 30, plot_upperlowerbound=True, plot_anomalies=True)
    time_analysis.plot_expotential_smoothing([0.02, 0.5])
    time_analysis.plot_double_expotential_smoothing([0.02, 0.5], [0.05, 0.08])
    plt.show()
