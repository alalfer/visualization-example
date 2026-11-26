"""PIECE · Sorted bars
Question: Which categories are largest, and by how much?
Needs: One categorical column and one numeric measure.
Avoid when: There are more than about 25 categories. Use top_n_bars.
Filter risk: Sorting must happen after filtering, or the order stops meaning anything.
Try it: Change the measure, then use horizontal=False.
New in Streamlit: st.plotly_chart shows any Plotly figure.
Session: S8
Unit: UD1
Docs: https://plotly.com/python/horizontal-bar-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def sorted_bars(df, category, value, aggregation="sum", horizontal=True, height=None):
    """Aggregate by category and draw the bars from largest to smallest."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    table = df.groupby(category, observed=True, as_index=False)[value].agg(aggregation)
    table = table.sort_values(value, ascending=horizontal)  # horizontal bars fill from the bottom up
    x, y = (value, category) if horizontal else (category, value)
    return px.bar(table, x=x, y=y, orientation="h" if horizontal else "v", height=height or max(280, 24 * len(table) + 90))


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    boroughs = sorted(df.borough.unique())
    borough = st.selectbox("Borough", boroughs, index=boroughs.index("Brooklyn"))
    selection = df[df.borough == borough].head(15)
    st.plotly_chart(sorted_bars(selection, "station_name", "trips_per_day"))


if __name__ == "__main__":
    demo()
