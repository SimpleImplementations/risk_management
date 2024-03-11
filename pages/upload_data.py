import base64
import io
import dash
import pandas as pd
from dash import dcc, html, callback, Input, Output, State
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
        html.Div(id="output-data"),
    ]
)


def parse_contents(contents, filename):
    _content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))
    df.to_excel(UPLOADED_XLSX_PATH, index=False)
    AppData().filename = filename
    return html.Div(
        [
            html.H4(filename),
            # html.H6("Raw Content:"),
            # html.Pre(contents[0:200] + "...", style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"}),
            html.Hr(),
            html.Div([html.H6("Parsed Content:"), dcc.Markdown(df.to_markdown())]),
        ]
    )


@callback(Output("output-data", "children"), [Input("input-data", "contents")], [State("input-data", "filename")])
def update_output(contents, filename):
    if contents is not None:
        children = [parse_contents(contents, filename)]
        return children
