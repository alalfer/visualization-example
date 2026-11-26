# Proposed dataset · Amazon purchases

Real Amazon purchase histories, shared by a panel of about 5,000 US consumers who also answered a short survey.

| | |
|---|---|
| File | `purchases.csv.gz`: 181,079 rows, 11 columns |
| One row is | one item bought, on one day, by one person of the panel |
| Key number | `spend`, in US dollars |
| Categories | `age_group`, `income`, `gender`, `household_size` |
| Many values | `category` (1,680 product types) and `state` (52) |
| Time | `order_date`, one day, from 1 January 2018 to 31 December 2022 |
| Place | `state`, two-letter code |

## Load it

```python
@st.cache_data
def load_data():
    return pd.read_csv("data/holiday_campaign/purchases.csv.gz", parse_dates=["order_date"])
```

pandas reads the compressed `.csv.gz` file directly.

## Columns

| Column | What it is |
|---|---|
| `order_date` | Day of the order |
| `category` | Amazon's own product type, for example `ABIS_BOOK` (books), `PET_FOOD` or `TOY_FIGURE` |
| `unit_price` | Price of one unit, in dollars |
| `quantity` | Units bought |
| `spend` | `unit_price` × `quantity` |
| `state` | State of the shipping address, as a two-letter code |
| `customer` | Number that identifies a person of the panel, from 1 to 5,027 |
| `age_group`, `income`, `gender`, `household_size` | That person's answers to the survey |

`us_states.csv` has the population in 2024 and the land area of each state, if you need rates.

A map by state: `px.choropleth(table, locations="state", locationmode="USA-states", color="...", scope="usa")`.

## Things to know

- **It is a sample.** The panel bought 1.81 million items in 2018–2022. This file is a random 10% of them, so multiply totals by 10 to estimate the whole panel. Shares, means and seasonal patterns need no correction.
- **It is a panel of volunteers**, not all Amazon customers. Some states have very few people in it.
- **Missing values.** 4.9% of the rows have no `category` and 4.7% have no `state`, mostly gift cards and digital items.
- **Long tail.** Half of the items cost less than $15, but a few cost thousands.
- **Growth over the years** mixes real changes in shopping with how long each person has used their account.

## Source

Berke, A. et al. *Open e-commerce 1.0: Five years of crowdsourced U.S. Amazon purchase histories with user demographics.* Harvard Dataverse, [doi:10.7910/DVN/YGLYDY](https://doi.org/10.7910/DVN/YGLYDY). Licence: CC0. Population and area: US Census Bureau, public domain. The script that built these files is kept by the teacher.
