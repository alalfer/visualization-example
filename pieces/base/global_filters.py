"""PIECE · Global filters
Question: How does one set of controls drive every chart on the page?
Needs: A table, one date column and the categorical columns to filter on.
Avoid when: A filter only makes sense for one chart. Put that widget beside the chart.
Filter risk: The user can select nothing. Handle it with the guard_empty piece.
Try it: Add a filter on another column by adding its name to the list.
New in Streamlit: Anything inside "with st.sidebar:" appears in the left panel.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def sidebar_filters(df, date_column=None, category_columns=()):
    """Draw the filters in the sidebar and return the filtered table."""
    with st.sidebar:
        st.header("Filters")
        if date_column:
            first, last = df[date_column].min().date(), df[date_column].max().date()
            picked = st.date_input("Period", (first, last), first, last)
            if len(picked) == 2:  # while the user is choosing, only one date exists
                start, end = pd.Timestamp(picked[0]), pd.Timestamp(picked[1])
                df = df[(df[date_column] >= start) & (df[date_column] < end + pd.Timedelta(days=1))]
        for column in category_columns:
            options = sorted(df[column].dropna().astype(str).unique())
            chosen = st.multiselect(column.replace("_", " ").title(), options, placeholder="All")
            if chosen:
                df = df[df[column].astype(str).isin(chosen)]
    return df


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    filtered = sidebar_filters(df, "timestamp", ["borough"])
    st.metric("Trips in the selection", f"{filtered.trips_started.sum():,}")
    st.line_chart(filtered.groupby(filtered.timestamp.dt.date).trips_started.sum())


if __name__ == "__main__":
    demo()
