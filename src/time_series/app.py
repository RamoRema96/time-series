from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
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
lag = int(input("Inserisci il numero di lag: ")) # 3000
acf_plot = analysis.acf_plot(train_data, "meantemp", lag)
period=int(input("Inserisci il periodo della seasonality: ")) #362
decomposition, result = analysis.decomposition_time_series(train_data, "meantemp", period, "Mean Temp" )

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
        dcc.Graph(figure=rolling_window_plot)  
    ]),

 html.Div([
        html.H3(children='ADF Test Results'),
        dcc.Markdown('''
            ADF Statistic: {0} \n
            p-value: {1} \n
            {2}
        '''.format(*adfuller_test))
    ]),

      html.Div([
        html.Label("Select lag:"),
        dcc.Slider(
            id='lag-slider',
            min=1,
            max=5000,
            step=1,
            marks={i: str(i) for i in range(0, 5001, 500)},
            value=3000
        ),
        html.H3(children='Auotocorrelation function analysis'),
        dcc.Graph(id='acf-plot')  
    ], style={'margin': '10px'}),
    
    html.Div([
        html.Label("Select period seasonality:"),
        dcc.Slider(
            id='period-slider',
            min=1,
            max=500,
            step=1,
            marks={i: str(i) for i in range(0, 501, 50)},
            value=362
        ),
        html.H3(children='Decomposition Time Series'),
        dcc.Graph(id="decomposition-plot")  
    ])


])


# Define callback to update acf-plot
@app.callback(
    Output('acf-plot', 'figure'),
    Input('lag-slider', 'value'),
)
def update_acf_plot(lag):
    acf_plot = analysis.acf_plot(train_data, "meantemp", lag)
    return acf_plot

@app.callback(
    Output('decomposition-plot', 'figure'),
    Input('period-slider', 'value'),
)
def update_decomposition_plot(period):
    decomposition, result = analysis.decomposition_time_series(train_data, "meantemp", period, "Mean Temp" )
    return decomposition




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