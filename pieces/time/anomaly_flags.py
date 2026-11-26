"""PIECE · Flag unusual values
Question: Which days are unusual for this series, and deserve a closer look?
Needs: A regular series with one row per period.
Avoid when: You will read a flag as an error or as a cause. It only means: go and check.
Filter risk: The median needs a full window. Short filters flag too much, or nothing.
Try it: Change the threshold. How many days would an analyst have to investigate?
New in Streamlit: Nothing new.
Session: S10
Unit: UD3.3
Docs: https://pandas.pydata.org/docs/reference/api/pandas.Series.rolling.html
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def flag_anomalies(series, window=29, threshold=3.0):
    """A value is unusual when it is far from the rolling median, in robust units (MAD)."""
    center = series.rolling(window, center=True, min_periods=window // 2).median()
    deviation = series - center
    mad = deviation.abs().rolling(window, center=True, min_periods=window // 2).median() * 1.4826
    return pd.DataFrame({"value": series, "expected": center, "score": deviation / mad.where(mad > 0)})


def anomaly_chart(series, window=29, threshold=3.0, height=430):
    """The series, its expected level and the flagged points."""
    if len(series) < window:
        return go.Figure(layout_title_text=f"Needs at least {window} points")
    table = flag_anomalies(series, window, threshold)
    flagged = table[table.score.abs() > threshold]
    fig = go.Figure().update_layout(height=height, title=f"{len(flagged)} points to check")
    fig.add_scatter(x=table.index, y=table.value, name="Series", line={"color": "#c3c2b7", "width": 1})
    fig.add_scatter(x=table.index, y=table.expected, name="Expected", line={"color": "#2a78d6", "width": 2})
    fig.add_scatter(x=flagged.index, y=flagged.value, name="Unusual", mode="markers", marker={"color": "#eb6834", "size": 10, "symbol": "diamond"})
    return fig


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    daily = df.groupby(df.timestamp.dt.normalize()).trips_started.sum()
    threshold = st.slider("Threshold (robust units)", 1.5, 6.0, 3.0, 0.5)
    st.plotly_chart(anomaly_chart(daily, 29, threshold))
    table = flag_anomalies(daily, 29, threshold)
    st.dataframe(table[table.score.abs() > threshold].round(1), height=240)


if __name__ == "__main__":
    demo()
