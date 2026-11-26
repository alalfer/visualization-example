"""PIECE · Load data once
Question: How do I stop reloading the file every time the user touches a widget?
Needs: A path to a CSV or Parquet file inside your data folder.
Avoid when: The data changes during the session. Add ttl=60 so the cache expires.
Filter risk: None here. Filter after loading, never inside this function.
Try it: Remove @st.cache_data, move the slider and watch the load time.
New in Streamlit: @st.cache_data remembers the result of a function between reruns.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/concepts/architecture/caching
"""
import time
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


@st.cache_data
def load_table(path, date_columns=None):
    """Read a CSV or Parquet file. Runs once; later calls return the stored copy."""
    path = Path(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path, parse_dates=date_columns)


def demo():
    st.slider("Touch me: the whole script runs again", 0, 10, 5)
    start = time.perf_counter()
    df = load_table(DATA / "station_day.parquet")
    st.metric("Time to get the table", f"{(time.perf_counter() - start) * 1000:.1f} ms")
    st.caption(f"{len(df):,} rows. The first run reads the file; later runs use the cache.")
    st.dataframe(df.head(), hide_index=True)


if __name__ == "__main__":
    demo()
