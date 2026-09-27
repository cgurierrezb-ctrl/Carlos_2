"""Flight Delay Time Statistics Dashboard.

Versión actualizada con tema oscuro, menú desplegable (dcc.Dropdown) 
y colores vivos con contraste optimizado para gráficos Plotly.
"""

from pathlib import Path

# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.graph_objects import Figure

# Read the airline data into pandas dataframe
DATA_FILE = Path(__file__).with_name('airline_data.csv')

airline_data = pd.read_csv(
    DATA_FILE,
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str, 'Div1TailNum': str,
        'Div2Airport': str, 'Div2TailNum': str
    }
)

# Obtener lista única de años ordenada
available_years = sorted(airline_data['Year'].unique())

# Create a dash application
app = dash.Dash(__name__)

# Configuración de plantilla de gráficos y colores vivos (Neon/Vivid)
DARK_GRAPH_TEMPLATE = "plotly_dark"
COLOR_PALETTE = px.colors.qualitative.Vivid

# Build dash app layout con tema oscuro
app.layout = html.Div(
    style={
        'backgroundColor': '#121212',
        'color': '#FFFFFF',
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px',
        'minHeight': '100vh'
    },
    children=[
        html.H1(
            'Flight Delay Time Statistics',
            style={
                'textAlign': 'center',
                'color': '#00E5FF',
                'fontSize': 34,
                'fontWeight': 'bold',
                'marginBottom': '20px'
            }
        ),
        
        # Selector desplegable de años (dcc.Dropdown)
        html.Div(
            [
                html.Label(
                    "Select Year: ",
                    style={'fontSize': 20, 'marginRight': '15px', 'color': '#E0E0E0'}
                ),
                dcc.Dropdown(
                    id='input-year',
                    options=[{'label': str(year), 'value': str(year)} for year in available_years],
                    value=str(available_years[-1]) if available_years else '2010',
                    clearable=False,
                    style={
                        'width': '200px',
                        'color': '#000000',  # Texto oscuro dentro de las opciones para legibilidad
                        'fontSize': 18
                    }
                )
            ],
            style={
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'marginBottom': '30px'
            }
        ),
        
        # Segment 1
        html.Div([
            html.Div(dcc.Graph(id='carrier-plot'), style={'width': '50%', 'padding': '10px'}),
            html.Div(dcc.Graph(id='weather-plot'), style={'width': '50%', 'padding': '10px'})
        ], style={'display': 'flex'}),
        
        # Segment 2
        html.Div([
            html.Div(dcc.Graph(id='nas-plot'), style={'width': '50%', 'padding': '10px'}),
            html.Div(dcc.Graph(id='security-plot'), style={'width': '50%', 'padding': '10px'})
        ], style={'display': 'flex'}),
        
        # Segment 3
        html.Div(
            dcc.Graph(id='late-plot'),
            style={'width': '100%', 'padding': '10px', 'display': 'flex', 'justifyContent': 'center'}
        )
    ]
)


def compute_info(airline_data, entered_year):
    """Compute average delay dataframes for carrier, weather, NAS, security, and late aircraft."""
    df = airline_data[airline_data['Year'] == int(entered_year)]
    
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


@app.callback(
    [
        Output(component_id='carrier-plot', component_property='figure'),
        Output(component_id='weather-plot', component_property='figure'),
        Output(component_id='nas-plot', component_property='figure'),
        Output(component_id='security-plot', component_property='figure'),
        Output(component_id='late-plot', component_property='figure')
    ],
    Input(component_id='input-year', component_property='value')
)
def get_graph(entered_year):
    try:
        int(entered_year)
    except (TypeError, ValueError):
        blank = Figure()
        blank.update_layout(
            title='Select a valid year',
            template=DARK_GRAPH_TEMPLATE,
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return [blank, blank, blank, blank, blank]

    # Cómputo de datos
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)

    # Gráfico 1: Carrier Delay
    carrier_fig = px.line(
        avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
        title='Average Carrier Delay Time (minutes) by Airline',
        template=DARK_GRAPH_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    # Gráfico 2: Weather Delay
    weather_fig = px.line(
        avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
        title='Average Weather Delay Time (minutes) by Airline',
        template=DARK_GRAPH_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    # Gráfico 3: NAS Delay
    nas_fig = px.line(
        avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
        title='Average NAS Delay Time (minutes) by Airline',
        template=DARK_GRAPH_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    # Gráfico 4: Security Delay
    sec_fig = px.line(
        avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
        title='Average Security Delay Time (minutes) by Airline',
        template=DARK_GRAPH_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    # Gráfico 5: Late Aircraft Delay
    late_fig = px.line(
        avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
        title='Average Late Aircraft Delay Time (minutes) by Airline',
        template=DARK_GRAPH_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE
    )

    # Ajuste para que las líneas destaquen mejor en fondo oscuro
    for fig in [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]:
        fig.update_traces(line=dict(width=2.5))

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]


# ---------------------------------------------------------------------------
# Arranque: desarrollo local y producción
# ---------------------------------------------------------------------------
server = app.server

try:
    _ = app.run_server
except Exception:
    setattr(app, 'run_server', app.run)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000)