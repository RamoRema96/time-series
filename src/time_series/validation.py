import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        return ((forecast[name] - test_data[name])**2).mean()
    

    def evaluate_forecast_plot(self, forecast:pd.DataFrame, test_data:pd.DataFrame, name:str, y_label:str):
        actual_values = test_data[name]
        forecast_values = forecast[name]
        actual_trace = go.Scatter(x=test_data['date_datetime'], y=actual_values, mode='lines', name='Actual')
        forecast_trace = go.Scatter(x=forecast['date_datetime'], y=forecast_values, mode='lines', name='Forecast')
        layout = go.Layout(title='Actual vs Forecasted Values', xaxis=dict(title='Date'), yaxis=dict(title=f'{y_label}'))
        fig = go.Figure(data=[actual_trace, forecast_trace], layout=layout)

        return fig