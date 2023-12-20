import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objs as go
class Analysis:
    def __init__(self) -> None:
        pass

    def check_stationarity(self, df:pd.DataFrame, name:str, window_size:int):
        self.__check_stationarity_approx(df, name)
        rolling_window_plot =self.__stationarity_rolling_window(df,name, window_size)
        adfuller_test = self.__adfuller_test(df, name)
        return rolling_window_plot, adfuller_test

    
    
    def __adfuller_test(self, df:pd.DataFrame, name:str):
        time_series_data = df[name]
        result = adfuller(time_series_data)
        ADF_Statistic= result[0]
        p_value = result[1]

        if result[1] <= 0.05:
            test_result = "Reject the null hypothesis. The time series is likely stationary."
    
        else:
            test_result="Fail to reject the null hypothesis. The time series is likely non-stationary."
        return ADF_Statistic, p_value, test_result

    
    def __check_stationarity_approx(self, df:pd.DataFrame, name:str):
        mean1, mean2 = df[:len(df)//2][name].mean(), df[len(df)//2:][name].mean()
        var1, var2 = df[:len(df)//2][name].var(), df[len(df)//2:][name].var()
        print("Approximate stationarity \n")
        print(f' \n Mean 1: {mean1}, \n Mean 2: {mean2} \n')
        print(f' \n Variance 1: {var1}, \n Variance 2: {var2}')
    
    def __stationarity_rolling_window(self, df: pd.DataFrame, name: str, window_size: int):
        df["rolling_mean"] = df[name].rolling(window=window_size).mean()
        df["rolling_standard_deviation"] = df[name].rolling(window=window_size).std()

        # Create a Plotly figure
        fig = go.Figure()

        # Add traces for original, rolling mean, and rolling standard deviation
        fig.add_trace(go.Scatter(x=df.index, y=df[name], mode='lines', name='Original'))
        fig.add_trace(go.Scatter(x=df.index, y=df["rolling_mean"], mode='lines', name='Rolling Mean'))
        fig.add_trace(go.Scatter(x=df.index, y=df["rolling_standard_deviation"], mode='lines', name='Rolling Std'))

        # Add layout information
        fig.update_layout(title='Rolling Window Analysis', xaxis_title='Date', yaxis_title=name)

        # Return the Plotly figure
        return fig

    
        