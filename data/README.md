# Data

| Folder or file | What it is |
|---|---|
| `holiday_campaign/` | Proposed dataset: Amazon purchases. See its README |
| `storm_risk/` | Proposed dataset: NOAA storm events. See its README |
| `climate_fund/` | Proposed dataset: CO₂ and energy by country. See its README |
| everything else | The Citi Bike example, used in the lesson, the catalog and `example_dashboard.py`. It is described below |

The three proposed datasets are real, already cleaned and ready to load. You may use one of them for your project, or bring your own data: put your files in this folder too.

# Example data: Citi Bike, New York, 2025

Built from 45.8 million real trips, all of 2025. To rebuild it, see `build/build_citibike.py`. Students do not need that script.

## Sources

| Data | Source | Licence |
|---|---|---|
| Trips | [Citi Bike trip histories](https://citibikenyc.com/system-data), 12 monthly files | [NYCBS Data Use Policy](https://ride.citibikenyc.com/data-sharing-policy) |
| Neighbourhood boundaries | [NYC 2020 Neighborhood Tabulation Areas](https://data.cityofnewyork.us/d/9nt8-h7nd) | NYC Open Data |
| Tract to neighbourhood table | [2020 Census Tracts to 2020 NTAs](https://data.cityofnewyork.us/d/hm78-6dwm) | NYC Open Data |
| Population | [US Census 2020, PL 94-171, New York](https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/New_York/) | US public domain |

## Tables

| File | One row is | Rows | Main columns |
|---|---|---|---|
| `stations.csv` | a station | 2,326 | name, coordinates, neighbourhood, borough, trips per day, net flow per day, member share, e-bike share, mean duration |
| `station_day.parquet` | a station on a day | about 776,000 | date, trips started and ended, net flow, member and e-bike trips, total minutes |
| `station_profile.parquet` | a station, day type and hour | about 108,000 | mean trips started, ended and net per active day |
| `system_hour.parquet` | a borough in an hour | about 37,000 | timestamp, trips started and ended, net flow |
| `trips_sample.parquet` | a sampled trip (1 in 300) | 151,819 | start time, rider type, bike type, stations, neighbourhood, duration, straight-line distance, speed |
| `neighborhoods.csv` | a neighbourhood | 262 | name, borough, residential or not, area, 2020 population, stations, trips |
| `neighborhoods.geojson` | a neighbourhood boundary | 262 | simplified shapes; the feature `id` matches `code` in `neighborhoods.csv` |
| `flows.csv` | a neighbourhood pair | 400 | origin, destination, trips and centre coordinates, largest pairs only |

## What this data cannot see

- **Unmet demand.** An empty station records no trips, so a low count can mean low demand or no bikes.
- **Rebalancing.** Net flow counts rider trips only. It does not include the bikes that the operator moves by van.
- **Capacity and station status.** The trip files do not say how many docks a station has, or when it was full or empty.
- **Who rides.** No personal data is included. Only member or casual.
- **Route.** `distance_km` is a straight line between stations, not the path ridden. Round trips show 0 km.

## Quirks left in on purpose

They are real, and finding them is part of the exercise.

- **Durations are not clean.** Negative values appear on 2 November 2025, when clocks changed. Some trips last close to 24 hours. Decide how to handle them, and say so.
- **Trips cross into New Jersey.** Some 80 stations outside New York City only appear as trip destinations. They are labelled `Outside NYC`.
- **Neighbourhoods at the edge of the service area** can have a single station, so rates per station there are extreme.

## Removed

Four test stations: `Bronx WH station`, at latitude 0 and longitude 0, and `LA Metro Demo 1`, `2` and `3`, in Los Angeles. Together they had 99 trip starts and ends. With them, every map opened on the whole of North America.

## Example used in session 8

Weekdays in 2025, net bikes per hour (trips ended minus trips started):

| Station | Trips per day | Net per day | Largest loss | Largest gain |
|---|---|---|---|---|
| W 41 St & 8 Ave | 295 | −0.8 | −35.3 at 5h | +20.9 at 16h |
| 1 Ave & E 68 St | 307 | +1.9 | −38.4 at 17h | +29.0 at 6h |

The first is next to the Port Authority bus terminal and the second is close to a large hospital area. That explanation is a hypothesis, not something the data shows.
