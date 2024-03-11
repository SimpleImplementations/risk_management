import pandas as pd
from scipy.stats import sem, mode, kurtosis, skew, t
from dataclases.descriptive_stat_dc import DescriptiveStat


def calculate_statistics(df: pd.DataFrame, confidence_level: float = 0.95):
    ret = df["returns"]
    mean_value = ret.mean()
    se_value = sem(ret)
    median_value = ret.median()
    mode_value = mode(ret)[0]
    std_dev_value = ret.std()
    variance_value = ret.var()
    kurtosis_value = kurtosis(ret)
    skewness_value = skew(ret)
    range_value = ret.max() - ret.min()
    min_value = ret.min()
    max_value = ret.max()
    sum_value = ret.sum()
    count_value = ret.count()
    largest_value = ret.nlargest(1).iloc[0]
    smallest_value = ret.nsmallest(1).iloc[0]
    confidence_level = 0.95
    _confidence_interval = t.interval(confidence_level, ret.count() - 1, loc=mean_value, scale=se_value)
    confidence_interval_upper = _confidence_interval[1]
    confidence_interval_lower = _confidence_interval[0]

    return DescriptiveStat(
        mean_value,
        se_value,
        median_value,
        mode_value,
        std_dev_value,
        variance_value,
        kurtosis_value,
        skewness_value,
        range_value,
        min_value,
        max_value,
        sum_value,
        count_value,
        largest_value,
        smallest_value,
        confidence_level,
        confidence_interval_upper,
        confidence_interval_lower,
    )
