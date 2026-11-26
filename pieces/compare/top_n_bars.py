"""PIECE · Top N plus the rest
Question: Who matters most when there are too many categories to show?
Needs: One categorical column with many values and one numeric measure.
Avoid when: The small categories are the point. Use a table with a search box.
Filter risk: The top N changes with every filter, so keep the "Others" bar for scale.
Try it: Move N to 3 and to 30. When does the chart stop answering the question?
New in Streamlit: st.slider returns a number that you can use directly in your code.
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


def top_n_bars(df, category, value, n=10, others_label="Others"):
    """Keep the n largest categories and group the rest in one grey bar."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    totals = df.groupby(category, observed=True)[value].sum().sort_values(ascending=False)
    table = pd.DataFrame({"item": totals.head(n).index.astype(str), value: totals.head(n).values, "kind": "Top"})
    if len(totals) > n:
        rest = pd.DataFrame({"item": [f"{others_label} ({len(totals) - n})"], value: [totals.iloc[n:].sum()], "kind": [others_label]})
        table = pd.concat([table, rest], ignore_index=True)
    fig = px.bar(table, x=value, y="item", color="kind", orientation="h", height=max(280, 26 * len(table) + 90),
                 color_discrete_map={"Top": "#2a78d6", others_label: "#b5b4ad"})
    return fig.update_layout(yaxis={"autorange": "reversed", "title": None}, showlegend=False)


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    column = st.segmented_control("Group by", ["neighborhood", "station_name"], default="neighborhood", required=True)
    n = st.slider("How many to show (N)", 3, 30, 10)
    st.plotly_chart(top_n_bars(df, column, "trips_started", n))


if __name__ == "__main__":
    demo()
