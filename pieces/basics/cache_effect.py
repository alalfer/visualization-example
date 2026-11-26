"""PIECE · What the cache does
Question: Why is my dashboard slow, and when does the cache help?
Needs: Nothing.
Avoid when: Do not cache a function whose result must change with time, unless you set ttl.
Filter risk: The cache stores one copy per argument. Do not pass huge tables if you can pass a path.
Try it: Move the slider with the cache off, then with it on. Which delay would you tolerate?
New in Streamlit: @st.cache_data stores results by function and arguments.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/concepts/architecture/caching
"""
import time

import streamlit as st


def slow_calculation(month):
    time.sleep(1.5)  # imagine reading a large file or fitting a model
    return month * 1000


@st.cache_data
def cached_calculation(month):
    time.sleep(1.5)
    return month * 1000


def demo():
    use_cache = st.toggle("Use the cache", False)
    month = st.slider("Month", 1, 12, 6)
    start = time.perf_counter()
    result = cached_calculation(month) if use_cache else slow_calculation(month)
    st.metric("Result", f"{result:,}")
    st.metric("Time for this rerun", f"{time.perf_counter() - start:.2f} s")
    st.caption("Research on latency: even modest delays reduce how much people explore (Liu & Heer, 2014).")


if __name__ == "__main__":
    demo()
