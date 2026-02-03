import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="About Us")

FILE_PATH = "ENG 220 cleaned data NMCRG.csv"


@st.cache_data
def load_data():
    """Load CSV and return DataFrame."""
    try:
        df = pd.read_csv(FILE_PATH)

        # Clean numeric columns (convert all possible columns to numeric)
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')

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


def plot_histogram(data, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=12, edgecolor="black", alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    return fig


# ---------------- PAGE CONTENT ----------------

st.title("Play Around Page!")
st.markdown(
    """
    This page allows you to select **ANY numeric column** from the CSV to analyze.
    You can also filter by county and display histograms and summary statistics.
    """
)

df = load_data()
if df.empty:
    st.stop()

# Identify usable numeric columns
numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

# County list
counties = ["All"] + sorted(df["County Name"].unique().tolist())

# Sidebar options
st.sidebar.header("Options")
selected_county = st.sidebar.selectbox("Select County", counties)
selected_column = st.sidebar.selectbox("Select Data Column", numeric_columns)

# Filter DF by county
if selected_county == "All":
    filtered_df = df
else:
    filtered_df = df[df["County Name"] == selected_county]

# Extract selected column values
data = pd.to_numeric(filtered_df[selected_column], errors="coerce").dropna()

# Stats Output Section
st.subheader(f"Statistics for: **{selected_column}** ({selected_county})")

stats = calculate_stats(data)

col1, col2, col3, col4, col5, col6 = st.columns(6)

metrics = ["Min", "Max", "Mean", "Median", "Std Dev", "Variance"]
for col, key in zip([col1, col2, col3, col4, col5, col6], metrics):
    value = stats[key]
    if isinstance(value, float):
        col.metric(key, f"{value:.2f}")
    else:
        col.metric(key, value)

# Histogram
st.subheader("Histogram")
fig = plot_histogram(data, f"{selected_column} Distribution ({selected_county})")
st.pyplot(fig)

# Show raw selected column preview
with st.expander("Raw Data Preview"):
    st.dataframe(filtered_df[[selected_column, "County Name", "Year"]].head(20))

st.info(f"Analysis based on {len(data)} valid entries from the dataset.")
