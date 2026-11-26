"""PIECE · Drill-down
Question: How do I go from the overview to the detail without changing page?
Needs: A hierarchy, such as borough, neighbourhood and station.
Avoid when: Users need to compare across branches. Drill-down hides the other branches.
Filter risk: A stored selection can become invalid after a filter. Reset it when that happens.
Try it: Click a bar to go down one level. Add a third level.
New in Streamlit: st.session_state remembers values between reruns; st.button returns True on the run after a click.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def clicked_bar(fig, key):
    """Draw a bar chart and return the label of the clicked bar, or None."""
    event = st.plotly_chart(fig, on_select="rerun", selection_mode="points", key=key)
    points = event.selection.points
    return points[0]["y"] if points else None


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    if "borough" not in st.session_state:
        st.session_state.borough = None
    if st.session_state.borough is None:
        st.markdown("**Trips by borough. Click a bar.**")
        table = df.groupby("borough", as_index=False).trips_started.sum().sort_values("trips_started")
        picked = clicked_bar(px.bar(table, x="trips_started", y="borough", orientation="h"), "level_1")
        if picked:
            st.session_state.borough = picked
            st.rerun()
    else:
        if st.button("Back to all boroughs"):
            st.session_state.borough = None
            st.rerun()
        st.markdown(f"**{st.session_state.borough}: top neighbourhoods**")
        part = df[df.borough == st.session_state.borough]
        table = part.groupby("neighborhood", as_index=False).trips_started.sum().nlargest(15, "trips_started").sort_values("trips_started")
        st.plotly_chart(px.bar(table, x="trips_started", y="neighborhood", orientation="h", height=480))


if __name__ == "__main__":
    demo()
