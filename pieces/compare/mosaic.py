"""PIECE · Mosaic plot
Question: Do two categorical variables depend on each other, and how large is each group?
Needs: Two categorical columns with few values each.
Avoid when: Either column has more than about 6 values. It becomes unreadable.
Filter risk: A filter that leaves one category turns the mosaic into plain stacked bars.
Try it: Swap width and colour. The picture changes but the numbers do not.
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/bar-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]


def mosaic(df, x, color, height=430):
    """Bar width = size of each x group. Bar height = share of each colour within it."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    table = pd.crosstab(df[x], df[color])
    widths = table.sum(axis=1) / table.values.sum()
    shares = table.div(table.sum(axis=1), axis=0)
    left = widths.cumsum().shift(fill_value=0)
    fig = go.Figure()
    for i, name in enumerate(shares.columns):
        fig.add_bar(name=str(name), x=left, y=shares[name], width=widths, offset=0, marker_color=COLORS[i % 6],
                    marker_line={"color": "white", "width": 2}, customdata=table[name],
                    hovertemplate="%{y:.1%} of group · %{customdata:,} rows")
    fig.update_xaxes(tickvals=left + widths / 2, ticktext=[str(v) for v in table.index], range=[0, 1])
    return fig.update_layout(barmode="stack", height=height, yaxis_tickformat=".0%", legend_title=color)


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    x = st.selectbox("Width", ["rider_type", "day_type", "bike_type"])
    color = st.selectbox("Colour", ["bike_type", "rider_type", "day_type"])
    if x == color:
        st.info("Choose two different variables.")
    else:
        st.plotly_chart(mosaic(df, x, color))


if __name__ == "__main__":
    demo()
