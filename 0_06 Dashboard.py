from dash import dcc, html, dash, callback
from dash.dependencies import Input, Output  # Make sure these are correctly imported
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import datetime as dt
import pytz

# This is an archived version to show Liam.
# ------------------------------------------------------------------------------------------------

# Read a sample GitHub CSV file
# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Generate time points from 00:00 to 23:30 at 30-minute intervals
times = [
    dt.datetime.combine(dt.date.today(), dt.time(hour, minute))
    for hour in range(24) for minute in range(0, 60, 30)
]

url = 'https://raw.githubusercontent.com/linusrandu/GhostPostCC/main/data/CISO_carbon_from_src_prod_forecasts_direct.csv'
CarbonData = pd.read_csv(url)

# Create sample data using the generated times
sample_data = pd.DataFrame({
    'x': times,  # Time points
    'y': [
        20, 21, 22, 20, 21, 19, 20, 22, 23, 24,
        30, 34, 33, 36, 35, 40, 41, 42, 41, 42,
        53, 52, 54, 56, 58, 60, 58, 57, 64, 65,
        70, 72, 70, 78, 82, 74, 68, 63, 62, 61,
        60, 58, 54, 56, 52, 55, 61, 54, 51, 50,
        46, 43, 44, 42, 45, 40, 39, 37, 32, 30,
        32, 35, 30, 29, 27, 29, 24, 23, 24, 23,
        21, 22, 20, 23, 20, 24, 22, 25, 26, 29,
        31, 30, 36, 34, 38, 40, 45, 44, 45, 40,
        39, 38, 36, 32, 35, 34, 29, 27, 25, 29
    ][:len(times)]  # Match 'y' values with 'x' values
})
sample_data['x'] = sample_data['x'].dt.strftime('%H:%M')  # Format the time for display

def round_time(dt_time, round_to):
    seconds = (dt_time.replace(tzinfo=None) - dt.datetime.min).seconds
    rounding = (seconds+round_to/2) // round_to * round_to
    return dt_time + dt.timedelta(0,rounding-seconds,-dt_time.microsecond)

# Get the current time in Ohio (Eastern Time Zone)
now = dt.datetime.now(pytz.timezone('US/Eastern'))

# Round the current time to the nearest half hour
current_time = round_time(now, 30*60)  # 30 minutes is 1800 seconds

# Add two hours to the current time and round to the nearest half hour

# Format the times as strings in the format "HH:MM"
current_time_str = current_time.strftime("%H:%M")

# Add an hour to the current time
current_time_plus_one_hour = current_time + dt.timedelta(hours=2)

# Format the times as strings in the format "HH:MM"
current_time_str_plus_one_hour = current_time_plus_one_hour.strftime("%H:%M")


energy_mix = {
    'Coal': 33,
    'Nuclear': 22,
    'Natural Gas': 32,
    'Hydro': 6,
    'Wind': 5,
    'Solar': 2
}

app.layout = dbc.Container(
    fluid=True, 
    style={'backgroundColor': '#1b0723', 'minHeight': '100vh', 'padding': '20px'}, 
    children=[
        dbc.Row([
            dbc.Col([
                html.A('Go back to website', href='http://ghostposts.ai', style={
                    'color': '#c876fe', 
                    'backgroundColor': '#36213d', 
                    'padding': '10px 20px', 
                    'borderRadius': '5px', 
                    'textDecoration': 'none', 
                    'display': 'inline-block', 
                }),
            ], width={"size": 4}, style={"textAlign": "left"}),
            dbc.Col([
                html.H1('Carbon Dashboard', style={'color': 'white', 'textAlign': 'center'}),
            ], width={"size": 4}),
            dbc.Col([
                html.Img(src='https://github.com/AdamSarissky/Test/blob/main/Untitled%20design.png?raw=true', style={'width': '200px'}),
            ], width={"size": 4}, style={"textAlign": "right"}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card(style={'margin': '20px 1px 1px 1px', 'backgroundColor': '#36213d', 'padding': '10px', 'height': '100%'}, children=[
                    dbc.CardBody([
                        html.Div(style={'display': 'grid', 'gridGap': '10px'}, children=[
                            html.Label('Select number of tokens:', style={'color': 'white'}),
                            dcc.Input(id='number-input', type='number', min=0, max=1000, step=1, value=500, style={
                                'color': 'black', 'backgroundColor': 'white', 'borderRadius': '30px'}),
                            html.Label('Select device:', style={'color': 'white'}),
                            dcc.Dropdown(
                                id='device-dropdown',
                                options=[{'label': i, 'value': i} for i in ['banana', 'orange']],
                                value='banana',
                                style={'backgroundColor': 'white', 'color': 'black', 'borderRadius': '30px'}),
                            html.Label('Select connection type:', style={'color': 'white'}),
                            dcc.Dropdown(
                                id='connection-dropdown',
                                options=[{'label': i, 'value': i} for i in ['will of god', 'science']],
                                value='will of god',
                                style={'backgroundColor': 'white', 'color': 'black', 'borderRadius': '30px'}),
                            dcc.Graph(id='donut-chart', figure={
                        'data': [
                                        go.Pie(
                                            labels=list(energy_mix.keys()),
                                            values=list(energy_mix.values()),
                                            hole=0.8,  # Reduced hole size for more label space
                                            textinfo='label+percent',
                                            textposition='outside',
                                            insidetextorientation='radial',
                                            marker_colors=['#6a0575', '#9b00a6', '#b900b4', '#d300c2', '#ed00d1', '#ff80e5'],
                                            hovertemplate="<b>%{label}</b> (%{percent})<extra></extra>",  # Customize hover here

                                        )
                                    ],
                                    'layout': go.Layout(
                                        title='Current Energy Mix',
                                        plot_bgcolor='#36213d',
                                        paper_bgcolor='#36213d',
                                        font=dict(color='#d4c2dd'),
                                        showlegend=False,
                                        margin={'l': 40, 'r': 40, 't': 50, 'b': 40}  # Increased margins
                                    )
                                }, style={'height': '350px'})  # Optionally increase the height
                        ])
                    ])
                ]),
            ], width=4),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card(style={'margin': '10px', 'backgroundColor': '#36213d', 'padding': '20px'}, children=[
                            html.H4('Estimated CO2 emissions and water consumption associated with your use of the ghostposts.ai platform are:', style={'textAlign': 'justify', 'color': 'white', 'fontSize': '18px'}),
                            html.H5(id='dynamic-x-value', style={'textAlign': 'center', 'color': 'white', 'fontSize': '24px'})  # This element will display the dynamic X and L
                        ]),
                    ], width=6),
                    dbc.Col([
                        dbc.Card(style={'margin': '10px', 'backgroundColor': '#36213d', 'padding': '20px'}, children=[
                            html.H4("OpenAI’s servers consume a great amount of electricity and water for cooling. By 2027 AI may guzzle power equaling the Netherlands' usage every year. This dashboard is a tool to calculate the emissions associated with your usage of OpenAI’s servers that ghost posts.ai platform uses.", style={'textAlign': 'justify', 'color': 'white', 'fontSize' : '14px'}),
                        ]),
                    ], width=6),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(style={'margin': '10px', 'backgroundColor': '#36213d', 'height': '100%'}, children=[
                            dbc.CardBody([
                                dcc.Graph(id='line-chart', figure={
                                    'data': [
                                        go.Scatter(
                                            x=sample_data['x'],
                                            y=sample_data['y'],
                                            mode='lines',
                                            name='CO2 Emissions',
                                            line=dict(color='#c876fe')
                                        ),
                                    ],
                                    'layout': go.Layout(
                                        title='Predicted grams of CO2 per KWh',
                                        title_font=dict(color='white'),  # Change title color here
                                        xaxis=dict(
                                            title='Time UTC-4',
                                            title_font=dict(color='#c876fe'),  # Change x-axis title color here
                                            tickfont=dict(color='#c876fe'),
                                            nticks=12  # Limit the number of tick labels
                                         # Change x-axis tick labels color here
                                        ),
                                        yaxis=dict(
                                            title='CO2',
                                            title_font=dict(color='#d4c2dd'),  # Change y-axis title color here
                                            tickfont=dict(color='#d4c2dd')  # Change y-axis tick labels color here
                                        ),
                                        plot_bgcolor='#36213d',
                                        paper_bgcolor='#36213d',
                                        shapes=[
                                            dict(
                                                type="line",
                                                x0=current_time_str,
                                                y0=0,
                                                x1=current_time_str,
                                                y1=1,
                                                yref="paper",
                                                line=dict(
                                                    color="#b4dd40",
                                                    width=2,
                                                    dash="dot",
                                                ),
                                            )
                                        ],
                                        annotations=[
                                            dict(
                                                x=current_time_str_plus_one_hour,
                                                y=0.95,
                                                yref="paper",
                                                text="current emissions",
                                                showarrow=False,
                                                font=dict(
                                                    size=12,
                                                    color="#b4dd40"
                                                ),
                                            ),
                                             dict(
                                                xref='paper',
                                                yref='paper',
                                                x=0.5,  # Center position
                                                y=-0.9,  # Adjust vertical position below the x-axis
                                                text="Using U.S. midwest time, where OpenAI's servers are located",
                                                showarrow=False,
                                                font=dict(
                                                    size=12,
                                                    color="white"
                                                ),
                                                align="right"
                                            )
                                        ]
                                    )
                                })
                            ])
                        ]),
                    ], width=12),
                ]),
            ], width=8),
        ]),
    ]
)


@app.callback(
    Output('dynamic-x-value', 'children'),
    [Input('number-input', 'value'),
     Input('device-dropdown', 'value'),
     Input('connection-dropdown', 'value')]
)
def update_dynamic_x(number, device, connection):
    if number is None:
        return "Please enter a valid number of tokens"

    # Calculation for x_value based on the device and connection
    x_value = number * 0.1 * 5
    if device == 'banana':
        x_value *= 2
    elif device == 'orange':
        x_value *= 5

    if connection == 'will of god':
        x_value *= 2
    elif connection == 'science':
        x_value /= 2

    # New calculation for L based on the number input
    L = number * 0.2

    # Format the string to be displayed in the H5 component
    return f"{round(x_value, 1)} tons and {round(L, 1)} liters"

# Run the server in debug mode
if __name__ == '__main__':
    app.run_server(debug=True)
