"""PIECE · Recommendation card
Question: What do you recommend, on what evidence, and what could prove you wrong?
Needs: Your decision, written by you. Evidence should come from values computed in the dashboard.
Avoid when: You have no decision yet. An empty card is a good to-do list, though.
Filter risk: Hard-coded numbers go stale when filters move. Compute them, or fix the tab to the full data.
Try it: Write your own project's recommendation in one sentence.
New in Streamlit: st.container(border=True) groups elements in a visible box.
Session: S10
Unit: UD4
Docs: https://docs.streamlit.io/develop/api-reference/layout/st.container
"""
import streamlit as st


def recommendation_card(decision, evidence, risks, change_my_mind, next_step=None):
    """decision: one sentence. evidence: list of (label, value, note). risks: list of short sentences."""
    with st.container(border=True):
        st.subheader("Recommendation")
        st.markdown(f"### {decision}")
        for column, (label, value, note) in zip(st.columns(len(evidence)), evidence):
            column.metric(label, value, help=note)
        left, right = st.columns(2)
        with left:
            st.markdown("**Main risks**")
            for risk in risks:
                st.markdown(f"- {risk}")
        with right:
            st.markdown("**What would change my mind**")
            st.markdown(change_my_mind)
            if next_step:
                st.markdown(f"**Next step:** {next_step}")


def demo():
    recommendation_card(
        decision="Write one sentence here that someone could act on tomorrow.",
        evidence=[("Evidence 1", "123", "Where it comes from"), ("Evidence 2", "45%", "Where it comes from"), ("Evidence 3", "+7", "Where it comes from")],
        risks=["What the data cannot see.", "Which assumption matters most."],
        change_my_mind="Name the result that would make you recommend something else.",
        next_step="The smallest action that would test this recommendation.",
    )


if __name__ == "__main__":
    demo()
