import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import time

from data import get_latest_data

df = pd.read_csv("aqi.csv")
print(df.head())

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container(
    [
        dbc.Row([html.Div('Air Quality Index (AQI)', className="text-primary text-center fs-3")]),
        dbc.Row([
            html.Button('Refresh', id='submit-val'),
            html.Div(id='container-button-basic', children="Click to refresh")
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=px.line(df, x='date', y="pm10"))], width=6),
            dbc.Col([dcc.Graph(figure=px.line(df, x='date', y="pm2_5"))], width=6),
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=px.line(df, x='date', y="carbon_monoxide"))], width=6),
            dbc.Col([dcc.Graph(figure=px.line(df, x='date', y="sulphur_dioxide"))], width=6),
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=px.line(df, x='date', y="ozone"))], width=6),
            dbc.Col([dcc.Graph(figure=px.line(df, x='date', y="dust"))], width=6),
        ]),
        dbc.Row([dbc.Col([dcc.Graph(figure=px.line(df, x='date', y="uv_index"))], width=6)]),
        dbc.Row([dbc.Col([dcc.Graph(figure=px.bar(df, x="date", y=["pm10", "pm2_5", "carbon_monoxide", "sulphur_dioxide", "ozone"],
                                        color_discrete_sequence=["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#33FFF6"]))])])
    ]
)

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    prevent_initial_call=True
)
def update_output(n_clicks):
    if n_clicks > 0:
        # Fetch latest data
        get_latest_data()
        
        # Reload the data and update the figures (this part assumes you want to update df)
        global df
        df = pd.read_csv("aqi.csv")  # or any other logic to refresh your data
        
        # Indicate that the data has been updated
        return "Latest data is being fetched..."

# If you need a loading indicator or some other behavior, consider adding async handling or `dcc.Loading`

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
