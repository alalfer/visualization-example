"""PIECE · Layout
Question: How do I organise a page?
Needs: Nothing.
Avoid when: You add tabs only to hide clutter. Each tab should answer its own question.
Filter risk: Charts inside tabs still run, so slow charts cost time even when hidden.
Try it: Move the slider into the first column. Tip: code runs top to bottom, so a name must exist before the line that uses it. Create the columns first, then the slider.
New in Streamlit: st.sidebar, st.columns, st.tabs, st.expander and st.container.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/layout
"""
import streamlit as st


def demo():
    with st.sidebar:
        size = st.slider("In the sidebar", 1, 10, 5)
    left, middle, right = st.columns([2, 1, 1])
    left.info("st.columns: wide")
    middle.info("narrow")
    right.info("narrow")
    st.write(f"The slider value is {size}")
    first, second = st.tabs(["First tab", "Second tab"])
    first.write("Each tab can hold a different question.")
    second.write("All tabs are computed on every rerun.")
    with st.expander("st.expander: details on demand"):
        st.write("Good for notes on method and data limits.")
    with st.container(border=True):
        st.write("st.container groups elements. With border=True it draws a box.")


if __name__ == "__main__":
    demo()
