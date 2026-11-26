"""PIECE · Share a filtered view by link
Question: How do I send someone exactly the view I am looking at?
Needs: A few filters with simple values.
Avoid when: The state is too large to fit in a link, such as a long list of selected items.
Filter risk: A link can carry a value that no longer exists. Check it before using it.
Try it: Choose a borough, copy the address bar and open it in a new tab.
New in Streamlit: st.query_params reads and writes the values in the page address.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.query_params
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def linked_selectbox(label, options, parameter):
    """A selectbox whose value is stored in the address, so that the link keeps it."""
    current = st.query_params.get(parameter, options[0])
    index = options.index(current) if current in options else 0
    choice = st.selectbox(label, options, index=index)
    st.query_params[parameter] = choice
    return choice


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    borough = linked_selectbox("Borough", sorted(df.borough.unique()), "borough")
    top = df[df.borough == borough].nlargest(10, "trips_per_day").sort_values("trips_per_day")
    st.plotly_chart(px.bar(top, x="trips_per_day", y="station_name", orientation="h", title=f"Busiest stations in {borough}"))
    st.code(f"?borough={borough}", language=None)


if __name__ == "__main__":
    demo()
