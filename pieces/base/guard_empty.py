"""PIECE · Guard against empty results
Question: What should the page show when a filter leaves nothing, or too little?
Needs: The filtered table and the minimum number of rows that makes a chart honest.
Avoid when: Never. Every filtered dashboard reaches this state sooner or later.
Filter risk: This piece exists because of it.
Try it: Raise the minimum and see at what point a chart stops being meaningful.
New in Streamlit: st.stop ends the run, so nothing below it is drawn.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/execution-flow/st.stop
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def guard_empty(df, minimum=1, message="No data for these filters. Try a wider selection."):
    """Stop the page with a friendly message when there are too few rows."""
    if len(df) < minimum:
        st.info(f"{message} ({len(df):,} rows, {minimum:,} needed.)")
        st.stop()
    if len(df) < 30:
        st.warning(f"Only {len(df)} rows: read these charts with care.")


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    largest = int(df.trips_per_day.max())
    threshold = st.slider("Keep stations with more trips per day than", 0, largest, 20)
    selection = df[df.trips_per_day > threshold]
    guard_empty(selection, minimum=5)
    st.plotly_chart(px.histogram(selection, x="net_flow_per_day", title=f"{len(selection):,} stations"))


if __name__ == "__main__":
    demo()
