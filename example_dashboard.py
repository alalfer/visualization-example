"""Worked example of the final project. Run it with: streamlit run example_dashboard.py

Decision: where should Citi Bike put its next stations?
Every chart comes from one file in pieces/. Copy this structure, not this question.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from pieces.base.download_button import download_csv
from pieces.base.guard_empty import guard_empty
from pieces.base.load_data import load_table
from pieces.base.theme import apply_theme
from pieces.compare.top_n_bars import top_n_bars
from pieces.decision.decision_sensitivity import decision_sensitivity, win_share
from pieces.decision.recommendation_card import recommendation_card
from pieces.decision.weighted_ranking import score_options, weighted_ranking
from pieces.distribution.box_points import box_points
from pieces.interaction.cross_filter import selected_names
from pieces.kpi.kpi_card import kpi_row
from pieces.maps.normalized_choropleth import normalized_choropleth
from pieces.relationship.bubble_chart import bubble_chart
from pieces.relationship.ci_bars import ci_bars
from pieces.relationship.correlation_matrix import correlation_matrix
from pieces.relationship.pca_explorer import pca_explorer
from pieces.time.grain_selector import GRAINS, grain_chart
from pieces.time.hour_weekday_heatmap import hour_weekday_heatmap

st.set_page_config(page_title="Next Citi Bike stations", layout="wide")
apply_theme()

DATA = Path(__file__).parent / "data"
MONTHS = [pd.Timestamp(2025, m, 1).strftime("%b") for m in range(1, 13)]
CRITERIA = {"residents_per_station": 1, "trips_per_station": 1, "stations_per_km2": -1}
PROFILE_COLUMNS = ["trips_per_station", "residents_per_station", "stations_per_km2", "member_share", "electric_share", "avg_minutes"]


@st.cache_data
def neighborhood_table(first_month, last_month):
    """One row per residential neighbourhood with Citi Bike, for the chosen months."""
    days = load_table(DATA / "station_day.parquet")
    part = days[days.date.dt.month.between(first_month, last_month)]
    part = part.astype({"neighborhood": str})
    usage = part.groupby("neighborhood", as_index=False).agg(
        trips=("trips_started", "sum"), station_count=("station_name", "nunique"), members=("member_started", "sum"),
        electric=("electric_started", "sum"), minutes=("duration_min_sum", "sum"))
    usage = usage.merge(load_table(DATA / "neighborhoods.csv"), on="neighborhood")
    usage = usage[usage.is_residential & (usage.population_2020 >= 5000) & (usage.trips > 0)].copy()
    usage["residents_per_station"] = usage.population_2020 / usage.station_count
    usage["trips_per_station"] = usage.trips / usage.station_count
    usage["stations_per_km2"] = usage.station_count / usage.area_km2
    usage["member_share"] = usage.members / usage.trips
    usage["electric_share"] = usage.electric / usage.trips
    usage["avg_minutes"] = usage.minutes / usage.trips
    return usage


st.title("Where should Citi Bike put its next stations?")

with st.sidebar:
    st.header("Filters")
    first, last = st.select_slider("Months of 2025", MONTHS, value=("Jan", "Dec"))
    first_month, last_month = MONTHS.index(first) + 1, MONTHS.index(last) + 1
    all_boroughs = ["Manhattan", "Brooklyn", "Queens", "Bronx"]
    boroughs = st.multiselect("Borough", all_boroughs, default=all_boroughs)

areas = neighborhood_table(first_month, last_month)
areas = areas[areas.borough.isin(boroughs)]
guard_empty(areas, minimum=4, message="Choose at least one borough with Citi Bike service.")

hours = load_table(DATA / "system_hour.parquet")
hours = hours[hours.timestamp.dt.month.between(first_month, last_month) & hours.borough.isin(boroughs)]
stations = load_table(DATA / "stations.csv")
stations = stations[stations.borough.isin(boroughs)]
profile = load_table(DATA / "station_profile.parquet")
geojson = json.loads((DATA / "neighborhoods.geojson").read_text())

everywhere = load_table(DATA / "neighborhoods.csv")
uncovered = everywhere[everywhere.is_residential & (everywhere.stations == 0)]
busiest = areas.groupby("borough").trips.sum().idxmax()
share = areas.groupby("borough").trips.sum().max() / areas.trips.sum()
people_share = areas[areas.borough == busiest].population_2020.sum() / areas.population_2020.sum()
st.markdown(f"#### {busiest} starts {share:.0%} of the trips here, but holds {people_share:.0%} of the residents in these neighbourhoods.")

overview, explore, dimensions, space, time_tab, decision = st.tabs(
    ["Overview", "Explore", "Many dimensions", "Space", "Time", "Decision"])

with overview:
    kpi_row([
        {"label": "Trips in the selection", "value": areas.trips.sum()},
        {"label": "Stations", "value": areas.station_count.sum()},
        {"label": "Residents per station", "value": areas.population_2020.sum() / areas.station_count.sum()},
    ])
    left, right = st.columns(2)
    top_share = areas.trips.nlargest(10).sum() / areas.trips.sum()
    left.markdown(f"**Ten neighbourhoods start {top_share:.0%} of the trips**")
    left.plotly_chart(top_n_bars(areas, "neighborhood", "trips", 10).update_layout(xaxis_title="Trips"))
    right.markdown("**Trips per month**")
    monthly = hours.astype({"borough": str})
    monthly = monthly.groupby([monthly.timestamp.dt.to_period("M").dt.start_time, "borough"]).trips_started.sum().reset_index()
    right.plotly_chart(px.line(monthly, x="timestamp", y="trips_started", color="borough", height=420,
                               labels={"timestamp": "", "trips_started": "Trips"}))
    st.caption(f"Outside this selection: {uncovered.population_2020.sum():,} residents live in residential neighbourhoods with no station at all. "
               "Trip data cannot tell us their demand, so they are not scored in the Decision tab.")

with explore:
    left, right = st.columns(2)
    left.markdown("**Stations differ most inside each borough** (distribution)")
    left.plotly_chart(box_points(stations[stations.trips_per_day > 0], "borough", "trips_per_day", log_scale=True))
    right.markdown("**More residents per station does not always mean busier stations** (relationship)")
    right.plotly_chart(bubble_chart(areas, "residents_per_station", "trips_per_station", "population_2020", "neighborhood", "borough", log_x=True))
    left, right = st.columns(2)
    left.markdown("**Trips per station by borough, with 95% intervals** (uncertainty)")
    left.plotly_chart(ci_bars(areas, "borough", "trips_per_station"))
    right.markdown("**Which measures move together?**")
    right.plotly_chart(correlation_matrix(areas, PROFILE_COLUMNS))

with dimensions:
    st.markdown("**Neighbourhoods with a similar profile sit close together.** Arrows show what each axis means.")
    st.plotly_chart(pca_explorer(areas, PROFILE_COLUMNS, "borough", "neighborhood"))
    st.caption("PCA is recalculated with each filter, so its axes can change between selections.")

with space:
    measure = st.segmented_control("Colour by", ["Total trips", "Trips per station", "Residents per station", "Stations per km2"],
                                   default="Residents per station", required=True)
    names = {"Total trips": "trips", "Trips per station": "trips_per_station", "Residents per station": "residents_per_station", "Stations per km2": "stations_per_km2"}
    center = {"lat": areas.latitude.mean(), "lon": areas.longitude.mean()}
    st.plotly_chart(normalized_choropleth(areas, geojson, "code", names[measure], "neighborhood", center))
    st.caption("Residential neighbourhoods with at least 5,000 residents and some Citi Bike trips. Population: 2020 US census.")

with time_tab:
    grain = st.segmented_control("Grain", list(GRAINS), default="Week", required=True)
    st.plotly_chart(grain_chart(hours, "timestamp", "trips_started", grain))
    st.plotly_chart(hour_weekday_heatmap(hours, "timestamp", "trips_started"))
    st.markdown("**Drag a box over the map to see the daily cycle of those stations**")
    active = stations[stations.trips_per_day > 2]
    left, right = st.columns(2)
    with left:
        fig = px.scatter_map(active, lat="latitude", lon="longitude", size="trips_per_day", hover_name="station_name", custom_data=["station_name"],
                             size_max=9, opacity=0.6, center={"lat": active.latitude.mean(), "lon": active.longitude.mean()},
                             zoom=np.log2(360 / 0.35) - 0.9, map_style="carto-positron", height=460)
        event = st.plotly_chart(fig, on_select="rerun", selection_mode=("box", "lasso"), key="time_map")
    chosen = selected_names(event) or active.station_name.tolist()
    cycle = profile[profile.station_name.isin(chosen)].groupby(["day_type", "hour"], observed=True, as_index=False).net_per_day.sum()
    with right:
        st.markdown(f"**Net bikes per hour: {len(chosen):,} stations**")
        fig = px.bar(cycle, x="hour", y="net_per_day", facet_col="day_type", height=430, labels={"net_per_day": "Net bikes per hour", "hour": "Hour"})
        st.plotly_chart(fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])))

with decision:
    st.markdown("Each neighbourhood is scored on three criteria. **Change the weights: does the answer change?**")
    columns = st.columns(3)
    labels = {"residents_per_station": "Residents per station (more is worse served)", "trips_per_station": "Trips per station (more is busier)",
              "stations_per_km2": "Stations per km2 (fewer is thinner coverage)"}
    weights = {name: slot.slider(labels[name], 0, 10, 5) for slot, name in zip(columns, CRITERIA)}
    scored = score_options(areas, CRITERIA, weights)
    left, right = st.columns(2)
    left.markdown("**Ranking with these weights**")
    left.plotly_chart(weighted_ranking(scored, "neighborhood"))
    right.markdown("**Ranking under 2,000 other sets of weights**")
    right.plotly_chart(decision_sensitivity(areas, "neighborhood", CRITERIA, top_k=3))
    best = scored.head(3)
    robust = win_share(areas, "neighborhood", CRITERIA, top_k=3).set_index("neighborhood").share_of_scenarios
    recommendation_card(
        decision=f"Put the next stations in {best.neighborhood.iloc[0]}, then {best.neighborhood.iloc[1]} and {best.neighborhood.iloc[2]}.",
        evidence=[
            ("Residents per station", f"{best.residents_per_station.iloc[0]:,.0f}", f"Selection average: {areas.population_2020.sum() / areas.station_count.sum():,.0f}"),
            ("Trips per station", f"{best.trips_per_station.iloc[0]:,.0f}", f"Selection median: {areas.trips_per_station.median():,.0f}"),
            ("Top 3 across other weights", f"{robust[best.neighborhood.iloc[0]]:.0%}", "Share of 2,000 random weightings that place it in the top 3"),
        ],
        risks=[
            "Trip data shows use, not unmet demand: an empty station records no trips.",
            "No station capacity, street access or cost data is included.",
            "Residents are not the only riders: jobs and visitors also generate trips.",
        ],
        change_my_mind="Live station status showing that stations here are rarely empty or full, or a site survey showing there is no space.",
        next_step="Check station-status history for these neighbourhoods before committing any budget.",
    )
    download_csv(scored.drop(columns=["members", "electric", "minutes"]), "neighbourhood_scores.csv", "Download the scores")
