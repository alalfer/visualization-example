"""PIECE · Pair plot
Question: What do all the pairwise relationships look like at once?
Needs: Three to six numeric columns. Works best with fewer than about 5,000 rows.
Avoid when: You have many columns. Use the correlation matrix first to choose.
Filter risk: Grouping colours can repaint if a group disappears. Use a fixed colour map.
Try it: Select points with the box tool on one panel: they highlight in all panels.
New in Streamlit: Nothing new. The selection is handled inside Plotly.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/splom/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def pair_plot(df, columns, color=None, height=640):
    """A grid of scatter plots, one per pair of columns."""
    if df.empty or len(columns) < 2:
        return go.Figure(layout_title_text="Too few rows or columns")
    fig = px.scatter_matrix(df, dimensions=columns, color=color, opacity=0.45, height=height)
    return fig.update_traces(diagonal_visible=False, marker={"size": 4})


def demo():
    df = pd.read_csv(DATA / "stations.csv").query("borough != 'Outside NYC'")
    options = ["trips_per_day", "net_flow_per_day", "member_share", "electric_share", "avg_duration_min"]
    columns = st.multiselect("Measures", options, default=options[:4])
    st.plotly_chart(pair_plot(df, columns, "borough"))


if __name__ == "__main__":
    demo()
