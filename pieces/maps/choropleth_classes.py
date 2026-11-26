"""PIECE · Choropleth classes
Question: How much does the choice of colour classes decide what the map says?
Needs: One row per area, its code in the GeoJSON and a numeric measure.
Avoid when: Values must be read exactly. Add a table or use a continuous scale.
Filter risk: Quantile classes are recomputed on the selection, so one colour changes meaning.
Try it: Compare equal intervals and quantiles. Which map would you show to justify a decision?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.2
Docs: https://pandas.pydata.org/docs/reference/api/pandas.qcut.html
"""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"
SHADES = ["#d5e5f6", "#a3c6ea", "#6ea3dc", "#2a78d6", "#134a8e"]


def classify(values, scheme="Quantiles", classes=5):
    """Return text labels for each value, using equal-width or equal-count classes."""
    cut = pd.qcut(values, classes, duplicates="drop") if scheme == "Quantiles" else pd.cut(values, classes)
    return cut.map(lambda interval: f"{interval.left:,.0f} to {interval.right:,.0f}"), [
        f"{i.left:,.0f} to {i.right:,.0f}" for i in cut.cat.categories]


def choropleth_classes(df, geojson, code, value, name, center, scheme="Quantiles", classes=5, zoom=9.6, height=520):
    """Map with a stepped legend. Class order follows the values, from light to dark."""
    data = df.dropna(subset=[value])
    if data[value].nunique() < classes:
        return go.Figure(layout_title_text="Too few different values for these classes")
    labels, order = classify(data[value], scheme, classes)
    data = data.assign(**{"class": labels.astype(str)})
    return px.choropleth_map(data, geojson=geojson, locations=code, color="class", hover_name=name, center=center, zoom=zoom, opacity=0.8,
                             map_style="carto-positron", category_orders={"class": order}, color_discrete_sequence=SHADES, height=height)


def demo():
    df = pd.read_csv(DATA / "neighborhoods.csv").query("is_residential and stations > 0")
    geojson = json.loads((DATA / "neighborhoods.geojson").read_text())
    df["trips_per_station"] = df.trips_started / df.stations
    scheme = st.segmented_control("Classes", ["Equal intervals", "Quantiles"], default="Equal intervals", required=True)
    center = {"lat": df.latitude.mean(), "lon": df.longitude.mean()}
    st.plotly_chart(choropleth_classes(df, geojson, "code", "trips_per_station", "neighborhood", center, scheme))


if __name__ == "__main__":
    demo()
