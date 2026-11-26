"""PIECE · Animation or small multiples?
Question: How should change over space and time be shown?
Needs: Coordinates, a measure and a column with a few time steps.
Avoid when: You have more than about 12 time steps. Aggregate them first.
Filter risk: Bubble sizes must use the same maximum in every frame or panel, or the change is invented.
Try it: Press play and name which area grew most. Then answer using the panels.
New in Streamlit: A loop can fill st.columns one by one.
Session: S10
Unit: UD3.2
Docs: https://plotly.com/python/animations/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def animated_map(df, lat, lon, size, frame, name, center, zoom=10.2, height=500):
    """One frame per time step. Good for showing off; weak for comparing."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    return px.scatter_map(df, lat=lat, lon=lon, size=size, animation_frame=frame, hover_name=name, center=center, zoom=zoom,
                          map_style="carto-positron", size_max=30, height=height)


def map_panels(df, lat, lon, size, frame, name, center, zoom=9.4, columns=4, height=340):
    """Draw one small map per time step. The size scale is shared, so panels are comparable."""
    largest = df[size].max()
    for slot, (step, part) in zip(st.columns(columns), df.groupby(frame, observed=True)):
        fig = px.scatter_map(part, lat=lat, lon=lon, size=size, hover_name=name, center=center, zoom=zoom, map_style="carto-positron", height=height)
        fig.update_traces(marker={"sizeref": 2 * largest / 26 ** 2, "sizemode": "area"})
        slot.markdown(f"**{step}**")
        slot.plotly_chart(fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0}), key=f"panel_{step}")


def demo():
    days = pd.read_parquet(DATA / "station_day.parquet", columns=["date", "neighborhood", "trips_started"]).astype({"neighborhood": str})
    places = pd.read_csv(DATA / "neighborhoods.csv")[["neighborhood", "latitude", "longitude"]]
    days["quarter"] = "Q" + days.date.dt.quarter.astype(str)
    table = days.groupby(["quarter", "neighborhood"], as_index=False).trips_started.sum().merge(places, on="neighborhood")
    table = table[table.trips_started > 0]
    center = {"lat": table.latitude.mean(), "lon": table.longitude.mean()}
    view = st.segmented_control("View", ["Animation", "Small multiples"], default="Animation", required=True)
    if view == "Animation":
        st.plotly_chart(animated_map(table, "latitude", "longitude", "trips_started", "quarter", "neighborhood", center))
    else:
        map_panels(table, "latitude", "longitude", "trips_started", "quarter", "neighborhood", center)


if __name__ == "__main__":
    demo()
