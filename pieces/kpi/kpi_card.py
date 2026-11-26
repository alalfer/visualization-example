"""PIECE · KPI cards
Question: What is the one number I should see first, and is it going up or down?
Needs: A value and, ideally, the value of a comparable previous period.
Avoid when: You have no comparison. A number alone says little: compared to what?
Filter risk: The previous period must get the same filters, or the delta lies.
Try it: Add delta_color="inverse" for a measure where going up is bad.
New in Streamlit: st.metric draws a number with its change; st.columns places them side by side.
Session: S8
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/data/st.metric
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[2] / "data"


def percent_change(current, previous):
    """Text for the delta, or None when there is nothing to compare with."""
    return f"{(current - previous) / previous:+.1%}" if previous else None


def short_number(value):
    """1234567 becomes 1.2M. Long numbers are cut off in narrow cards, and few readers need all the digits."""
    if abs(value) >= 1e6:
        return f"{value / 1e6:,.1f}M"
    return f"{value:,.0f}" if abs(value) >= 100 or float(value).is_integer() else f"{value:,.1f}"


def kpi_row(cards):
    """Draw one card per dictionary: {"label": ..., "value": ..., "previous": ...}."""
    for column, card in zip(st.columns(len(cards)), cards):
        value, previous = card["value"], card.get("previous")
        column.metric(card["label"], short_number(value), percent_change(value, previous), border=True)


def demo():
    df = pd.read_parquet(DATA / "system_hour.parquet")
    month = st.slider("Month", 2, 12, 9)
    current = df[df.timestamp.dt.month == month]
    before = df[df.timestamp.dt.month == month - 1]
    kpi_row([
        {"label": "Trips", "value": current.trips_started.sum(), "previous": before.trips_started.sum()},
        {"label": "Member trips", "value": current.member_started.sum(), "previous": before.member_started.sum()},
        {"label": "E-bike trips", "value": current.electric_started.sum(), "previous": before.electric_started.sum()},
    ])
    st.caption("Change is against the previous month, which may have a different number of days.")


if __name__ == "__main__":
    demo()
