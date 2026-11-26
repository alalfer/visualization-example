"""PIECE · Violin plot
Question: What is the full shape of each group, not only its median?
Needs: One numeric column, one categorical column and enough rows in each group.
Avoid when: A group has fewer than about 30 rows. The shape is then mostly invented.
Filter risk: Each violin is scaled on its own, so a tiny group can look as large as a huge one.
Try it: Switch from box to violin. Does a second peak appear?
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/violin/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def violin(df, category, value, split=None, height=430):
    """One violin per group, with the box inside. split colours two sub-groups."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    return px.violin(df, x=category, y=value, color=split, box=True, points=False, height=height)


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    df = df[df.duration_min.between(0, 60)].sample(20000, random_state=1)
    split = st.toggle("Split by rider type")
    st.plotly_chart(violin(df, "day_type", "duration_min", "rider_type" if split else None))


if __name__ == "__main__":
    demo()
