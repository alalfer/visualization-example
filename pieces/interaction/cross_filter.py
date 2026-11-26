"""PIECE · Cross-filter from a chart
Question: How can a selection in one view drive the others?
Needs: A chart with custom_data naming each mark, and a second table to filter.
Avoid when: You have only one view. A plain widget is simpler.
Filter risk: An empty selection means "all", not "nothing". Handle both cases on purpose.
Try it: Drag over the map to draw a box, or pick the lasso at the top right of the chart. Double-click to clear.
New in Streamlit: on_select="rerun" makes a chart behave like a widget that returns a selection.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def selected_names(event):
    """Turn the selection returned by st.plotly_chart into a list of names."""
    return [point["customdata"][0] for point in event.selection.points]


def demo():
    stations = pd.read_csv(DATA / "stations.csv").query("borough != 'Outside NYC'")
    profile = pd.read_parquet(DATA / "station_profile.parquet")
    profile = profile[profile.day_type == "Weekday"].astype({"station_name": str})
    center = {"lat": stations.latitude.mean(), "lon": stations.longitude.mean()}
    left, right = st.columns(2)
    with left:
        fig = px.scatter_map(stations, lat="latitude", lon="longitude", size="trips_per_day", hover_name="station_name", size_max=14,
                             custom_data=["station_name"], center=center, zoom=np.log2(360 / 0.35) - 0.9, map_style="carto-positron", height=480)
        event = st.plotly_chart(fig, on_select="rerun", selection_mode=("box", "lasso"), key="station_map")
    chosen = selected_names(event)
    data = profile[profile.station_name.isin(chosen)] if chosen else profile
    hourly = data.groupby("hour", as_index=False).net_per_day.sum()
    with right:
        st.markdown(f"**Net bikes per weekday hour, {len(chosen) or 'all'} stations**")
        st.plotly_chart(px.bar(hourly, x="hour", y="net_per_day", height=440))


if __name__ == "__main__":
    demo()
