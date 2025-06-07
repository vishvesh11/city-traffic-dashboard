import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np


df = pd.read_csv("futuristic_city_traffic.csv")

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.FLATLY])


 # dashboard initialization
numerical_df = df.select_dtypes(include=np.number)
correlation_matrix = numerical_df.corr()

# Define the layout of the dashboard
app.layout = html.Div(id='dashboard-container', children=[
    dcc.Store(id='theme-store', data='light'), # Initial theme is white

    # Row for the title and dark mode toggle
    dbc.Row([
        dbc.Col(html.H1("Traffic Data Analysis Dashboard", style={'text-align': 'center', 'color': 'inherit'}), width=10),
        dbc.Col(
            dbc.Switch(
                id='dark-mode-toggle',
                label="Dark Mode",
                value=False,
                style={'margin-top': '20px', 'text-align': 'right', 'color': 'inherit'}
            ),
            width=2,
            align="end"
        )
    ], justify="center", align="center", style={'padding': '20px'}),

    # Filters (City and Vehicle Type)
    html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                html.Label("Select City:", style={'font-weight': 'bold', 'color': 'inherit'}),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[{'label': city, 'value': city} for city in df['City'].unique()],
                    value='Ecoopolis', # Default selected city
                    multi=False,
                    clearable=False
                )
            ])),
            dbc.Col(html.Div([
                html.Label("Select Vehicle Type:", style={'font-weight': 'bold', 'color': 'inherit'}),
                dcc.Dropdown(
                    id='vehicle-type-dropdown',
                    options=[{'label': v_type, 'value': v_type} for v_type in df['Vehicle Type'].unique()],
                    value='Autonomous Vehicle', # Default selected vehicle type
                    multi=False,
                    clearable=False
                )
            ]))
        ])
    ], style={'padding': '10px'}),

    html.Hr(),
    html.Hr(),

    # Speed vs Traffic Density and Avg Energy by Economic Condition
    dbc.Row([
        dbc.Col(dcc.Graph(id='speed-traffic-scatter'), width=6),
        dbc.Col(dcc.Graph(id='avg-energy-by-economic-condition'), width=6)
    ], style={'padding': '20px'}),

    # Avg Speed by Day of Week and Avg Energy by Weather
    dbc.Row([
        dbc.Col(dcc.Graph(id='avg-speed-by-day-of-week'), width=6),
        dbc.Col(dcc.Graph(id='avg-energy-by-weather'), width=6)
    ], style={'padding': '20px'}),

    # Correlation Matrix
    dbc.Row([
        dbc.Col(html.H3("Correlation Matrix of Numerical Features", style={'text-align': 'center', 'color': 'inherit'}), width=12),
        dbc.Col(dcc.Graph(id='correlation-matrix-heatmap'), width=12)
    ], style={'padding': '20px'})
])

# for theme toggling
@app.callback(
    Output('theme-store', 'data'),
    Output('dashboard-container', 'className'),
    Input('dark-mode-toggle', 'value')
)
def toggle_theme(is_dark_mode_on):
    if is_dark_mode_on:
        return 'dark', 'dark-theme'
    return 'light', 'light-theme'

# for Speed vs. Traffic Density scatter plot
@app.callback(
    Output('speed-traffic-scatter', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('vehicle-type-dropdown', 'value'),
     Input('theme-store', 'data')]
)
def update_speed_traffic_scatter(selected_city, selected_vehicle_type, current_theme):
    filtered_df = df[
        (df['City'] == selected_city) &
        (df['Vehicle Type'] == selected_vehicle_type)
    ]
    template = 'plotly_dark' if current_theme == 'dark' else 'plotly_white'
    fig = px.scatter(filtered_df, x='Traffic Density', y='Speed',
                     color='Weather',
                     size='Energy Consumption',
                     hover_data=['Hour Of Day', 'Is Peak Hour', 'Economic Condition'],
                     title=f'Speed vs. Traffic Density for {selected_vehicle_type} in {selected_city}',
                     labels={'Traffic Density': 'Traffic Density', 'Speed': 'Speed (km/h)'},
                     template=template)
    fig.update_layout(transition_duration=500)
    return fig

# for Average Energy Consumption by Economic Condition bar chart
@app.callback(
    Output('avg-energy-by-economic-condition', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('vehicle-type-dropdown', 'value'),
     Input('theme-store', 'data')]
)
def update_avg_energy_bar(selected_city, selected_vehicle_type, current_theme):
    filtered_df = df[
        (df['City'] == selected_city) &
        (df['Vehicle Type'] == selected_vehicle_type)
    ]
    avg_energy = filtered_df.groupby('Economic Condition')['Energy Consumption'].mean().reset_index()
    template = 'plotly_dark' if current_theme == 'dark' else 'plotly_white'
    fig = px.bar(avg_energy, x='Economic Condition', y='Energy Consumption',
                 title=f'Avg Energy Consumption by Economic Condition for {selected_vehicle_type} in {selected_city}',
                 labels={'Economic Condition': 'Economic Condition', 'Energy Consumption': 'Avg Energy Consumption (kWh)'},
                 template=template)
    fig.update_layout(transition_duration=500)
    return fig

# for Average Speed by Day of Week
@app.callback(
    Output('avg-speed-by-day-of-week', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('vehicle-type-dropdown', 'value'),
     Input('theme-store', 'data')]
)
def update_avg_speed_day_of_week(selected_city, selected_vehicle_type, current_theme):
    filtered_df = df[
        (df['City'] == selected_city) &
        (df['Vehicle Type'] == selected_vehicle_type)
    ]

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    avg_speed_day = filtered_df.groupby('Day Of Week')['Speed'].mean().reindex(day_order).reset_index()
    avg_speed_day.columns = ['Day Of Week', 'Average Speed'] # Rename for clarity

    template = 'plotly_dark' if current_theme == 'dark' else 'plotly_white'
    fig = px.bar(avg_speed_day, x='Day Of Week', y='Average Speed',
                 title=f'Avg Speed by Day of Week for {selected_vehicle_type} in {selected_city}',
                 labels={'Day Of Week': 'Day Of Week', 'Average Speed': 'Average Speed (km/h)'},
                 template=template)
    fig.update_layout(transition_duration=500)
    return fig

# for Average Energy Consumption by Weather
@app.callback(
    Output('avg-energy-by-weather', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('vehicle-type-dropdown', 'value'),
     Input('theme-store', 'data')]
)
def update_avg_energy_by_weather(selected_city, selected_vehicle_type, current_theme):
    filtered_df = df[
        (df['City'] == selected_city) &
        (df['Vehicle Type'] == selected_vehicle_type)
    ]
    avg_energy_weather = filtered_df.groupby('Weather')['Energy Consumption'].mean().reset_index()
    template = 'plotly_dark' if current_theme == 'dark' else 'plotly_white'
    fig = px.bar(avg_energy_weather, x='Weather', y='Energy Consumption',
                 title=f'Avg Energy Consumption by Weather for {selected_vehicle_type} in {selected_city}',
                 labels={'Weather': 'Weather', 'Energy Consumption': 'Avg Energy Consumption (kWh)'},
                 template=template)
    fig.update_layout(transition_duration=500)
    return fig

# For correlation matrix
@app.callback(
    Output('correlation-matrix-heatmap', 'figure'),
    Input('theme-store', 'data')
)
def update_correlation_matrix(current_theme):
    template = 'plotly_dark' if current_theme == 'dark' else 'plotly_white'
    fig = px.imshow(correlation_matrix,
                    text_auto=True,
                    color_continuous_scale='RdBu',
                    title='Correlation Matrix of Numerical Features',
                    template=template)
    fig.update_layout(transition_duration=500)
    return fig


server = app.server

