"""PIECE · Highlight among many series
Question: How does one series behave against all the others?
Needs: A date column, a measure and a column with many series.
Avoid when: Every series matters equally. Use small multiples.
Filter risk: Too few series remove the context that makes the highlight meaningful.
Try it: Highlight an outer neighbourhood. Does it follow the system?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.3
Docs: https://plotly.com/python/line-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def highlight_series(df, time, value, series, highlight, height=460):
    """All series in thin grey. The chosen ones drawn on top, in colour and labelled."""
    fig = go.Figure().update_layout(height=height, yaxis_title=value, showlegend=False)
    if df.empty:
        return fig.update_layout(title="No data for these filters")
    colors = ["#2a78d6", "#eb6834", "#1baf7a"]
    data = df.sort_values(time)
    for name, part in data.groupby(series, observed=True):
        if name not in highlight:
            fig.add_scatter(x=part[time], y=part[value], mode="lines", line={"color": "#d8d7d0", "width": 1}, hoverinfo="skip")
    for i, name in enumerate(highlight):
        part = data[data[series] == name]
        if part.empty:
            continue
        fig.add_scatter(x=part[time], y=part[value], mode="lines", name=name, line={"color": colors[i % 3], "width": 2.5})
        fig.add_annotation(x=part[time].iloc[-1], y=part[value].iloc[-1], text=name, showarrow=False, xanchor="left", xshift=6,
                           font={"color": "#0b0b0b"})
    return fig.update_layout(margin={"r": 170})


def demo():
    df = pd.read_parquet(DATA / "station_day.parquet", columns=["date", "neighborhood", "trips_started"])
    df = df.astype({"neighborhood": str})
    monthly = df.groupby([df.date.dt.to_period("M").dt.start_time, "neighborhood"]).trips_started.sum().reset_index()
    top = monthly.groupby("neighborhood").trips_started.sum().nlargest(40).index
    monthly = monthly[monthly.neighborhood.isin(top)]
    chosen = st.multiselect("Highlight", sorted(top), default=sorted(top)[:1], max_selections=3)
    st.plotly_chart(highlight_series(monthly, "date", "trips_started", "neighborhood", chosen))


if __name__ == "__main__":
    demo()
