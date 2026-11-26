"""PIECE · Theme
Question: How do all my charts share one look without repeating code?
Needs: Nothing. Call it once at the top of the dashboard.
Avoid when: You want one chart to differ on purpose. Pass colours to that chart instead.
Filter risk: Colours assigned by order repaint categories when a filter removes one. Use color_map below.
Try it: Switch template to "plotly_dark" or "simple_white" and rerun.
New in Streamlit: The .streamlit/config.toml file sets the app theme; this piece sets the chart theme.
Session: S8
Unit: UD1
Docs: https://plotly.com/python/templates/
"""
import plotly.express as px

COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQUENTIAL = "Blues"
DIVERGING = ["#c8501f", "#f1f0ec", "#1f5fae"]  # orange = losing, grey = zero, blue = gaining


def apply_theme(template="plotly_white"):
    """Set the defaults used by every Plotly Express chart that follows."""
    px.defaults.template = template
    px.defaults.color_discrete_sequence = COLORS
    px.defaults.color_continuous_scale = SEQUENTIAL


def color_map(categories):
    """Give each category a fixed colour, so a filter never repaints the survivors."""
    return {name: COLORS[i % len(COLORS)] for i, name in enumerate(sorted(categories))}


def demo():
    import pandas as pd
    import streamlit as st

    template = st.selectbox("Template", ["plotly_white", "simple_white", "ggplot2", "plotly_dark", "seaborn"])
    apply_theme(template)
    df = pd.DataFrame({"borough": ["Manhattan", "Brooklyn", "Queens", "Bronx"], "trips": [28, 11, 4, 1]})
    st.plotly_chart(px.bar(df, x="borough", y="trips", color="borough", color_discrete_map=color_map(df.borough)), theme=None)


if __name__ == "__main__":
    demo()
