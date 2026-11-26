"""Catalog of pieces. Run it with: streamlit run catalog.py

Browse every piece live, read its code and see when not to use it.
"""
import ast
import importlib
from pathlib import Path

import pandas as pd
import streamlit as st

from pieces.base.theme import apply_theme

st.set_page_config(page_title="Dashboard kit", layout="wide")
apply_theme()

ROOT = Path(__file__).parent
FAMILIES = {
    "basics": "Streamlit basics", "base": "Base", "kpi": "KPI", "compare": "Comparison",
    "distribution": "Distribution", "relationship": "Relationship", "composition": "Composition",
    "time": "Time", "maps": "Maps", "interaction": "Interaction", "decision": "Decision",
}


def read_header(path):
    """Read the docstring of a piece without importing it."""
    lines = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))).splitlines()
    fields = {"title": lines[0].replace("PIECE · ", "")}
    for line in lines[1:]:
        key, _, value = line.partition(": ")
        fields[key] = value
    return fields


@st.cache_data
def read_catalog():
    rows = []
    for family in FAMILIES:
        for path in sorted((ROOT / "pieces" / family).glob("*.py")):
            rows.append({"id": f"{family}/{path.stem}", "family": FAMILIES[family], "path": str(path), **read_header(path)})
    return pd.DataFrame(rows)


catalog = read_catalog()
requested = st.query_params.get("piece")

with st.sidebar:
    st.title("Dashboard kit")
    st.caption(f"{len(catalog)} pieces. Each one is a single file you can copy and change.")
    session = st.segmented_control("Session", ["All", "S8", "S9", "S10"], default="All", required=True)
    subset = catalog if session == "All" else catalog[catalog["Session"] == session]
    families = [name for name in FAMILIES.values() if name in set(subset.family)]
    start_family = 0
    if requested in set(catalog.id):
        wanted = catalog.loc[catalog.id == requested, "family"].iloc[0]
        start_family = families.index(wanted) if wanted in families else 0
    family = st.radio("Family", families, index=start_family)
    choices = subset[subset.family == family]
    labels = choices.title.tolist()
    start_piece = 0
    if requested in set(choices.id):
        start_piece = choices.id.tolist().index(requested)
    title = st.radio("Piece", labels, index=start_piece)
    st.divider()
    st.link_button("All Plotly charts", "https://plotly.com/python/")
    st.link_button("Streamlit docs", "https://docs.streamlit.io/develop/api-reference")

piece = choices[choices.title == title].iloc[0]
st.query_params["piece"] = piece["id"]

st.title(piece["title"])
st.markdown(f"#### {piece['Question']}")
needs, avoid, risk = st.columns(3)
needs.markdown(f"**Needs**  \n{piece['Needs']}")
avoid.markdown(f"**Avoid when**  \n{piece['Avoid when']}")
risk.markdown(f"**When filtered**  \n{piece['Filter risk']}")
st.caption(f"{piece['Session']} · {piece['Unit']} · [Documentation]({piece['Docs']}) · Run alone: `streamlit run pieces/{piece['id']}.py`")

live, code = st.tabs(["Live", "Code"])
with code:
    st.markdown(f"**New in Streamlit:** {piece['New in Streamlit']}")
    st.code(Path(piece["path"]).read_text(encoding="utf-8"), language="python", line_numbers=True)
with live:
    st.info(f"**Try it:** {piece['Try it']}")
    module = importlib.import_module("pieces." + piece["id"].replace("/", "."))
    module.demo()
