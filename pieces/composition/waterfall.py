"""PIECE · Waterfall
Question: Which parts explain the change between two totals?
Needs: A start total, an end total and the same parts in both.
Avoid when: You have more than about 10 parts. Group the small ones first.
Filter risk: Filtering parts changes both totals. Show them, or the steps stop adding up.
Try it: Choose two months far apart. Which borough explains most of the change?
New in Streamlit: Nothing new.
Session: S9
Unit: UD1
Docs: https://plotly.com/python/waterfall-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def waterfall(before, after, start_label="Start", end_label="End", height=440):
    """before and after are Series indexed by part. Bars show how one becomes the other."""
    parts = sorted(set(before.index) | set(after.index))
    if not parts:
        return go.Figure(layout_title_text="No data for these filters")
    change = after.reindex(parts, fill_value=0) - before.reindex(parts, fill_value=0)
    change = change.sort_values(ascending=False)
    fig = go.Figure(go.Waterfall(
        x=[start_label, *change.index, end_label], y=[before.sum(), *change.values, after.sum()],
        measure=["absolute", *["relative"] * len(change), "total"],
        increasing={"marker": {"color": "#1f5fae"}}, decreasing={"marker": {"color": "#c8501f"}}, totals={"marker": {"color": "#52514e"}},
        connector={"line": {"color": "#b5b4ad"}},
    ))
    return fig.update_layout(height=height, showlegend=False, yaxis_title="Trips")


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    months = {pd.Timestamp(2025, m, 1).strftime("%B"): m for m in range(1, 13)}
    first = st.selectbox("From", list(months), index=0)
    second = st.selectbox("To", list(months), index=6)
    totals = df.groupby([df.timestamp.dt.month, "borough"], observed=True).trips_started.sum()
    st.plotly_chart(waterfall(totals[months[first]], totals[months[second]], first, second))


if __name__ == "__main__":
    demo()
