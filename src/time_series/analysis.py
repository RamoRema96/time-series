import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objs as go
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.arima.model import ARIMA
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
        fig.add_trace(go.Scatter(x=df["date_datetime"], y=df[name], mode='lines', name='Original'))
        fig.add_trace(go.Scatter(x=df["date_datetime"], y=df["rolling_mean"], mode='lines', name='Rolling Mean'))
        fig.add_trace(go.Scatter(x=df["date_datetime"], y=df["rolling_standard_deviation"], mode='lines', name='Rolling Std'))

        # Add layout information
        fig.update_layout(title='Rolling Window Analysis', xaxis_title='Date', yaxis_title=name)

        # Return the Plotly figure
        return fig
    
    def acf_plot(self, df:pd.DataFrame, name:str, lags:int):

        acf_values = acf(df[name], nlags=lags)
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=list(range(lags + 1)), y=acf_values, mode='lines+markers', name='ACF'))

        fig.update_layout(title='Autocorrelation Function (ACF) Plot',
                      xaxis=dict(title='Lag'),
                      yaxis=dict(title='Autocorrelation'),
                      showlegend=True)

        return fig
    
    def pacf_plot(self, df: pd.DataFrame, name: str, lags: int):
        pacf_values = pacf(df[name], nlags=lags)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=list(range(lags + 1)), y=pacf_values, mode='lines+markers', name='PACF'))

        fig.update_layout(title='Partial Autocorrelation Function (PACF) Plot',
                          xaxis=dict(title='Lag'),
                          yaxis=dict(title='Partial Autocorrelation'),
                          showlegend=True)

        return fig

    def decomposition_time_series(self, df:pd.DataFrame, name:str, period:int, title:str):
        result = STL(df[name], period=period).fit()

       # Create an interactive plot with Plotly
        fig = go.Figure()

        # Oiginal Series
        fig.add_trace(go.Scatter(x=df["date_datetime"], y=df['meantemp'], mode='lines', name='Original Series'))

        # Trend Component
        fig.add_trace(go.Scatter(x=df["date_datetime"], y=result.trend, mode='lines', name='Trend Component'))

        # Seasonal Component
        fig.add_trace(go.Scatter(x=df["date_datetime"], y=result.seasonal, mode='lines', name='Seasonal Component'))

        #  Residual Component
        fig.add_trace(go.Scatter(x=df["date_datetime"], y=result.resid, mode='lines', name='Residual Component'))

       # Update layout
        fig.update_layout(title='Time Series Decomposition',
                      xaxis=dict(title='Date'),
                      yaxis=dict(title=title),
                      showlegend=True)

        return fig, result
    def forecast_component(self,train: pd.DataFrame, test:pd.DataFrame, order: tuple):
    #train_size = int(len(df) * train_used)  # 80% for training
    
    
        model = ARIMA(train['meantemp'], order=order)
        fitted_model = model.fit()

        # Forecast future values
        forecast_steps = len(test)
        predictions = fitted_model.get_forecast(steps=forecast_steps)

        # Create a DataFrame with forecast values and corresponding dates
        forecast_dates = pd.date_range(start=train['date_datetime'].iloc[-1], periods=forecast_steps, freq='D')
        forecast_df = pd.DataFrame({'date_datetime': forecast_dates, 'forecast': predictions.predicted_mean})

        return forecast_df


    
        