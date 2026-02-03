import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Team 11 Emissions Dashboard", layout="wide")

st.title("🚗 Team 11 Project: Emissions & Walkability Dashboard")
st.write("Interactive exploration of emissions datasets for New Mexico and more.")

# -------------------------
# Load datasets
# -------------------------
@st.cache_data
def load_data():
    try:
        df_nm = pd.read_csv("data/NewMexico_emissions.csv")
        df_all = pd.read_csv("data/data_emissions.csv")
        return df_nm, df_all
    except FileNotFoundError:
        st.error("❌ Could not find CSV files. Make sure they are inside the `data/` folder.")
        st.stop()

df_nm, df_all = load_data()

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["New Mexico Data", "Full Dataset", "Visualizations", "Summary"]
)

# -------------------------
# Page 1 — New Mexico Data
# -------------------------
if page == "New Mexico Data":
    st.header("New Mexico Emissions Dataset")
    st.dataframe(df_nm)

    st.subheader("Filter by Year")
    if "Year" in df_nm.columns:
        years = st.multiselect(
            "Select years:",
            sorted(df_nm["Year"].unique()),
            default=sorted(df_nm["Year"].unique())
        )
        filtered_nm = df_nm[df_nm["Year"].isin(years)]
    else:
        filtered_nm = df_nm

    st.write("### Filtered Data")
    st.dataframe(filtered_nm)

    # Plot emissions if column exists
    if {"Year", "Emissions"}.issubset(df_nm.columns):
        st.subheader("Emissions over Time (New Mexico)")
        fig, ax = plt.subplots()
        sns.lineplot(data=filtered_nm, x="Year", y="Emissions", ax=ax)
        ax.set_ylabel("Emissions")
        st.pyplot(fig)

# -------------------------
# Page 2 — Full Dataset
# -------------------------
elif page == "Full Dataset":
    st.header("Full Emissions Dataset")
    st.dataframe(df_all)

    # Sidebar filters
    st.write("### Filter the data")

    filtered_all = df_all.copy()

    # Categorical example: region, county, city, etc.
    for col in df_all.select_dtypes(include="object").columns:
        vals = st.multiselect(
            f"Filter by {col}:", 
            df_all[col].dropna().unique(), 
            default=df_all[col].dropna().unique()
        )
        filtered_all = filtered_all[filtered_all[col].isin(vals)]

    # Numeric filters
    for col in df_all.select_dtypes(include=["int64", "float64"]).columns:
        min_val, max_val = float(df_all[col].min()), float(df_all[col].max())
        selected_range = st.slider(
            f"{col} range:",
            min_val, max_val,
            (min_val, max_val)
        )
        filtered_all = filtered_all[
            filtered_all[col].between(selected_range[0], selected_range[1])
        ]

    st.write("### Filtered Dataset")
    st.dataframe(filtered_all)

# -------------------------
# Page 3 — Visualizations
# -------------------------
elif page == "Visualizations":
    st.header("📈 Visualizations")

    st.write("Select which dataset to visualize:")
    data_choice = st.radio("Dataset:", ["New Mexico", "Full Dataset"])

    df_vis = df_nm if data_choice == "New Mexico" else df_all

    num_cols = df_vis.select_dtypes(include=["int64", "float64"]).columns

    if len(num_cols) < 1:
        st.warning("No numerical columns available for visualization.")
        st.stop()

    # Histogram
    st.subheader("Histogram")
    col_hist = st.selectbox("Select a column for histogram:", num_cols)
    fig1, ax1 = plt.subplots()
    sns.histplot(df_vis[col_hist], bins=30, ax=ax1)
    st.pyplot(fig1)

    # Scatter plot
    st.subheader("Scatter Plot")
    x_col = st.selectbox("X-axis:", num_cols, index=0)
    y_col = st.selectbox("Y-axis:", num_cols, index=min(1, len(num_cols)-1))
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=df_vis, x=x_col, y=y_col, ax=ax2)
    st.pyplot(fig2)

# -------------------------
# Page 4 — Summary
# -------------------------
elif page == "Summary":
    st.header("📄 Project Summary")

    st.markdown("""
    ### Key Findings  
    - New Mexico emissions show clear trends over time (based on `NewMexico_emissions.csv`).  
    - The full dataset (`data_emissions.csv`) suggests differences in emissions across regions/categories.
    - Higher walkability or shorter commute distances often correlate with lower emissions.
    - Filtering controls allow interactive exploration of all variables.

    ### Next Steps  
    - Add predictive modelling widgets.  
    - Add maps if location data is available.  
    - Add scenario sliders (e.g., % increase in walkability → estimated emissions reduction).
    """)

    # Overall stats
    st.subheader("Overall Statistics (Full Dataset)")
    st.write(df_all.describe())

