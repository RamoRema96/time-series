import pandas as pd
import plotly.express as px

class Plot:
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
        #fig.show()