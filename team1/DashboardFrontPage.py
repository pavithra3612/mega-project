import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rio Grande Water Consumption Analysis", layout="wide")

FILE_PATH = "ENG 220 cleaned data NMCRG.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(FILE_PATH)

        # Rename long CSV columns to simple names used by the dashboard
        df = df.rename(columns={
            "County Name": "County",
            "Public Supply total self-supplied withdrawals, total, in Mgal/d": "Consumption"
        })

        # Convert Consumption to numeric
        df["Consumption"] = pd.to_numeric(df["Consumption"], errors="coerce")
        df = df.dropna(subset=["Consumption"])

        return df
    except FileNotFoundError:
        st.error(f"File '{FILE_PATH}' not found.")
        return pd.DataFrame()

def calculate_stats(data):
    if len(data) == 0:
        return {}
    return {
        "Min": np.min(data),
        "Max": np.max(data),
        "Mean": np.mean(data),
        "Median": np.median(data),
        "Std Dev": np.std(data, ddof=1),
        "Variance": np.var(data, ddof=1)
    }

def plot_histogram(data, title, bins=10):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=bins, edgecolor="black", alpha=0.7, color="skyblue")
    ax.set_title(title)
    ax.set_xlabel("Water Consumption (Mgal/day)")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    return fig

# ------------------ MAIN APP ------------------

st.title("Rio Grande Water Consumption Analysis (NM Counties, 2000–2020)")

df = load_data()
if df.empty:
    st.stop()

# Overall stats
st.subheader("Overall Statistics (All Counties)")
overall_stats = calculate_stats(df["Consumption"])

# Display metrics
cols = st.columns(6)
keys = ["Min", "Max", "Mean", "Median", "Std Dev", "Variance"]
for col, key in zip(cols, keys):
    value = overall_stats[key]
    if isinstance(value, float):
        col.metric(key, f"{value:.2f}")
    else:
        col.metric(key, value)

# Letting the user select a county.
counties = ["All"] + sorted(df["County"].unique().tolist())
selected_county = st.selectbox("Select County", counties)

# Filter
if selected_county == "All":
    filtered_df = df
    data = df["Consumption"]
    label = "All Counties"
else:
    filtered_df = df[df["County"] == selected_county]
    data = filtered_df["Consumption"]
    label = selected_county

# Stats for selected county but if none are chosen it shows averages overall. (Look at the above function.)
st.subheader(f"Statistics ({label})")
stats_selected = calculate_stats(data)

cols2 = st.columns(6)
for col, key in zip(cols2, keys):
    value = stats_selected[key]
    if isinstance(value, float):
        col.metric(key, f"{value:.2f}")
    else:
        col.metric(key, value)

# Histogram generator.
st.subheader(f"Histogram ({label})")
fig = plot_histogram(data, f"Water Consumption Distribution ({label})")
st.pyplot(fig)

# Preview of the data
with st.expander("Raw Data Preview"):
    st.dataframe(df.head(15))

st.info(f"Dataset contains {len(df)} rows across {len(counties)-1} counties.")
