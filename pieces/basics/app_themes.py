"""PIECE · Try themes
Question: How do I change the look of the whole app?
Needs: Nothing.
Avoid when: Never leave decoration in charge of the data: test contrast first.
Filter risk: None.
Try it: Open .streamlit/config.toml, change primaryColor and base, save and rerun.
New in Streamlit: The file .streamlit/config.toml sets the app theme. The theme= argument of st.plotly_chart decides who styles the chart.
Session: S8
Unit: UD1
Docs: https://docs.streamlit.io/develop/concepts/configuration/theming
"""
import pandas as pd
import plotly.express as px
import streamlit as st


def demo():
    df = pd.DataFrame({"borough": ["Manhattan", "Brooklyn", "Queens", "Bronx"], "share": [0.62, 0.27, 0.09, 0.02]})
    template = st.selectbox("Plotly template", ["plotly_white", "simple_white", "ggplot2", "seaborn", "plotly_dark", "presentation"])
    streamlit_style = st.toggle("Let Streamlit style the chart", False)
    fig = px.bar(df, x="borough", y="share", template=template, title="Same chart, different theme")
    st.plotly_chart(fig, theme="streamlit" if streamlit_style else None)
    st.code('[theme]\nbase = "light"\nprimaryColor = "#2a78d6"\nfont = "sans serif"', language="toml")
    st.caption("Example shares for the theme demo, not real figures.")


if __name__ == "__main__":
    demo()
