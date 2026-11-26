"""PIECE · Count, share or index
Question: Which version of this series answers the question: total, share, or growth from a base?
Needs: A date column, a measure and a column with a few groups.
Avoid when: Groups are so small that index 100 multiplies noise.
Filter risk: Share and index depend on which groups and dates are selected. Note the base in the title.
Try it: Look at Queens in the three modes. Does it look small, stable or fast-growing?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.3
Docs: https://plotly.com/python/line-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def transform_measure(table, time, value, group, mode):
    """mode: "Count", "Share" (of each period) or "Index" (first period = 100)."""
    data = table.sort_values(time).copy()
    if mode == "Share":
        data[mode] = data[value] / data.groupby(time, observed=True)[value].transform("sum")
    elif mode == "Index":
        base = data.groupby(group, observed=True)[value].transform("first")
        data[mode] = 100 * data[value] / base.where(base != 0)
    else:
        data[mode] = data[value]
    return data


def count_share_index(table, time, value, group, mode="Count", height=430):
    """The same data, three different questions."""
    if table.empty:
        return go.Figure(layout_title_text="No data for these filters")
    data = transform_measure(table, time, value, group, mode)
    fig = px.line(data, x=time, y=mode, color=group, height=height)
    if mode == "Share":
        fig.update_layout(yaxis_tickformat=".0%")
    return fig


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    monthly = df[df.borough != "Outside NYC"].astype({"borough": str})
    monthly = monthly.groupby([monthly.timestamp.dt.to_period("M").dt.start_time, "borough"]).trips_started.sum().reset_index()
    mode = st.segmented_control("Show", ["Count", "Share", "Index"], default="Count", required=True)
    st.plotly_chart(count_share_index(monthly, "timestamp", "trips_started", "borough", mode))


if __name__ == "__main__":
    demo()
