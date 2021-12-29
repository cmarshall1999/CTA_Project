# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px

import pandas as pd

from data import getRuns, getStats, showDist, showDelayProp

app = dash.Dash(__name__)

delays, headways, times = getRuns()

# Load Tables
delay_stats = getStats(delays).reset_index()

# Load figures
d_fig = showDist(delays)
h_fig = showDist(headways)


d_prop_fig = showDelayProp(delays)


app.layout = html.Div(children=[
    html.H1(children='CTA Data Exploration'),

    html.Div(children='''
        Delay propagation analysis of CTA Purple Line data during the AM period.
    '''),

    dash_table.DataTable(
        id='Delay-Stats',
        columns = [{"name": i, "id": i} for i in delay_stats.columns],
        data = delay_stats.to_dict('records')
    ),

    dcc.Graph(
        id='Delay-Dist',
        figure=d_fig
    ), 

    dcc.Graph(
        id='Delay-Prop',
        figure=d_prop_fig
    )
])

if __name__ == '__main__':
    app.run_server(host = '127.0.0.1', debug = True)
