import dash
from dash import html, dcc, Input, Output, callback, dash_table
from backend.app_data import AppData


dash.register_page(__name__, path="/desc_stat")

layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        html.Div(id="output-desc_stat"),
        html.Button("Update Data", id="update-button", style={"display": "none"}),
    ]
)


def descriptive_stat():
    desc_stat_df = AppData().descriptive_stat.as_pd()
    updated_layout = html.Div(
        [
            html.H1("Descriptive Statistics"),
            dash_table.DataTable(
                desc_stat_df.to_dict("records"),
                [{"name": i, "id": i} for i in desc_stat_df.columns],
            ),
        ]
    )
    return updated_layout


# @callback(Output("output-desc_stat", "children"), Input("url", "pathname"))
# def update_layout(_pathname):
#     return descriptive_stat()


@callback(Output("output-desc_stat", "children"), [Input("update-button", "n_clicks")])
def update_table(n_clicks):
    return descriptive_stat()
