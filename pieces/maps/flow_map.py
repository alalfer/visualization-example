"""PIECE · Flow map
Question: Where do things travel from and to?
Needs: One row per origin-destination pair, with coordinates for both ends and a weight.
Avoid when: You have many pairs. Show only the top ones, and say so.
Filter risk: Line width rescales to the largest flow left. Hide flows below a threshold.
Try it: Raise the number of flows until the map becomes useless. Where is that limit?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.2
Docs: https://plotly.com/python/lines-on-tile-maps/
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def flow_map(df, from_lat, from_lon, to_lat, to_lon, weight, label=None, top=30, height=520):
    """Draw the largest flows. Line width is proportional to the weight."""
    fig = go.Figure().update_layout(height=height, showlegend=False, margin={"l": 0, "r": 0, "t": 10, "b": 0})
    data = df.nlargest(top, weight)
    if data.empty:
        return fig.update_layout(title="No data for these filters")
    largest = data[weight].max()
    for _, row in data.iterrows():
        fig.add_trace(go.Scattermap(lat=[row[from_lat], row[to_lat]], lon=[row[from_lon], row[to_lon]], mode="lines",
                                    line={"width": 1 + 8 * row[weight] / largest, "color": "#2a78d6"}, opacity=0.55,
                                    text=f"{row[label]}: {row[weight]:,.0f}" if label else None, hoverinfo="text"))
    center = {"lat": float(data[[from_lat, to_lat]].stack().mean()), "lon": float(data[[from_lon, to_lon]].stack().mean())}
    return fig.update_layout(map={"style": "carto-positron", "center": center, "zoom": 11})


def demo():
    df = pd.read_csv(DATA / "flows.csv")
    df = df[df.origin != df.destination].copy()  # trips inside one neighbourhood have no line to draw
    df["pair"] = df.origin_name + " to " + df.destination_name
    top = st.slider("Number of flows", 5, 200, 30)
    st.plotly_chart(flow_map(df, "origin_lat", "origin_lon", "destination_lat", "destination_lon", "trips", "pair", top))


if __name__ == "__main__":
    demo()
