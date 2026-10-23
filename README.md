# ROUTE//IQ — Last-Mile Delivery Analytics

ROUTE//IQ is a delivery-performance dashboard that helps logistics teams explore patterns in last-mile operations using delivery records.

## Key Features

- **Operations Overview:** Summarises delivery volume, average and median delivery time, late-delivery rate, and average agent rating.
- **Delay Analyzer:** Compares delivery times across traffic and weather conditions.
- **Vehicle Comparison:** Examines delivery-time performance by vehicle type.
- **Agent Performance:** Explores the relationship between agent ratings, age groups, and delivery time.
- **Area Heatmap:** Highlights differences in delivery time across areas and traffic conditions.
- **Category Analysis:** Compares delivery-time distributions across product categories.
- **Additional Insights:** Includes monthly trends, delivery-time distribution, and late-delivery analysis.

## Interactive Analysis

Users can filter the dataset by weather, traffic, vehicle type, area, product category, and order-date range. Summary metrics and visualisations update to reflect the selected records.

## Data Notes

Delivery-time values are reported in the dataset's units because the source file does not specify a unit. A late delivery is defined as a delivery time greater than the full dataset mean plus one standard deviation. Missing values, small sample groups, and unusual records should be considered when interpreting patterns. Observed relationships indicate associations, not proof of causation.



Streamlit Link: https://routeiqfa-2.streamlit.app/
