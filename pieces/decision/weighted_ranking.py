"""PIECE · Weighted ranking
Question: Which option comes out on top when I state clearly what matters?
Needs: One row per option and several measures. Each one needs a direction: higher better or lower better.
Avoid when: One criterion is a hard limit. Remove those options first, do not trade them off.
Filter risk: Scaling depends on which options are in the table. Removing one can reorder the others.
Try it: Move the weights to the extremes, then switch the scaling. Is there a clear winner, or does it depend on you?
New in Streamlit: Widgets created in a loop need different labels or keys.
Session: S10
Unit: UD4
Docs: https://plotly.com/python/horizontal-bar-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def scale(values, method="rank"):
    """Put a column on a 0-1 scale. With "rank", one extreme value cannot decide the whole ranking."""
    if method == "rank":
        return values.rank(pct=True)
    return (values - values.min()) / ((values.max() - values.min()) or 1)


def score_options(df, criteria, weights, method="rank"):
    """criteria = {"column": +1 or -1}. Each column is scaled 0-1, then combined with the weights."""
    scored = df.copy()
    total = sum(weights.values()) or 1
    scored["score"] = 0.0
    for column, direction in criteria.items():
        scaled = scale(df[column], method)
        scored[f"{column}_scaled"] = scaled if direction > 0 else 1 - scaled
        scored["score"] += scored[f"{column}_scaled"] * weights[column] / total
    return scored.sort_values("score", ascending=False)


def weighted_ranking(scored, name, top=10, height=None):
    """Bars with the score of the best options."""
    if scored.empty:
        return go.Figure(layout_title_text="No options left with these filters")
    table = scored.head(top).sort_values("score")
    fig = px.bar(table, x="score", y=name, orientation="h", height=height or 26 * len(table) + 110, range_x=[0, 1])
    return fig.update_layout(yaxis_title=None, xaxis_title="Score (0 to 1)")


def candidate_table():
    """Example options: residential neighbourhoods served by Citi Bike."""
    df = pd.read_csv(DATA / "neighborhoods.csv").query("is_residential and stations > 0 and population_2020 >= 5000")
    df["residents_per_station"] = df.population_2020 / df.stations
    df["trips_per_station"] = df.trips_started / df.stations
    df["stations_per_km2"] = df.stations / df.area_km2
    return df


def demo():
    df = candidate_table()
    criteria = {"residents_per_station": 1, "trips_per_station": 1, "stations_per_km2": -1}
    weights = {column: st.slider(f"Weight: {column}", 0, 10, 5) for column in criteria}
    method = st.segmented_control("Scaling", ["rank", "min-max"], default="rank", required=True)
    scored = score_options(df, criteria, weights, method)
    st.plotly_chart(weighted_ranking(scored, "neighborhood"))


if __name__ == "__main__":
    demo()
