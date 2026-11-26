"""PIECE · Density curve (KDE) with bandwidth
Question: What is the smooth shape of a distribution, and how much does smoothing decide it?
Needs: One numeric column with at least about 30 values.
Avoid when: The data is discrete or has a hard limit. KDE leaks past the limit (negative durations).
Filter risk: With few points the curve looks far more certain than it is.
Try it: Set the bandwidth very low, then very high. Which picture would you publish?
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/distplot/
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import gaussian_kde

DATA = Path(__file__).parents[2] / "data"
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]


def kde_curve(df, value, group=None, bandwidth=None, rug=True, height=420):
    """One density curve per group. bandwidth multiplies the automatic width (1 = automatic)."""
    fig = go.Figure().update_layout(height=height, xaxis_title=value, yaxis_title="Density")
    groups = df.groupby(group, observed=True) if group else [("All", df)]
    x = np.linspace(df[value].min(), df[value].max(), 300) if len(df) else []
    for i, (name, part) in enumerate(groups):
        values = part[value].dropna().to_numpy()
        if len(values) < 5 or values.std() == 0:
            continue  # a curve needs variation, so we skip tiny groups
        kde = gaussian_kde(values)
        if bandwidth:
            kde.set_bandwidth(kde.factor * bandwidth)
        fig.add_scatter(x=x, y=kde(x), name=str(name), mode="lines", line={"color": COLORS[i % 4], "width": 2})
        if rug:
            sample = np.random.default_rng(0).choice(values, min(200, len(values)), replace=False)
            fig.add_scatter(x=sample, y=[-0.02 * (i + 1) * kde(x).max()] * len(sample), mode="markers", showlegend=False,
                            hoverinfo="skip", marker={"symbol": "line-ns-open", "size": 8, "color": COLORS[i % 4]})
    if not fig.data:
        fig.update_layout(title="Too few values to draw a curve")
    return fig


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet", columns=["duration_min", "rider_type"])
    sample = df[df.duration_min.between(0, 60)].sample(5000, random_state=1)
    bandwidth = st.slider("Bandwidth multiplier", 0.1, 5.0, 1.0, 0.1)
    st.plotly_chart(kde_curve(sample, "duration_min", "rider_type", bandwidth))
    st.caption("Trips up to 60 minutes. Calculated on a sample of 5,000 so the slider stays fast.")


if __name__ == "__main__":
    demo()
