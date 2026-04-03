# Cardiac Disease Dashboard

An interactive web dashboard for exploratory analysis of cardiovascular disease data, built with Python, Streamlit and Plotly. Visualizes clinical indicators from a real-world dataset of 918 patients, with dynamic filters and clinical interpretations for each chart.

## Features

- 6 summary metric cards: total patients, average age, heart disease prevalence, most affected sex, average resting blood pressure and average cholesterol
- Interactive sidebar filters: sex, age range and heart disease status — all charts update in real time
- 5 interactive Plotly charts with clinical interpretations
- Basic statistics table
- Data cleaning pipeline removing duplicates and invalid clinical values

## Charts

- **Age Distribution** — histogram comparing age distribution between patients with and without heart disease
- **Heart Disease by Sex** — grouped bar chart showing heart disease prevalence by sex
- **Cholesterol by Heart Disease** — boxplot comparing cholesterol distributions between groups
- **Max Heart Rate by Age** — scatter plot showing the relationship between age, maximum heart rate and heart disease
- **Correlation Heatmap** — heatmap of correlations between all numerical clinical variables

## Dataset

Heart Failure Prediction Dataset — Kaggle  
https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction

918 patients, 746 after cleaning. Variables include age, sex, chest pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, maximum heart rate, exercise angina, ST depression and heart disease diagnosis.

## Technologies

- Python
- Streamlit
- Plotly
- Pandas

## How to Run
```bash
pip install streamlit plotly pandas
streamlit run dashboard.py
```

## Data Cleaning

The following records were removed from the original dataset:
- Duplicate rows
- Cholesterol = 0 (missing values encoded as zero)
- Resting blood pressure = 0
- Age outside the 20–100 range

## Clinical Findings

- Patients with heart disease are more prevalent from age 55 onwards
- Males show higher heart disease prevalence than females in this dataset
- MaxHR is the strongest differentiator — patients with heart disease achieve lower maximum heart rates, consistent with chronotropic incompetence
- Cholesterol alone is not a strong predictor in this dataset

## Disclaimer

This dashboard is for educational purposes only and must not be used for clinical decision-making.

## Author

Vinícius Mourão Mendes Costa  