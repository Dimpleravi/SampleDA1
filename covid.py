import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

data = pd.read_csv('WHO-COVID-19-global-daily-data.csv')

print(data.head())

# Map WHO columns to expected names
column_mapping = {
    'Date_reported': 'date',
    'Country': 'location',
    'Cumulative_cases': 'total_cases',
    'New_cases': 'new_cases',
    'Cumulative_deaths': 'total_deaths',
    'New_deaths': 'new_deaths',
}

missing_required = [src for src in column_mapping.keys() if src not in data.columns]
if missing_required:
    raise ValueError(f"Missing required columns in CSV: {missing_required}")

# Rename and type-clean
data = data.rename(columns=column_mapping)

# Parse date and sort
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Keep only used columns (people_vaccinated not present in WHO file)
used_columns = [
    'date', 'location', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths'
]

# Coerce numeric columns
for col in ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Drop rows with invalid date or missing location
data = data.dropna(subset=['date', 'location']).sort_values('date')

# Fill remaining NaNs with 0 for plotting
data[used_columns] = data[used_columns].fillna(0)

india = data[data['location'] == 'India']

plt.figure(figsize=(10,6))
if not india.empty:
    plt.plot(india['date'], india['total_cases'], label='Total Cases', color='blue')
    plt.plot(india['date'], india['total_deaths'], label='Total Deaths', color='red')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('COVID-19 Cases & Deaths in India')
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print('No India data available to plot time series.')

latest = data[data['date'] == data['date'].max()]

top10 = latest.sort_values('total_cases', ascending=False).head(10)
plt.figure(figsize=(12,6))
if not top10.empty:
    sns.barplot(x='location', y='total_cases', data=top10, palette='Blues_r')
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Countries by Total Cases')
    plt.tight_layout()
    plt.show()
else:
    print('No latest snapshot available for Top 10 chart.')

corr_cols = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']
if not india.empty and india[corr_cols].dropna().shape[0] > 1:
    corr = india[corr_cols].corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap (India COVID Data)')
    plt.tight_layout()
    plt.show()
else:
    print('Not enough India data to compute correlation heatmap.')

if not latest.empty:
    fig = px.choropleth(
        latest,
        locations='location',
        locationmode='country names',
        color='total_cases',
        hover_name='location',
        color_continuous_scale='Reds',
        title='Worldwide COVID-19 Cases'
    )
    fig.show()
else:
    print('No latest data for choropleth.')
