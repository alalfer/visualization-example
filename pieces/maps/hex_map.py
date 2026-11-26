"""PIECE · Hexagon map
Question: Does the answer depend on how I draw the zones?
Needs: Latitude, longitude and a numeric measure.
Avoid when: Real boundaries matter for the decision (districts, states). Use a choropleth.
Filter risk: Few points leave isolated hexagons that look like hot spots.
Try it: Move the slider and watch the "worst zone" change. That is the MAUP.
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.2
Docs: https://plotly.com/python/hexbin-mapbox/
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def fit_view(lat, lon):
    """Centre and zoom that keep every point on screen."""
    span = max(lat.max() - lat.min(), (lon.max() - lon.min()) * 0.75, 0.005)
    return {"lat": float(lat.mean()), "lon": float(lon.mean())}, float(np.clip(np.log2(360 / span) - 0.9, 1, 15))


def hex_map(df, lat, lon, value, hexagons=20, aggregation=np.sum, height=500):
    """Aggregate points into a hexagon grid. hexagons = number of cells across the map."""
    data = df.dropna(subset=[lat, lon, value])
    if len(data) < 2 or data[lat].nunique() < 2 or data[lon].nunique() < 2:
        return go.Figure(layout_title_text="Too few points for a hexagon grid")
    center, zoom = fit_view(data[lat], data[lon])
    fig = ff.create_hexbin_map(data, lat=lat, lon=lon, color=value, agg_func=aggregation, nx_hexagon=hexagons, min_count=1,
                               opacity=0.65, center=center, zoom=zoom, map_style="carto-positron", color_continuous_scale="Blues")
    return fig.update_layout(height=height, margin={"l": 0, "r": 0, "t": 10, "b": 0})


def demo():
    df = pd.read_csv(DATA / "stations.csv").query("borough != 'Outside NYC'")
    hexagons = st.slider("Hexagons across the map", 4, 50, 16)
    st.plotly_chart(hex_map(df, "latitude", "longitude", "trips_started", hexagons))


if __name__ == "__main__":
    demo()
