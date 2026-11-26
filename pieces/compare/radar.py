"""PIECE · Radar profile
Question: How does the profile of a few items differ across several measures?
Needs: 3 to 8 measures, normalised to the same scale, and very few items.
Avoid when: You need exact comparisons, or have more than 3 items. Use a dot plot.
Filter risk: Scaling depends on the current selection, so a filter redraws every shape.
Try it: Reorder the measures. The shape changes, the data does not. That is the main flaw of radars.
New in Streamlit: st.multiselect can limit how many items are chosen.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/radar-chart/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def radar(df, item, measures, height=460):
    """Scale each measure from 0 to 1 and draw one closed polygon per item."""
    if df.empty or not measures:
        return go.Figure(layout_title_text="No data for these filters")
    scaled = df[[item, *measures]].copy()
    for measure in measures:
        span = scaled[measure].max() - scaled[measure].min()
        scaled[measure] = (scaled[measure] - scaled[measure].min()) / (span or 1)
    long = scaled.melt(id_vars=item, var_name="measure", value_name="scaled_value")
    fig = px.line_polar(long, r="scaled_value", theta="measure", color=item, line_close=True, height=height)
    return fig.update_traces(fill="toself", opacity=0.55)


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    busiest = df.head(40)
    picked = st.multiselect("Stations (up to 3)", busiest.station_name.tolist(),
                            default=busiest.station_name.iloc[[0, 12]].tolist(), max_selections=3)
    measures = ["trips_per_day", "member_share", "electric_share", "avg_duration_min", "net_flow_per_day"]
    st.plotly_chart(radar(busiest[busiest.station_name.isin(picked)], "station_name", measures))
    st.caption("Scaled to 0-1 within the selected stations only.")


if __name__ == "__main__":
    demo()
