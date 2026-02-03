"""ENG 220 Final Project
Group 12: Finance"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycountry_convert as pc
import math

st.set_page_config(page_title="Global Economy Dashboard", layout="wide")

st.title("🌍 Global Economy Indicators — Interactive Dashboard")

# ==========================================================
# ---------------------- FILE UPLOAD ------------------------
# ==========================================================

st.info("Using built-in dataset bundled with this app.")
T = pd.read_csv("Global Economy Indicators.csv")

# ==========================================================
#                PART 1 — CLEANING + STATISTICS
# ==========================================================

st.header("Part 1 — Data Cleaning & Summary Statistics")

# Clean column names
T.columns = T.columns.str.strip()

# Replace NaN with 0 in numeric columns
for col in T.columns:
    if pd.api.types.is_numeric_dtype(T[col]):
        T[col] = T[col].fillna(0)

st.write("### Sample of Cleaned Data")
st.dataframe(T.head())

# --- Statistics per numeric column ---
numeric_columns = T.select_dtypes(include=[np.number])
convert = numeric_columns.to_numpy()
columns = numeric_columns.columns

Table = pd.DataFrame({
    'Name': columns,
    'Count': (convert != 0).sum(axis=0),
    'Mean': convert.mean(axis=0),
    'StdDev': convert.std(axis=0, ddof=1),
    'Min': convert.min(axis=0),
    'Median': np.median(convert, axis=0),
    'Max': convert.max(axis=0),
    'Sum': convert.sum(axis=0)
})

st.subheader("📊 Statistics Per Column")
st.dataframe(Table)

# --- Statistics per country ---
grouped = T.groupby("Country")[numeric_columns.columns]
count_df = grouped.apply(lambda df: (df != 0).sum()).rename(
    columns=lambda c: f"{c}_Count"
).reset_index()

agg_df = grouped.agg(['mean', 'std', 'min', 'median', 'max', 'sum'])
agg_df.columns = [f"{col}_{stat.capitalize()}" for col, stat in agg_df.columns]
agg_df = agg_df.reset_index()

Table_countries = pd.merge(count_df, agg_df, on="Country", how="outer")
Table_countries = Table_countries.sort_values("Country")

st.subheader("📊 Statistics Per Country")
st.dataframe(Table_countries)

# ==========================================================
#                PART 2 — GNI & EXCHANGE RATES
# ==========================================================

st.header("Part 2 — Global Trends (GNI Per Capita & Exchange Rates)")

data = T.copy()

# Rename GNI column
if "Gross National Income(GNI) in USD" in data.columns:
    data.rename(columns={"Gross National Income(GNI) in USD": "GNI"}, inplace=True)

# --- Verify required columns ---
required_cols = {"GNI", "Population", "Year"}
if not required_cols.issubset(data.columns):
    st.error(f"Missing columns: {required_cols}")
    st.stop()

data["GNI_per_Capita"] = data["GNI"] / data["Population"]

global_gni_pc = (
    data.groupby("Year")["GNI_per_Capita"]
    .mean()
    .reset_index()
    .sort_values("Year")
)

st.subheader("🌐 Global Average GNI per Capita Over Time")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(global_gni_pc["Year"], global_gni_pc["GNI_per_Capita"], marker="o")
ax.set_xlabel("Year")
ax.set_ylabel("GNI per Capita (USD)")
ax.grid(True)
st.pyplot(fig)

# --- Exchange rates ---
required_exCols = {"AMA exchange rate", "IMF based exchange rate"}

if required_exCols.issubset(data.columns):
    exchange_by_year = (
        data.groupby("Year")[list(required_exCols)]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    st.subheader("💱 Average Exchange Rates Over Time")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(exchange_by_year["Year"], exchange_by_year["AMA exchange rate"], label="AMA")
    ax.plot(exchange_by_year["Year"], exchange_by_year["IMF based exchange rate"], label="IMF")
    ax.set_xlabel("Year")
    ax.set_ylabel("Exchange Rate")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

else:
    st.warning("Exchange-rate columns missing. Skipping this section.")

# ==========================================================
#                      PART 3 — CONTINENTS & GNI CHANGE
# ==========================================================

st.header("Part 3 — Continent Trends (5-Year Intervals)")

data["Country"] = data["Country"].str.strip()
data["Country"] = data["Country"].str.replace(r"\s+", " ", regex=True)

def country_to_continent(country_name):
    try:
        alpha = pc.country_name_to_country_alpha2(country_name)
        cont = pc.country_alpha2_to_continent_code(alpha)
        mapping = {
            'AF': 'Africa', 'AS': 'Asia', 'EU': 'Europe',
            'NA': 'North America', 'OC': 'Oceania', 'SA': 'South America'
        }
        return mapping.get(cont, "Other")
    except:
        return "Other"

data["Continent"] = data["Country"].apply(country_to_continent)
data["Interval"] = (data["Year"] // 5) * 5

gni_intervals = (
    data.groupby(["Country", "Continent", "Interval"])["GNI"]
    .mean()
    .reset_index()
)

gni_intervals["GNI_change"] = gni_intervals.groupby("Country")["GNI"].diff()

continent_trends = (
    gni_intervals.groupby(["Continent", "Interval"])[["GNI", "GNI_change"]]
    .mean()
    .reset_index()
)

# -------- BAR CHART --------
st.subheader("📉 GNI Change Across Continents (5-Year Intervals)")

intervals = sorted(continent_trends["Interval"].unique())
continents = continent_trends["Continent"].unique()
bar_width = 0.12
x = np.arange(len(intervals))

fig, ax = plt.subplots(figsize=(12, 6))

for i, cont in enumerate(continents):
    subset = continent_trends[continent_trends["Continent"] == cont]
    y = [
        subset.loc[subset["Interval"] == interval, "GNI_change"].values[0]
        if interval in subset["Interval"].values else 0
        for interval in intervals
    ]
    ax.bar(x + i*bar_width, y, width=bar_width, label=cont)

ax.set_xticks(x + bar_width * (len(continents)-1) / 2)
ax.set_xticklabels(intervals, rotation=45)
ax.set_xlabel("Interval")
ax.set_ylabel("GNI Change")
ax.legend()
ax.grid(axis="y")

st.pyplot(fig)

# -------- LINE PLOT --------
st.subheader("📈 GNI Change Line Plot")

fig, ax = plt.subplots(figsize=(12, 6))

for cont in continents:
    subset = continent_trends[continent_trends["Continent"] == cont]
    ax.plot(subset["Interval"], subset["GNI_change"], marker="o", label=cont)

ax.set_xlabel("5-Year Interval")
ax.set_ylabel("GNI Change (USD)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.success("Dashboard generated successfully!")
