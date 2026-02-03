import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="California Housing Comparison", layout="wide")

@st.cache_data
def load_data():
    cl_data_1990 = pd.read_csv("cleaned_california_housing_1990.csv")
    cl_data_updated = pd.read_csv("cleaned_california_housing_updated.csv")
    return cl_data_1990, cl_data_updated

cl_data_1990, cl_data_updated = load_data()

st.title("California Housing: 1990 vs Updated Data")

st.subheader("Dataset Summaries")
with st.expander("Show summary for 1990 data"):
    st.write(cl_data_1990.describe(include="all"))

with st.expander("Show summary for updated data"):
    st.write(cl_data_updated.describe(include="all"))


# =========================
# Pie Charts for ocean_proximity
# =========================
st.header("Ocean Proximity Distribution (Pie Charts)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ocean Proximity - 1990 Data")
    fig1, ax1 = plt.subplots()
    counts_1990 = cl_data_1990["ocean_proximity"].value_counts(dropna=False)
    ax1.pie(counts_1990.values, labels=counts_1990.index, autopct="%1.1f%%")
    ax1.axis("equal")
    st.pyplot(fig1)

with col2:
    st.subheader("Ocean Proximity - Updated Data")
    fig2, ax2 = plt.subplots()
    counts_updated = cl_data_updated["ocean_proximity"].value_counts(dropna=False)
    ax2.pie(counts_updated.values, labels=counts_updated.index, autopct="%1.1f%%")
    ax2.axis("equal")
    st.pyplot(fig2)


# =========================
# Grouped Bar: Median House Value by Age Range
# =========================
st.header("Median House Value by Housing Age Range")

# Define age bins and labels
edges = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100]
xlabels = ["0-9", "10-19", "20-29", "30-39", "40-49",
           "50-59", "60-69", "70-79", "80+"]

# 1990 age bins
age_bins_1990 = pd.cut(
    cl_data_1990["housing_median_age"],
    bins=edges,
    right=False,
    labels=xlabels
)
mean_value_1990 = cl_data_1990.groupby(age_bins_1990)["median_house_value"].mean()

# Updated age bins (average_house_age)
age_bins_updated = pd.cut(
    cl_data_updated["average_house_age"],
    bins=edges,
    right=False,
    labels=xlabels
)
mean_value_updated = cl_data_updated.groupby(age_bins_updated)["median_house_value"].mean()

# Align on the same labels
mean_value_1990 = mean_value_1990.reindex(xlabels)
mean_value_updated = mean_value_updated.reindex(xlabels)

fig3, ax3 = plt.subplots()
x = np.arange(len(xlabels))
width = 0.35

ax3.bar(x - width/2, mean_value_1990.values, width, label="1990 Data")
ax3.bar(x + width/2, mean_value_updated.values, width, label="Updated Data")

ax3.set_xticks(x)
ax3.set_xticklabels(xlabels, rotation=45)
ax3.set_xlabel("Housing Age Range")
ax3.set_ylabel("Average Median House Value ($)")
ax3.set_title("Comparison of Housing Median Age and Value")
ax3.legend(loc="upper right")
ax3.grid(axis="y")

fig3.tight_layout()
st.pyplot(fig3)


# =========================
# Grouped Bar: Median House Value by Ocean Proximity
# =========================
st.header("Median House Value by Ocean Proximity")

cats_1990 = cl_data_1990["ocean_proximity"].dropna().unique()
cats_updated = cl_data_updated["ocean_proximity"].dropna().unique()
all_categories = sorted(set(cats_1990).union(set(cats_updated)))

mean_val_1990 = []
mean_val_updated = []

for group in all_categories:
    # 1990
    idx_1990 = cl_data_1990["ocean_proximity"] == group
    if idx_1990.any():
        mean_val_1990.append(cl_data_1990.loc[idx_1990, "median_house_value"].mean())
    else:
        mean_val_1990.append(np.nan)

    # Updated
    idx_updated = cl_data_updated["ocean_proximity"] == group
    if idx_updated.any():
        mean_val_updated.append(cl_data_updated.loc[idx_updated, "median_house_value"].mean())
    else:
        mean_val_updated.append(np.nan)

fig4, ax4 = plt.subplots()
x = np.arange(len(all_categories))
width = 0.35

ax4.bar(x - width/2, mean_val_1990, width, label="1990 Data")
ax4.bar(x + width/2, mean_val_updated, width, label="Updated Data")

ax4.set_xticks(x)
ax4.set_xticklabels(all_categories, rotation=45)
ax4.set_xlabel("Ocean Proximity")
ax4.set_ylabel("Average Median House Value ($)")
ax4.set_title("Comparison of Median House Value by Ocean Proximity")
ax4.legend(loc="upper right")
ax4.grid(axis="y")

fig4.tight_layout()
st.pyplot(fig4)


# =========================
# Box Plot: Distribution Comparison
# =========================
st.header("Box Plot: Median House Value Distributions")

vals_1990 = cl_data_1990["median_house_value"].dropna()
vals_updated = cl_data_updated["median_house_value"].dropna()

fig5, ax5 = plt.subplots()
ax5.boxplot([vals_1990.values, vals_updated.values],
            labels=["1990", "Updated"])
ax5.set_title("Comparison of Median House Value Distributions")
ax5.set_ylabel("Median House Value ($)")
st.pyplot(fig5)

# Max and Min values
max_value_1990 = vals_1990.max()
min_value_1990 = vals_1990.min()
max_value_updated = vals_updated.max()
min_value_updated = vals_updated.min()

st.subheader("Max and Min Median House Values")
st.text(f"1990 Data:   Max = ${max_value_1990:,.2f}, Min = ${min_value_1990:,.2f}")
st.text(f"Updated Data: Max = ${max_value_updated:,.2f}, Min = ${min_value_updated:,.2f}")


# =========================
# Double Bar Graph: House Value Ranges
# =========================
st.header("Median House Value Distribution by Price Range")

# Extract values again (including NaN drop)
vals_1990 = cl_data_1990["median_house_value"].dropna().values
vals_updated = cl_data_updated["median_house_value"].dropna().values

# Bin edges
edges_val = [0, 100000, 200000, 300000, 400000, 500000, np.inf]
labels_val = [
    "0–100k",
    "100–200k",
    "200–300k",
    "300–400k",
    "400–500k",
    ">500k"
]

counts_1990, _ = np.histogram(vals_1990, bins=edges_val)
counts_updated, _ = np.histogram(vals_updated, bins=edges_val)

fig6, ax6 = plt.subplots()
x = np.arange(len(labels_val))
width = 0.35

ax6.bar(x - width/2, counts_1990, width, label="1990 Data")
ax6.bar(x + width/2, counts_updated, width, label="Updated Data")

ax6.set_xticks(x)
ax6.set_xticklabels(labels_val, rotation=45)
ax6.set_xlabel("Median House Value Range ($)")
ax6.set_ylabel("Number of Blocks")
ax6.set_title("Comparison of Median House Value Distribution (1990 vs Updated)")
ax6.legend()
ax6.grid(axis="y")

fig6.tight_layout()
st.pyplot(fig6)
