"""PIECE · Map or ranking?
Question: Does this question really need a map?
Needs: A table with coordinates, one measure and a name.
Avoid when: The question is about adjacency or distance. Then the map wins.
Filter risk: Both views must receive the same filtered table, or they contradict each other.
Try it: Ask "which is the busiest?" and "are the busiest ones close together?". Which view answers each?
New in Streamlit: st.columns places two charts side by side.
Session: S10
Unit: UD3.2
Docs: https://plotly.com/python/tile-scatter-maps/
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def fit_view(lat, lon):
    """Centre and zoom that keep every point on screen."""
    span = max(lat.max() - lat.min(), (lon.max() - lon.min()) * 0.75, 0.005)
    return {"lat": float(lat.mean()), "lon": float(lon.mean())}, float(np.clip(np.log2(360 / span) - 0.9, 1, 15))


def map_vs_ranking(df, lat, lon, value, name, top=15, height=520):
    """Return the same top items twice: as positions on a map and as an ordered list."""
    data = df.nlargest(top, value)
    if data.empty:
        empty = go.Figure(layout_title_text="No data for these filters")
        return empty, empty
    center, zoom = fit_view(data[lat], data[lon])
    the_map = px.scatter_map(data, lat=lat, lon=lon, size=value, hover_name=name, size_max=22, center=center, zoom=zoom,
                             map_style="carto-positron", height=height)
    ranking = px.bar(data.sort_values(value), x=value, y=name, orientation="h", height=height)
    return the_map, ranking


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    top = st.slider("Stations", 5, 30, 15)
    the_map, ranking = map_vs_ranking(df, "latitude", "longitude", "trips_per_day", "station_name", top)
    left, right = st.columns(2)
    left.plotly_chart(the_map)
    right.plotly_chart(ranking)


if __name__ == "__main__":
    demo()
