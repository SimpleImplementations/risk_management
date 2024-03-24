import os
import dash
from dash import html, html, dcc, Input, Output, callback
from backend.app_data import AppData
from backend.globals import UPLOADED_XLSX_PATH

dash.register_page(__name__, path="/returns")

layout = html.Div(
    [
        html.H3(AppData().filename),
        html.Div(id="returns-graph"),
        html.Hr(),
        # html.Div(id="plot-graph"),
        html.Button("Update Data", id="update-button", style={"display": "none"}),
    ],
)


@callback(Output("returns-graph", "children"), [Input("update-button", "n_clicks")])
def update_table(n_clicks):
    return dcc.Graph(figure=AppData().plot_creator.return_fig)
