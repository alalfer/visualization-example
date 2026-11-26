"""PIECE · Scatter with trend and confidence band
Question: Do two measures move together, and how sure are we about the line?
Needs: Two numeric columns.
Avoid when: You have tens of thousands of points. Use density_2d.
Filter risk: A filter can flip or invent a correlation. Always show n and r in the title.
Try it: Filter to one borough. Does the slope keep its sign?
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/linear-fits/
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

DATA = Path(__file__).parents[2] / "data"


def scatter_trend(df, x, y, hover=None, level=0.95, height=460):
    """Scatter plot, least-squares line and the confidence band of that line."""
    data = df.dropna(subset=[x, y])
    if len(data) < 3 or data[x].nunique() < 2:
        return go.Figure(layout_title_text="Too few points for a trend")
    fit = stats.linregress(data[x], data[y])
    grid = np.linspace(data[x].min(), data[x].max(), 100)
    line = fit.intercept + fit.slope * grid
    n = len(data)
    residual_sd = np.sqrt(((data[y] - fit.intercept - fit.slope * data[x]) ** 2).sum() / (n - 2))
    spread = ((data[x] - data[x].mean()) ** 2).sum()
    margin = stats.t.ppf((1 + level) / 2, n - 2) * residual_sd * np.sqrt(1 / n + (grid - data[x].mean()) ** 2 / spread)
    fig = px.scatter(data, x=x, y=y, hover_name=hover, opacity=0.5, height=height,
                     title=f"n = {n:,}   r = {fit.rvalue:.2f}   slope = {fit.slope:.3g}")
    fig.add_scatter(x=np.r_[grid, grid[::-1]], y=np.r_[line + margin, (line - margin)[::-1]], fill="toself",
                    fillcolor="rgba(235,104,52,.22)", line={"width": 0}, hoverinfo="skip", name=f"{level:.0%} band")
    fig.add_scatter(x=grid, y=line, mode="lines", line={"color": "#eb6834", "width": 2}, name="Trend")
    return fig


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    borough = st.selectbox("Borough", ["All", *sorted(df.borough.unique())])
    data = df if borough == "All" else df[df.borough == borough]
    st.plotly_chart(scatter_trend(data, "electric_share", "avg_duration_min", hover="station_name"))


if __name__ == "__main__":
    demo()
