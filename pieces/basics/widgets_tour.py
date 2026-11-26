"""PIECE · Widgets return values
Question: How does a user's choice get into my code?
Needs: Nothing.
Avoid when: You have many options. Use a selectbox instead of radio buttons.
Filter risk: A multiselect can return an empty list. Your code must handle that.
Try it: Change a widget type, for example the selectbox to st.radio.
New in Streamlit: A widget is a function call that returns the current value.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/widgets
"""
from datetime import date

import streamlit as st


def demo():
    number = st.slider("st.slider", 0, 10, 3)
    text = st.selectbox("st.selectbox", ["Manhattan", "Brooklyn", "Queens"])
    many = st.multiselect("st.multiselect", ["member", "casual"], default=["member"])
    when = st.date_input("st.date_input", date(2025, 7, 1))
    flag = st.toggle("st.toggle")
    pill = st.segmented_control("st.segmented_control", ["Day", "Week", "Month"], default="Week")
    st.subheader("What your code receives")
    st.write({"slider": number, "selectbox": text, "multiselect": many, "date_input": when, "toggle": flag, "segmented_control": pill})


if __name__ == "__main__":
    demo()
