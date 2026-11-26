"""PIECE · KPI against a target
Question: Are we on track against a goal someone actually set?
Needs: A current value, a target and the thresholds that matter.
Avoid when: Nobody agreed on the target. An invented target suggests false precision.
Filter risk: A yearly target makes no sense for one filtered week. Scale it, or hide it.
Try it: Change the target and the near-target threshold.
New in Streamlit: Nothing new. Plotly draws it; st.plotly_chart shows it.
Session: S9
Unit: UD4
Docs: https://plotly.com/python/bullet-charts/
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def bullet(value, target, label="", height=130):
    """A horizontal bullet: bar = value, black line = target, grey bands = below and near target."""
    top = max(value, target) * 1.2 or 1
    return go.Figure(go.Indicator(
        mode="number+gauge+delta", value=value, title={"text": label},
        delta={"reference": target, "relative": True, "valueformat": "+.1%"},
        gauge={
            "shape": "bullet", "axis": {"range": [0, top]}, "bar": {"color": "#2a78d6", "thickness": 0.45},
            "threshold": {"line": {"color": "#0b0b0b", "width": 3}, "thickness": 0.9, "value": target},
            "steps": [{"range": [0, target * 0.8], "color": "#e4e3de"}, {"range": [target * 0.8, target], "color": "#f1f0ec"}],
        },
    )).update_layout(height=height, margin={"l": 170, "r": 40, "t": 20, "b": 30})


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    actual = int(df[df.timestamp.dt.month == 9].trips_started.sum())
    target = st.slider("Target for September (trips)", 1_000_000, 8_000_000, int(actual * 1.1), step=50_000)
    st.plotly_chart(bullet(actual, target, "September trips"))
    st.caption("The target is an example for class, not a real Citi Bike goal.")


if __name__ == "__main__":
    demo()
