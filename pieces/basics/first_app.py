"""PIECE · Your first data app
Question: What is the smallest useful dashboard?
Needs: A table.
Avoid when: Never. Start here and add one piece at a time.
Filter risk: If the user clears the filter, the table is empty. See guard_empty.
Try it: Chart avg_duration_min instead of trips_per_day. Then add a metric with the mean of trips_per_day (Manhattan gives 117.7).
New in Streamlit: Title, widget, filter, metric, chart. That is the whole pattern.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/get-started/tutorials/create-an-app
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def demo():
    st.title("Citi Bike stations")
    df = pd.read_csv(DATA / "stations.csv")
    boroughs = st.multiselect("Borough", sorted(df.borough.unique()), default=["Manhattan"])
    selection = df[df.borough.isin(boroughs)]
    st.metric("Stations", len(selection))
    st.plotly_chart(px.histogram(selection, x="trips_per_day", nbins=40))


if __name__ == "__main__":
    demo()
