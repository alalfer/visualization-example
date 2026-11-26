"""PIECE · Annotated events
Question: What happened at that spike or dip?
Needs: A time series and a short list of events you have checked.
Avoid when: You have not verified the event. A label suggests a cause.
Filter risk: Events outside the filtered dates must disappear, or the axis stretches to reach them.
Try it: Add an event of your own and find out whether it coincides with a change.
New in Streamlit: Nothing new.
Session: S10
Unit: UD1
Docs: https://plotly.com/python/text-and-annotations/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def annotated_events(df, time, value, events, height=430):
    """Line chart with a labelled vertical line per event. events = {"2025-01-01": "New Year"}."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    fig = px.line(df.sort_values(time), x=time, y=value, height=height)
    first, last = df[time].min(), df[time].max()
    for date, label in events.items():
        when = pd.Timestamp(date)
        if first <= when <= last:
            fig.add_shape(type="line", x0=when, x1=when, y0=0, y1=1, yref="paper", line={"color": "#52514e", "dash": "dot"})
            fig.add_annotation(x=when, y=1, yref="paper", text=label, showarrow=False, yanchor="bottom")
    return fig.update_layout(margin={"t": 40})


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    daily = df.groupby(df.timestamp.dt.normalize()).trips_started.sum().reset_index()
    events = {"2025-07-04": "Independence Day", "2025-11-27": "Thanksgiving", "2025-12-25": "Christmas"}
    st.plotly_chart(annotated_events(daily, "timestamp", "trips_started", events))
    st.caption("These are calendar dates. A date near a dip does not prove it caused the dip.")


if __name__ == "__main__":
    demo()
