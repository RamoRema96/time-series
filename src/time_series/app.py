from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
from preprocessing import PrePro
from validation import Validation
from analysis import Analysis
import os 
import numpy as np
# # Incorporate data
script_dir = os.path.dirname(os.path.realpath(__file__))
# Construct file paths based on the project structure
file_path_train = os.path.join(script_dir, "..", "..", "data", "DailyDelhiClimateTrain.csv")
file_path_test = os.path.join(script_dir, "..", "..", "data", "DailyDelhiClimateTest.csv")

train_data = pd.read_csv(file_path_train)
test_data = pd.read_csv(file_path_test)

prepro = PrePro()
validation = Validation()
analysis = Analysis()

prepro.to_datetime(df=train_data, name_column="date")
prepro.to_datetime(df=test_data, name_column="date")

rolling_window_plot, adfuller_test = analysis.check_stationarity(train_data,"meantemp",12)
lag = int(input("Inserisci il numero di lag: ")) # 3000
acf_plot = analysis.acf_plot(train_data, "meantemp", lag)
period=int(input("Inserisci il periodo della seasonality: ")) #362

decomposition, result = analysis.decomposition_time_series(train_data, "meantemp", period, "Mean Temp" )
residuals = pd.DataFrame({"meantemp":result.resid, "date_datetime":train_data["date_datetime"]})
trend = pd.DataFrame({"meantemp":result.trend, "date_datetime":train_data["date_datetime"]})
seasonality = pd.DataFrame({"meantemp":result.seasonal, "date_datetime":train_data["date_datetime"]})

rolling_window_plot_after_dec, adfuller_test_after_dec = analysis.check_stationarity(residuals, name="meantemp", window_size=12)
forecast_residuals = analysis.forecast_component(residuals,test_data, (1,0,1),)
forecast_trend = analysis.forecast_component(trend, test_data, (1,4,1))
forecast_residuals.reset_index(inplace=True)
forecast_trend.reset_index(inplace=True)

start_date_seasonal = "2013-01-01"
end_date_seasonal = "2013-04-24"
start_date_seasonal = pd.to_datetime(start_date_seasonal)
end_date_seasonal = pd.to_datetime(end_date_seasonal)

forecast_seasonal = seasonality[(seasonality['date_datetime'] >= start_date_seasonal) & (seasonality['date_datetime'] <= end_date_seasonal)]
forecast_seasonal.reset_index(inplace=True)

forecast = pd.DataFrame()
forecast["meantemp"] = forecast_trend["forecast"] + forecast_seasonal["meantemp"]+ forecast_residuals["forecast"]
forecast["date_datetime"] = forecast_trend["date_datetime"]
mse = validation.mse_error(forecast, test_data, "meantemp" )
percentage_error = validation.percentage_error(forecast,test_data,"meantemp")
print(f" Mean squared error: {round(mse,2)}  \n Root Mean Squared error: {round(np.sqrt(mse),2)} \n Percentage error: {round(percentage_error,2)} %")


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(className='row', children='Time Series Analysis',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
    
    html.Div([
        dcc.Graph(
            figure=validation.plot_time_series(df=train_data, x="date", y="meantemp", title=f"Time Series Temperature")
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
    ]),

 html.Div([
        html.H3(children='Rolling Window Analysis'),
        dcc.Graph(figure=rolling_window_plot_after_dec)  
    ]),

 html.Div([
        html.H3(children='ADF Test Results'),
        dcc.Markdown('''
            ADF Statistic: {0} \n
            p-value: {1} \n
            {2}
        '''.format(*adfuller_test_after_dec))
    ]),

html.Div(className='row', children='Autocorrelation function resiudals',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
html.Div([
        dcc.Graph(figure= analysis.acf_plot(residuals, "meantemp", 40))  
    ]),

html.Div(className='row', children='Partial Autocorrelation function resiudals',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
html.Div([
        dcc.Graph(figure= analysis.pacf_plot(residuals, "meantemp", 40))  
    ]),

html.Div(className='row', children='Forecast vs True Values',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
html.Div([
        dcc.Graph(figure=validation.evaluate_forecast_plot(forecast, test_data, "meantemp", "Mean Temperature" ) )  
    ]),

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