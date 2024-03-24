from typing import Dict
import pandas as pd
from backend.plot_parameters import PlotParameters
from backend.qq_plot import qq_plot
import plotly.express as px
from plotly.graph_objs import Figure


class PlotCreator:
    def __init__(self, returns_df):
        self.plot_parameters = PlotParameters()
        self._returns_df: pd.DataFrame = returns_df
        self._return_fig: Figure | None = None
        self._qq_plot: Dict[str, Figure] | None = None

    @property
    def return_fig(self) -> Figure:
        if self._return_fig is None:
            cols = self._returns_df.columns
            self._return_fig = px.line(
                self._returns_df, x=cols[0], y=cols[1], labels={cols[0]: "Dates", cols[1]: "Returns"}
            )
        return self._return_fig

    @property
    def qq_plot_dict(self) -> Dict[str, Figure]:
        if self._qq_plot is None:
            self._qq_plot = qq_plot(self._returns_df, self.plot_parameters.degrees_of_freedom_t)
        return self._qq_plot

    def change_parameters(self, degrees_of_freedom_t: int):
        self.plot_parameters = PlotParameters(degrees_of_freedom_t)
        self._qq_plot = None
