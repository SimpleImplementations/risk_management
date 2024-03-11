from dataclasses import asdict, dataclass
from typing import Any
import pandas as pd


@dataclass
class DescriptiveStat:
    mean: float
    se: float
    median: float
    mode: float
    std_dev: float
    variance: Any
    kurtosis: float
    skewness: float
    range_val: float
    min_val: float
    max_val: float
    sum_val: float
    count_val: int
    largest_val: float
    smallest_val: float
    confidence_level: float
    confidence_interval_upper: float
    confidence_interval_lower: float

    def as_pd(self) -> pd.DataFrame:
        obj_dict = asdict(self)
        df = pd.DataFrame(list(obj_dict.items()), columns=["variables", "vals"])
        return df
