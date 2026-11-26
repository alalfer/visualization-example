"""PIECE · Cleveland dot plot
Question: How do many categories compare, when bars would be heavy?
Needs: One categorical column and one or two numeric measures.
Avoid when: The zero baseline is what you want to stress. Use bars.
Filter risk: Dots do not start at zero, so a filter can zoom the axis and exaggerate gaps.
Try it: Replace the mean by the median and see which neighbourhoods move.
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/dot-plots/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def dot_plot(df, category, value, group=None, height=None):
    """One dot per category (and per group), sorted by the measure."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    keys = [category, group] if group else [category]
    table = df.groupby(keys, observed=True, as_index=False)[value].mean()
    order = table.groupby(category, observed=True)[value].mean().sort_values().index.tolist()
    fig = px.scatter(table, x=value, y=category, color=group, height=height or max(320, 24 * len(order) + 100),
                     category_orders={category: order[::-1]})
    return fig.update_traces(marker={"size": 11}).update_yaxes(showgrid=True, gridcolor="#e4e3de", title=None)


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    df = df[df.duration_min.between(1, 120)]
    top = df.start_neighborhood.value_counts().head(20).index
    selection = df[df.start_neighborhood.isin(top)]
    st.plotly_chart(dot_plot(selection, "start_neighborhood", "duration_min", "rider_type"))
    st.caption("Mean trip duration in minutes, for the 20 neighbourhoods with most sampled trips.")


if __name__ == "__main__":
    demo()
