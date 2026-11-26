"""PIECE · Heatmap of two categories
Question: Which combinations of two categories stand out?
Needs: Two categorical columns and, optionally, one measure.
Avoid when: Either column has more than about 30 values. Filter or group them first.
Filter risk: Empty cells can mean zero or no data. Say which one in the caption.
Try it: Compare the raw count with the share of each row.
New in Streamlit: st.segmented_control is a row of buttons where one is selected.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/imshow/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def category_heatmap(df, rows, columns, value=None, normalize=None, height=420):
    """Cross two categories. normalize can be None, "row" or "column"."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    if value:
        table = df.pivot_table(index=rows, columns=columns, values=value, aggfunc="sum", observed=True)
    else:
        table = pd.crosstab(df[rows], df[columns])
    if normalize == "row":
        table = table.div(table.sum(axis=1), axis=0)
    elif normalize == "column":
        table = table.div(table.sum(axis=0), axis=1)
    return px.imshow(table, text_auto=".0%" if normalize else ",.0f", aspect="auto", color_continuous_scale="Blues", height=height)


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    mode = st.segmented_control("Show", ["Count", "Share of each row"], default="Count", required=True)
    st.plotly_chart(category_heatmap(df, "start_borough", "bike_type", normalize="row" if mode != "Count" else None))


if __name__ == "__main__":
    demo()
