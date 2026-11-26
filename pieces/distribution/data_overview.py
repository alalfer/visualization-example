"""PIECE · Data overview
Question: What is in this table, before I draw anything?
Needs: Any table.
Avoid when: Never. This is the first tab you build on a new dataset.
Filter risk: Missing values may hide inside one group only. Rerun it after filtering.
Try it: Load your own dataset here. Which column surprises you?
New in Streamlit: st.dataframe shows a sortable, scrollable table.
Session: S8
Unit: UD2
Docs: https://docs.streamlit.io/develop/api-reference/data/st.dataframe
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def column_summary(df):
    """One row per column: type, share missing, number of distinct values, example."""
    return pd.DataFrame({
        "column": df.columns,
        "type": [str(t) for t in df.dtypes],
        "missing": df.isna().mean().round(3).values,
        "distinct": df.nunique().values,
        "example": [str(df[c].dropna().iloc[0])[:40] if df[c].notna().any() else "" for c in df.columns],
    })


def data_overview(df):
    """Rows, columns and a summary of every column."""
    left, right, third = st.columns(3)
    left.metric("Rows", f"{len(df):,}")
    right.metric("Columns", df.shape[1])
    third.metric("Exact duplicates", f"{int(df.duplicated().sum()):,}")
    st.dataframe(column_summary(df), hide_index=True,
                 column_config={"missing": st.column_config.ProgressColumn("Missing", format="percent", min_value=0, max_value=1)})
    with st.expander("Numeric summary"):
        numeric = df.select_dtypes("number")
        if numeric.empty:
            st.info("This table has no numeric columns.")
        else:
            st.dataframe(numeric.describe().T)


def demo():
    table = st.selectbox("Table", ["stations.csv", "trips_sample.parquet", "neighborhoods.csv"])
    path = DATA / table
    data_overview(pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path))


if __name__ == "__main__":
    demo()
