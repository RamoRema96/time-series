from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
from preprocessing import PrePro
from validation import Plot
from analysis import Analysis
# Incorporate data
file_path_train = "/Users/omare/Desktop/personal_project/time-series/data/DailyDelhiClimateTrain.csv"
train_data = pd.read_csv(file_path_train)
prepro = PrePro()
plot = Plot()
analysis = Analysis()
prepro.to_datetime(df=train_data, name_column="date")
rolling_window_plot, adfuller_test = analysis.check_stationarity(train_data,"meantemp",12)
print(adfuller_test)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(className='row', children='Time Series Analysis',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
    
    html.Div([
        dcc.Graph(
            figure=plot.plot_time_series(df=train_data, x="date", y="meantemp", title=f"Time Series Temperature")
        )
    ], style={'margin': '10px'}),  # Adjust margin as needed
    
    html.Div([
        html.H3(children='Rolling Window Analysis'),
        dcc.Graph(figure=rolling_window_plot)  # Use the returned figure here
    ]),

 html.Div([
        html.H3(children='ADF Test Results'),
        dcc.Markdown('''
            ADF Statistic: {0} \n
            p-value: {1} \n
            {2}
        '''.format(*adfuller_test))
    ])



])






# Run the app
if __name__ == '__main__':
    app.run(debug=True)

# Add this line to stop the server when the script is interrupted
try:
    # This blocks execution until the server is stopped by pressing Ctrl+C
    while True:
        pass
except KeyboardInterrupt:
    # When Ctrl+C is pressed, stop the server and exit
    print("\nStopping the Dash app...")