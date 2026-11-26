# Proposed dataset · CO₂ and energy by country

Emissions, energy and economy of every country, year by year, compiled by Our World in Data.

| | |
|---|---|
| File | `co2_energy.csv`: 7,595 rows, 29 columns |
| One row is | one country in one year |
| Key number | `co2_per_capita`, tonnes of CO₂ per person (or `co2`, the total) |
| Categories | `continent` (6) |
| Many values | `country` (217) |
| Time | `year`, from 1990 to 2024 |
| Place | `iso_code`, three-letter country code |

## Load it

```python
@st.cache_data
def load_data():
    return pd.read_csv("data/climate_fund/co2_energy.csv")
```

There is no date column, only `year`. To follow something over time, group by `year`: you do not need `resample`.

## Columns

| Column | What it is |
|---|---|
| `country`, `iso_code`, `continent`, `year` | Who and when |
| `population`, `gdp` | Inhabitants, and GDP in international dollars of 2011 |
| `co2` | CO₂ from fossil fuels and industry, in million tonnes |
| `co2_per_capita` | Tonnes per person |
| `co2_per_gdp` | Kilograms per dollar of GDP |
| `share_global_co2` | Percentage of the world's CO₂ that year |
| `cumulative_co2` | Million tonnes since records began |
| `coal_co2`, `oil_co2`, `gas_co2`, `cement_co2` | The total, split by source, in million tonnes |
| `consumption_co2`, `trade_co2` | Emissions of what the country consumes, including imports, and the difference with what it produces |
| `ghg_per_capita` | All greenhouse gases, in tonnes of CO₂ equivalent per person |
| `primary_energy_consumption`, `energy_per_capita` | Energy used, in TWh, and in kWh per person |
| `fossil_share_energy`, `coal_share_energy`, `renewables_share_energy`, `low_carbon_share_energy`, `solar_share_energy`, `wind_share_energy`, `nuclear_share_energy` | Share of the energy used, in % |
| `renewables_share_elec`, `carbon_intensity_elec` | Share of electricity from renewables, and grams of CO₂ per kWh of electricity |

A world map: `px.choropleth(table, locations="iso_code", color="...")`.

## Things to know

- **Not every column reaches 2024.** `gdp` and `co2_per_gdp` end in 2022, and the trade columns end earlier. The energy shares exist for about 80 countries only.
- **Small countries have extreme values per person.** Qatar emits 41 tonnes per person and the United States 14, but the United States emits far more in total. Decide whether you rank by total, per person or per dollar, and say why.
- **Only countries.** The totals for the world, continents and income groups were removed. If you need them, add the countries up yourself, and weight per-person values by population.

## Source

Our World in Data, [CO₂ and Greenhouse Gas Emissions](https://github.com/owid/co2-data) and [Energy](https://github.com/owid/energy-data) datasets, with continents from Our World in Data's regions. Licence: CC BY 4.0. The script that built this file is kept by the teacher.
