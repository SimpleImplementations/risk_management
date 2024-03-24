from typing import Dict, List
import pandas as pd
import scipy.stats
import plotly.graph_objects as go
from scipy.stats import skew, kurtosis, norm
from plotly.graph_objs import Figure


def qq_plot(returns_df: pd.DataFrame, degrees_of_freedom_t: int) -> Dict:

    df = returns_df.copy()  # critical step

    df.sort_values(by="returns", inplace=True)
    lenght = df.returns.count()
    unit_probability = 1 / lenght
    df["cum_prob"] = [unit_probability * i for i in range(1, lenght + 1)]
    mean = df.returns.mean()
    stdev = df.returns.std()
    df["standarized_ret"] = (df["returns"] - mean) / stdev
    df["z_scores_normal"] = scipy.stats.norm.ppf(df["cum_prob"])
    df["z_scores_t_student"] = scipy.stats.t.ppf(df["cum_prob"], degrees_of_freedom_t)  # prob, degree_of_freedom
    cf_exp = cornish_fisher_expansion(df)
    cf_exp.append(None)  # only for matching lenghts
    df["cf_expansion"] = cf_exp
    df.reset_index(inplace=True, drop=True)
    df.drop(df.index[-1], inplace=True)

    return create_qq_plot_figure(
        df,
        ["z_scores_normal", "z_scores_t_student", "cf_expansion"],
        [
            "Z-Scores Normal Distribution",
            f"Z-Scores T Student: {degrees_of_freedom_t} Degrees of Freedom",
            "Z-Scores Cornish Fisher Expansion",
        ],
    )


def create_qq_plot_figure(df: pd.DataFrame, comparison_models: List, titles: List) -> Dict:
    qq_plots_dict: Dict[str, Figure] = {}
    for title, model in zip(titles, comparison_models):
        qq_plot_fig = go.Figure()
        # scatter plot for z_scores_normal vs standarized_ret
        qq_plot_fig.add_trace(go.Scatter(x=df["standarized_ret"], y=df[model], mode="lines", name="QQ Plot"))
        qq_plot_fig.add_trace(
            go.Scatter(x=[-6, 6], y=[-6, 6], mode="lines", line=dict(color="red", dash="dash"), name="45-Degree Line")
        )
        qq_plot_fig.add_shape(type="line", x0=-6, y0=0, x1=6, y1=0, line=dict(color="black", dash="dash"))
        qq_plot_fig.add_shape(type="line", x0=0, y0=-6, x1=0, y1=6, line=dict(color="black", dash="dash"))
        # TODO change possition of this
        qq_plot_fig.update_layout(
            title="QQ Plot",
            xaxis_title="Standardized Returns",
            yaxis_title=title,
            xaxis=dict(
                range=[-6, 6],  # kind of hardcoded
                zeroline=True,
            ),
            yaxis=dict(
                range=[-6, 6],
                zeroline=True,
            ),
            width=600,
            height=600,
            autosize=False,
        )
        qq_plots_dict[model] = qq_plot_fig
    return qq_plots_dict


def cornish_fisher_expansion(df: pd.DataFrame) -> List:
    lenght = len(df)
    kurt = kurtosis(df["returns"])
    skewness = skew(df["returns"])
    cf_df = pd.DataFrame([i / lenght for i in range(1, lenght + 1)], columns=["prob"])
    cf_df["z_normal"] = norm.ppf(cf_df.prob)
    cf_df.drop(lenght - 1, inplace=True)
    cf_df["cf_term_1"] = cf_df["z_normal"]
    cf_df["cf_term_2"] = (1 / 6) * (cf_df["z_normal"] ** 2 - 1) * skewness
    cf_df["cf_term_3"] = (1 / 24) * (cf_df["z_normal"] ** 3 - 3 * cf_df["z_normal"]) * kurt
    cf_df["cf_term_4"] = (1 / 36) * (2 * cf_df["z_normal"] ** 3 - 5 * cf_df["z_normal"]) * skewness**2
    cf_df["cf_expansion"] = cf_df["cf_term_1"] + cf_df["cf_term_2"] + cf_df["cf_term_3"] + cf_df["cf_term_4"]
    return list(cf_df["cf_expansion"])
