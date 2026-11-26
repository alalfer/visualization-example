"""PIECE · Linked selection
Question: What do the items I just selected in one chart look like in another?
Needs: Two views of the same rows.
Avoid when: You have many thousands of points. Sample first, or the browser slows down.
Filter risk: A selection can be very small. Keep the overall shape as a reference.
Try it: Select the fastest trips and see what their duration looks like.
New in Streamlit: Selections arrive as point_indices as well as customdata.
Session: S9
Unit: UD4
Docs: https://docs.streamlit.io/develop/concepts/design/custom-classes
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def demo():
    df = pd.read_parquet(DATA / "trips_sample.parquet")
    df = df[df.duration_min.between(1, 60) & df.distance_km.between(0.05, 12)].sample(4000, random_state=1).reset_index(drop=True)
    left, right = st.columns(2)
    with left:
        fig = px.scatter(df, x="distance_km", y="duration_min", opacity=0.4, height=440)
        event = st.plotly_chart(fig, on_select="rerun", selection_mode=("box", "lasso"), key="scatter")
    chosen = event.selection.point_indices
    subset = df.iloc[chosen] if chosen else df
    with right:
        st.markdown(f"**{len(subset):,} of {len(df):,} trips, share by hour**")
        all_hours = df.hour.value_counts(normalize=True).rename("All trips")
        chosen_hours = subset.hour.value_counts(normalize=True).rename("Selection")
        table = pd.concat([all_hours, chosen_hours], axis=1).fillna(0).sort_index().rename_axis("hour").reset_index().melt("hour", var_name="group", value_name="share")
        st.plotly_chart(px.line(table, x="hour", y="share", color="group", height=400).update_layout(yaxis_tickformat=".0%"))


if __name__ == "__main__":
    demo()
