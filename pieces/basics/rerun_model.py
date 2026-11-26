"""PIECE · The rerun model
Question: What actually happens when somebody moves a slider?
Needs: Nothing.
Avoid when: Never. Everything else in Streamlit follows from this one idea.
Filter risk: None.
Try it: Move the slider and press the button. Watch the run counter and the clock.
New in Streamlit: The whole script runs again from top to bottom on every interaction.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/get-started/fundamentals/main-concepts
"""
from datetime import datetime

import streamlit as st


def demo():
    st.session_state.runs = st.session_state.get("runs", 0) + 1
    number = st.slider("Pick a number", 0, 100, 50)
    st.button("Press me (this button does nothing else)")
    st.metric("This script has run", f"{st.session_state.runs} times")
    st.write(f"Your number squared is **{number ** 2}**")
    st.caption(f"This line was written at {datetime.now():%H:%M:%S}")


if __name__ == "__main__":
    demo()
