"""PIECE · t-SNE explorer
Question: Are there local groups of similar items that PCA cannot separate?
Needs: Three or more numeric columns. Keep it under about 2,000 rows so it stays usable in class.
Avoid when: You want to read distances or cluster sizes. t-SNE does not preserve either.
Filter risk: Every run gives a different map. Cache it and never compare two maps directly.
Try it: Change perplexity from 5 to 50. Are these the same groups?
New in Streamlit: st.spinner tells the user that something slow is running.
Session: S9
Unit: UD3.1
Docs: https://plotly.com/python/t-sne-and-umap-projections/
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).parents[2] / "data"


@st.cache_data
def tsne_scores(df, features, perplexity=30):
    """Compute the two t-SNE axes. Cached, because it takes seconds."""
    data = df.dropna(subset=features)
    scaled = StandardScaler().fit_transform(data[features])
    safe_perplexity = min(perplexity, max(2, (len(data) - 1) // 3))
    scores = TSNE(n_components=2, perplexity=safe_perplexity, random_state=42, init="pca").fit_transform(scaled)
    return data.assign(axis_1=scores[:, 0], axis_2=scores[:, 1])


def tsne_explorer(df, features, perplexity=30, color=None, name=None, height=500):
    """Scatter of the t-SNE map. Its axes have no meaning, so they are hidden."""
    if len(df.dropna(subset=features)) < 5:
        return go.Figure(layout_title_text="t-SNE needs at least five rows")
    fig = px.scatter(tsne_scores(df, features, perplexity), x="axis_1", y="axis_2", color=color, hover_name=name, opacity=0.65, height=height)
    return fig.update_xaxes(visible=False).update_yaxes(visible=False)


def demo():
    df = pd.read_csv(DATA / "stations.csv").query("borough != 'Outside NYC' and trips_per_day > 5").head(1200)
    features = ["trips_per_day", "net_flow_per_day", "member_share", "electric_share", "avg_duration_min"]
    perplexity = st.select_slider("Perplexity", [5, 15, 30, 50], value=30)
    with st.spinner("Computing the map..."):
        st.plotly_chart(tsne_explorer(df, features, perplexity, "borough", "station_name"))


if __name__ == "__main__":
    demo()
