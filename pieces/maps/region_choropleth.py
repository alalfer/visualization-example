"""PIECE · Choropleth by country or US state
Question: How does a measure vary across countries or US states?
Needs: One row per area with an ISO-3 country code or a two-letter US state code.
Avoid when: Large empty areas dominate the picture. Check a ranking next to the map.
Filter risk: Missing areas appear as blanks. Blank can mean zero or no data, so say which one.
Try it: Replace the population by a rate. Does the map change?
New in Streamlit: Nothing new. No GeoJSON file is needed: Plotly already knows these shapes.
Session: S10
Unit: UD3.2
Docs: https://plotly.com/python/choropleth-maps/
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def region_choropleth(df, code, value, name=None, level="usa", height=480):
    """level = "usa" for state codes such as NY, "world" for ISO-3 codes such as ESP."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    mode = "USA-states" if level == "usa" else "ISO-3"
    scope = "usa" if level == "usa" else "world"
    return px.choropleth(df, locations=code, locationmode=mode, color=value, hover_name=name, scope=scope,
                         color_continuous_scale="Blues", height=height)


def demo():
    df = pd.DataFrame({
        "state": ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"],
        "population_2020": [39538223, 29145505, 21538187, 20201249, 13002700, 12812508, 11799448, 10711908, 10439388, 10077331],
    })
    st.plotly_chart(region_choropleth(df, "state", "population_2020"))
    st.caption("Ten most populated states, 2020 US census. Blank states are outside this short example, not zero.")


if __name__ == "__main__":
    demo()
