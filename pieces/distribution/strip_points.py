"""PIECE · Strip plot
Question: Where is every individual value, and how many are there?
Needs: One numeric column and one categorical column with few rows per group.
Avoid when: You have many thousands of points. They merge into a block. Use box or violin.
Filter risk: This one improves with filters: fewer rows make each point readable.
Try it: Lower the sample size until single points become visible.
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/strip-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def strip_points(df, category, value, hover=None, height=430):
    """One mark per row, with horizontal jitter so that points do not overlap."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    fig = px.strip(df, x=category, y=value, hover_name=hover, height=height, stripmode="overlay")
    return fig.update_traces(marker={"opacity": 0.45, "size": 6}, jitter=0.6)


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    df = df[df.borough != "Outside NYC"]
    st.plotly_chart(strip_points(df, "borough", "trips_per_day", hover="station_name"))
    st.caption("Each point is one station. Hover to read its name.")


if __name__ == "__main__":
    demo()
