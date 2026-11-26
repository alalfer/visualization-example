"""PIECE · Compare with another period
Question: Compared to what? Is this period better or worse than a fair reference?
Needs: Daily data covering both periods.
Avoid when: The two periods are not comparable (holidays, price change). Say so.
Filter risk: Periods of different length or with different weekends give a false difference.
Try it: Compare two months aligned by date, then align them by weekday.
New in Streamlit: st.columns also organises widgets.
Session: S10
Unit: UD3.3
Docs: https://plotly.com/python/line-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def align_periods(daily, time, value, ranges, by_weekday=False):
    """ranges = {"label": (start, end)}. Each period is indexed by day number from its start."""
    parts = []
    for label, (start, end) in ranges.items():
        part = daily[daily[time].between(start, end)].sort_values(time).copy()
        if by_weekday and not part.empty:  # start at the first Monday, so that weekends line up
            first_monday = part[part[time].dt.day_of_week == 0][time].min()
            part = part[part[time] >= first_monday]
        part["day_number"] = range(1, len(part) + 1)
        part["period"] = label
        parts.append(part)
    return pd.concat(parts)


def compare_periods(daily, time, value, ranges, by_weekday=False, height=430):
    """Overlay the periods on a common day number."""
    table = align_periods(daily, time, value, ranges, by_weekday)
    if table.empty:
        return go.Figure(layout_title_text="No data for these filters")
    return px.line(table, x="day_number", y=value, color="period", height=height, hover_data={time: "|%a %d %b"})


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    daily = df.groupby(df.timestamp.dt.normalize()).trips_started.sum().reset_index()
    names = [pd.Timestamp(2025, m, 1).strftime("%B") for m in range(1, 13)]
    left, right = st.columns(2)
    first, second = left.selectbox("Period A", names, 5), right.selectbox("Period B", names, 8)
    ranges = {}
    for name in (first, second):
        start = pd.Timestamp(f"1 {name} 2025")
        ranges[name] = (start, start + pd.offsets.MonthEnd(0))
    weekday = st.toggle("Align by weekday")
    st.plotly_chart(compare_periods(daily, "timestamp", "trips_started", ranges, weekday))


if __name__ == "__main__":
    demo()
