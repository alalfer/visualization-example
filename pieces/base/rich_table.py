"""PIECE · Rich table
Question: Which exact items should I look at, with the numbers visible?
Needs: A table with one row per item, already sorted.
Avoid when: The reader needs a pattern, not exact values. Use a chart.
Filter risk: Bars inside cells rescale with the filter unless you fix the maximum.
Try it: Add a new column with st.column_config.NumberColumn and a format.
New in Streamlit: st.column_config turns plain columns into bars, links or sparklines.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/data/st.column_config
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def rich_table(df, name, bar, sparkline=None, height=420):
    """Show a table with a bar column and, optionally, a small line per row."""
    config = {
        name: st.column_config.TextColumn(name.replace("_", " ").title(), width="large"),
        bar: st.column_config.ProgressColumn(bar.replace("_", " ").title(), format="%.0f",
                                             min_value=0, max_value=float(df[bar].max() or 1)),
    }
    if sparkline:
        config[sparkline] = st.column_config.LineChartColumn(sparkline.replace("_", " ").title())
    st.dataframe(df, column_config=config, hide_index=True, height=height)


def demo():
    stations = pd.read_csv(DATA / "stations.csv")
    daily = pd.read_parquet(DATA / "station_day.parquet", columns=["date", "station_name", "trips_started"])
    top = stations.head(15)[["station_name", "trips_per_day"]].copy()
    daily = daily[daily.station_name.isin(top.station_name)].astype({"station_name": str})
    by_month = daily.groupby(["station_name", daily.date.dt.month]).trips_started.sum()
    top["by_month"] = top.station_name.map(lambda name: by_month[name].tolist())
    rich_table(top, "station_name", "trips_per_day", "by_month")


if __name__ == "__main__":
    demo()
