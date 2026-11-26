"""PIECE · Box plot with points
Question: How do the median and spread compare across groups?
Needs: One numeric column and one categorical column.
Avoid when: The distribution has two peaks. A box hides them. Use violin.
Filter risk: A box from 4 rows looks as solid as one from 4,000. Show the points and the count.
Try it: Switch points to "all" and compare what you see.
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/box-plots/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def box_points(df, category, value, points="outliers", log_scale=False, height=430):
    """Box per group, ordered by median, with the row count in each label."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    counts = df.groupby(category, observed=True)[value].transform("size")
    labelled = df.assign(group=df[category].astype(str) + " (n=" + counts.map("{:,}".format) + ")")
    order = labelled.groupby("group")[value].median().sort_values().index.tolist()
    fig = px.box(labelled, x="group", y=value, points=points, log_y=log_scale, height=height,
                 category_orders={"group": order})
    return fig.update_layout(xaxis_title=category)


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    df = df[df.duration_min > 0]
    group = st.selectbox("Group by", ["rider_type", "bike_type", "day_type", "start_borough"])
    points = st.segmented_control("Points", ["outliers", "all", "none"], default="outliers", required=True)
    log_scale = st.toggle("Log scale", True)
    sample = df.sample(min(len(df), 8000), random_state=1) if points == "all" else df
    st.plotly_chart(box_points(sample, group, "duration_min", False if points == "none" else points, log_scale))


if __name__ == "__main__":
    demo()
