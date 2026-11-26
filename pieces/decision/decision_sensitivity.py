"""PIECE · Does the decision survive other weights?
Question: How robust is my recommendation to what someone else might value?
Needs: The options, the criteria and their directions.
Avoid when: The weights are fixed by policy. Then report only the ranking.
Filter risk: A smaller set of options inflates each option's share of wins.
Try it: Require a top-3 place instead of first place. Who survives?
New in Streamlit: Nothing new.
Session: S10
Unit: UD4
Docs: https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.dirichlet.html
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def win_share(df, name, criteria, top_k=3, trials=2000):
    """Try many random weights. Return how often each option lands in the top k."""
    scaled = pd.DataFrame(index=df.index)
    for column, direction in criteria.items():
        rank = df[column].rank(pct=True)  # same scaling as weighted_ranking
        scaled[column] = rank if direction > 0 else 1 - rank
    weights = np.random.default_rng(42).dirichlet(np.ones(len(criteria)), trials)
    scores = scaled.to_numpy() @ weights.T
    positions = np.argsort(-scores, axis=0)[:top_k]
    wins = np.bincount(positions.ravel(), minlength=len(df)) / trials
    return pd.DataFrame({name: df[name].to_numpy(), "share_of_scenarios": wins}).sort_values("share_of_scenarios", ascending=False)


def decision_sensitivity(df, name, criteria, top_k=3, show=10, height=None):
    """Bars with the share of weightings under which each option reaches the top k."""
    if len(df) <= top_k:
        return go.Figure(layout_title_text="Too few options to compare")
    table = win_share(df, name, criteria, top_k).head(show).sort_values("share_of_scenarios")
    fig = px.bar(table, x="share_of_scenarios", y=name, orientation="h", range_x=[0, 1], height=height or 26 * len(table) + 110)
    return fig.update_layout(xaxis_tickformat=".0%", xaxis_title=f"Weightings that place it in the top {top_k}", yaxis_title=None)


def demo():
    df = pd.read_csv(DATA / "neighborhoods.csv").query("is_residential and stations > 0 and population_2020 >= 5000")
    df["residents_per_station"] = df.population_2020 / df.stations
    df["trips_per_station"] = df.trips_started / df.stations
    df["stations_per_km2"] = df.stations / df.area_km2
    top_k = st.slider("Must reach the top", 1, 10, 3)
    criteria = {"residents_per_station": 1, "trips_per_station": 1, "stations_per_km2": -1}
    st.plotly_chart(decision_sensitivity(df, "neighborhood", criteria, top_k))


if __name__ == "__main__":
    demo()
