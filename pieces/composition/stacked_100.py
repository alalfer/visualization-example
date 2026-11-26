"""PIECE · 100% stacked bars
Question: How does the mix change across groups, whatever their size?
Needs: Two categorical columns and one measure (or none, to count rows).
Avoid when: Size differences matter. The chart hides them: add n to the labels.
Filter risk: A group with three rows gets the same bar as one with 3,000.
Try it: Reorder the x axis by share of members.
New in Streamlit: Nothing new.
Session: S9
Unit: UD1
Docs: https://plotly.com/python/bar-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def stacked_100(df, x, color, value=None, height=420):
    """Stacked bars that always reach 100%, with the group size in the label."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    if value:
        table = df.groupby([x, color], observed=True, as_index=False)[value].sum()
    else:
        table = df.groupby([x, color], observed=True).size().reset_index(name="rows")
        value = "rows"
    totals = table.groupby(x, observed=True)[value].transform("sum")
    table["share"] = table[value] / totals
    table["group"] = table[x].astype(str) + "<br>n=" + totals.map("{:,.0f}".format)
    return px.bar(table, x="group", y="share", color=color, height=height, labels={"group": x}).update_layout(yaxis_tickformat=".0%")


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    x = st.selectbox("Groups", ["start_borough", "day_type", "month"])
    color = st.selectbox("Mix of", ["rider_type", "bike_type"])
    st.plotly_chart(stacked_100(df, x, color))


if __name__ == "__main__":
    demo()
