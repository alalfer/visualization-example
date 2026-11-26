"""PIECE · Compare two groups
Question: Is the difference between two groups large, and is it distinguishable from noise?
Needs: One numeric column and a column with at least two groups.
Avoid when: You tried many comparisons. Some will look significant by chance alone.
Filter risk: Filtering until p < 0.05 is p-hacking. Decide the comparison first.
Try it: Take a very large sample. A tiny difference becomes "significant". Is it important?
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

DATA = Path(__file__).parents[2] / "data"


def welch_test(a, b, level=0.95):
    """Difference of means (a minus b), its interval and the p-value, without assuming equal variances."""
    result = stats.ttest_ind(a, b, equal_var=False)
    interval = result.confidence_interval(level)
    pooled = np.sqrt((a.var() + b.var()) / 2)
    return {"difference": a.mean() - b.mean(), "low": interval.low, "high": interval.high,
            "p": result.pvalue, "effect_size": (a.mean() - b.mean()) / pooled if pooled else np.nan}


def group_test(df, group, value, first, second, height=380):
    """Return the test result and two overlaid histograms of the groups."""
    a, b = df.loc[df[group] == first, value].dropna(), df.loc[df[group] == second, value].dropna()
    if len(a) < 2 or len(b) < 2:
        return None, go.Figure(layout_title_text="Each group needs at least two rows")
    fig = px.histogram(df[df[group].isin([first, second])], x=value, color=group, nbins=60, barmode="overlay", opacity=0.65,
                       histnorm="probability density", height=height)
    return welch_test(a, b), fig


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    df = df[df.duration_min.between(0, 60)]
    n = st.slider("Rows used", 100, len(df), min(5000, len(df)), step=100)
    result, fig = group_test(df.sample(n, random_state=1), "rider_type", "duration_min", "casual", "member")
    if result:
        left, middle, right = st.columns(3)
        left.metric("Casual minus member (min)", f"{result['difference']:.2f}", f"CI {result['low']:.2f} to {result['high']:.2f}", delta_color="off")
        middle.metric("p-value", "< 0.001" if result['p'] < 0.001 else f"{result['p']:.3f}")
        right.metric("Effect size (d)", f"{result['effect_size']:.2f}")
    st.plotly_chart(fig)


if __name__ == "__main__":
    demo()
