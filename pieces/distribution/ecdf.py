"""PIECE · Cumulative distribution (ECDF)
Question: What share of cases are below a value, and how do groups compare at every point?
Needs: One numeric column. Works with very different group sizes.
Avoid when: Your audience has not seen one. Explain it first or use a histogram.
Filter risk: Robust. No bins and no smoothing, so nothing to re-tune when the filter changes.
Try it: Read the chart aloud: "80% of member trips last less than ... minutes".
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/ecdf-plots/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def ecdf(df, value, group=None, log_scale=False, height=420):
    """For each value on x, the share of rows at or below it."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    fig = px.ecdf(df, x=value, color=group, log_x=log_scale, height=height)
    return fig.update_layout(yaxis_tickformat=".0%", yaxis_title="Share of rows at or below")


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet", columns=["duration_min", "rider_type", "bike_type"])
    df = df[df.duration_min > 0].sample(20000, random_state=1)
    group = st.selectbox("Compare by", ["rider_type", "bike_type"])
    st.plotly_chart(ecdf(df, "duration_min", group, log_scale=True))


if __name__ == "__main__":
    demo()
