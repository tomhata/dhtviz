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

from dotenv import load_dotenv

load_dotenv(".env")

conn = psycopg2.connect(
    host=os.getenv("SQL_HOST"),
    port=os.getenv("SQL_PORT"),
    database=os.getenv("SQL_DATABASE"),
    user=os.getenv("SQL_USER"),
    password=os.getenv("SQL_PASSWORD"),
)

query = f'SELECT * from {os.getenv("SQL_TABLE")}'
df = pd.read_sql(query, con=conn)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Tent environment"

trace_t = go.Line(x=df.datetime, y=df.temperature, name="temperature")
trace_h = go.Line(x=df.datetime, y=df.humidity, name="humidity", yaxis="y2")

app.layout = html.Div(
    children=[
        html.H1(children="DHT22 log"),
        dcc.Graph(
            id="dht22log",
            figure={
                "data": [trace_t, trace_h],
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
            # n_intervals=0,
        ),
    ]
)

app.run_server(host="0.0.0.0")
