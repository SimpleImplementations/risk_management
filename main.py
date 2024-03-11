import dash
import os
import pandas as pd
from dash import Dash, html, dcc, page_registry, page_container
from backend.app_data import AppData
from backend.globals import remove_old_files

app = Dash(__name__, use_pages=True)

remove_old_files()
excel_path = os.path.join("data", "returns.xlsx")
filename = "returns.xlsx"
df = pd.read_excel(excel_path)
app_data = AppData()


app.layout = html.Div(dash.page_container)

name_list = [page["name"] for page in page_registry.values()]
path_list = [page["path"] for page in page_registry.values()]

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [dcc.Link(name, href=path) for name, path in zip(name_list, path_list)],
            className="nav",
        ),  # link to existing paths
        html.Div(id="page-content"),
        page_container,  # This display the page
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
