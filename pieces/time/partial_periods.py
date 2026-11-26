"""PIECE · Partial period warning
Question: Is that last drop real, or is the last period simply incomplete?
Needs: One datetime column and one numeric measure.
Avoid when: You show rates or means per day, which are comparable across partial periods.
Filter risk: Any date filter creates partial periods at both ends of the chart.
Try it: Set the grain to Week: the last bar collapses. Then remove the incomplete periods.
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.3
Docs: https://pandas.pydata.org/docs/reference/api/pandas.Period.html
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"
FREQUENCIES = {"Week": "W", "Month": "M", "Quarter": "Q"}


def flag_partial(df, time, value, freq="W"):
    """Aggregate by period and mark the periods that the data does not fully cover."""
    periods = df[time].dt.to_period(freq)
    table = df.groupby(periods)[value].sum().rename_axis("period").reset_index(name=value)
    first, last = df[time].min().normalize(), df[time].max().normalize()
    table["start"] = table.period.dt.start_time
    table["complete"] = (table.start >= first) & (table.period.dt.end_time.dt.normalize() <= last)
    return table


def partial_chart(df, time, value, freq="W", hide_partial=False, height=430):
    """Bars by period. Incomplete periods are grey and named in the title."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    table = flag_partial(df, time, value, freq)
    partial = int((~table.complete).sum())
    if hide_partial:
        table = table[table.complete]
    table["status"] = table.complete.map({True: "Complete", False: "Incomplete"})
    return px.bar(table, x="start", y=value, color="status", height=height, title=f"{partial} incomplete period(s)",
                  color_discrete_map={"Complete": "#2a78d6", "Incomplete": "#b5b4ad"})


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    end = st.date_input("Data available until", pd.Timestamp(2025, 9, 16), pd.Timestamp(2025, 2, 1), pd.Timestamp(2025, 12, 31))
    grain = st.segmented_control("Grain", list(FREQUENCIES), default="Week", required=True)
    hide = st.toggle("Remove incomplete periods")
    data = df[df.timestamp < pd.Timestamp(end) + pd.Timedelta(days=1)]
    st.plotly_chart(partial_chart(data, "timestamp", "trips_started", FREQUENCIES[grain], hide))


if __name__ == "__main__":
    demo()
