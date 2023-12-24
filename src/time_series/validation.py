import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
class Validation:
    def __init__(self) -> None:
        pass

    def plot_time_series(self, df:pd.DataFrame, x:str, y:str, title:str, verbose = False):
        '''
        This function plot the time series in a fancy way. You can zoom etc..

        Arguments:
        df(pd.Dataframe): it is the time series
        x(str): it is the column name of the dates
        y(str): it is the column name of the value you want to plot
        '''
        fig = px.line(df, x=x, y=y, title=title)

    
        fig.update_layout(
        xaxis_title='Date',
        yaxis_title=f"{y}",
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=30),  
        template='plotly',  
    )

    
        if verbose:
            fig.write_html(f'{title}.html')
        return fig
    
    def mse_error(self, forecast:pd.DataFrame, test_data:pd.DataFrame, name:str):
        """
        Calculate the Mean Squared Error (MSE) between forecasted and actual values.

        Parameters:
            forecast (pd.DataFrame): DataFrame containing forecasted values and dates.
            test_data (pd.DataFrame): DataFrame containing actual values and dates for comparison.
            name (str): The name of the column representing the time series.

        Returns:
            float: The Mean Squared Error (MSE) between forecasted and actual values.

        """
        return ((forecast[name] - test_data[name])**2).mean()
    
    
    
    def percentage_error(self, forecast: pd.DataFrame, test_data: pd.DataFrame, name: str):
        """
        Calculate the Percentage Error between forecasted and actual values.

        Parameters:
            forecast (pd.DataFrame): DataFrame containing forecasted values and dates.
            test_data (pd.DataFrame): DataFrame containing actual values and dates for comparison.
            name (str): The name of the column representing the time series.

        Returns:
            float: The Percentage Error between forecasted and actual values.

        """
        n = len(test_data)
        percentage_error = (1 / n) * ((test_data[name] - forecast[name]) / test_data[name])**2
        percentage_error = percentage_error.sum() * 100
        return percentage_error
    
    def evaluate_forecast_plot(self, forecast:pd.DataFrame, test_data:pd.DataFrame, name:str, y_label:str):
        """
        Create a Plotly figure for visual evaluation of forecasted and actual values.

        Parameters:
            forecast (pd.DataFrame): DataFrame containing forecasted values and dates.
            test_data (pd.DataFrame): DataFrame containing actual values and dates for comparison.
            name (str): The name of the column representing the time series.
            y_label (str): The label for the y-axis.

        Returns:
            go.Figure: A Plotly figure comparing actual and forecasted values.

        """
        actual_values = test_data[name]
        forecast_values = forecast[name]
        actual_trace = go.Scatter(x=test_data['date_datetime'], y=actual_values, mode='lines', name='Actual')
        forecast_trace = go.Scatter(x=forecast['date_datetime'], y=forecast_values, mode='lines', name='Forecast')
        layout = go.Layout(title='Actual vs Forecasted Values', xaxis=dict(title='Date'), yaxis=dict(title=f'{y_label}'))
        fig = go.Figure(data=[actual_trace, forecast_trace], layout=layout)

        return fig