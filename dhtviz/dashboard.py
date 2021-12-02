"""
Access temperature and humidity data from postgres server and plot locally.
"""

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import psycopg2

from dash.dependencies import Input, Output
from dotenv import load_dotenv

load_dotenv(".env")


def get_traces():
    conn = psycopg2.connect(
        host=os.getenv("SQL_HOST"),
        port=os.getenv("SQL_PORT"),
        database=os.getenv("SQL_DATABASE"),
        user=os.getenv("SQL_USER"),
        password=os.getenv("SQL_PASSWORD"),
    )
    query = f'SELECT * from {os.getenv("SQL_TABLE")}'
    df = pd.read_sql(query, con=conn)
    trace_t = go.Line(x=df.datetime, y=df.temperature, name="temperature")
    trace_h = go.Line(x=df.datetime, y=df.humidity, name="humidity", yaxis="y2")
    return [trace_t, trace_h]


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Tent environment"


traces = get_traces()

app.layout = html.Div(
    children=[
        html.H1(children="DHT22 log"),
        dcc.Graph(
            id="dht22log",
            figure={
                "data": traces,
                "layout": go.Layout(
                    title="Temperature and humidity log",
                    yaxis={
                        "title": "temperature",
                    },
                    yaxis2={
                        "title": "humidity",
                        "overlaying": "y",
                        "side": "right",
                    },
                ),
            },
        ),
        dcc.Interval(
            id="interval-component",
            interval=60000,
            n_intervals=0,
        ),
    ]
)


@app.callback(
    Output("dht22log", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_graph(n):
    traces = get_traces()
    output_params = {
            "data": traces,
            "layout": go.Layout(
                title="Temperature and humidity log",
                yaxis={
                    "title": "temperature",
                },
                yaxis2={
                    "title": "humidity",
                    "overlaying": "y",
                    "side": "right",
                }
            )
        }
    return output_params


app.run_server(host="0.0.0.0")
