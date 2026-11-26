"""PIECE · 2D density
Question: Where do most points fall when a scatter plot turns into a solid blob?
Needs: Two numeric columns and many rows.
Avoid when: There are fewer than about 200 points. Show them directly.
Filter risk: After a narrow filter the grid becomes sparse. Fall back to the scatter.
Try it: Change the number of bins and look for a second cluster.
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/2D-Histogram/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def density_2d(df, x, y, bins=50, height=460):
    """Count points per cell. Cells with no rows stay blank."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    if len(df) < 200:
        return px.scatter(df, x=x, y=y, height=height, title="Few points: showing them directly")
    return px.density_heatmap(df, x=x, y=y, nbinsx=bins, nbinsy=bins, color_continuous_scale="Blues", height=height)


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    df = df[df.duration_min.between(1, 60) & df.distance_km.between(0.01, 12)]
    bins = st.slider("Bins per axis", 10, 120, 50)
    view = st.segmented_control("View", ["Density", "Raw points"], default="Density", required=True)
    if view == "Density":
        st.plotly_chart(density_2d(df, "distance_km", "duration_min", bins))
    else:
        st.plotly_chart(px.scatter(df, x="distance_km", y="duration_min", opacity=0.3, height=460))


if __name__ == "__main__":
    demo()
