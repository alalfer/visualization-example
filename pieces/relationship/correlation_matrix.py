"""PIECE · Correlation matrix
Question: Which pairs of measures are worth looking at more closely?
Needs: Three or more numeric columns.
Avoid when: You want to prove a link. r only measures linear association; plot the pair.
Filter risk: Small selections give extreme correlations. Show n, and hide the matrix below about 30 rows.
Try it: Switch to spearman. Which cells move most, and what does that tell you about outliers?
New in Streamlit: Nothing new.
Session: S9
Unit: UD2
Docs: https://plotly.com/python/imshow/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def correlation_matrix(df, columns, method="pearson", height=460):
    """Correlation between all pairs, on a diverging scale fixed from -1 to 1."""
    if len(df) < 3 or len(columns) < 2:
        return go.Figure(layout_title_text="Too few rows or columns")
    matrix = df[columns].corr(method=method).round(2)
    return px.imshow(matrix, zmin=-1, zmax=1, text_auto=True, aspect="auto", height=height, title=f"{method.title()} correlation · n = {len(df):,}",
                     color_continuous_scale=["#c8501f", "#f1f0ec", "#1f5fae"])


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    columns = ["trips_per_day", "net_flow_per_day", "member_share", "electric_share", "avg_duration_min"]
    method = st.segmented_control("Method", ["pearson", "spearman"], default="pearson", required=True)
    st.plotly_chart(correlation_matrix(df, columns, method))


if __name__ == "__main__":
    demo()
