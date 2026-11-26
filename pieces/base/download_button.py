"""PIECE · Download what you see
Question: How can someone take the filtered data away for their own report?
Needs: The filtered table.
Avoid when: The data is confidential, or the file would be huge.
Filter risk: Make sure you pass the filtered table, not the original one.
Try it: Change the file name so it includes the selected borough.
New in Streamlit: st.download_button sends a file to the browser.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def download_csv(df, file_name="selection.csv", label="Download this selection"):
    """Add a button that downloads the table as CSV."""
    st.download_button(label, df.to_csv(index=False).encode("utf-8"), file_name, "text/csv")


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    borough = st.selectbox("Borough", sorted(df.borough.unique()))
    selection = df[df.borough == borough]
    st.dataframe(selection.head(20), hide_index=True)
    download_csv(selection, f"stations_{borough}.csv")


if __name__ == "__main__":
    demo()
