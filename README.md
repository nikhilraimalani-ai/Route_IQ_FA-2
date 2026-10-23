# ROUTE//IQ — Last-mile Delivery Intelligence

**Mathematics for AI-II · Formative Assessment 2**

A Streamlit dashboard built from the delivery workbook supplied for the assignment. It turns the FA-1 storyboard into an interactive application with sidebar filters and the five compulsory visualisations.

## Included

- `app.py` — complete Streamlit application
- `requirements.txt` — Python package requirements
- `data/last_mile_delivery.csv` — source workbook converted to CSV for simple deployment

## Dashboard features

1. **Delay Analyzer (bar chart):** average delivery time by weather, split by traffic.
2. **Vehicle Comparison (bar chart):** average delivery time by vehicle with medians and sample counts available on hover.
3. **Agent Performance Scatter Plot:** Agent_Rating vs Delivery_Time, coloured by agent age group.
4. **Area Heatmap:** average delivery time by area and traffic condition.
5. **Category Visualizer (box plot):** category-wise delivery-time distributions.

Additional visuals: monthly average-time trend, delivery-time histogram, and late-delivery percentage by traffic.

## Data handling choices

- Text categories are trimmed and missing Weather/Traffic values are retained as `Unknown`.
- Rows without a usable `Delivery_Time` are excluded from analysis.
- Missing agent ratings remain missing rather than being imputed.
- Late delivery follows the assignment's example: `Delivery_Time > full-dataset mean + 1 standard deviation`. The threshold remains fixed while filters change.
- The app flags small sample groups and the unusually low Grocery delivery times so users do not mistake data quality issues for reliable business conclusions.

The source workbook contains agent ratings as high as 6. This app does not silently cap them; the rating scale should be confirmed with the dataset provider.

## Run locally on Windows

1. Install Python 3.10 or newer.
2. Extract this project folder.
3. Open Command Prompt or PowerShell in the `ROUTE_IQ_FA2` folder.
4. Create and activate a virtual environment (recommended):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install packages:

   ```powershell
   pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   streamlit run app.py
   ```

The dashboard will open in your browser. If Streamlit prints a local URL, open that URL manually.

## Deploy using GitHub + Streamlit Community Cloud

1. Sign in to GitHub and create a **public repository** for this project.
2. Upload `app.py`, `requirements.txt`, and the whole `data` folder (including the CSV).
3. Open Streamlit Community Cloud and connect your GitHub account.
4. Create a new app, select your repository and branch, and set the app file path to `app.py`.
5. Deploy. After it builds successfully, test the public URL and check that all five tabs, all sidebar filters, and the optional visuals work.

Do not upload credentials or personal secrets. The included dataset is the course dataset; follow your teacher's data-sharing instructions before making a repository public.

## Notes

- All delivery times are displayed in **dataset units** because the workbook does not explicitly label the unit.
- The heatmap intentionally combines Area and Traffic to help inspect area bottlenecks under different traffic conditions.
- Association in a chart does not establish cause.
