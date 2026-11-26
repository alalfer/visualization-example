"""PIECE · Moving average
Question: What is the underlying direction once I remove the short-term wiggle?
Needs: A regular time series with one row per period, in order.
Avoid when: The series has few points, or you need to see single events.
Filter risk: The first window has no average. Narrow date filters leave little of the line.
Try it: Compare a window of 7 with one of 28. Which removes the weekly cycle?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.3
Docs: https://pandas.pydata.org/docs/reference/api/pandas.Series.rolling.html
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def moving_average(df, time, value, window=7, height=430):
    """The raw series in pale grey and the moving average on top."""
    fig = go.Figure().update_layout(height=height, yaxis_title=value, hovermode="x unified")
    if df.empty:
        return fig.update_layout(title="No data for these filters")
    data = df.sort_values(time)
    fig.add_scatter(x=data[time], y=data[value], name="Raw", line={"color": "#c3c2b7", "width": 1})
    fig.add_scatter(x=data[time], y=data[value].rolling(window).mean(), name=f"{window}-period average", line={"color": "#2a78d6", "width": 2.5})
    return fig


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    daily = df.groupby(df.timestamp.dt.normalize()).trips_started.sum().reset_index()
    window = st.slider("Window (days)", 2, 60, 7)
    st.plotly_chart(moving_average(daily, "timestamp", "trips_started", window))


if __name__ == "__main__":
    demo()
