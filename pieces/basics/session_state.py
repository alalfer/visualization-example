"""PIECE · Remembering between reruns
Question: If the script restarts each time, how does the app remember anything?
Needs: Nothing.
Avoid when: The value already belongs to a widget, which remembers it by itself.
Filter risk: Stored selections can point to rows that a new filter removed.
Try it: Remove session_state and use a normal variable. What happens to the counter?
New in Streamlit: st.session_state is a dictionary that survives reruns, one per browser tab.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/concepts/architecture/session-state
"""
import streamlit as st


def demo():
    normal_variable = 0
    st.session_state.setdefault("clicks", 0)
    if st.button("Add one"):
        normal_variable += 1
        st.session_state.clicks += 1
    left, right = st.columns(2)
    left.metric("Normal variable", normal_variable)
    right.metric("st.session_state", st.session_state.clicks)


if __name__ == "__main__":
    demo()
