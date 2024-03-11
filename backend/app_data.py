import os
import pandas as pd
from backend.globals import DEFAULT_XLSX_PATH, UPLOADED_XLSX_PATH
from backend.statistic_calculations import calculate_statistics
from dataclases.descriptive_stat_dc import DescriptiveStat
import plotly.express as px
from plotly.graph_objs import Figure


class AppData:
    _instance = None  # type: ignore

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._returns_df: pd.DataFrame = self._set_returns_df()
        self._filename: str = "default file"
        self._descriptive_stat: DescriptiveStat | None = None
        self._return_fig: Figure | None = None

    @property
    def returns_df(self) -> pd.DataFrame:
        return self._returns_df

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def descriptive_stat(self) -> DescriptiveStat:
        if self._descriptive_stat is None:
            self._descriptive_stat = calculate_statistics(self._returns_df)
        return self._descriptive_stat

    @property
    def return_fig(self) -> str:
        if self._descriptive_stat is None:
            cols = self.returns_df.columns
            self._return_fig = px.line(
                self.returns_df, x=cols[0], y=cols[1], labels={cols[0]: "Dates", cols[1]: "Returns"}
            )
        return self._return_fig

    @filename.setter
    def filename(self, value: str):
        self._filename = value
        self._reload_data()

    def _reload_data(self):
        self._set_returns_df()
        self._descriptive_stat = None
        self._return_fig = None

    def _set_returns_df(self):
        if os.path.exists(UPLOADED_XLSX_PATH):
            return pd.read_excel(UPLOADED_XLSX_PATH)
        else:
            return pd.read_excel(DEFAULT_XLSX_PATH)
