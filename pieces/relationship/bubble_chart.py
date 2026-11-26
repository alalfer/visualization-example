"""PIECE · Bubble chart
Question: How do items compare across three measures at once?
Needs: Two numeric columns for position and one for size.
Avoid when: Exact size comparison matters. People judge areas poorly.
Filter risk: Bubble sizes rescale to the largest bubble left after the filter. Fix size_max.
Try it: Swap the size measure and see which items become prominent.
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/bubble-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def bubble_chart(df, x, y, size, name, color=None, log_x=False, height=480):
    """Position shows two measures, bubble area shows a third."""
    data = df.dropna(subset=[x, y, size])
    if data.empty:
        return go.Figure(layout_title_text="No data for these filters")
    return px.scatter(data, x=x, y=y, size=size, color=color, hover_name=name, log_x=log_x, size_max=24, opacity=0.6, height=height)


def demo():
    df = pd.read_csv(DATA / "neighborhoods.csv").query("stations > 0 and population_2020 > 0")
    df["residents_per_station"] = df.population_2020 / df.stations
    df["trips_per_station"] = df.trips_started / df.stations
    st.plotly_chart(bubble_chart(df, "residents_per_station", "trips_per_station", "population_2020", "neighborhood", "borough", log_x=True))


if __name__ == "__main__":
    demo()
