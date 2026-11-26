"""PIECE · PCA explorer
Question: Which items look alike when I consider many measures together?
Needs: Three or more numeric columns and one row per item.
Avoid when: The columns are few or nearly independent. Then plot them directly.
Filter risk: PCA is refitted on the selection, so axes change meaning with each filter.
Try it: Remove the largest loading from the list. Do the groups still separate?
New in Streamlit: @st.cache_data also works for slow calculations, not only for loading files.
Session: S9
Unit: UD3.1
Docs: https://plotly.com/python/pca-visualization/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).parents[2] / "data"


def pca_table(df, features):
    """Return the 2D scores, the loadings and the variance explained by each axis."""
    data = df.dropna(subset=features)
    model = PCA(n_components=2)
    scores = model.fit_transform(StandardScaler().fit_transform(data[features]))
    table = data.assign(PC1=scores[:, 0], PC2=scores[:, 1])
    loadings = pd.DataFrame(model.components_.T, index=features, columns=["PC1", "PC2"])
    return table, loadings, model.explained_variance_ratio_


def pca_explorer(df, features, color=None, name=None, height=500):
    """Scatter of the two main axes, with the arrows showing what each axis means."""
    if len(df.dropna(subset=features)) < 3 or len(features) < 2:
        return go.Figure(layout_title_text="PCA needs at least three rows and two measures")
    table, loadings, explained = pca_table(df, features)
    fig = px.scatter(table, x="PC1", y="PC2", color=color, hover_name=name, opacity=0.6, height=height,
                     labels={"PC1": f"PC1 ({explained[0]:.0%} of variance)", "PC2": f"PC2 ({explained[1]:.0%} of variance)"})
    scale = table[["PC1", "PC2"]].abs().max().max() * 0.9
    for feature, row in loadings.iterrows():
        fig.add_annotation(x=row.PC1 * scale, y=row.PC2 * scale, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", text="",
                           showarrow=True, arrowhead=2, arrowcolor="#52514e")
        fig.add_annotation(x=row.PC1 * scale, y=row.PC2 * scale, text=feature, showarrow=False, yshift=10 if row.PC2 >= 0 else -10,
                           font={"color": "#0b0b0b"}, bgcolor="rgba(255,255,255,.7)")
    return fig


def demo():
    df = pd.read_csv(DATA / "stations.csv").query("borough != 'Outside NYC' and trips_per_day > 5")
    options = ["trips_per_day", "net_flow_per_day", "member_share", "electric_share", "avg_duration_min"]
    features = st.multiselect("Measures", options, default=options)
    st.plotly_chart(pca_explorer(df, features, "borough", "station_name"))


if __name__ == "__main__":
    demo()
