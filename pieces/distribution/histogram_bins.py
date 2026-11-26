"""PIECE · Histogram with a bin slider
Question: What shape does this measure have?
Needs: One numeric column.
Avoid when: You compare more than three groups. Use box_points or ecdf.
Filter risk: Bins that suit the full table can hide or invent peaks in a small selection.
Try it: Move the slider from 5 to 200. When do you first see two peaks?
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/histograms/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def histogram_bins(df, value, bins=40, group=None, marginal="box", clip_quantile=None, height=430):
    """Histogram with optional marginal plot. clip_quantile hides the extreme tail, and says so."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    title = None
    if clip_quantile:
        limit = df[value].quantile(clip_quantile)
        title = f"Showing values up to {limit:,.1f}: {(df[value] > limit).mean():.1%} of rows are above"
        df = df[df[value] <= limit]
    return px.histogram(df, x=value, color=group, nbins=bins, marginal=marginal, barmode="overlay",
                        opacity=0.75 if group else 1, title=title, height=height)


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    bins = st.slider("Number of bins", 5, 200, 40)
    clip = st.toggle("Hide the longest 1% of trips", True)
    split = st.toggle("Split by rider type")
    st.plotly_chart(histogram_bins(df, "duration_min", bins, "rider_type" if split else None, clip_quantile=0.99 if clip else None))


if __name__ == "__main__":
    demo()
