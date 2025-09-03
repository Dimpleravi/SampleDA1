import streamlit as st
import pandas as pd
import plotly.express as px

# Load data

# The WHO file columns are: Date_reported, Country_code, Country, WHO_region,
# New_cases, Cumulative_cases, New_deaths, Cumulative_deaths
# Map them to simplified names used in the app.

data = pd.read_csv('WHO-COVID-19-global-daily-data.csv')

# Normalize column names to expected ones
column_mapping = {
    'Date_reported': 'date',
    'Country': 'location',
    'Cumulative_cases': 'total_cases',
}

# Ensure required columns exist
missing_required = [src for src in ['Date_reported', 'Country', 'Cumulative_cases'] if src not in data.columns]
if missing_required:
    st.error(f"Missing required columns in CSV: {missing_required}")
else:
    data = data.rename(columns=column_mapping)
    # Parse date and sort
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data = data.dropna(subset=['date'])
    data = data.sort_values('date')

    st.title("🌍 COVID-19 Dashboard")

    # Country selector
    countries = data["location"].dropna().unique()
    country = st.selectbox("Select a Country", sorted(countries))

    df_country = data[data["location"] == country]

    # Line Chart for cumulative cases
    if not df_country.empty:
        fig = px.line(df_country, x="date", y="total_cases", title=f"COVID-19 Total Cases in {country}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected country.")

    # Bar Chart (Top 10 Countries Latest Cases)
    latest_date = data['date'].max()
    latest = data[data["date"] == latest_date]
    top10 = latest.sort_values("total_cases", ascending=False).head(10)
    if not top10.empty:
        fig2 = px.bar(top10, x="location", y="total_cases", title=f"Top 10 Countries by Total Cases on {latest_date.date()}")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No latest snapshot available to display top 10 chart.")
