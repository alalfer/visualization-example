"""PIECE · KPI with sparkline
Question: Is today's number normal for this measure, or part of a trend?
Needs: A time-ordered list of values.
Avoid when: The series has so few points that the line is noise.
Filter risk: The line rescales to its own range, so small moves can look dramatic.
Try it: Switch chart_type to "bar" or "area".
New in Streamlit: st.metric can draw a small chart with chart_data.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/data/st.metric
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def kpi_sparkline(label, series, column=st, chart_type="line"):
    """A metric whose value is the last point of the series, with the series behind it."""
    series = series.dropna()
    if series.empty:
        column.metric(label, "No data", border=True)
        return
    delta = f"{series.iloc[-1] - series.iloc[-2]:+,.0f}" if len(series) > 1 else None
    column.metric(label, f"{series.iloc[-1]:,.0f}", delta, chart_data=series.tolist(), chart_type=chart_type, border=True)


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    weekly = df.set_index("timestamp").resample("W-SUN").sum(numeric_only=True).iloc[1:-1]  # drop partial weeks
    left, middle, right = st.columns(3)
    kpi_sparkline("Trips last full week", weekly.trips_started, left)
    kpi_sparkline("Member trips", weekly.member_started, middle)
    kpi_sparkline("E-bike trips", weekly.electric_started, right, "area")


if __name__ == "__main__":
    demo()
