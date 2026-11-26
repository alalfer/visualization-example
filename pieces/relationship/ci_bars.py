"""PIECE · Means with confidence intervals
Question: Is the difference between group means larger than the uncertainty around them?
Needs: One numeric column, one categorical column.
Avoid when: The distribution is very skewed. The mean may not represent anyone. Show medians.
Filter risk: Fewer rows mean wider intervals. This is the chart doing its job, so leave it visible.
Try it: Narrow the selection and watch the intervals grow.
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/error-bars/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

DATA = Path(__file__).parents[2] / "data"


def mean_ci(df, category, value, level=0.95):
    """Table with mean, n and the half-width of the t interval per group."""
    table = df.groupby(category, observed=True)[value].agg(["mean", "std", "count"]).reset_index()
    table = table[table["count"] >= 2]
    table["margin"] = stats.t.ppf((1 + level) / 2, table["count"] - 1) * table["std"] / table["count"] ** 0.5
    return table.sort_values("mean")


def ci_bars(df, category, value, level=0.95, height=None):
    """A dot per group with its interval. Dots, not bars: the mean is what is being compared."""
    table = mean_ci(df, category, value, level)
    if table.empty:
        return go.Figure(layout_title_text="Each group needs at least two rows")
    fig = px.scatter(table, x="mean", y=category, error_x="margin", hover_data={"count": ":,"}, height=height or max(300, 30 * len(table) + 100),
                     labels={"mean": f"Mean {value} (bars: {level:.0%} CI)"})
    return fig.update_traces(marker={"size": 10}).update_yaxes(title=None, type="category")


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    df = df[df.duration_min.between(0, 120)]
    keep = st.slider("Random share of the sample", 0.001, 1.0, 0.05, 0.001, format="%.3f")
    data = df.sample(frac=keep, random_state=1)
    st.plotly_chart(ci_bars(data, "start_borough", "duration_min"))
    st.caption(f"{len(data):,} sampled trips.")


if __name__ == "__main__":
    demo()
