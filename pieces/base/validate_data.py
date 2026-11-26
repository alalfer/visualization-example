"""PIECE · Validate the table
Question: Does this table have what my dashboard expects, before anything breaks?
Needs: A table and the list of columns your dashboard uses.
Avoid when: Never. A clear message beats a red traceback in front of your audience.
Filter risk: None. Run it on the full table, right after loading.
Try it: Add a column name that does not exist and read the message.
New in Streamlit: st.error shows a message; st.stop ends the script run there.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/status
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def check_table(df, required):
    """Return a list of problems. An empty list means the table is fine."""
    problems = [f"Missing column: {name}" for name in required if name not in df.columns]
    if df.empty:
        problems.append("The table has no rows.")
    duplicates = int(df.duplicated().sum())
    if duplicates:
        problems.append(f"{duplicates:,} rows are exact duplicates.")
    return problems


def stop_if_invalid(df, required):
    """Show the problems and stop the app if a required column is missing."""
    problems = check_table(df, required)
    for problem in problems:
        st.warning(problem)
    if any(p.startswith("Missing") for p in problems) or df.empty:
        st.error("Fix the table, then rerun.")
        st.stop()


def demo():
    df = pd.read_csv(DATA / "stations.csv")
    wanted = st.multiselect("Columns the dashboard needs", [*df.columns, "price_usd"], ["latitude", "longitude"])
    stop_if_invalid(df, wanted)
    st.success(f"All {len(wanted)} required columns found in {len(df):,} rows.")


if __name__ == "__main__":
    demo()
