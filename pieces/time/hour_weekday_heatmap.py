"""PIECE · Hour by weekday heatmap
Question: When, within the week, does the activity happen?
Needs: One datetime column with hours, and one measure.
Avoid when: You only have daily data. Then use a calendar heatmap by week and weekday.
Filter risk: Sums depend on how many of each weekday the filter contains. This piece uses means per day.
Try it: Filter to one borough: is the commuting pattern still there?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.3
Docs: https://plotly.com/python/imshow/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def hour_weekday_heatmap(df, time, value, height=380):
    """Mean of the measure per hour and weekday."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    hourly = df.groupby(df[time].dt.floor("h"))[value].sum()
    table = pd.DataFrame({"hour": hourly.index.hour, "weekday": hourly.index.day_name(), "value": hourly.values})
    grid = table.pivot_table(index="weekday", columns="hour", values="value", aggfunc="mean").reindex(DAYS)
    return px.imshow(grid, aspect="auto", color_continuous_scale="Blues", height=height, labels={"color": f"Mean {value}"})


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    borough = st.selectbox("Borough", ["All", *sorted(df.borough.astype(str).unique())])
    data = df if borough == "All" else df[df.borough == borough]
    st.plotly_chart(hour_weekday_heatmap(data, "timestamp", "trips_started"))


if __name__ == "__main__":
    demo()
