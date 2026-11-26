# Visualization: dashboard template

The starting point for the dashboards of the Visualization course. It runs in your browser with GitHub Codespaces, so there is nothing to install.

## Start

1. Press **Use this template**, then **Create a new repository**, and choose **Private**.
2. In your new repository, press **Code**, then **Codespaces**, then **Create codespace on main**. The first time takes a few minutes.
3. In the terminal, run `streamlit run lesson.py` and open the page it offers.

Save a file with `Ctrl+S` and the page updates by itself.

## What is here

| | |
|---|---|
| `lesson.py` | Where you type during session 8 |
| `dashboard.py` | Your project's dashboard |
| `example_dashboard.py` | A finished dashboard, on Citi Bike data |
| `catalog.py` | Examples of charts, with their code: `streamlit run catalog.py` |
| `pieces/` | The examples in the catalog. Each one also runs on its own, for example `streamlit run pieces/compare/top_n_bars.py` |
| `data/` | The Citi Bike example and three proposed datasets, each with a README. Your own data goes here too |
| `requirements.txt`, `.devcontainer/` | What the Codespace installs. If you need another package, add it to `requirements.txt` and run `pip install -r requirements.txt` |

GitHub Copilot is installed in the Codespace. You may use it, and you answer for everything it writes.

## Your own data

Drag your files from your computer onto the `data` folder, in the Explorer on the left. Then load them with `pd.read_csv("data/your_file.csv")`.

- GitHub does not accept files over 100 MB. Keep a smaller extract, or compress the file: `pd.read_csv` reads `.csv.gz` directly.
- Files from Spanish portals such as INE often use `;` between columns and a comma for decimals: `pd.read_csv(path, sep=";", decimal=",")`. If accents look wrong, add `encoding="latin-1"`.
- Excel files: `pd.read_excel("data/your_file.xlsx")`.

## Your project

The brief, the deliverables and the deadline are in PoliformaT. You may use your own data or one of the three proposed datasets in `data`. In class we build with Streamlit; the brief also allows Dash.

## Save your work

At the end of each session, open **Source Control** in the left bar, write a short message, and press **Commit**, then **Sync Changes**. A Codespace stops after 30 minutes without use and is deleted after 30 days without use. Your repository stays.
