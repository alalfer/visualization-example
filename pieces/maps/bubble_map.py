"""PIECE · Bubble map
Question: Where is a measure concentrated?
Needs: Latitude, longitude and one numeric measure.
Avoid when: Position adds nothing to the question. Use sorted bars.
Filter risk: Bubble size rescales to the largest point left. The view must follow the filtered points.
Try it: Colour the bubbles by member_share. What pattern appears?
New in Streamlit: Nothing new. Plotly needs an explicit center, or the map opens on the ocean.
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


def bubble_map(df, lat, lon, size, name, color=None, height=500, size_max=14, colors=None):
    """One bubble per row. Base map tiles need internet but no account or key."""
    data = df.dropna(subset=[lat, lon, size])
    data = data[data[size] > 0]
    if data.empty:
        return go.Figure(layout_title_text="No data for these filters")
    center, zoom = fit_view(data[lat], data[lon])
    return px.scatter_map(data, lat=lat, lon=lon, size=size, color=color, hover_name=name, custom_data=[name], size_max=size_max,
                          zoom=zoom, center=center, map_style="carto-positron", opacity=0.7, height=height, color_discrete_map=colors)


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    borough = st.selectbox("Borough", ["All", *sorted(df.borough.unique())])
    data = df if borough == "All" else df[df.borough == borough]
    st.plotly_chart(bubble_map(data, "latitude", "longitude", "trips_per_day", "station_name", "member_share"))


if __name__ == "__main__":
    demo()
