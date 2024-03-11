import os
import dash
import pandas as pd
import plotly.express as px
from dash import html, html, dcc, Input, Output, callback
from backend.app_data import AppData

# from main import app_data  # type: ignore

dash.register_page(__name__, path="/returns")

"""excel_path = os.path.join("data", "returns.xlsx")

df = pd.read_excel(excel_path)  # app_data.returns_df"""

"""df = AppData().returns_df

filename = "excel_name"
cols = df.columns
fig = px.line(df, x=cols[0], y=cols[1], labels={cols[0]: "Dates", cols[1]: "Returns"})
layout = html.Div(
    [
        html.H3(filename),
        dcc.Graph(figure=fig, id="graph"),
        html.Hr(),
    ]
)
"""
layout = html.Div(id="fig")


def plot_returns():
    return html.Div(
        [
            html.H3(AppData().filename),
            dcc.Graph(figure=AppData().return_fig, id="graph"),
            html.Hr(),
        ]
    )


@callback(Output("fig", "children"), [Input("url", "pathname")])
def update_layout(_pathname):
    return plot_returns()
