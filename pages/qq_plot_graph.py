import os
import dash
from dash import html, html, dcc, Input, Output, callback, State
from backend.app_data import AppData
from backend.globals import UPLOADED_XLSX_PATH

dash.register_page(__name__, path="/qq_plot_graph")

layout = html.Div(
    [
        html.H3(AppData().filename),
        html.Div(id="qq_plot_graph"),
        html.Div(
            [
                html.Label("Degrees of Freedom t Student:"),
                dcc.Input(id="degrees-input", type="number"),
                html.Button("Update Degrees of Freedom", id="degree_of_freedom"),
            ]
        ),
        html.Hr(),
        html.Button("Update Data", id="update-button", style={"display": "none"}),
    ],
)


def create_graphs():
    return html.Div(
        [dcc.Graph(figure=graph) for graph in AppData().plot_creator.qq_plot_dict.values()],
        style={"display": "flex", "flexDirection": "row", "flexWrap": "wrap"},
    )


@callback(
    Output("qq_plot_graph", "children"),
    [Input("update-button", "n_clicks"), Input("degree_of_freedom", "n_clicks")],
    [State("degrees-input", "value")],
)
def update_table(_n_clicks, _n_clicks_freedom, freedom_t):
    if freedom_t is not None and AppData().plot_creator.plot_parameters.degrees_of_freedom_t != freedom_t:
        AppData().plot_creator.change_parameters(freedom_t)
    return create_graphs()


# @callback(
#     Output("qq_plot_graph", "children"), [Input("degree_of_freedom", "n_clicks")], [Input("degrees-input", "value")]
# )
# def update_output(n_clicks, value):
#     AppData().plot_creator.plot_parameters.degrees_of_freedom_t = value
#     return create_graphs()
