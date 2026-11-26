"""PIECE · Density map
Question: Where do points pile up when bubbles overlap too much?
Needs: Latitude, longitude and many rows. A weight column is optional.
Avoid when: You need to identify single places. A heat blob has no names.
Filter risk: Colour scale is relative to the current selection. The same red can mean very different totals.
Try it: Change the radius from 5 to 40. Is the hot spot the same?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.2
Docs: https://plotly.com/python/density-heatmaps/
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


def densest_cell(lat, lon, weights, radius, zoom):
    """Total weight in the fullest cell. Without this ceiling, thousands of points paint one solid block."""
    cell = max(radius * 360 / (256 * 2 ** zoom), 1e-4)  # degrees covered by the radius at this zoom
    lat_bins = max(int((lat.max() - lat.min()) / cell), 2)
    lon_bins = max(int((lon.max() - lon.min()) / cell), 2)
    grid, _, _ = np.histogram2d(lat, lon, bins=[lat_bins, lon_bins], weights=weights)
    return max(float(grid.max()) * 0.01, 1.0)  # 0.01 was tuned by eye on this kind of map, across several radii


def density_map(df, lat, lon, weight=None, radius=18, height=500):
    """Smooth density of points. The radius decides how much local detail survives."""
    data = df.dropna(subset=[lat, lon])
    if data.empty:
        return go.Figure(layout_title_text="No data for these filters")
    center, zoom = fit_view(data[lat], data[lon])
    weights = data[weight].fillna(0) if weight else pd.Series(1.0, index=data.index)
    ceiling = densest_cell(data[lat], data[lon], weights, radius, zoom)
    fig = px.density_map(data.assign(point_weight=weights), lat=lat, lon=lon, z="point_weight", radius=radius, zoom=zoom, center=center,
                         range_color=[0, ceiling], map_style="carto-positron", color_continuous_scale="Blues", height=height)
    return fig.update_layout(coloraxis_showscale=False)  # the units of a heat map are not meaningful, so no colour bar


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet", columns=["start_lat", "start_lng", "hour"])
    radius = st.slider("Radius (pixels)", 3, 40, 12)
    hours = st.slider("Start hour", 0, 23, (7, 9))
    st.plotly_chart(density_map(df[df.hour.between(*hours)], "start_lat", "start_lng", radius=radius))


if __name__ == "__main__":
    demo()
