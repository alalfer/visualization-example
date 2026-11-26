"""PIECE · Trend, cycle and residual
Question: How much of what I see is trend, how much is a repeated cycle, and what is left over?
Needs: A regular series that spans several full cycles.
Avoid when: You have less than two cycles, or irregular dates.
Filter risk: A short date filter removes the cycles that the method needs.
Try it: Change the period from 7 to 30. A wrong period moves the cycle into the residual.
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.3
Docs: https://otexts.com/fpp3/classical-decomposition.html
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

DATA = Path(__file__).parents[2] / "data"


def decompose(series, period=7):
    """Classical additive decomposition: trend + cycle + residual = series."""
    trend = series.rolling(period, center=True, min_periods=period).mean()
    detrended = series - trend
    position = pd.Series(range(len(series)), index=series.index) % period
    pattern = detrended.groupby(position).mean()
    cycle = position.map(pattern - pattern.mean())
    return pd.DataFrame({"Series": series, "Trend": trend, "Cycle": cycle, "Residual": series - trend - cycle})


def decomposition_chart(series, period=7, height=620):
    """Four stacked panels on a shared time axis."""
    if len(series) < 2 * period:
        return go.Figure(layout_title_text=f"Needs at least two full cycles ({2 * period} points)")
    parts = decompose(series, period)
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=list(parts.columns), vertical_spacing=0.05)
    for row, name in enumerate(parts.columns, start=1):
        fig.add_scatter(x=parts.index, y=parts[name], row=row, col=1, showlegend=False, line={"color": "#2a78d6", "width": 1.5})
    return fig.update_layout(height=height, margin={"t": 40})


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    daily = df.groupby(df.timestamp.dt.normalize()).trips_started.sum()
    period = st.select_slider("Cycle length (days)", [7, 14, 30, 90], value=7)
    st.plotly_chart(decomposition_chart(daily, period))


if __name__ == "__main__":
    demo()
