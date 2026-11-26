"""PIECE · Time grain selector
Question: At what level of detail does the pattern appear, or disappear?
Needs: One datetime column and one numeric measure.
Avoid when: The data does not exist at that level. Do not offer hours if you only have days.
Filter risk: A filter can leave one or two points at coarse grains. A line then implies too much.
Try it: Start at Hour and move up to Month. Where does the daily cycle go?
New in Streamlit: st.segmented_control with required=True always returns one option.
Session: S10
Unit: UD3.3
Docs: https://pandas.pydata.org/docs/user_guide/timeseries.html#period
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"
GRAINS = {"Hour": "h", "Day": "D", "Week": "W", "Month": "M", "Quarter": "Q"}


def by_grain(df, time, value, grain="Day", aggregation="sum", group=None):
    """Aggregate the measure into periods. Each row gets the first moment of its period."""
    period = df[time].dt.to_period(GRAINS[grain]).dt.start_time.rename(time)
    keys = [period, group] if group else [period]
    return df.groupby(keys, observed=True)[value].agg(aggregation).reset_index()


def grain_chart(df, time, value, grain="Day", aggregation="sum", group=None, height=430):
    """Line chart of the measure at the chosen grain."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    return px.line(by_grain(df, time, value, grain, aggregation, group), x=time, y=value, color=group, height=height)


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    grain = st.segmented_control("Grain", list(GRAINS), default="Day", required=True)
    st.plotly_chart(grain_chart(df, "timestamp", "trips_started", grain))


if __name__ == "__main__":
    demo()
