import base64
import io
import os
import dash
import pandas as pd
from dash import dcc, html, callback, Input, Output, State
from dash.exceptions import PreventUpdate
from backend.app_data import AppData
from backend.globals import UPLOADED_XLSX_PATH

dash.register_page(__name__, path="/upload_data")

layout = html.Div(
    [
        dcc.Upload(
            ["Drag and Drop or ", html.A("Select a File")],
            id="input-data",
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
            },
        ),
        html.Div(id="data-loaded"),
        html.Button("Update Data", id="update-button"),
        html.Div(id="table-content"),
    ]
)


def update_app_data(contents, filename):
    _content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))
    df.to_excel(UPLOADED_XLSX_PATH, index=False)
    AppData().filename = filename
    return html.Div("Data Loaded Correctly")


@callback(Output("data-loaded", "children"), [Input("input-data", "contents")], [State("input-data", "filename")])
def update_data(contents, filename):
    if contents is not None:
        return update_app_data(contents, filename)


@callback(Output("table-content", "children"), [Input("update-button", "n_clicks")])
def update_table(n_clicks):
    # if n_clicks is None:
    #     raise PreventUpdate
    return html.Div(
        [
            html.H4(AppData().filename),
            html.Hr(),
            html.Div([html.H6("Parsed Content:"), dcc.Markdown(AppData().returns_df.to_markdown())]),
        ]
    )
