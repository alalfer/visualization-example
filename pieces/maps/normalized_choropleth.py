"""PIECE · Choropleth with normalisation
Question: Is this area high because it is big, or because something is really different there?
Needs: One row per area, a code that matches the GeoJSON, and a count plus its denominator.
Avoid when: You only have raw counts. They usually draw a population map.
Filter risk: Small denominators give extreme rates. Hide areas below a minimum.
Try it: Switch from total trips to trips per resident. Which neighbourhood moves most?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.2
Docs: https://plotly.com/python/tile-county-choropleth/
"""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def normalized_choropleth(df, geojson, code, value, name, center, zoom=10, height=560, cap_quantile=0.95):
    """Colour each area by the value. The feature id in the GeoJSON must equal the code column.

    Values above cap_quantile share the darkest colour, so that one extreme area does not wash out the rest.
    """
    data = df.dropna(subset=[value])
    if data.empty:
        return go.Figure(layout_title_text="No data for these filters")
    top = data[value].quantile(cap_quantile) if cap_quantile else data[value].max()
    return px.choropleth_map(data, geojson=geojson, locations=code, color=value, hover_name=name, center=center, zoom=zoom,
                             range_color=[0, top], map_style="carto-positron", opacity=0.75, color_continuous_scale="Blues", height=height)


def demo():
    df = pd.read_csv(DATA / "neighborhoods.csv").query("is_residential and stations > 0")
    geojson = json.loads((DATA / "neighborhoods.geojson").read_text())
    df["Total trips"] = df.trips_started
    df["Trips per km2"] = df.trips_started / df.area_km2
    df["Trips per resident"] = df.trips_started / df.population_2020.where(df.population_2020 >= 1000)
    df["Trips per station"] = df.trips_started / df.stations
    measure = st.segmented_control("Colour by", ["Total trips", "Trips per km2", "Trips per resident", "Trips per station"],
                                   default="Total trips", required=True)
    center = {"lat": df.latitude.mean(), "lon": df.longitude.mean()}
    st.plotly_chart(normalized_choropleth(df, geojson, "code", measure, "neighborhood", center))
    st.caption("Top five: " + ", ".join(df.nlargest(5, measure).neighborhood))


if __name__ == "__main__":
    demo()
