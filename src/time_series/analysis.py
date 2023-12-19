import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

class Analysis:
    def __init__(self) -> None:
        pass

    def check_stationarity(self, df:pd.DataFrame, name:str, window_size:int):
        self.__check_stationarity_approx(df, name)
        self.__stationarity_rolling_window(df,name, window_size)
        self.__adfuller_test(df, name)

    
    
    def __adfuller_test(self, df:pd.DataFrame, name:str):
        time_series_data = df[name]
        result = adfuller(time_series_data)
        print('ADF Statistic:', result[0])
        print('p-value:', result[1])

        if result[1] <= 0.05:
            print("Reject the null hypothesis. The time series is likely stationary.")
        else:
            print("Fail to reject the null hypothesis. The time series is likely non-stationary.")

    
    def __check_stationarity_approx(self, df:pd.DataFrame, name:str):
        mean1, mean2 = df[:len(df)//2][name].mean(), df[len(df)//2:][name].mean()
        var1, var2 = df[:len(df)//2][name].var(), df[len(df)//2:][name].var()
        print("Approximate stationarity \n")
        print(f' \n Mean 1: {mean1}, \n Mean 2: {mean2} \n')
        print(f' \n Variance 1: {var1}, \n Variance 2: {var2}')
    
    def __stationarity_rolling_window(self, df:pd.DataFrame, name:str, window_size:int ):

        df["rolling_mean"] = df[name].rolling(window=window_size).mean()
        df["rolling_standard_deviation"] = df[name].rolling(window=window_size).std()

        plt.plot(df[name], label='Original')
        plt.plot(df["rolling_mean"], label='Rolling Mean')
        plt.plot(df["rolling_standard_deviation"], label='Rolling Std')
        plt.legend()
        plt.show()

    
        