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


# ---------------- UPDATED PLOTTING FUNCTIONS ----------------

def plot_histogram(data, title):
    fig, ax = plt.subplots(figsize=(6, 4))  # smaller
    ax.hist(data, bins=12, edgecolor="black", alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    return fig


def plot_dotplot(data, title):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(data, np.zeros_like(data), 'o')
    ax.set_title(title)
    ax.set_yticks([])
    ax.set_xlabel("Value")
    return fig


def plot_bar(data, title):
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = data.value_counts().sort_index()
    ax.bar(counts.index.astype(str), counts.values)
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    return fig


def plot_pie(data, title):
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = data.value_counts()
    ax.pie(counts.values, labels=counts.index.astype(str), autopct='%1.1f%%')
    ax.set_title(title)
    return fig


# ---------------- PAGE CONTENT ----------------

st.title("Data Visualizer")
st.markdown(
    """
    This page allows you to select **ANY numeric column** from the CSV to analyze.  
    You can filter by county and choose how you want the data visualized.
    """
)

df = load_data()
if df.empty:
    st.stop()

numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
counties = ["All"] + sorted(df["County Name"].unique().tolist())

# Sidebar options
st.sidebar.header("Options")
selected_county = st.sidebar.selectbox("Select County", counties)
selected_column = st.sidebar.selectbox("Select Data Column", numeric_columns)

# Visualization dropdown
visualization_type = st.sidebar.selectbox(
    "Choose Visualization Type",
    ["Histogram", "Dot Plot", "Bar Chart", "Pie Chart"]
)

# Filter DF by county
if selected_county == "All":
    filtered_df = df
else:
    filtered_df = df[df["County Name"] == selected_county]

# Prepare data
data = pd.to_numeric(filtered_df[selected_column], errors="coerce").dropna()

# Display statistics
st.subheader(f"Statistics for: **{selected_column}** ({selected_county})")
stats = calculate_stats(data)

col1, col2, col3, col4, col5, col6 = st.columns(6)
metrics = ["Min", "Max", "Mean", "Median", "Std Dev", "Variance"]

for col, key in zip([col1, col2, col3, col4, col5, col6], metrics):
    value = stats[key]
    col.metric(key, f"{value:.2f}" if isinstance(value, float) else value)

# ---------------- VISUALIZATION HANDLER ----------------

st.subheader(f"{visualization_type}")

if visualization_type == "Histogram":
    fig = plot_histogram(data, f"{selected_column} Distribution")
elif visualization_type == "Dot Plot":
    fig = plot_dotplot(data, f"{selected_column} Dot Plot")
elif visualization_type == "Bar Chart":
    fig = plot_bar(data, f"{selected_column} Bar Chart")
elif visualization_type == "Pie Chart":
    fig = plot_pie(data, f"{selected_column} Pie Chart")

# USE CONTAINER WIDTH HERE 👇
st.pyplot(fig, use_container_width=True)

# Raw preview
with st.expander("Raw Data Preview"):
    st.dataframe(filtered_df[[selected_column, "County Name", "Year"]].head(20))

st.info(f"Analysis based on {len(data)} valid entries from the dataset.")
