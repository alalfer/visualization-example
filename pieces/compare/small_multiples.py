"""PIECE · Small multiples
Question: Is the pattern the same in every group?
Needs: Data with a categorical column with 2 to 12 values.
Avoid when: You have more than about 12 panels. They become too small to read.
Filter risk: A shared axis makes small groups look flat. That can be the honest view, so choose it on purpose.
Try it: Turn off the shared scale and see which conclusion changes.
New in Streamlit: st.toggle returns True or False.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/facet-plots/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def small_multiples(df, x, y, panel, shared_y=True, columns=3, kind="line", height=None):
    """Draw the same chart once per group, with the panels in a grid."""
    if df.empty:
        return go.Figure(layout_title_text="No data for these filters")
    draw = {"line": px.line, "bar": px.bar}[kind]
    rows = -(-df[panel].nunique() // columns)
    fig = draw(df, x=x, y=y, facet_col=panel, facet_col_wrap=columns, height=height or 230 * rows + 60)
    if not shared_y:
        fig.update_yaxes(matches=None, showticklabels=True)
    return fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    df["hour"] = df.timestamp.dt.hour
    profile = df.groupby(["borough", "hour"], as_index=False, observed=True).trips_started.mean()
    profile = profile[profile.borough != "Outside NYC"]
    shared = st.toggle("Same vertical scale in all panels", True)
    st.plotly_chart(small_multiples(profile, "hour", "trips_started", "borough", shared))


if __name__ == "__main__":
    demo()
