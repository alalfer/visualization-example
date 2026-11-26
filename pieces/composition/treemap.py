"""PIECE · Treemap
Question: How is a total divided across a hierarchy?
Needs: One or more nested categorical columns and a positive measure.
Avoid when: Values can be negative, or you need exact comparison. Use bars.
Filter risk: Rectangles rearrange after each filter, so the eye cannot track an item.
Try it: Click a borough to zoom in. Click the top bar to come back.
New in Streamlit: Nothing new.
Session: S9
Unit: UD1
Docs: https://plotly.com/python/treemaps/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def treemap(df, path, value, height=520):
    """Rectangles with an area proportional to the measure. Zero values are dropped."""
    data = df[df[value] > 0] if not df.empty else df
    if data.empty:
        return go.Figure(layout_title_text="No data for these filters")
    fig = px.treemap(data, path=[px.Constant("All"), *path], values=value, height=height)
    return fig.update_traces(root_color="#f1f0ec", textinfo="label+percent root")


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    table = df.groupby(["borough", "neighborhood"], as_index=False).trips_started.sum()
    st.plotly_chart(treemap(table, ["borough", "neighborhood"], "trips_started"))


if __name__ == "__main__":
    demo()
