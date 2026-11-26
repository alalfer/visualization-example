# Proposed dataset · NOAA storm events

Official records of storms and other severe weather in the United States, from the National Weather Service.

| | |
|---|---|
| File | `storm_events.csv.gz`: 151,631 rows, 13 columns |
| One row is | one weather event in one county or forecast zone that caused damage, injuries or deaths |
| Key number | `damage_property`, in US dollars |
| Categories | `event_group` (8 groups) |
| Many values | `event_type` (43), `state` (52) and `county_or_zone` |
| Time | `begin_date`, date and time, from January 2015 to December 2025 |
| Place | `state`, two-letter code, and `latitude` and `longitude` for most events |

## Load it

```python
@st.cache_data
def load_data():
    return pd.read_csv("data/storm_risk/storm_events.csv.gz", parse_dates=["begin_date"])
```

pandas reads the compressed `.csv.gz` file directly.

## Columns

| Column | What it is |
|---|---|
| `begin_date` | When the event started |
| `state` | Two-letter code of the state |
| `county_or_zone` | County or forecast zone where it happened |
| `event_type` | NOAA's type, for example `Flash Flood`, `Hail` or `Hurricane` |
| `event_group` | Our grouping of the types: Flood, Tropical, Thunderstorm, hail and tornado, Wind, Winter and cold, Heat and drought, Wildfire, Other |
| `damage_property`, `damage_crops` | Estimated damage, in dollars of that year |
| `injuries`, `deaths` | Direct and indirect, added together |
| `latitude`, `longitude` | Where the event began |
| `episode_id` | One storm system can cause many events, and they share this number |
| `event_id` | Unique number of the event |

`us_states.csv` has the population in 2024 and the land area of each state, for damage per person or per km².

A map by state: `px.choropleth(table, locations="state", locationmode="USA-states", color="...", scope="usa")`. A map of points: `px.scatter_map(table, lat="latitude", lon="longitude", ...)`.

## Things to know

- **Only events with an impact.** NOAA recorded 681,344 events in 2015–2025 in the 50 states, DC and Puerto Rico. This file keeps the 151,631 with any damage, injury or death. Marine areas and other territories are left out.
- **Damage is an estimate** made by each weather office, often rounded, and not adjusted for inflation. It is missing for 1.4% of the events.
- **Extremely concentrated.** 1% of the events cause 96% of the damage. One wildfire, in California in November 2018, accounts for $17 billion. Totals jump from year to year, and one storm can decide a ranking.
- **Floods and winter weather are recorded by zone**, so 17.4% of the events have no coordinates.
- **Recent years** can still be revised by NOAA.

## Source

NOAA National Centers for Environmental Information, [Storm Events Database](https://www.ncdc.noaa.gov/stormevents/), details files 2015–2025. US public domain. Population and area: US Census Bureau, public domain. The script that built these files is kept by the teacher.
