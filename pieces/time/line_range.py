"""PIECE · Line with range controls
Question: How has the measure changed, and can I zoom into a period?
Needs: One date column and one numeric measure.
Avoid when: The dates are not evenly spaced and you hide that fact. Show the gaps.
Filter risk: A filter can leave a few points, or create gaps that the line silently joins.
Try it: Press 1m and then drag the slider. Does the trend look the same?
New in Streamlit: Nothing new. The controls live inside the Plotly chart, without a rerun.
Session: S10
Unit: UD3.3
Docs: https://plotly.com/python/range-slider/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def line_range(df, time, value, color=None, height=460):
    """A line chart with quick range buttons and a slider below."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    fig = px.line(df.sort_values(time), x=time, y=value, color=color, height=height)
    return fig.update_xaxes(rangeslider_visible=True, rangeselector={"buttons": [
        {"count": 7, "label": "1w", "step": "day", "stepmode": "backward"},
        {"count": 1, "label": "1m", "step": "month", "stepmode": "backward"},
        {"count": 3, "label": "3m", "step": "month", "stepmode": "backward"},
        {"step": "all", "label": "All"},
    ]})


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    daily = df.groupby(df.timestamp.dt.normalize()).trips_started.sum().reset_index()
    st.plotly_chart(line_range(daily, "timestamp", "trips_started"))


if __name__ == "__main__":
    demo()
