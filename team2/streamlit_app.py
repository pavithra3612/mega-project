import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Team 2 AQI Project", layout="wide")

st.title("🌫️ Team 2: Air Quality Index (AQI) Analysis")

st.write("""
This project analyzes AQI data to understand pollution trends and identify areas with the lowest air quality.
""")

# Load data safely
data_path = BASE_DIR / "data_date.csv"

if data_path.exists():
    df = pd.read_csv(data_path)
    
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Basic Statistics")
    st.write(df.describe())

else:
    st.warning("Dataset not found in Team 2 folder.")
