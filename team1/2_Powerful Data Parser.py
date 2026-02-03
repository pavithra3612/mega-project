import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Data Explorer (Full CSV)",
    layout="wide"
)

# Background styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f4f8;
        color: #333333;
        font-family: 'Arial', sans-serif;
        padding: 20px;
        border-radius: 15px;
    }
    .stSelectbox, .stSlider {
        background: rgba(255, 255, 255, 0.6);
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to our Powerful Data Parser!")
st.markdown(" :streamlit: Select any columns to explore and filter the data interactively.")
st.markdown("WARNING: Very complicated to use but the page will dynamically update as you select columns and filters. The outputted table is at the bottom of the page (Depending on your device it may be off screen so scroll down!).")

# Load data
FILE_PATH = "ENG 220 cleaned data NMCRG.csv"

@st.cache_data
def load_data():
    return pd.read_csv(FILE_PATH)

df = load_data()

# --- Column Selection ---
st.subheader("Choose Columns to Display")
all_columns = df.columns.tolist()
selected_columns = st.multiselect("Select columns", all_columns, default=all_columns)
display_df = df[selected_columns]

# --- Filters Section ---
st.subheader("Apply Filters")

numeric_cols = display_df.select_dtypes(include=["float64", "int64"]).columns
categorical_cols = display_df.select_dtypes(include=["object"]).columns

num_filters = {}
cat_filters = {}

# Numeric sliders with FIXED RANGE ISSUE
st.markdown("### Numeric Filters")
for col in numeric_cols:
    min_val = float(display_df[col].min())
    max_val = float(display_df[col].max())

    if min_val == max_val:
        # FIX: prevent Streamlit slider error
        st.markdown(f"**{col}:** Only one value ({min_val}). No range to filter.")
        num_filters[col] = (min_val, max_val)
    else:
        num_filters[col] = st.slider(
            f"{col}",
            min_val,
            max_val,
            (min_val, max_val)
        )

# Categorical filters
st.markdown("### Category Filters")
for col in categorical_cols:
    unique_vals = display_df[col].dropna().unique().tolist()
    cat_filters[col] = st.multiselect(f"{col}", unique_vals, default=unique_vals)

# --- Apply All Filters ---
filtered_df = display_df.copy()

for col, (low, high) in num_filters.items():
    filtered_df = filtered_df[(filtered_df[col] >= low) & (filtered_df[col] <= high)]

for col, allowed_vals in cat_filters.items():
    filtered_df = filtered_df[filtered_df[col].isin(allowed_vals)]

# --- Show Results ---
st.subheader("Filtered Results")
st.dataframe(filtered_df, use_container_width=True)

st.info(f"Showing {len(filtered_df)} rows after filtering.")
